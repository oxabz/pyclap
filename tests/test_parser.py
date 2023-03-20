"""
Tests for the `clapp` package.
"""

import clapp

def test_version():
    assert clapp.__version__ == '0.1.0'

def test_basic_usage():
    @clapp.parser()
    class Test:
        a: int
        b: float
        c: str

    t = Test(["2", "0.4", "test"])
    assert t.a == 2
    assert t.b == 0.4
    assert t.c == "test"

def test_named_arguments():
    @clapp.parser()
    class Test:
        positional: int
        not_positional_: float

    t = Test(["2", "-n", "0.4"])
    assert t.positional == 2
    assert t.not_positional_ == 0.4

    t = Test(["2", "--not_positional", "0.4"])
    assert t.positional == 2
    assert t.not_positional_ == 0.4

    try:
        t = Test(["2"])
        assert False
    except SystemExit:
        assert True

def test_default_values():
    @clapp.parser()
    class Test:
        not_named: int # a positional argument cant have a default value
        named_: float = 0.4

    t = Test(["2"])
    assert t.not_named == 2
    assert t.named_ == 0.4

    t = Test(["4", '-n', "0.7"])
    assert t.not_named == 4
    assert t.named_ == 0.7

def test_custom_parsers():
    class TestType:
        inner: float
        def __init__(self, s: str) -> None:
            self.inner = float(s)
            super().__init__()

    @clapp.parser()
    class Test:
        a: int
        b: float
        c: float
        d: TestType
        e_: int = 0
        hello: str = "world"

        def _parse_a(arg: str) -> int:
            return int(arg) + 1
        
        def _parse_float(arg: str) -> float:
            return float(arg) + 0.1
        
        def _parse_c(arg: str) -> float:
            return float(arg) + 0.4
        
        def _parse_hello(arg: str) -> str:
            return "hello " + arg + "!"
        
        def _parse_e(arg: str) -> int:
            return int(arg) + 1
        


    t = Test(["2", "0.4", "0.4", "0.4", "matt"])
    assert t.a == 3
    assert t.b == 0.5
    assert t.c == 0.8
    assert t.d.inner == 0.4
    assert t.hello == "hello matt!"
    assert t.e_ == 0