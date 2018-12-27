import datetime as date

class FloorCall() :

    def __init__(self, source, direction) :
        self.time = date.datetime.now()
        self.source = source
        self.direction = direction
 
class CarCall() :

    def __init__(self, to) :
        self.to = to