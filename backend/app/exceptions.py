class RestaurantNotFound(Exception): pass
class CapacityExceeded(Exception):
    def __init__(self, max_capacity: int):
        self.max_capacity = max_capacity
class TimeSlotConflict(Exception): pass