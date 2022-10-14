import typing
import pathlib


class NotFound(Exception):
    """NotFound is the error that there is no file for some path."""

    pass


class NameCollision(Exception):
    """NameCollision is the error that try to create a file with invalid path."""

    pass


class File(typing.Protocol):
    """File is a interface that can read and write content."""

    def read(self) -> bytes:
        pass

    def write(self, content: bytes) -> None:
        pass


class Path(typing.Protocol):
    """Path is a interface that represent the path and name of some file."""

    def __hash__(self) -> int:
        pass

    def __eq__(self, other) -> bool:
        pass

    def __str__(self) -> str:
        pass

    def parent(self) -> str:
        pass

    def base(self) -> str:
        pass


class Directory(typing.Protocol):
    """Directory is a interface that can add, remove and iterate files"""

    def __iter__(self) -> typing.Iterator[Path]:
        pass

    def add(self, path: Path, file: File) -> None:
        pass

    def create(self, path: Path) -> File:
        pass

    def remove(self, path: Path) -> None:
        pass

    def get(self, path: Path) -> File:
        pass


class FakeFile:
    """FakeFile is a file that can be used on "add" method for some Directory"""

    _content: bytes

    def __init__(self, content: bytes) -> None:
        self._content = content

    def read(self) -> bytes:
        return self._content

    def write(self, content: bytes) -> None:
        self._content = content


class FakeDirectory:
    """FakeDirectory implements Directory protocol in memory."""

    _dir: typing.Dict[str, bytes]

    def __init__(self) -> None:
        self._dir = {}
        pass

    def __iter__(self) -> typing.Iterator[Path]:
        paths: typing.List[Path] = []
        for key in self._dir:
            paths.append(SomePath(key))

        return iter(paths)

    def add(self, path: Path, file: File) -> None:
        if str(path) in self._dir:
            raise NameCollision()

        self._dir[str(path)] = file.read()

    def create(self, path: Path) -> File:
        if str(path) in self._dir:
            raise NameCollision()

        self._dir[str(path)] = b""
        return _FakeDirectoryFile(self._dir, str(path))

    def remove(self, path: Path) -> None:
        if str(path) not in self._dir:
            raise NotFound()

        del self._dir[str(path)]

    def get(self, path: Path) -> File:
        if str(path) not in self._dir:
            raise NotFound()

        return _FakeDirectoryFile(self._dir, str(path))


class _FakeDirectoryFile:
    _dir: typing.Dict[str, bytes]
    _path: str

    def __init__(self, dir: typing.Dict[str, bytes], path: str) -> None:
        self._dir = dir
        self._path = path

    def read(self) -> bytes:
        return self._dir[self._path]

    def write(self, content: bytes) -> None:
        self._dir[self._path] = content


class SomePath:
    _path: pathlib.PurePath

    def __init__(self, path: str) -> None:
        self._path = pathlib.PurePath(path)
        self._path.__hash__

    def __hash__(self) -> int:
        return hash(self._path)

    def __eq__(self, other) -> bool:
        if not isinstance(other, SomePath):
            return NotImplemented
        return self._path == other._path

    def __str__(self) -> str:
        return str(self._path)

    def parent(self) -> str:
        return str(self._path.parent)

    def base(self) -> str:
        return self._path.name
