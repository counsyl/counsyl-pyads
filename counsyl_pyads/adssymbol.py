class AdsSymbol(object):
    def __init__(
            self, read_length, index_group, index_offset, name, symtype,
            comment):
        self.read_length = read_length
        self.index_group = index_group
        self.index_offset = index_offset
        self.name = name
        self.symtype = symtype
        self.comment = comment
