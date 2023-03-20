"""
# Command Line Argument Parser for Python
A simple library for parsing command line arguments into class attributes using type annotations to reduce the boiler plate.
This library is inspired by the rust library clap. It is a wrapper arround the argparse library.

## Usage
*basic usage*
```python
from clapp import parser

@parser
class Test:
    a: int
    b: float
    c: str

# when called with the command line arguments "2 0.4 test"
t = Test()
print(t.a, t.b, t.c) # 2 0.4 test

*named arguments*
```python
from clapp import parser

@parser
class Test:
    positional: int # a positional argument
    not_positional_: float # a named argument recognized by the trailing underscore

# when called with the command line arguments "2 -n 0.4" or "2 --not_positional 0.4"
t = Test()
print(t.positional, t.not_positional) # 2 0.4
```

*default values*
```python
from clapp import parser

@parser
class Test:
    a: int # a positional argument cant have a default value
    b: float
    c_: str = "test"

# when called with the command line arguments "2 0.4"
t = Test()
print(t.a, t.b, t.c) # 2 0.4 test

# when called with the command line arguments "4 0.7 -c hello"
t = Test()
print(t.a, t.b, t.c) # 4 0.7 hello
```

*custom parsers*
```python
from clapp import parser

@parser
class TestType:
    inner: float

    def __init__(self, s: str) -> None:
        self.inner = float(s)

class Test:
    a: int
    b: float
    c: float
    t: TestType
    d_: int = 0

    # custom parser for the argument "a"
    def _parse_a(arg: str) -> int:
        return int(arg) + 1
    
    # custom parser for all the arguments of type float
    def _parse_float(arg: str) -> float:
        return float(arg) + 0.1

    # argument specific parser overrides the type specific parser
    def _parse_c(arg: str) -> float:
        return float(arg)

# when called with the command line arguments "2 0.4 0.5 0.6"
t = Test()
print(t.a, t.b, t.c) # 3 0.5 0.4
print(t.t.inner) # 0.6
print(t.d_) # 0
```
*flags*
```python
from clapp import parser

@parser
class Test:
    a_: bool
    b_: bool

# when called with the command line arguments "-a"
t = Test()
print(t.a, t.b) # True False
"""

import sys
from typing import Any, Callable, List, Tuple, Optional
from argparse import ArgumentParser
from clapp.generators import add_arg
from clapp.readers import get_attributes



def parser(**kwargs):
    """Decorator for creating a command line parser.
    
    Keyword Arguments:
    The decorater takes the same arguments as the [ArgumentParser](https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser) constructor.
        - prog -- The name of the program (default:
            ``os.path.basename(sys.argv[0])``)
        - usage -- A usage message (default: auto-generated from arguments)
        - description -- A description of what the program does
        - epilog -- Text following the argument descriptions
        - parents -- Parsers whose arguments should be copied into this one
        - formatter_class -- HelpFormatter class for printing help messages
        - prefix_chars -- Characters that prefix optional arguments
        - fromfile_prefix_chars -- Characters that prefix files containing
            additional arguments
        - argument_default -- The default value for all arguments
        - conflict_handler -- String indicating how to handle conflicts
        - add_help -- Add a -h/-help option
        - allow_abbrev -- Allow long options to be abbreviated unambiguously
        - exit_on_error -- Determines whether or not ArgumentParser exits with
            error info when an error occurs

    Returns:
        A decorator that parses the command line arguments into the class attributes.
    """
    def parser(cls):
        attrs = get_attributes(cls)

        # Replacing the old init with the init that parses the input
        old_init = cls.__init__
        def __new_init__(self, args_seq: Optional[List[str]] = None, **kwargs):
            self._parser = ArgumentParser(**kwargs)
            args_seq = args_seq if args_seq is not None else sys.argv[1:]

            used_short = []
            # Adding the arguments to the parser
            for (name, typ, default_val, parser_fn) in attrs:
                short = add_arg(self._parser, name, typ, default_val, used_short, parser_fn)
                if short is not None:
                    used_short.append(short)
                
            # Parsing the arguments
            args = self._parser.parse_args(args_seq).__dict__

            # Setting the attributes
            for (name, typ, default_val, parser_fn) in attrs:
                setattr(self, name, args[name.removesuffix('_')])

            # Calling the old init
            if old_init is not None:
                old_init(self)
        cls.__init__ = __new_init__
        return cls
    return parser

__version__ = "0.1.0"