import k2
import torch
from typing import Optional
from typing import Union


def _chain_expand_table(symbols: k2.SymbolTable) -> k2.SymbolTable:
    for s in symbols.symbols[1:-1]:
        symbols.add("#" + s)
    return symbols


def chain_topo(symbols: k2.SymbolTable,
               device: Optional[Union[torch.device, str]] = None) -> k2.Fsa:
    '''Create a Chain topology.
    Args:
        symbols:
        We assume that token IDs are contiguous (start from 1).
        Last token is global <blk>.
        device:
        Optional. It can be either a string (e.g., 'cpu',
        'cuda:0') or a torch.device.
        If it is None, then the returned FSA is on CPU.
    Returns:
        Return Chain topology as an FSA and expanded symbol table.
    '''
    blk = symbols.ids[-1]
    max_int = blk - 1
    ext_symbols = _chain_expand_table(symbols)
    fsa_str = ["0 0 %d 0" % (blk)]
    fsa_str += ["0 %d %d 0" % (s, s) for s in range(1, max_int+1)]
    fsa_str += ["%d %d %d 0" % (s, s*2, s*2+1) for s in range(1, max_int+1)]
    fsa_str += ["%d %d %d 0" % (s*2, s*2, s*2+1) for s in range(1, max_int+1)]
    fsa_str += ["%d 0 0 0" % (s) for s in range(1, max_int+1)]
    fsa_str += ["%d %d -1 0" % (s, max_int*2+1) for s in range(0, max_int+1)]
    fsa_str += ["%d %d -1 0" % (s*2, max_int*2+1) for s in range(0, max_int+1)]
    fsa_str += [str(max_int*2+1)]
    fsa = k2.Fsa.from_str("\n".join(sorted(fsa_str)))
    return k2.arc_sort(fsa), ext_symbols
