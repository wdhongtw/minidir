# minidir: Minimal directory interface and implementation

The minimal interface for directories and files and
two implementations: in-memory and real file system versions.

It's a good choice when we want to separate file-access side effects from
pure functional part of our code base.

## Installation

Already published on Pypi

```shell
pip install minidir
```

## Usage

- Interface: `Directory` -> `Path`, `File`
    - `Directory` is the container where we access `File` by `Path`
- Implementation
    - `SystemDirectory`: a `Directory` backed by real file system.
    - `FakeDirectory`: a `Directory` only exists in-memory.

Some error like `NameCollision` and `NotFound` will be raised in corresponding situations.

Example:

```python
import minidir

class SomeClass:
    folder: minidir.Directory

    def __init__(self, folder: minidir.Directory) -> None:
        # inject directory to separate side effect from core logic
        pass

def main():
    # use actual file system during production
    instance = SomeClass(minidir.SystemDirectory("/path/to/root"))

def test_some_class():
    # use in-memory implementation during test
    instance = SomeClass(minidir.FakeDirectory())
```

## Future Work

- Implementations for network-oriented storage, e.g. WebDAV, S3, Dropbox ...
- Stream based file read / write interface.
