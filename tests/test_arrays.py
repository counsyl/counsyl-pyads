import pytest

from counsyl_pyads.adsdatatypes import AdsArrayDatatype
from counsyl_pyads.adsdatatypes import INT


@pytest.fixture
def dims_1dim():
    return [(1, 3)]


@pytest.fixture
def flat_1dim():
    return (9, 8, 7)


@pytest.fixture
def dict_1dim():
    return {1: 9, 2: 8, 3: 7}


@pytest.fixture
def dims_2dim():
    return [(1, 2), (3, 4)]


@pytest.fixture
def flat_2dim():
    return (1, 2, 3, 5)


@pytest.fixture
def dict_2dim():
    return {1: {3: 1, 4: 2}, 2: {3: 3, 4: 5}}


class TestArray(object):

    def test_flatten_1dim(self, dims_1dim, flat_1dim, dict_1dim):
        arr = AdsArrayDatatype(INT, dims_1dim)
        dict_ = dict_1dim
        flat = arr._dict_to_flat_list(dict_)
        assert(flat == flat_1dim)

    def test_flatten_2dim(self, dims_2dim, flat_2dim, dict_2dim):
        arr = AdsArrayDatatype(INT, dims_2dim)
        dict_ = dict_2dim
        flat = arr._dict_to_flat_list(dict_)
        assert(flat == flat_2dim)

    def test_unflatten_1dim(self, dims_1dim, flat_1dim, dict_1dim):
        arr = AdsArrayDatatype(INT, dims_1dim)
        flat = flat_1dim
        dict_ = arr._flat_list_to_dict(flat)
        assert(dict_ == dict_1dim)

    def test_unflatten_2dim(self, dims_2dim, flat_2dim, dict_2dim):
        arr = AdsArrayDatatype(INT, dims_2dim)
        flat = flat_2dim
        dict_ = arr._flat_list_to_dict(flat)
        assert(dict_ == dict_2dim)
