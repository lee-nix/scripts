'''
Packet Delivery -- Enforcing Constraints
https://www.codewars.com/kata/packet-delivery-enforcing-constraints/python
Author: Lee Nix
Version: 1.0

Testing:
from packet_delivery import Package
p = Package(*[351, 30, 10, 10])
'''
class DimensionsOutOfBoundError(Exception):
    pass

class Package(object):
    _MAX_VALUES = { 'length': 350,
                    'width': 300,
                    'height': 150,
                    'weight': 40 }
    
    def __init__(self, length, width, height, weight):
        # Use custom Package setattr function to enable input validation
        self.length = length
        self.width = width
        self.height = height
        self.weight = weight

    def __setattr__(self, name, value):
        # Only try to validate input if it's an expected attribute
        # This has the added affect of preventing any other attributes
        # from being added to instances and protects the value of volume
        if name in self._MAX_VALUES:
            if 0 < value <= self._MAX_VALUES[name]:
                object.__setattr__(self, name, value)
            else:
                # Raise our custom exception if values are out of bounds
                raise DimensionsOutOfBoundError('Package {}=={} out of bounds, should be: 0 < {} <= {}'.format(name, value, name, self._MAX_VALUES[name]))
            
            # Update the volume each time an attribute is updated
            # IF all the values needed already exist
            # This avoids AttributeErrors during init
            if hasattr(self, 'length') and hasattr(self, 'width') and hasattr(self,'height'):
                object.__setattr__(self, 'volume', self.length * self.width * self.height)
