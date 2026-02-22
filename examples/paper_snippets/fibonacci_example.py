"""Runnable Fibonacci example referenced in the manuscript."""


def fibonacci(n: int) -> int:
    """Return the nth Fibonacci number (0-indexed)."""
    if n < 0:
        raise ValueError("n must be non-negative")
    if n <= 1:
        return n

    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def solve_fifteenth_fibonacci() -> int:
    """Mirror the paper's example query: 15th Fibonacci number."""
    return fibonacci(15)


if __name__ == "__main__":
    print(solve_fifteenth_fibonacci())
