from typing import TypedDict, Optional, Type


class ValidationOptions(TypedDict):
    """
    :param default: since this is replacing the field’s default, its first argument is used
      to set the default, use ellipsis (``...``) to indicate the field is required
    :param alias: the public name of the field
    :param title: can be any string, used in the schema
    :param description: can be any string, used in the schema
    :param gt: only applies to numbers, requires the field to be "greater than". The schema
      will have an ``exclusiveMinimum`` validation keyword
    :param ge: only applies to numbers, requires the field to be "greater than or equal to". The
      schema will have a ``minimum`` validation keyword
    :param lt: only applies to numbers, requires the field to be "less than". The schema
      will have an ``exclusiveMaximum`` validation keyword
    :param le: only applies to numbers, requires the field to be "less than or equal to". The
      schema will have a ``maximum`` validation keyword
    :param multiple_of: only applies to numbers, requires the field to be "a multiple of". The
      schema will have a ``multipleOf`` validation keyword
    :param allow_inf_nan: only applies to numbers, allows the field to be NaN or infinity (+inf or -inf),
        which is a valid Python float. Default True, set to False for compatibility with JSON.
    :param max_digits: only applies to Decimals, requires the field to have a maximum number
      of digits within the decimal. It does not include a zero before the decimal point or trailing decimal zeroes.
    :param decimal_places: only applies to Decimals, requires the field to have at most a number of decimal places
      allowed. It does not include trailing decimal zeroes.
    :param min_length: only applies to strings, requires the field to have a minimum length. The
      schema will have a ``minLength`` validation keyword
    :param max_length: only applies to strings, requires the field to have a maximum length. The
      schema will have a ``maxLength`` validation keyword
    :param allow_mutation: a boolean which defaults to True. When False, the field raises a TypeError if the field is
      assigned on an instance.  The BaseModel Config must set validate_assignment to True
    :param regex: only applies to strings, requires the field match against a regular expression
      pattern string. The schema will have a ``pattern`` validation keyword
    :param repr: show this field in the representation
    """
    required: Optional[bool]
    alias: Optional[str]
    title: Optional[str]
    description: Optional[str]
    const: Optional[bool]
    gt: Optional[float]
    ge: Optional[float]
    lt: Optional[float]
    le: Optional[float]
    multiple_of: Optional[float]
    allow_inf_nan: Optional[bool]
    max_digits: Optional[int]
    decimal_places: Optional[int]
    min_length: Optional[int]
    max_length: Optional[int]
    allow_mutation: bool
    regex: Optional[str]
    repr: bool
    type: Optional[Type]
