import k2

def __make_chain_graph(symbols: k2.RaggedTensor,
                       device: Optional[Union[torch.device, str]] = "cpu") ->Fsa:
    symbols.

def expand_table(symbol_table: k2.SymbolTable) -> k2.SymbolTable:
    for s in symbol_table.symbols:
      symbol_table.add("#" + s)
    return symbol_table

def chain_graph(symbols: Union[List[List[int]], k2.RaggedTensor],
              device: Optional[Union[torch.device, str]] = "cpu") -> Fsa:
    '''Construct chain graphs from symbols.
    Note:
      The scores of arcs in the returned FSA are all 0.
    Args:
      symbols:
        It can be one of the following types:
            - A list of list-of-integers, e..g, `[ [1, 2], [1, 2, 3] ]`
            - An instance of :class:`k2.RaggedTensor`.
              Must have `num_axes == 2`.
      device:
        Optional. It can be either a string (e.g., 'cpu', 'cuda:0') or a
        torch.device.
        By default, the returned FSA is on CPU.
        If `symbols` is an instance of :class:`k2.RaggedTensor`, the returned
        FSA will on the same device as `k2.RaggedTensor`.
    Returns:
        An FsaVec containing the returned chain graphs, with "Dim0()" the same as
        "len(symbols)"(List[List[int]]) or "dim0"(k2.RaggedTensor)
    '''
    if not isinstance(symbols, k2.RaggedTensor):
        symbols = k2.RaggedTensor(symbols, device=device)

    ragged_arc, aux_labels = __make_chain_graph(symbols, device)
    fsa = Fsa(ragged_arc, aux_labels=aux_labels)
    return fsa