import numpy as np

from numpy.testing import assert_equal
from numpy.testing import assert_array_equal
from pyuoi.decomposition import CUR


def test_column_select_all():
    """Test that column select function selects all columns when provided the
    entire SVD and a suitable value of c."""
    X = np.random.randint(low=1, high=5, size=(10, 5))
    _, _, V = np.linalg.svd(X)
    column_flags = CUR.column_select(V.T, c=5)

    assert_array_equal(column_flags, np.array([True, True, True, True, True]))


def test_column_select():
    """Test that the column select function selects the vector with the highest
    leverage score most often."""
    n_samples = 10
    n_features = 5
    rank = 3
    n_reps = 5000

    X = np.random.randint(low=1, high=5, size=(n_samples, n_features))
    _, _, V = np.linalg.svd(X)
    V_subset = V[:rank].T
    column_flags = np.zeros((n_reps, n_features))

    for rep in range(n_reps):
        column_flags[rep] = CUR.column_select(V_subset, c=1)

    counts = np.sum(column_flags, axis=0)

    assert_equal(np.argmax(counts), np.argmax(np.sum(V_subset**2, axis=1)))


def test_UoI_CUR_basic():
    """Test UoI CUR with no resampling."""
    n_samples = 10
    n_features = 5
    max_k = 3
    n_resamples = 1
    resample_frac = 1

    X = np.random.randint(low=1, high=5, size=(n_samples, n_features))
    _, _, V = np.linalg.svd(X)
    V_subset = V[:max_k].T

    uoi_cur = CUR(n_resamples=n_resamples,
                  max_k=max_k,
                  resample_frac=resample_frac)
    uoi_cur.fit(X, c=2)

    max_col = np.argmax(np.sum(V_subset**2, axis=1))

    assert (max_col in uoi_cur.columns_)
