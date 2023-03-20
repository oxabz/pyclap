from argparse import ArgumentParser
from typing import Any, List


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
    