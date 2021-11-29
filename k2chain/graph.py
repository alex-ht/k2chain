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
    fsa_str = [[0, 0, blk, 0, 0]]
    fsa_str += [[0, s, s, s, 0] for s in range(1, max_int+1)]
    fsa_str += [[s, s*2, s*2+1, 0, 0] for s in range(1, max_int+1)]
    fsa_str += [[s*2, s*2, s*2+1, 0, 0] for s in range(1, max_int+1)]
    fsa_str += [[s, 0, 0, 0, 0] for s in range(1, max_int+1)]
    fsa_str += [[s, max_int*2+1, -1, -1, 0] for s in range(0, max_int+1)]
    fsa_str += [[s*2, max_int*2+1, -1, -1, 0] for s in range(0, max_int+1)]
    fsa_str = [f"{x[0]} {x[1]} {x[2]} {x[3]} {x[4]}" for x in sorted(fsa_str)]
    fsa_str += [f"{max_int*2+1}"]
    fsa = k2.Fsa.from_str("\n".join(fsa_str), acceptor=False, num_aux_labels=1, aux_label_names=symbols.symbols)
    fsa.labels_sym = ext_symbols
    fsa = k2.arc_sort(fsa)
    return fsa
