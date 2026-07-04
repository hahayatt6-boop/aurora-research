"""校验 Aurora 研究仓库的结构约束。"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Dict, List


RESEARCH_STATES = {"planned", "active", "review", "complete", "superseded"}
HYPOTHESIS_STATES = {
    "proposed",
    "testing",
    "supported",
    "weakened",
    "rejected",
    "inconclusive",
}
LINK_PATTERN = re.compile(r"(?<!!)\[[^]]*]\(([^)]+)\)")
FENCED_CODE_PATTERN = re.compile(r"^(```|~~~).*?^\1\s*$", re.MULTILINE | re.DOTALL)


def frontmatter(text: str) -> Dict[str, str]:
    """读取 Markdown 头部中的简单标量字段。"""
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    fields = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip().strip('"')
    return fields


def validate_repository(root: Path) -> List[str]:
    """返回仓库校验错误，不修改任何文件。"""
    errors = []
    seen = {}
    for path in sorted(root.rglob("*.md")):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        fields = frontmatter(text)
        record_id = fields.get("id")
        if record_id:
            if record_id in seen:
                errors.append(
                    f"{path}：编号 {record_id} 重复（首次出现于 {seen[record_id]}）"
                )
            else:
                seen[record_id] = path
        status = fields.get("status")
        if record_id and record_id.startswith("RES-") and status not in RESEARCH_STATES:
            errors.append(f"{path}：研究状态 {status} 非法")
        if record_id and record_id.startswith("HYP-") and status not in HYPOTHESIS_STATES:
            errors.append(f"{path}：假设状态 {status} 非法")
        prose = FENCED_CODE_PATTERN.sub("", text)
        for target in LINK_PATTERN.findall(prose):
            target = target.split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            if not (path.parent / target).resolve().exists():
                errors.append(f"{path}：链接 {target} 失效")
    return errors


def main() -> int:
    repository = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    findings = validate_repository(repository)
    if findings:
        print("\n".join(findings))
        return 1
    print("仓库校验通过。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
