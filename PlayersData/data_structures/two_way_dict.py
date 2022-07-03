class TwoWayDict(dict):
    def __init__(self, *args):
        if len(args) and isinstance(args[0], dict):
            args[0].update({value: key for key, value in args[0].items()})
        super().__init__(*args)

    def __setitem__(self, key, value):
        # Remove any previous connections with these values
        if key in self:
            del self[key]
        if value in self:
            del self[value]
        dict.__setitem__(self, key, value)
        dict.__setitem__(self, value, key)

    def __delitem__(self, key):
        dict.__delitem__(self, self[key])
        dict.__delitem__(self, key)

    def __len__(self):
        """Returns the number of connections"""
        return dict.__len__(self) // 2