

from skbio import DistanceMatrix
from skbio.tree import nj
import numpy as np

data = [[0.0,  5.0,  9.0,  9.0,  8.0],
        [5.0,  0.0, 10.0, 10.0,  9.0],
        [9.0, 10.0,  0.0,  8.0,  7.0],
        [9.0, 10.0,  8.0,  0.0,  3.0],
        [8.0,  9.0,  7.0,  3.0,  0.0]]

def normalize_matrix(m):
    m = np.array(m)
    print(m.max())
    max_matrix = m.max()
    for f in range(0, len(m)):
        for c in range(0, len(m)):
            #print(m[f,c])
            m[f, c] = m[f, c]/max_matrix

    print(m)

normalize_matrix(data)

ids = list('abcde')
dm = DistanceMatrix(data, ids)

tree = nj(dm)
print(tree.ascii_art())