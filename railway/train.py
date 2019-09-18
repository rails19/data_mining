class Train(object):
    """Train class"""

    def __init__(self, id):
        super(Train, self).__init__()
        self.id = id

    def __str__(self):
        return str({'train_id': self.id})
