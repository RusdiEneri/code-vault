import time

class TokenBucket:
    def __init__(self, capacity: int, fill_rate: float):
        self.capacity = capacity
        self.fill_rate = fill_rate
        self.tokens = capacity
        self.last_update = time.time()

    def consume(self, amount: int = 1) -> bool:
        now = time.time()
        self.tokens = min(self.capacity, self.tokens + (now - self.last_update) * self.fill_rate)
        self.last_update = now
        if self.tokens >= amount:
            self.tokens -= amount
            return True
        return False
