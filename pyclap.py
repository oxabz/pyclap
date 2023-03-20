from typing import Any, Callable, List, Tuple, Optional
from argparse import ArgumentParser

def add_arg(parser: ArgumentParser, attr: str, typ:type, default:Any, used_short: List[str], parse = None):
    parse = parse if parse is not None else lambda x: typ(x)
    if(attr.endswith('_')):
        attr = attr.removesuffix('_')
        short = None
        for i in range(len(attr)):
            if (short := attr[i]) not in used_short and short != '_':
                break
        if short is None: 
            parser.add_argument(f"--{attr}", type=parse, default=default)
        else:
            parser.add_argument(f"-{short}", f"--{attr}", type=parse, default=default)
            used_short.append(short)
    else:
        parser.add_argument(attr, type=parse, default=default)

def get_attributes(cls) -> List[Tuple[str, type, Any, Optional[Callable]]]:
    attrs = cls.__annotations__
    return [(k, v, getattr(cls, k, None)) for k, v in attrs.items()]


def get_type_parser(cls, typ: type) -> Optional[Callable]:
    type_name = typ.__name__.lower()
    if f"_parse_{type_name}" in cls.__dict__:
        return cls.__dict__[f"_parse_t_{type_name}"]

def get_arg_parser(cls, arg: str) -> Optional[Callable]:
    arg = arg.lower()
    if f"_parse_{arg}" in cls.__dict__:
        return cls.__dict__[f"_parse_{arg}"]
    

def parser(param=None):
    def parser(cls):
        attrs = cls.__annotations__

        # Replacing the old init with the init that parses the input
        old_init = cls.__init__
        def __new_init__(self):
            print("edited init ran")

            self._parser = ArgumentParser()

            used_short = []
            for [k, t] in attrs.items():
                add_arg(self._parser, k, t, None, used_short)

            args = self._parser.parse_args(["2", "0.4", "test"]).__dict__

            for k in attrs.keys():
                setattr(self, k, args[k.removesuffix('_')])


            if old_init is not None:
                old_init(self)
        cls.__init__ = __new_init__
        return cls
    return parser