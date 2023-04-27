import os
import dotenv
import warnings
from .env import Env
from pathlib import Path
from pydantic import BaseModel
from pydantic.fields import FieldInfo
from .validations import ValidationOptions
from pydantic.error_wrappers import ValidationError
from typing import Iterable, Union, Dict, Optional, Sequence


class BaseConfig:
    """
    Base Config required for env creation

    - `envs` (typing.Iterable[typing.Union[tuple[str, str], str]]): List of env variables to be created.
        Elements in `envs` can be either a tuple of (name, default) or just the name.
        If the element is a tuple, the first element is the name of the env variable and the
        second element is the default value.
    - `dot_env_path` (typing.Union[str, 'os.PathLike[str]']): Path to the .env file
    - `contained` (bool): If True, the env variables loaded from the .env file will be contained within instance and
     not set as env variables. default: True
     This is helpful when you do not want to populate global env variables and maintain a clean env.
    - `validations` (typing.Dict[str, ValidationOptions]): Dict of validations to be applied to the env variables.
        The key of the dict is the name of the env variable and the value is the validation options.
        The validation options are the same as the pydantic field info.
    - `eagerly_validate` (bool): If True, the env variables will be validated on class creation.
    """
    envs: Iterable[Union[tuple[str, str], str]] = tuple()
    dot_env_path: Union[str, 'os.PathLike[str]'] = None
    contained: bool = True
    validations: Dict[str, ValidationOptions] = {}
    eagerly_validate: bool = False


class EnvMeta(type):
    """
    Metaclass for populating env variables
    as class attributes to the child class.
    if the child class has a Config class, it will
    be used to populate the env variables.

    by default, the env variables are populated on first access
    and cached for subsequent access. This can be overriden by
    setting the value on the instance.

    if the env variable is not set, it uses the default value provided.

    This class also initializes the instance of the child class and
    make it available as `instance` attribute on the child class. So it can be accessed as
    `ChildClass.instance`.

    Example:

        >>> class ABC(BaseEnv):
                def generate_uri(self):
                    return f'{self.DB_HOST}:{self.DB_PORT}'
                class Config(BaseConfig):
                    envs = ('dev', ('test', 'test_value'),
                            'prd', 'DB_HOST', 'DB_PORT')
                    dot_env_path = Path(__file__).parent / '.env.test'

        >>> # access env variables
        >>> ABC.instance.dev
        >>> ABC.instance.test
        >>> ABC.instance.prd
    """
    def __new__(mcs, name, bases, attrs: dict):
        config_attrs = attrs.pop('Config', BaseConfig)  # type: BaseConfig
        if config_attrs:
            mcs.validate_envs(config_attrs)
            mcs.validate_dotenv_path(config_attrs)
            # loading env variables from file
            dot_env_path = getattr(config_attrs, 'dot_env_path', None)
            __contained__ = {}
            if not config_attrs.contained:
                dotenv.load_dotenv(dot_env_path)
            else:
                __contained__ = dotenv.dotenv_values(dot_env_path)
                if __contained__:
                    attrs['__contained__'] = __contained__
            # patching the class attrs with env variables
            env_attr_ = mcs.process_config_attrs(config_attrs)
            if config_attrs.eagerly_validate:
                errs_ = []
                name_space_, __annotations__ = {}, {}
                for k, v in env_attr_.items():
                    _, errors_ = v.validate(name, contained=__contained__)
                    if errors_:
                        name_space_[k] = FieldInfo(default=v.default, **v.extras)
                        __annotations__[k] = v.type
                        if isinstance(errors_, Sequence):
                            errs_.extend(errors_)
                        else:
                            errs_.append(errors_)
                name_space_['__annotations__'] = __annotations__
                if errs_:
                    raise ValidationError(errors=errs_,
                                          model=type(name, (BaseModel,),
                                                     name_space_))
            attrs.update(env_attr_)
        cls_ = super().__new__(mcs, name, bases, attrs)
        # initializing the instance
        cls_.instance = cls_()
        return cls_

    def validate_envs(config_attrs: BaseConfig):
        """
        Function to validate the config attributes

        Args:
            config_attrs (BaseConfig): Attributes of the config class

        Raises:
            TypeError: If envs is not an iterable
        """
        if not isinstance(config_attrs.envs, (tuple, list)):
            raise TypeError('envs should be an iterable, either tuple or list')

    def validate_dotenv_path(config_attrs: BaseConfig):
        """
        Function to validate the config attributes

        Args:
            config_attrs (BaseConfig): _description_

        Raises:
            FileNotFoundError: _description_
        """
        if config_attrs.dot_env_path:
            path_ = Path(config_attrs.dot_env_path)
            if not path_.exists():
                raise FileNotFoundError(f'File not found at {path_}')

    def process_config_attrs(config_attrs: BaseConfig) -> dict[str, Env]:
        """
        Function to process the config attributes
        and prepare namespaced env variables

        Args:
            config_attrs (BaseConfig): _description_

        Returns:
            _type_: _description_
        """
        validation_map = config_attrs.validations
        default_type = Optional[str]
        c_ = {}
        for attr_name in getattr(config_attrs, 'envs', tuple()):
            name_ = attr_name
            default_ = None
            if isinstance(attr_name, (tuple, list)):
                [name_, default_] = attr_name
            validation_kwargs = validation_map.get(name_, {})
            default_ = default_ or validation_kwargs.pop('default', None)
            # selecting the type of the env variable
            required_ = validation_kwargs.get('required', False)
            type_ = validation_kwargs.pop('type', default_type)
            if required_ and type_ is default_type:
                warnings.warn(
                    f"Optional types cannot be required. {default_type}, will update required to False."
                )
                validation_kwargs['required'] = False
            env_ = Env(default_, type_=type_, **validation_kwargs)
            env_.__set_name__(None, name_)
            c_[name_] = env_
        return c_


class BaseEnv(metaclass=EnvMeta):
    """
    Base class for env variables
    This can be used as a base class for env variables.

    You would need to override the `Config` class with the following attributes:

    - `envs`: Iterable[Union[tuple[str, str], str]] = List of env variables to be populated as class attributes.
    - `dot_env_path`: Union[str, 'os.PathLike[str]'] = Path to the .env file to be loaded. By default,
    it will load the .env file in the current directory.

    > Note: `Config` class is optional. If not provided, it will not load any env variables.
    `Config` class won't be available as an attribute on the child class.

    Example:

        >>> class ABC(BaseEnv):
                def generate_uri(self):
                    return f'{self.DB_HOST}:{self.DB_PORT}'
                class Config(BaseConfig):
                    envs = ('dev', ('test', 'test_value'),
                            'prd', 'DB_HOST', 'DB_PORT')
                    # if not set, it will pick `.env`
                    dot_env_path = Path(__file__).parent / '.env'
        >>> # access env variables
        >>> ABC.instance.dev
        >>> ABC.instance.test
        >>> ABC.instance.prd
        >>> # override env variable
        >>> ABC.instance.dev = 'dev_value'
    """
    class Config(BaseConfig):
        ...
