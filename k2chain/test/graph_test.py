import k2
from ..graph import chain_topo
def test_compose():
    syms = k2.SymbolTable.from_str('<eps> 0\nA 1\nB 2\nC 3\n')
    fst_a = chain_topo(syms, 'cpu')
    fsa_b = k2.linear_fsa([2, 2, 3])
    fsa_b.labels_sym = syms
    fst_c = k2.compose(fst_a, fsa_b)
