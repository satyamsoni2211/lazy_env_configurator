import os
from pydantic.class_validators import Validator
from pydantic.fields import ModelField, FieldInfo
from typing import Dict, Optional, Type, Tuple, Any
from pydantic.error_wrappers import ValidationError, ErrorList
from pydantic import BaseConfig as PydanticBaseConfigModel, BaseModel


class Env(object):
    """
    Env descriptor for env variables. This class populates env
    variables on first access and caches the value for subsequent access.
    If the env variable is not set, it uses the default value provided.
    Values can be overriden by setting the value on the instance.
    """
    __slots__ = ('name', 'value', 'default',
                 '__calculated', 'type', 'validators',
                 'required', 'extras')

    def __init__(self, default=None,
                 validators: Optional[Dict[str, Validator]] = None,
                 type_: Type = None,
                 **kwargs):
        """
        Initalizer for Env
        Captures the default value and name of the env variable

        Args:
            default (typing.Any, optional): Default to override in case of unset Env. Defaults to None.
        """
        self.name = None
        self.value = None
        self.default = default
        # flag to check if the value is already calculated
        self.__calculated = False
        self.validators = validators
        self.required = kwargs.pop("required", None) or default == Ellipsis
        self.type = type_
        self.extras = kwargs
        # super().__init__(self.default, **kwargs)

    @property
    def validator(self) -> ModelField:
        # configuration Pydantic model
        config = PydanticBaseConfigModel
        config.fields = {self.name: self.extras}
        default = ... if (self.default is Ellipsis or self.required) else self.default
        m_ = ModelField.infer(
            name=self.name,
            value=default,
            annotation=self.type,
            class_validators=self.validators,
            config=config,
        )
        return m_

    def validate(self, model: Optional[str],
                 *,
                 value: Any = None,
                 contained: dict = {}) -> Tuple[Any, Tuple[Optional[Any], Optional[ErrorList]]]:
        val = value or (contained.get(self.name) or os.getenv(self.name, self.default))
        v_, errors = self.validator.validate(val,
                                             {},
                                             loc=(model, self.name),
                                             cls=None)
        return v_, errors

    def __get__(self, instance, obj_type=None):
        '''
        descriptor __get__ method

        Returns:
            typing.Any: value of the env variable
        '''
        contained_ = getattr(instance, '__contained__', {})
        # using the cached value if already calculated
        if not self.__calculated:
            instance_name_ = instance.__class__.__name__
            v_ = self.get_validated_value(instance_name_,
                                          contained=contained_)
            self.value = v_
            self.__calculated = True
        return self.value

    def get_validated_value(self, instance_name_: str, *, value: Any = None, contained: dict = {}):
        v_, errors = self.validate(instance_name_, value=value, contained=contained)
        if errors:
            error = ValidationError(errors=[errors], model=type(instance_name_, (BaseModel,), {
                self.name: FieldInfo(default=self.default, **self.extras),
                "__annotations__": {self.name: self.type}
            })
            )
            raise error
        return v_

    def __set__(self, instance, value):
        val_ = self.get_validated_value(instance.__class__.__name__, value=value)
        self.value = val_
        # marking this as calculated
        # otherwise this recalculates the value
        self.__calculated = True

    def __set_name__(self, _, name):
        self.name = name
