"""校验 Aurora 研究仓库的结构约束。"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


RESEARCH_STATES = {"planned", "active", "review", "complete", "superseded"}
HYPOTHESIS_STATES = {
    "proposed",
    "testing",
    "supported",
    "weakened",
    "rejected",
    "inconclusive",
}
DECISION_STATES = {"proposed", "accepted", "superseded", "rejected"}
MVP_STATES = {"draft", "review", "authorized", "superseded"}
MVP_SAFETY_STATES = {"required", "in-progress", "complete"}
CONFIDENCE_LEVELS = {"low", "medium", "high"}
EVIDENCE_RELIABILITY = {"low", "medium", "high"}
EVIDENCE_SOURCE_TYPES = {
    "primary-research",
    "peer-reviewed",
    "official-guidance",
    "company-material",
    "practitioner-account",
    "market-data",
    "secondary-analysis",
}
ADVERSARIAL_DISPOSITIONS = {"accepted", "rejected", "unresolved"}
AGENT_TASK_STATES = {"planned", "active", "done", "blocked"}
APPROVAL_RECORD_IDS = {"external-human-approval", "signed-project-owner-note", "meeting-decision-record"}

DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
LINK_PATTERN = re.compile(r"(?<!!)\[[^]]*]\(([^)]+)\)")
FENCED_CODE_PATTERN = re.compile(r"^(```|~~~).*?^\1\s*$", re.MULTILINE | re.DOTALL)
EMAIL_PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PHONE_PATTERN = re.compile(r"(?<!\d)(?:1[3-9]\d{9}|\d{3,4}[- ]\d{7,8})(?!\d)")
ADDRESS_PATTERN = re.compile(
    r"(?:住址|地址|家庭地址|住在|位于).{0,20}(?:小区|楼|单元|室|街道|路\d*号|[0-9]+号)"
)
CHILD_SCHOOL_PATTERN = re.compile(
    r"(?:儿童|孩子|学生|未成年人).{0,12}(?:就读于|来自|所在|在).{0,12}(?:学校|小学|中学|班级)"
)
RECORD_ID_PATTERN = re.compile(r"\b(?:EVD|RES|HYP|ADR|MVP|ARV|TASK)-\d{3}\b")
TEMPLATE_PLACEHOLDERS = {
    "name@example.com",
    "test@example.com",
    "example@example.com",
    "TASK-NNN",
    "ARV-NNN",
    "EVD-NNN",
    "RES-NNN",
    "HYP-NNN",
    "ADR-NNN",
    "MVP-NNN",
    "YYYY-MM-DD",
}


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


def split_ids(value: str | None) -> List[str]:
    """读取逗号分隔的简单 id 列表。"""
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def prose_without_code(text: str) -> str:
    return FENCED_CODE_PATTERN.sub("", text)


def is_markdown_record(path: Path) -> bool:
    return path.suffix == ".md" and path.name != "README.md" and "templates" not in path.parts


def record_kind(path: Path, record_id: str | None) -> str | None:
    if not record_id:
        return None
    if "evidence" in path.parts and record_id.startswith("EVD-"):
        return "EVD"
    if "research" in path.parts and record_id.startswith("RES-"):
        return "RES"
    if "hypotheses" in path.parts and record_id.startswith("HYP-"):
        return "HYP"
    if "decisions" in path.parts and record_id.startswith("ADR-"):
        return "ADR"
    if "mvp" in path.parts and record_id.startswith("MVP-"):
        return "MVP"
    if "collaboration" in path.parts and record_id.startswith("TASK-"):
        return "TASK"
    if "collaboration" in path.parts and record_id.startswith("ARV-"):
        return "ARV"
    if "approvals" in path.parts and record_id.startswith("APP-"):
        return "APP"
    return None


def require_fields(path: Path, fields: Dict[str, str], names: Iterable[str], errors: List[str]) -> None:
    for name in names:
        if not fields.get(name):
            errors.append(f"{path}：缺少 frontmatter 字段 {name}")


def validate_enum(path: Path, field: str, value: str | None, allowed: set[str], errors: List[str]) -> None:
    if value and value not in allowed:
        errors.append(f"{path}：字段 {field} 的值 {value} 非法")


def validate_date(path: Path, field: str, value: str | None, errors: List[str], allow_unknown: bool = False) -> None:
    if not value:
        return
    if allow_unknown and value == "unknown":
        return
    if not DATE_PATTERN.match(value):
        errors.append(f"{path}：字段 {field} 必须是 YYYY-MM-DD")


def has_section(text: str, title: str) -> bool:
    return re.search(rf"^#+\s*{re.escape(title)}\s*$", text, re.MULTILINE) is not None


def validate_links(path: Path, text: str, errors: List[str]) -> None:
    prose = prose_without_code(text)
    for target in LINK_PATTERN.findall(prose):
        target = target.split("#", 1)[0]
        if not target or target.startswith(("http://", "https://", "mailto:")):
            continue
        if not (path.parent / target).resolve().exists():
            errors.append(f"{path}：链接 {target} 失效")


def validate_privacy(path: Path, text: str, errors: List[str]) -> None:
    prose = text
    for placeholder in TEMPLATE_PLACEHOLDERS:
        prose = prose.replace(placeholder, "")
    for match in EMAIL_PATTERN.findall(prose):
        errors.append(f"{path}：疑似联系方式 {match} 不得入库，请移除或仓库外处理")
    for match in PHONE_PATTERN.findall(prose):
        errors.append(f"{path}：疑似电话号码 {match} 不得入库，请移除或仓库外处理")
    if ADDRESS_PATTERN.search(prose):
        errors.append(f"{path}：疑似精确地址或可识别地点，不得入库")
    if CHILD_SCHOOL_PATTERN.search(prose):
        errors.append(f"{path}：疑似儿童/家庭与学校标识组合，不得入库")


def collect_records(root: Path) -> Tuple[Dict[str, Tuple[Path, Dict[str, str], str]], List[str]]:
    records: Dict[str, Tuple[Path, Dict[str, str], str]] = {}
    errors: List[str] = []
    for path in sorted(root.rglob("*.md")):
        if ".git" in path.parts or "templates" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        fields = frontmatter(text)
        record_id = fields.get("id")
        if record_id:
            if record_id in records:
                errors.append(f"{path}：编号 {record_id} 重复（首次出现于 {records[record_id][0]}）")
            else:
                records[record_id] = (path, fields, text)
    return records, errors


def validate_schema(root: Path, path: Path, fields: Dict[str, str], text: str, records: Dict[str, Tuple[Path, Dict[str, str], str]], errors: List[str]) -> None:
    record_id = fields.get("id")
    kind = record_kind(path, record_id)
    if record_id and is_markdown_record(path) and not kind:
        errors.append(f"{path}：编号 {record_id} 与目录不匹配")
        return

    if kind == "EVD":
        require_fields(path, fields, ["id", "title", "source_type", "published", "retrieved", "reliability", "reports"], errors)
        validate_enum(path, "source_type", fields.get("source_type"), EVIDENCE_SOURCE_TYPES, errors)
        validate_enum(path, "reliability", fields.get("reliability"), EVIDENCE_RELIABILITY, errors)
        validate_date(path, "published", fields.get("published"), errors, allow_unknown=True)
        validate_date(path, "retrieved", fields.get("retrieved"), errors)
        for report_id in split_ids(fields.get("reports")):
            if report_id not in records or not report_id.startswith("RES-"):
                errors.append(f"{path}：reports 指向不存在的研究报告 {report_id}")

    if kind == "RES":
        require_fields(path, fields, ["id", "title", "status", "owner", "created", "updated", "decision", "confidence"], errors)
        status = fields.get("status")
        validate_enum(path, "status", status, RESEARCH_STATES, errors)
        validate_enum(path, "confidence", fields.get("confidence"), CONFIDENCE_LEVELS, errors)
        validate_date(path, "created", fields.get("created"), errors)
        validate_date(path, "updated", fields.get("updated"), errors)
        decision = fields.get("decision")
        if status in {"review", "complete", "superseded"} and decision not in {None, "none"}:
            if decision not in records or not decision.startswith("ADR-"):
                errors.append(f"{path}：decision 指向不存在的决策记录 {decision}")
        if status in {"review", "complete"}:
            for section in ["证据", "反证与替代解释", "未知项", "结论"]:
                if not has_section(text, section):
                    errors.append(f"{path}：状态 {status} 必须包含章节 {section}")

    if kind == "HYP":
        require_fields(path, fields, ["id", "title", "status", "owner", "created", "updated", "gates"], errors)
        status = fields.get("status")
        validate_enum(path, "status", status, HYPOTHESIS_STATES, errors)
        validate_date(path, "created", fields.get("created"), errors)
        validate_date(path, "updated", fields.get("updated"), errors)
        gates = fields.get("gates")
        if status not in {"proposed", "testing"} and gates not in {None, "none"}:
            if gates not in records or not gates.startswith("ADR-"):
                errors.append(f"{path}：gates 指向不存在的决策记录 {gates}")

    if kind == "ADR":
        require_fields(path, fields, ["id", "title", "status", "created", "deciders", "research", "confidence"], errors)
        validate_enum(path, "status", fields.get("status"), DECISION_STATES, errors)
        validate_enum(path, "confidence", fields.get("confidence"), CONFIDENCE_LEVELS, errors)
        validate_date(path, "created", fields.get("created"), errors)
        research = fields.get("research")
        if research not in {None, "none"} and (research not in records or not research.startswith("RES-")):
            errors.append(f"{path}：research 指向不存在的研究报告 {research}")
        validate_accepted_adr(root, path, fields, errors)

    if kind == "MVP":
        validate_mvp(path, fields, text, records, errors)

    if kind == "TASK":
        require_fields(path, fields, ["id", "role", "status", "allowed_files", "forbidden_inputs", "validation"], errors)
        validate_enum(path, "status", fields.get("status"), AGENT_TASK_STATES, errors)

    if kind == "ARV":
        validate_adversarial_review(path, fields, errors)

    if kind == "APP":
        require_fields(path, fields, ["id", "decision", "approved_by", "approved_at", "approval_record"], errors)
        validate_date(path, "approved_at", fields.get("approved_at"), errors)
        validate_enum(path, "approval_record", fields.get("approval_record"), APPROVAL_RECORD_IDS, errors)


def validate_accepted_adr(root: Path, path: Path, fields: Dict[str, str], errors: List[str]) -> None:
    decision_id = fields.get("id")
    if fields.get("status") != "accepted" or decision_id == "ADR-000":
        return

    evidence_path = fields.get("approval_evidence")
    if not evidence_path:
        errors.append(f"{path}：accepted ADR 必须引用审批证据 approval_evidence；静态校验不能替代项目负责人身份认证")
        return

    evidence = (root / evidence_path).resolve()
    if not evidence.exists() or root.resolve() not in evidence.parents:
        errors.append(f"{path}：approval_evidence 指向不存在或越界的审批证据 {evidence_path}")
        return

    evidence_fields = frontmatter(evidence.read_text(encoding="utf-8"))
    if evidence_fields.get("decision") != decision_id:
        errors.append(f"{path}：审批证据必须指向同一 ADR")
    require_fields(evidence, evidence_fields, ["id", "decision", "approved_by", "approved_at", "approval_record"], errors)


def validate_mvp(path: Path, fields: Dict[str, str], text: str, records: Dict[str, Tuple[Path, Dict[str, str], str]], errors: List[str]) -> None:
    require_fields(
        path,
        fields,
        ["id", "title", "status", "authorizing_decision", "research", "hypotheses", "safety_review", "created", "updated"],
        errors,
    )
    status = fields.get("status")
    validate_enum(path, "status", status, MVP_STATES, errors)
    validate_enum(path, "safety_review", fields.get("safety_review"), MVP_SAFETY_STATES, errors)
    validate_date(path, "created", fields.get("created"), errors)
    validate_date(path, "updated", fields.get("updated"), errors)

    decision_id = fields.get("authorizing_decision")
    decision = records.get(decision_id or "")
    if not decision or decision[1].get("status") != "accepted":
        errors.append(f"{path}：MVP 必须引用已接受的授权 ADR")
    elif decision[1].get("authorizes_mvp") != "true":
        errors.append(f"{path}：MVP 引用的 ADR 必须明确 authorizes_mvp: true")

    research_id = fields.get("research")
    research = records.get(research_id or "")
    if not research or research[1].get("status") != "complete":
        errors.append(f"{path}：MVP 必须引用已完成的研究报告")

    for hypothesis_id in split_ids(fields.get("hypotheses")):
        if hypothesis_id not in records or not hypothesis_id.startswith("HYP-"):
            errors.append(f"{path}：hypotheses 指向不存在的假设 {hypothesis_id}")
            continue
        hypothesis_status = records[hypothesis_id][1].get("status")
        if status == "authorized" and hypothesis_status in {"proposed", "testing"}:
            errors.append(f"{path}：authorized MVP 不能引用仍处于 {hypothesis_status} 的假设 {hypothesis_id}")
    if not split_ids(fields.get("hypotheses")):
        errors.append(f"{path}：MVP 必须至少引用一个可证伪假设")

    if status == "authorized" and fields.get("safety_review") != "complete":
        errors.append(f"{path}：authorized MVP 必须完成 safety_review")

    for section in ["目标人群", "可证伪假设", "成功阈值", "时间范围", "停止规则"]:
        if not has_section(text, section):
            errors.append(f"{path}：MVP 缺少准入章节 {section}")
    safety_terms = ["儿童安全", "同意", "数据最小化", "家庭所有", "删除", "人工监督"]
    missing = [term for term in safety_terms if term not in text]
    if missing:
        errors.append(f"{path}：MVP 缺少安全要求 {', '.join(missing)}")


def validate_adversarial_review(path: Path, fields: Dict[str, str], errors: List[str]) -> None:
    require_fields(
        path,
        fields,
        [
            "id",
            "reviewer_role",
            "reviewer_id",
            "original_author_or_source",
            "original_author_id",
            "claims_reviewed",
            "disposition",
            "impact_on_confidence",
            "owner_next_step",
        ],
        errors,
    )
    validate_enum(path, "disposition", fields.get("disposition"), ADVERSARIAL_DISPOSITIONS, errors)
    if fields.get("reviewer_role") and fields.get("reviewer_role") == fields.get("original_author_or_source"):
        errors.append(f"{path}：reviewer_role 不能与 original_author_or_source 相同")
    if fields.get("reviewer_id") and fields.get("reviewer_id") == fields.get("original_author_id"):
        errors.append(f"{path}：reviewer_id 不能与 original_author_id 相同")
    if fields.get("disposition") == "unresolved":
        errors.append(f"{path}：[REVIEW] 反方审阅 unresolved，必须处理后才能推进")


def reviewed_ids(records: Dict[str, Tuple[Path, Dict[str, str], str]]) -> set[str]:
    reviewed: set[str] = set()
    for record_id, (_path, fields, text) in records.items():
        if not record_id.startswith("ARV-"):
            continue
        if fields.get("disposition") != "accepted":
            continue
        reviewed.update(RECORD_ID_PATTERN.findall(fields.get("claims_reviewed", "")))
    return reviewed


def validate_review_gates(records: Dict[str, Tuple[Path, Dict[str, str], str]], errors: List[str]) -> None:
    reviewed = reviewed_ids(records)
    for record_id, (path, fields, _text) in records.items():
        status = fields.get("status")
        needs_review = False
        if record_id.startswith("RES-") and status in {"review", "complete"}:
            needs_review = True
        if record_id.startswith("HYP-") and status in {"supported", "weakened", "rejected", "inconclusive"}:
            needs_review = True
        if record_id.startswith("ADR-") and status == "accepted" and record_id != "ADR-000":
            needs_review = True
        if record_id.startswith("MVP-") and status in {"review", "authorized"}:
            needs_review = True
        if needs_review and record_id not in reviewed:
            errors.append(f"{path}：状态 {status} 需要独立反方审阅记录")


def validate_repository(root: Path) -> List[str]:
    """返回仓库校验错误，不修改任何文件。"""
    errors = []
    records, duplicate_errors = collect_records(root)
    errors.extend(duplicate_errors)

    for path in sorted(root.rglob("*.md")):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        fields = frontmatter(text)
        validate_schema(root, path, fields, text, records, errors)
        validate_links(path, text, errors)
        validate_privacy(path, text, errors)

    validate_review_gates(records, errors)
    return errors


def main() -> int:
    repository = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    findings = validate_repository(repository)
    errors = [finding for finding in findings if "[WARN]" not in finding]
    if errors:
        print("\n".join(findings))
        return 1
    print("仓库校验通过。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
