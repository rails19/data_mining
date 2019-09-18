class Station(object):
    """Station class"""

    def __init__(self, id, name, isPlatform):
        super(Station, self).__init__()
        self.id = id
        self.name = name
        self.isPlatform = isPlatform

    def __str__(self):
        return str({'station_id': self.id,
                    'station_name': self.name,
                    'station_isPlatform': self.isPlatform})
