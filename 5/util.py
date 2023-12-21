from typing import Generator, TypeVar


T = TypeVar("T")


def chunk_by_size(xs: list[T], chunk_size: int) -> Generator[T, None, None]:
    chunk = []
    for x in xs:
        if len(chunk) == chunk_size:
            yield chunk
            chunk = []

        chunk.append(x)

    yield chunk


def chunk_by_value(xs: list[T], value: T) -> Generator[T, None, None]:
    chunk = []
    for x in xs:
        if x == value and len(chunk) > 0:
            yield chunk
            chunk = []
        else:
            if x != "":
                chunk.append(x)

    yield chunk
