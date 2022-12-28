from typing import (Any, ByteString, Callable, Dict, Generator, Iterable,
                    Iterator, List, NoReturn, Optional, Sequence, Set, Tuple, Type,
                    Union, NewType)
from pwnxy.globals import __registered_cmds_cls__
import pwnxy.file
from pwnxy.cmds import (Cmd, register)
from pwnxy.utils.debugger import (unwrap, assert_eq, assert_ne, todo)
from pwnxy.utils.output import (xy_print, info, err, note, dbg)
from pwnxy.utils.color import Color
import gdb
from collections import OrderedDict
TYPES = OrderedDict({
    bool : gdb.PARAM_BOOLEAN,
    int  : gdb.PARAM_ZINTEGER,
    str  : gdb.PARAM_STRING
})
def get_gdb_param_by_type(t : type):
    ret = TYPES[t]
    if ret is None:
        err("TODO:")
    return ret
    
'''GDB API
The value of `set_doc` should give a brief summary specific to the set action, this text is only displayed when the user runs the help set command for this parameter. 

The value of `show_doc` should give a brief summary specific to the show action, this text is only displayed when the user runs the help show command for this parameter. The class documentation should be used to give a fuller description of what the parameter does, this text is displayed for both the help set and help show commands.

```
# pwnxy @ function > help set squ
123
This command is not documented.

# pwnxy @ function > help show squ
Custom show doc
This command is not documented.
```
'''
class Parameter(gdb.Parameter):
    '''
    TODO: this is document
    '''
    def __init__(self, argname, default_val, setdesc : str = "", docdesc : str = ""):
        self.set_doc = docdesc
        self.show_doc = setdesc
        super().__init__(argname, 
                         gdb.COMMAND_SUPPORT,
                         get_gdb_param_by_type(type(default_val)))
        