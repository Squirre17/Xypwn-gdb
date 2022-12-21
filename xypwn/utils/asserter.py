from typing import (Any, ByteString, Callable, Dict, Generator, Iterable,
                    Iterator, List, NoReturn, Optional, Sequence, Set, Tuple, Type,
                    Union)
from xypwn.utils.output import (info, err, hint, dbg)

def assert_eq(x : Any, y : Any):
    if x != y:
        err(f"{x} != {y}")
        assert(x == y)

def assert_ne(x : Any, y : Any):
    if x == y:
        err(f"{x} == {y}")
        assert(x != y)

def todo():
    err("Plz impl me")
    exit(1)
    
if __name__ == "__main__":
    assert_eq(1, 2)

        
