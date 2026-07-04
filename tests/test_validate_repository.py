import tempfile
import unittest
from pathlib import Path

from scripts.validate_repository import validate_repository


class 仓库校验测试(unittest.TestCase):
    def write(self, root: Path, name: str, body: str) -> None:
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8")

    def test_接受有效记录和链接(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "README.md", "[Report](research/RES-001.md)\n")
            self.write(
                root,
                "research/RES-001.md",
                "---\nid: RES-001\nstatus: planned\n---\n",
            )

            self.assertEqual([], validate_repository(root))

    def test_报告重复编号(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "research/a.md", "---\nid: RES-001\nstatus: planned\n---\n")
            self.write(root, "research/b.md", "---\nid: RES-001\nstatus: planned\n---\n")

            errors = validate_repository(root)

            self.assertTrue(any("编号 RES-001 重复" in error for error in errors))

    def test_报告非法记录状态(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "research/a.md", "---\nid: RES-001\nstatus: imagined\n---\n")
            self.write(root, "hypotheses/a.md", "---\nid: HYP-001\nstatus: imagined\n---\n")

            errors = validate_repository(root)

            self.assertTrue(any("研究状态 imagined 非法" in error for error in errors))
            self.assertTrue(any("假设状态 imagined 非法" in error for error in errors))

    def test_报告失效相对链接但允许外部链接(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(
                root,
                "README.md",
                "[Missing](missing.md) [Web](https://example.com) [Email](mailto:test@example.com)\n",
            )

            errors = validate_repository(root)

            self.assertTrue(any("链接 missing.md 失效" in error for error in errors))
            self.assertFalse(any("example.com" in error for error in errors))

    def test_忽略代码块中的Markdown链接(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(
                root,
                "README.md",
                "```python\nexample = '[Fixture](missing.md)'\n```\n",
            )

            self.assertEqual([], validate_repository(root))


if __name__ == "__main__":
    unittest.main()
