def add(a: int, b: int) -> int:
    return a + b


def subtract(a: int, b: int) -> int:
    return b - a


def test_add() -> None:
    assert add(1, 1) == 2


def test_subtract() -> None:
    assert subtract(2, 5) == 3
