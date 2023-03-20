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

def test_usage_flags():
    @clapp.parser()
    class Test:
        a_: bool
        b_: bool
    
    t = Test(["-a"])
    assert t.a_ == True
    assert t.b_ == False

    t = Test(["-b"])
    assert t.a_ == False
    assert t.b_ == True

    t = Test(["-a", "-b"])
    assert t.a_ == True
    assert t.b_ == True

def test_usage_choices():
    @clapp.parser()
    class Test:
        a_: str = "a"
        b_: str
        c: str

        _options_a_ = ["a", "b", "c"]
        _options_b_ = ["a", "b", "c"]
        _options_c = ["a", "b", "c"]

    t = Test(["-b", "a", "b"])
    assert t.a_ == "a"
    assert t.b_ == "a"
    assert t.c == "b"

    t = Test(["-a", "c", "-b", "b", "b"])
    assert t.a_ == "c"
    assert t.b_ == "b"
    assert t.c == "b"

    try:
        t = Test(["-a", "d", "-b", "b", "b"])
        assert False
    except SystemExit:
        assert True
