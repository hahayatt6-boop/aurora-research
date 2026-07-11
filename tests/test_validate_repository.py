import tempfile
import unittest
from pathlib import Path
from typing import Optional

from scripts.validate_repository import validate_repository


class 仓库校验测试(unittest.TestCase):
    def write(self, root: Path, name: str, body: str) -> None:
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8")

    def valid_res(self, status: str = "planned", decision: str = "none") -> str:
        return f"""---
id: RES-001
title: 研究报告
status: {status}
owner: 研究负责人
created: 2026-07-04
updated: 2026-07-04
decision: {decision}
confidence: low
---

# 研究问题
"""

    def valid_hyp(self, status: str = "proposed", gates: str = "none") -> str:
        return f"""---
id: HYP-001
title: 可证伪假设
status: {status}
owner: 研究负责人
created: 2026-07-04
updated: 2026-07-04
gates: {gates}
---

# 假设
"""

    def valid_adr(
        self,
        record_id: str = "ADR-001",
        status: str = "accepted",
        research: str = "none",
        approval_evidence: Optional[str] = "approvals/ADR-001-approval.md",
        authorizes_mvp: bool = False,
    ) -> str:
        approval_line = f"approval_evidence: {approval_evidence}\n" if approval_evidence else ""
        mvp_line = "authorizes_mvp: true\n" if authorizes_mvp else ""
        return f"""---
id: {record_id}
title: 决策
status: {status}
created: 2026-07-04
deciders: 项目负责人
research: {research}
confidence: medium
{mvp_line}
{approval_line}---

# 决策
"""

    def valid_approval(self, decision: str = "ADR-001") -> str:
        return f"""---
id: APP-001
decision: {decision}
approved_by: project-owner
approved_at: 2026-07-04
approval_record: external-human-approval
---

# 审批证据
"""

    def valid_arv(self, claim: str = "RES-001", disposition: str = "accepted") -> str:
        return f"""---
id: ARV-001
reviewer_role: adversarial-reviewer
reviewer_id: reviewer-001
original_author_or_source: research-author
original_author_id: author-001
claims_reviewed: {claim}
disposition: {disposition}
impact_on_confidence: lowers-confidence
owner_next_step: update-record
---

# 反方审阅记录

审阅 {claim}。
"""

    def test_接受有效记录和链接(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "README.md", "[Report](research/RES-001.md)\n")
            self.write(root, "research/RES-001.md", self.valid_res())

            self.assertEqual([], validate_repository(root))

    def test_报告重复编号(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "research/a.md", self.valid_res())
            self.write(root, "research/b.md", self.valid_res())

            errors = validate_repository(root)

            self.assertTrue(any("编号 RES-001 重复" in error for error in errors))

    def test_报告非法记录状态(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "research/a.md", self.valid_res(status="imagined"))
            self.write(root, "hypotheses/a.md", self.valid_hyp(status="imagined"))

            errors = validate_repository(root)

            self.assertTrue(any("字段 status 的值 imagined 非法" in error for error in errors))

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

    def test_忽略代码块中的Markdown链接但不忽略隐私样例(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(
                root,
                "README.md",
                "```python\nexample = '[Fixture](missing.md) user@example.com 13800138000'\n```\n",
            )

            errors = validate_repository(root)
            self.assertFalse(any("链接" in error for error in errors))
            self.assertTrue(any("user@example.com" in error for error in errors))
            self.assertTrue(any("13800138000" in error for error in errors))

    def test_证据记录校验字段枚举和关系(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "research/RES-001.md", self.valid_res())
            self.write(
                root,
                "evidence/EVD-001.md",
                """---
id: EVD-001
title: 来源
source_type: primary-research
published: unknown
retrieved: 2026-07-04
reliability: medium
reports: RES-001
---
""",
            )

            self.assertEqual([], validate_repository(root))

            self.write(
                root,
                "evidence/EVD-002.md",
                """---
id: EVD-002
title: 来源
source_type: made-up
published: 2026/07/04
retrieved: yesterday
reliability: strong
reports: RES-999
---
""",
            )

            errors = validate_repository(root)

            self.assertTrue(any("source_type" in error and "made-up" in error for error in errors))
            self.assertTrue(any("reliability" in error and "strong" in error for error in errors))
            self.assertTrue(any("reports 指向不存在" in error for error in errors))

    def test_MVP_必须有明确授权关系和准入内容(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "hypotheses/HYP-001.md", self.valid_hyp(status="supported", gates="ADR-001"))
            self.write(root, "research/RES-001.md", self.valid_res(status="complete", decision="ADR-001") + """
## 证据

有证据。

## 反证与替代解释

有反证。

## 未知项

有未知项。

## 结论

有结论。
""")
            self.write(root, "decisions/ADR-001.md", self.valid_adr(research="RES-001", authorizes_mvp=True))
            self.write(root, "approvals/ADR-001-approval.md", self.valid_approval())
            self.write(root, "collaboration/review/adversarial-review-001.md", self.valid_arv("RES-001,HYP-001,ADR-001,MVP-001"))
            self.write(
                root,
                "mvp/MVP-001.md",
                """---
id: MVP-001
title: 有限验证
status: authorized
authorizing_decision: ADR-001
research: RES-001
hypotheses: HYP-001
safety_review: complete
created: 2026-07-04
updated: 2026-07-04
---

# 有限验证

## 目标人群

去标识人群。

## 可证伪假设

HYP-001。

## 成功阈值

预先定义。

## 时间范围

两周。

## 停止规则

出现风险即停止。

## 儿童安全、同意、数据最小化、家庭所有、删除、人工监督

全部必须满足。
""",
            )

            self.assertEqual([], validate_repository(root))

            self.write(
                root,
                "mvp/MVP-002.md",
                """---
id: MVP-002
title: 未授权验证
status: authorized
authorizing_decision: ADR-999
research: RES-999
hypotheses: HYP-999
safety_review: required
created: 2026-07-04
updated: 2026-07-04
---

# 未授权验证
""",
            )

            errors = validate_repository(root)

            self.assertTrue(any("MVP 必须引用已接受" in error for error in errors))
            self.assertTrue(any("MVP 必须引用已完成" in error for error in errors))
            self.assertTrue(any("hypotheses 指向不存在" in error for error in errors))
            self.assertTrue(any("authorized MVP 必须完成" in error for error in errors))
            self.assertTrue(any("MVP 缺少准入章节" in error for error in errors))
            self.write(root, "decisions/ADR-001.md", self.valid_adr(research="RES-001", authorizes_mvp=False))

            errors = validate_repository(root)

            self.assertTrue(any("authorizes_mvp: true" in error for error in errors))

    def test_接受态ADR必须有审批证据且不能只靠伪造链条(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "research/RES-001.md", self.valid_res(status="complete", decision="ADR-001") + """
## 证据

有证据。

## 反证与替代解释

有反证。

## 未知项

有未知项。

## 结论

有结论。
""")
            self.write(root, "decisions/ADR-001.md", self.valid_adr(status="accepted", research="RES-001", approval_evidence=None))
            self.write(root, "collaboration/review/adversarial-review-001.md", self.valid_arv("RES-001,ADR-001"))

            errors = validate_repository(root)

            self.assertTrue(any("accepted ADR 必须引用审批证据" in error for error in errors))

            self.write(root, "decisions/ADR-001.md", self.valid_adr(status="accepted", research="RES-001"))
            self.write(root, "approvals/ADR-001-approval.md", self.valid_approval("ADR-999"))

            errors = validate_repository(root)

            self.assertTrue(any("审批证据必须指向同一 ADR" in error for error in errors))

    def test_反方审阅必须记录结构化独立身份(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(
                root,
                "collaboration/review/adversarial-review-001.md",
                """---
id: ARV-001
reviewer_role: adversarial-reviewer
reviewer_id: same-agent
original_author_or_source: research-author
original_author_id: same-agent
claims_reviewed: RES-001
disposition: accepted
impact_on_confidence: lowers-confidence
owner_next_step: update-record
---
""",
            )

            errors = validate_repository(root)

            self.assertTrue(any("reviewer_id 不能与 original_author_id 相同" in error for error in errors))

    def test_隐私最后防线发现疑似标识符但允许占位符(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "templates/example.md", "name@example.com\n")
            self.write(root, "research/RES-001.md", self.valid_res() + "联系 13800138000\n")
            self.write(root, "research/RES-002.md", self.valid_res().replace("RES-001", "RES-002") + "住址在示例路12号\n")
            self.write(root, "research/RES-003.md", self.valid_res().replace("RES-001", "RES-003") + "儿童就读于示例小学\n")

            errors = validate_repository(root)

            self.assertTrue(any("疑似电话号码" in error for error in errors))
            self.assertTrue(any("疑似精确地址" in error for error in errors))
            self.assertTrue(any("疑似儿童/家庭与学校" in error for error in errors))
            self.assertFalse(any("name@example.com" in error for error in errors))

    def test_隐私扫描不误报规程性文字(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "README.md", "仓库不得保存学校标识。研究路线图记录阶段。\n")

            self.assertEqual([], validate_repository(root))

    def test_状态推进需要独立反方审阅(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "research/RES-001.md", self.valid_res(status="review") + """
## 证据

有证据。

## 反证与替代解释

有反证。

## 未知项

有未知项。

## 结论

有结论。
""")

            errors = validate_repository(root)

            self.assertTrue(any("需要独立反方审阅记录" in error for error in errors))

            self.write(root, "collaboration/review/adversarial-review-001.md", self.valid_arv("RES-001"))

            self.assertEqual([], validate_repository(root))

    def test_unresolved_反方审阅不能静默通过(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "collaboration/review/adversarial-review-001.md", self.valid_arv("RES-001", disposition="unresolved"))

            errors = validate_repository(root)

            self.assertTrue(any("unresolved" in error for error in errors))

    def test_rejected_反方审阅不满足状态推进门(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "research/RES-001.md", self.valid_res(status="complete") + """
## 证据

有证据。

## 反证与替代解释

有反证。

## 未知项

有未知项。

## 结论

有结论。
""")
            self.write(root, "collaboration/review/adversarial-review-001.md", self.valid_arv("RES-001", disposition="rejected"))

            errors = validate_repository(root)

            self.assertTrue(any("需要独立反方审阅记录" in error for error in errors))

    def test_模板占位符不作为正式记录且任务记录可校验(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "templates/hypothesis.md", "---\nid: HYP-NNN\nstatus: proposed\n---\n")
            self.write(
                root,
                "collaboration/task/agent-task-001.md",
                """---
id: TASK-001
role: research-agent
status: planned
allowed_files: evidence/EVD-001.md
forbidden_inputs: identifiable-child-data
validation: python3 scripts/validate_repository.py
---

# 代理任务
""",
            )

            self.assertEqual([], validate_repository(root))


if __name__ == "__main__":
    unittest.main()
