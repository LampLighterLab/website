import os
import random
import shutil
import subprocess
import sys
import tempfile
import unittest
from io import BytesIO
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from prepare_portraits import MAX_BYTES, prepare


def photo(image_format="PNG", size=(1200, 900)):
    image = Image.frombytes("RGB", size, random.Random(7).randbytes(size[0] * size[1] * 3))
    output = BytesIO()
    image.save(output, image_format)
    return output.getvalue()


class PreparationTests(unittest.TestCase):
    def test_formats_are_square_small_metadata_free_and_idempotent(self):
        original = photo()
        for suffix, image_format in [(".jpg", "JPEG"), (".jpeg", "JPEG"), (".png", "PNG"), (".webp", "WEBP")]:
            with self.subTest(suffix=suffix):
                result = prepare(original, suffix)
                with Image.open(BytesIO(result)) as image:
                    self.assertEqual(image.format, image_format)
                    self.assertEqual(image.width, image.height)
                    self.assertLessEqual(image.width, 800)
                    self.assertFalse(image.getexif())
                self.assertLessEqual(len(result), MAX_BYTES)
                self.assertEqual(prepare(result, suffix), result)

    def test_camera_rotation_is_applied_before_crop(self):
        image = Image.new("RGB", (1200, 800), "red")
        image.paste("blue", (600, 0, 1200, 800))
        exif = Image.Exif()
        exif[274] = 6
        exif[315] = "Private metadata"
        source = BytesIO()
        image.save(source, "JPEG", exif=exif)
        with Image.open(BytesIO(prepare(source.getvalue(), ".jpg"))) as result:
            self.assertEqual(result.size, (800, 800))
            self.assertGreater(result.getpixel((400, 100))[0], 200)
            self.assertGreater(result.getpixel((400, 700))[2], 200)
            self.assertFalse(result.getexif())

    def test_small_transparent_photo_is_flattened_without_upscaling(self):
        source = BytesIO()
        Image.new("RGBA", (90, 120), (0, 0, 0, 0)).save(source, "PNG")
        with Image.open(BytesIO(prepare(source.getvalue(), ".jpg"))) as result:
            self.assertEqual(result.size, (90, 90))
            self.assertEqual(result.getpixel((45, 45)), (255, 255, 255))


class CommitHookTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.env = {**os.environ, "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1"}
        self.git("init", "-q")
        self.git("config", "user.name", "Portrait test")
        self.git("config", "user.email", "test@example.invalid")
        self.git("config", "core.hooksPath", str(ROOT / ".githooks"))
        (self.root / "scripts").mkdir()
        for name in ("check_commit.py", "prepare_portraits.py"):
            shutil.copy(ROOT / "scripts" / name, self.root / "scripts" / name)
        (self.root / ".venv/bin").mkdir(parents=True)
        (self.root / ".venv/bin/python").symlink_to(sys.executable)

    def git(self, *args, check=True):
        return subprocess.run(["git", *args], cwd=self.root, env=self.env,
                              check=check, capture_output=True)

    def add(self, name, data):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        self.git("add", "--", name)
        return path

    def check(self, *args):
        return subprocess.run([sys.executable, str(ROOT / "scripts/check_commit.py"), *args],
                              cwd=self.root, env=self.env, capture_output=True)

    def test_commit_automatically_prepares_and_stages_portrait(self):
        name = "assets/images/people/test_member.png"
        original = photo()
        path = self.add(name, original)
        result = self.git("commit", "-qm", "Add portrait", check=False)
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        committed = self.git("show", "HEAD:" + name).stdout
        self.assertEqual(committed, path.read_bytes())
        self.assertLess(len(committed), len(original))
        self.assertLessEqual(len(committed), MAX_BYTES)
        self.assertEqual(self.check("--check", "--all").returncode, 0)

    def test_large_files_are_checked_in_index_not_working_tree(self):
        path = self.add("large file.bin", b"x" * (1024 * 1024 + 1))
        path.write_bytes(b"small unstaged replacement")
        result = self.git("commit", "-qm", "Oversized", check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(b"1 MiB limit", result.stderr)
        self.assertEqual(path.read_bytes(), b"small unstaged replacement")

    def test_portrait_with_unstaged_changes_is_preserved(self):
        name = "assets/images/people/test_member.png"
        original = photo()
        path = self.add(name, original)
        path.write_bytes(b"unstaged photo edits")
        result = self.check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(b"unstaged changes", result.stderr)
        self.assertEqual(path.read_bytes(), b"unstaged photo edits")
        self.assertEqual(self.git("show", ":" + name).stdout, original)

    def test_check_mode_reports_unprepared_photo_without_modification(self):
        name = "assets/images/people/test_member.png"
        original = photo()
        path = self.add(name, original)
        result = self.check("--check", "--all")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(b"needs preparation", result.stderr)
        self.assertEqual(path.read_bytes(), original)
        self.assertEqual(self.git("show", ":" + name).stdout, original)

    def test_invalid_photo_or_filename_is_rejected(self):
        for name in ("assets/images/people/broken_photo.jpg", "assets/images/people/Wrong Name.jpg"):
            with self.subTest(name=name):
                self.add(name, b"not an image")
                self.assertNotEqual(self.check().returncode, 0)

    def test_large_unstaged_file_does_not_block_small_commit(self):
        (self.root / "not-staged.bin").write_bytes(b"x" * (1024 * 1024 + 1))
        self.add("small.txt", b"small change")
        self.assertEqual(self.check().returncode, 0)


if __name__ == "__main__":
    unittest.main()
