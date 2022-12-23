from enum import Enum
from typing import (Any, ByteString, Callable, Dict, Generator, Iterable,
                    Iterator, List, NoReturn, Optional, Sequence, Set, Tuple, Type,
                    Union, NewType)
from pwnxy.globals import __registered_cmds__
import pwnxy.file as file
from pwnxy.cmds import (Cmd, register)
from pwnxy.utils.debugger import (unwrap, assert_eq, assert_ne, todo)
from pwnxy.utils.output import (xy_print, info, err, hint, dbg)
from pwnxy.utils.color import Color

import gdb
'''GDB API
Programs which are being run under GDB are called inferiors
Python scripts can access information about and manipulate inferiors controlled by GDB via objects of the gdb.Inferior class.
'''

# NOTE: vmmap must be executed after program run
def vmmap():

    # TODO: considering to creat another pid class to get pid

    pid = gdb.selected_inferior().pid
    if pid == 0:
        ...
        # TODO: rt err : program not running, errmsg refer other full-fledged gdb-plugin
    if pid is None:
        err("gdb.selected_inferior().pid")
    vmmap_path = '/proc/%s/maps' % pid
    dbg(f"pid is {int(pid)}")

    data : ByteString = unwrap(file.get(vmmap_path))
    # if data_tmp is None:
    #     err("file.get(vmmap_path) failed")
    # data : ByteString = data_tmp

    lines = [line for line in data.decode().split('\n') if line is not '' ]
    '''
    [XYPRINT] : '00400000-00401000 r--p 00000000 08:20 102905                             /home/squ/prac/a.out'
    [XYPRINT] : '00401000-00402000 r-xp 00001000 08:20 102905                             /home/squ/prac/a.out'
    [XYPRINT] : '00402000-00403000 r--p 00002000 08:20 102905                             /home/squ/prac/a.out'
    [XYPRINT] : '00403000-00404000 r--p 00002000 08:20 102905                             /home/squ/prac/a.out'
    [XYPRINT] : '00404000-00405000 rw-p 00003000 08:20 102905                             /home/squ/prac/a.out'
    [XYPRINT] : '7ffff7dc1000-7ffff7de3000 r--p 00000000 08:20 33557850                   /usr/lib/x86_64-linux-gnu/libc-2.31.so'
    [XYPRINT] : '7ffff7de3000-7ffff7f5b000 r-xp 00022000 08:20 33557850                   /usr/lib/x86_64-linux-gnu/libc-2.31.so'
    [XYPRINT] : '7ffff7f5b000-7ffff7fa9000 r--p 0019a000 08:20 33557850                   /usr/lib/x86_64-linux-gnu/libc-2.31.so'
    [XYPRINT] : '7ffff7fa9000-7ffff7fad000 r--p 001e7000 08:20 33557850                   /usr/lib/x86_64-linux-gnu/libc-2.31.so'
    [XYPRINT] : '7ffff7fad000-7ffff7faf000 rw-p 001eb000 08:20 33557850                   /usr/lib/x86_64-linux-gnu/libc-2.31.so'
    [XYPRINT] : '7ffff7faf000-7ffff7fb5000 rw-p 00000000 00:00 0 '
    [XYPRINT] : '7ffff7fca000-7ffff7fce000 r--p 00000000 00:00 0                          [vvar]'
    [XYPRINT] : '7ffff7fce000-7ffff7fcf000 r-xp 00000000 00:00 0                          [vdso]'
    [XYPRINT] : '7ffff7fcf000-7ffff7fd0000 r--p 00000000 08:20 33557842                   /usr/lib/x86_64-linux-gnu/ld-2.31.so'
    [XYPRINT] : '7ffff7fd0000-7ffff7ff3000 r-xp 00001000 08:20 33557842                   /usr/lib/x86_64-linux-gnu/ld-2.31.so'
    [XYPRINT] : '7ffff7ff3000-7ffff7ffb000 r--p 00024000 08:20 33557842                   /usr/lib/x86_64-linux-gnu/ld-2.31.so'
    [XYPRINT] : '7ffff7ffc000-7ffff7ffd000 r--p 0002c000 08:20 33557842                   /usr/lib/x86_64-linux-gnu/ld-2.31.so'
    [XYPRINT] : '7ffff7ffd000-7ffff7ffe000 rw-p 0002d000 08:20 33557842                   /usr/lib/x86_64-linux-gnu/ld-2.31.so'
    [XYPRINT] : '7ffff7ffe000-7ffff7fff000 rw-p 00000000 00:00 0 '
    [XYPRINT] : '7ffffffdd000-7ffffffff000 rw-p 00000000 00:00 0                          [stack]'
    '''

    for ln in lines:
        xy_print(ln)

    # TODO: understand dev and inode 
    # dev => master:slave dev number
    # inode => TODO:
    maps, perm, offset, dev, inode, path = lines[0].split(None, 5)
    dbg(f"maps is {maps}")
    dbg(f"perm is {perm}")
    dbg(f"offset is {offset}")
    dbg(f"dev is {dev}")
    dbg(f"inode is {inode}")
    dbg(f"path is {path}")

    start, end = maps.split('-')

    

    '''
    ideal output like gef :

    Start              End                Offset             Perm Path
    0x0000000000400000 0x0000000000401000 0x0000000000000000 r-- /home/squ/prac/a.out
    '''

    # TODO: colorify it

@register
class VmmapCmd(Cmd):
    cmdname = "vmmap"
    
    # TODO: what's args
    def do_invoke(self, args : List[str]) -> None:
        argc = len(args)
        dbg("TODO:")

    ...
    # TODO:
    
