from argparse import ArgumentParser
from typing import Any, List, Optional
from clapp.readers import Attribute

def add_arg(parser: ArgumentParser, attribute: Attribute, used_short: List[str]) -> Optional[str]:
    """
    Adds an argument to the given parser.
    """
    attr = attribute.name
    typ = attribute.type
    default = attribute.default
    parse = attribute.parser

    parse = parse if parse is not None else lambda x: typ(x)
    if(attr.endswith('_')):
        attr = attr.removesuffix('_')
        short = None
        for i in range(len(attr)):
            if (short := attr[i]) not in used_short and short != '_':
                break

        # handling flags
        if typ == bool:
            if short is None:
                parser.add_argument(f"--{attr}", action="store_true")
            else:
                parser.add_argument(f"-{short}", f"--{attr}", action="store_true")
                return short
            return None    
        
        if short is None: 
            parser.add_argument(f"--{attr}", type=parse, default=default, required=default is None)
        else:
            parser.add_argument(f"-{short}", f"--{attr}", type=parse, default=default, required=default is None)
            return short
        
    else:
        parser.add_argument(attr, type=parse)
    