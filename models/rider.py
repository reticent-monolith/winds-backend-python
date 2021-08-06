class Rider:
    def __init__(self, weight, trolley, front=None, middle=None, rear=None, added=0, speed=0):
        self.weight = weight
        self.trolley = trolley
        self.frontSlider = front
        self.middleSlider = middle
        self.rearSlider = rear
        self.addedWeight = added
        self.speed = speed

    @classmethod
    def from_dict(cls, d):
        return cls(
            weight=d['weight'],
            trolley=d['trolley'],
            front=d['frontSlider'] if 'frontSlider' in d.keys() else None,
            middle=d['middleSlider'] if 'middleSlider' in d.keys() else None,
            rear=d['rearSlider'] if 'rearSlider' in d.keys() else None,
            added=d['addedWeight'] if 'addedWeight' in d.keys() else None,
            speed=d['speed'] if 'speed' in d.keys() else None
        )
