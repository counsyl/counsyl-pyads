class AdsSymbol(object):
    def __init__(
            self, index_group, index_offset, name, symtype, comment):
        self.index_group = index_group
        self.index_offset = index_offset
        self.name = name
        self.symtype = symtype
        self.comment = comment
