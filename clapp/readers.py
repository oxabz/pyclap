"""
This module contains the functions that read the classes passed to clapp and extract the attribute informations
"""
from typing import List, Any, Callable, Optional, Tuple

def get_attributes(cls) -> List[Tuple[str, type, Any, Optional[Callable]]]:
    """
    Returns a list of tuples containing the attribute name, type and default value.
    """
    attrs = cls.__annotations__

    return [(name, typ, getattr(cls, name, None), get_type_parser(cls, typ) or get_arg_parser()) for name, typ in attrs.items()]


def get_type_parser(cls, typ: type) -> Optional[Callable]:
    """
    Returns the parser function for the given type.
    """
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