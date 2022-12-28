from typing import (Any, ByteString, Callable, Dict, Generator, Iterable,
                    Iterator, List, NoReturn, Optional, Sequence, Set, Tuple, Type,
                    Union, NewType)
from pwnxy.utils.debugger import (assert_eq, assert_ne, todo, debug)
from pwnxy.utils.output import (info, err, note, dbg)
from pwnxy.utils.color import Color
# import pwnxy.globals
try:
    import gdb
except ModuleNotFoundError:
    note("import gdb can't be standalon")

cmds : List[Type["Cmd"]] = []
cmds_name : Set[str] = set()

__registered_cmds_cls__ : Set[Type["Cmd"]] = set()

'''APIs:
gdb.execute (command [, from_tty [, to_string]]) ->  str | None
    The `from_tty` flag specifies whether GDB ought to consider this command as having originated from the user invoking it interactively. It must be a boolean value. If omitted, it defaults to False.
    any output produced by command is sent to GDB’s standard output (and to the log output if logging is turned on). If the to_string parameter is True, then output will be collected by gdb.execute and returned as a string. The default is False
'''

'''Cmd:
    This is an abstract class for invoking commands, should not be instantiated
'''

class Cmd(gdb.Command):
    builtin_override_whitelist = {'up', 'down', 'search', 'pwd', 'start'} # TODO: 
    def __init__(self ,cmdline : str):
        super().__init__(cmdline, gdb.COMMAND_USER) # TODO:
        # TODO:
    # TODO: return type use?
    def __usage__(self) -> None:
        # TODO:
        ...
    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()

    def split_args(self, arguline : str) -> List[str]:
        '''
            Split a command-line string from the user into arguments.
        '''
        return gdb.string_to_argv(arguline)
    
    def invoke(self, arguline, from_tty):
        """
            Invoke the command with an argument string
        """
        # TODO: complete
        try:
            args : List[str] = self.split_args(arguline) 
        except Exception as e: # TODO: extend here
            err(e)
        
        # gdb.execute(args) TODO:

    def check_whether_recorded(self, argument_TODO ,from_tty : bool) -> bool :
        '''
        recoding all cmds, TODO: but not know what propose this fn?
        '''


        '''
        (gdb) show commands 
            1  q
            2  start
            3  q
            4  python help
            5  source ./gdbinit.py 
        '''
        lines_tmp = gdb.execute("show commands", from_tty = False, to_string = True)
        if lines_tmp is not None:
            lines = lines_tmp.splitlines()
        # empty history
        if not lines:
            return False

        last_line = lines[-1]

        '''split api
        sep : The delimiter according which to split the string. None means split according to any whitespace
        Maximum : number of splits to do. -1 (the default value) means no limit.
        ''' 
        num, cmd = last_line.split(None ,1)
        # TODO: history record this cmd if not executed before
        return True
    
        '''__call__
        Python has a set of built-in methods and __call__ is one of them.
        object() is shorthand for object.__call__()

        # Instance created
        e = Example()
        
        # __call__ method will be called
        e()
        '''
        def __call__(self, *args, **kwargs) :
            ...
            # TODO:

class PwnxyCmd:
    # TODO: Maybe load task delegate top Cmd class??
    # NOTE: instantiate all registered class
    def __inst_all__(self):
        '''
        Load all cmd to gdb
        '''
        args = []
        dbg(f"__registered_cmds_cls__ is {__registered_cmds_cls__}")
        for rcc in __registered_cmds_cls__:
            rcc_inst = rcc()




# TODO: seemings sloppy : This function should be used as ``argparse.ArgumentParser`` .add_argument method's `type` helper
def gdb_parse(s : str):
    _mask = 0xffffffffffffffff
    _mask_val_type = gdb.Value(_mask).type
    try:
        val = gdb.parse_and_eval(s)
        return int(val.cast(_mask_val_type))
    except Exception as e:
        err(e)
    
# TODO: Maybe have register function
def register(cls: Type["Cmd"]) -> Type[Cmd] :
    dbg(f"{cls} registered")
    assert(issubclass(cls, Cmd))
    assert(hasattr(cls, "invoke"))
    assert(hasattr(cls, "cmdname"))
    assert(all(map(lambda x: x.cmdname != cls.cmdname, __registered_cmds_cls__)))
    __registered_cmds_cls__.add(cls)
    return cls

@debug
def show_registered_cmds():
    for i in __registered_cmds_cls__:
        dbg(f"{i}")

# TODO: move to other
def is_alive() -> bool:
    """Check if GDB is running."""
    try:
        return gdb.selected_inferior().pid > 0
    except Exception:
        return False

# DECORATOR
# DEPRE: 
def only_if_running(func : Callable):
    import functools
    dbg("DEPRECATED:")
    @functools.wraps(func)
    def inner(*args, **kwargs):
        if is_alive():
            return func(*args, **kwargs)
        else:
            note("This program in not running")
    return inner

