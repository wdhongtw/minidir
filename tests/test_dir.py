import unittest
import tempfile

import minidir as pydir


class TestFakeDirectory(unittest.TestCase):
    """Test feature about fake directory."""

    def test_set_get(self) -> None:
        directory = pydir.FakeDirectory()

        file_bar = directory.create(pydir.SomePath("dir/bar"))
        file_bar.write(b"bar content")

        self.assertDictEqual(
            {
                "dir/bar": b"bar content",
            },
            directory._dir,
        )

    def test_iterate(self) -> None:

        directory = pydir.FakeDirectory()
        directory.create(pydir.SomePath("dir/bar"))
        directory.create(pydir.SomePath("dir/foo"))
        directory.remove(pydir.SomePath("dir/foo"))
        directory.create(pydir.SomePath("dir/dir/foo"))

        paths = set()
        for path in directory:
            paths.add(str(path))
        self.assertSetEqual(
            set(
                [
                    "dir/bar",
                    "dir/dir/foo",
                ]
            ),
            paths,
        )

    def test_create_collision(self) -> None:
        directory = pydir.FakeDirectory()
        directory.create(pydir.SomePath("dir/bar"))

        with self.assertRaises(pydir.NameCollision):
            directory.create(pydir.SomePath("dir/bar"))

    def test_get_not_found(self) -> None:
        directory = pydir.FakeDirectory()

        with self.assertRaises(pydir.NotFound):
            directory.get(pydir.SomePath("foo"))

    def test_remove_not_found(self) -> None:
        directory = pydir.FakeDirectory()

        with self.assertRaises(pydir.NotFound):
            directory.remove(pydir.SomePath("foo"))


class TestSystemDirectory(unittest.TestCase):
    """Test feature about file system directory."""

    def test_set_get(self) -> None:
        with tempfile.TemporaryDirectory() as name:

            directory = pydir.SystemDirectory(name)
            file_bar = directory.create(pydir.SomePath("bar"))
            file_bar.write(b"bar content")

            file_foo = directory.get(pydir.SomePath("bar"))
            self.assertEqual(b"bar content", file_foo.read())
            directory.remove(pydir.SomePath("bar"))

    def test_nested_folder(self) -> None:
        with tempfile.TemporaryDirectory() as name:

            directory = pydir.SystemDirectory(name)
            file_bar = directory.create(pydir.SomePath("dir/bar"))
            file_bar.write(b"bar content")

    def test_iterate(self) -> None:
        with tempfile.TemporaryDirectory() as name:

            directory = pydir.SystemDirectory(name)
            directory.create(pydir.SomePath("dir/bar"))
            directory.create(pydir.SomePath("dir/foo"))
            directory.remove(pydir.SomePath("dir/foo"))
            directory.create(pydir.SomePath("dir/dir/foo"))

            paths = set()
            for path in directory:
                paths.add(str(path))
            self.assertSetEqual(
                set(
                    [
                        "dir/bar",
                        "dir/dir/foo",
                    ]
                ),
                paths,
            )
