"""
This module contains the functions that read the classes passed to clapp and extract the attribute informations
"""
from typing import List, Any, Callable, Optional, Tuple
import typing

from attr import dataclass


@dataclass
class Attribute:
    """
    Represents an attribute of a class.
    """
    name: str
    type: type
    default: Any
    parser: Optional[Callable]
    options: Optional[List[str]]


def get_attributes(cls) -> List[Attribute]:
    """
    Returns a list of tuples containing the attribute name, type and default value.
    """
    attrs = cls.__annotations__

    return [Attribute(name, typ, getattr(cls, name, None), get_arg_parser(cls, name) or get_type_parser(cls, typ), get_arg_options(cls, name)) for name, typ in attrs.items()]


def get_type_parser(cls, typ: type) -> Optional[Callable]:
    """
    Returns the parser function for the given type.
    """
    if is_optional(typ):
        typ = get_optional_t(typ)
    type_name = typ.__name__.lower()
    if f"_parse_{type_name}" in cls.__dict__:
        return cls.__dict__[f"_parse_{type_name}"]


def get_arg_parser(cls, arg: str) -> Optional[Callable]:
    """
    Returns the parser function for the given command line argument.
    """
    arg = arg.lower()
    if f"_parse_{arg}" in cls.__dict__:
        return cls.__dict__[f"_parse_{arg}"]


def get_arg_options(cls, arg: str) -> Optional[List[str]]:
    """
    Returns the options for the given command line argument.
    """
    arg = arg.lower()
    if f"_options_{arg}" in cls.__dict__:
        return cls.__dict__[f"_options_{arg}"]


def is_optional(t):
    if not hasattr(t, "__origin__"):
        return False
    if not hasattr(t, "__args__"):
        return False
    return t.__origin__ == typing.Union and t.__args__[1] == type(None)


def get_optional_t(t):
    return t.__args__[0]
