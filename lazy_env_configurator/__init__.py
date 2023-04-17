import os
import dotenv
from dataclasses import dataclass
from typing import Iterable, Union


@dataclass(frozen=True)
class BaseConfig:
    """
    Base Config required for env creation

    - `envs` (typing.Iterable[typing.Union[tuple[str, str], str]]): List of env variables to be created.
        Elements in `envs` can be either a tuple of (name, default) or just the name.
        If the element is a tuple, the first element is the name of the env variable and the
        second element is the default value.
    - `dot_env_path` (typing.Union[str, 'os.PathLike[str]']): Path to the .env file
    """
    envs: Iterable[Union[tuple[str, str], str]] = tuple()
    dot_env_path: Union[str, 'os.PathLike[str]'] = None


class Env(object):
    """
    Env descriptor for env variables. This class populates env
    variables on first access and caches the value for subsequent access.
    If the env variable is not set, it uses the default value provided.
    Values can be overriden by setting the value on the instance.
    """

    def __init__(self, default=None):
        """
        Initalizer for Env
        Captures the default value and name of the env variable

        Args:
            default (typing.Any, optional): Default to override in case of unset Env. Defaults to None.
        """
        self.__name = None
        self.__value = None
        self.__default = default

    def __get__(self, *_):
        '''
        descriptor __get__ method

        Returns:
            typing.Any: value of the env variable
        '''
        if not self.__value:
            self.__value = os.getenv(self.__name, self.__default)
        return self.__value

    def __set__(self, _, value):
        self.__value = value

    def __set_name__(self, _, name):
        self.__name = name


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
        config_attrs = attrs.pop('Config', None)
        if config_attrs:
            # patching the class attrs with env variables
            attrs.update(mcs.process_config_attrs(config_attrs))
            # loading env variables from file
            dot_env_path = getattr(config_attrs, 'dot_env_path', None)
            dotenv.load_dotenv(dot_env_path)
        cls_ = super().__new__(mcs, name, bases, attrs)
        # initializing the instance
        cls_.instance = cls_()
        return cls_

    def process_config_attrs(config_attrs: BaseConfig) -> dict[str, Env]:
        """
        Function to process the config attributes
        and prepare namespaced env variables

        Args:
            config_attrs (BaseConfig): _description_

        Returns:
            _type_: _description_
        """
        c_ = {}
        for attr_name in getattr(config_attrs, 'envs', tuple()):
            name_ = attr_name
            default_ = None
            if isinstance(attr_name, (tuple, list)):
                [name_, default_] = attr_name
            c_[name_] = Env(default_)
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
