import time

from fastapi import HTTPException, Request


class TokenBucket:
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill_time = time.time()

    def allow_request(self) -> bool:
        current_time = time.time()
        elapsed_time = current_time - self.last_refill_time

        new_tokens = elapsed_time * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + new_tokens)
        self.last_refill_time = current_time

        if self.tokens >= 1:
            self.tokens -= 1
            return True

        return False


class TokenBucketRateLimiter:
    def __init__(self, capacity: int = 10, refill_rate: float = 1.0):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.buckets: dict[str, TokenBucket] = {}

    def get_client_key(self, request: Request) -> str:
        if request.client is None:
            return "unknown-client"

        return request.client.host

    def check_request(self, request: Request):
        client_key = self.get_client_key(request)

        if client_key not in self.buckets:
            self.buckets[client_key] = TokenBucket(
                capacity=self.capacity,
                refill_rate=self.refill_rate,
            )

        bucket = self.buckets[client_key]

        if not bucket.allow_request():
            raise HTTPException(
                status_code=429,
                detail="Too many requests. Please try again later.",
            )


rate_limiter = TokenBucketRateLimiter(
    capacity=10,
    refill_rate=1.0,
)
