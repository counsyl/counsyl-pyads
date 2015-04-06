from counsyl_pyads.adsdatatypes import AdsArrayDatatype
from counsyl_pyads.adsdatatypes import INT


class TestArray(object):

    dims_1dim = [(1, 3)]
    flat_1dim = (9, 8, 7)
    dict_1dim = {1: 9, 2: 8, 3: 7}

    dims_2dim = [(1, 2), (3, 4)]
    flat_2dim = (1, 2, 3, 5)
    dict_2dim = {1: {3: 1, 4: 2}, 2: {3: 3, 4: 5}}

    def test_flatten_1dim(self):
        arr = AdsArrayDatatype(INT, self.dims_1dim)
        dict_ = self.dict_1dim
        flat = arr._dict_to_flat_list(dict_)
        assert(flat == self.flat_1dim)

    def test_flatten_2dim(self):
        arr = AdsArrayDatatype(INT, self.dims_2dim)
        dict_ = self.dict_2dim
        flat = arr._dict_to_flat_list(dict_)
        assert(flat == self.flat_2dim)

    def test_unflatten_1dim(self):
        arr = AdsArrayDatatype(INT, self.dims_1dim)
        flat = self.flat_1dim
        dict_ = arr._flat_list_to_dict(flat)
        assert(dict_ == self.dict_1dim)

    def test_unflatten_2dim(self):
        arr = AdsArrayDatatype(INT, self.dims_2dim)
        flat = self.flat_2dim
        dict_ = arr._flat_list_to_dict(flat)
        assert(dict_ == self.dict_2dim)
