# app/exceptions.py
# Domain exceptions — raised by CRUD/service layer.
# HTTP mapping is done exclusively in the endpoint layer.


class RestaurantNotFound(Exception):
    """Raised when a restaurant_id does not exist in the database."""
    pass


class CapacityExceeded(Exception):
    """Raised when new booking would exceed restaurant max_capacity in the time window."""
    def __init__(self, max_capacity: int, available: int):
        self.max_capacity = max_capacity
        self.available = available
        super().__init__(f"Capacity exceeded: max={max_capacity}, available={available}")


class TimeSlotConflict(Exception):
    """Raised when the restaurant is fully booked for the requested time window."""
    pass


class BookingNotFound(Exception):
    """Raised when a booking_id does not exist or does not belong to the requesting user."""
    pass


class InvalidBookingStatus(Exception):
    """Raised when an invalid status string is provided."""
    def __init__(self, value: str):
        self.value = value
        super().__init__(f"Invalid booking status: {value}")