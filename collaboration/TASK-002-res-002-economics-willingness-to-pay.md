---
id: TASK-002
role: research-agent
status: done
allowed_files: evidence/**, research/RES-002-economics-willingness-to-pay.md, hypotheses/HYP-002-willingness-to-pay.md, collaboration/TASK-002-res-002-economics-willingness-to-pay.md, evidence/README.md, research/README.md, hypotheses/README.md, decisions/README.md
forbidden_inputs: identifiable-child-family-school-contact-health-location-data
validation: python3 -m unittest discover -s tests -v && python3 scripts/validate_repository.py
---

# RES-002 运营经济性与付费意愿研究

## 目标

按 ADR-001 方案 3 的第一优先研究方向，用公开证据回答：儿童 STEAM/AI 教育产品的运营经济性是否足以支撑商业可行性？目标家庭的付费意愿和可比产品的单位经济，能否为 Aurora 提供可行商业模型的证据基础？

**停止阈值（来自 ADR-001）：** 若研究显示核心目标人群系统性不愿为 Aurora 类产品付费，则直接触发停止流程，不再暂缓或收窄。

## 时间盒

截止：2026-07-18（ADR-001 指定 1 周时间盒，自 2026-07-11 起）

## 输入来源

- 公司官网、产品定价页、公开财务披露、众筹页面。
- 市场研究机构公开报告（Statista、市场研究机构公开摘要等）。
- 政府统计数据（BLS Consumer Expenditure Survey 等）。
- 同行评审的付费意愿与教育科技经济性研究。
- 可信的创业失败分析、破产公告、关闭说明。

只允许公开来源和不可识别摘要。不得使用任何儿童、家庭、学校或联系方式数据。

## 研究问题与竞争解释

主要问题：Aurora 类儿童 AI/STEAM 产品的目标家庭是否愿意以可行的价格持续付费？

竞争解释必须包括：
1. 市场被免费/机构资助产品主导，商业定价结构性不可行。
2. 付费意愿存在但价格上限低于单位成本（硬件+软件+运营）。
3. 首购意愿高但长期订阅留存差（新奇感驱动而非持续价值）。
4. 主要付费者是学校/机构而非家庭，改变了分发和收入模式。

## 证据线

1. **可比产品的定价与经济性：** 成功和失败的儿童 STEAM/AI 硬件+软件产品的价格区间、商业模式、留存和单位成本。
2. **家庭教育支出与付费意愿调查：** 权威统计来源对家庭教育支出的实际数据，以及消费者调查中对订阅/硬件付费的意愿数据。
3. **EdTech 获客成本与运营经济性：** CAC、毛利率、订阅续费等行业基准。

每条证据线至少包含一个直接质疑"目标家庭愿意付费"的候选来源。

## 允许修改文件

- `evidence/**`（新增 EVD 记录）
- `research/RES-002-economics-willingness-to-pay.md`
- `hypotheses/HYP-002-willingness-to-pay.md`
- `collaboration/TASK-002-res-002-economics-willingness-to-pay.md`
- `evidence/README.md`、`research/README.md`、`hypotheses/README.md`

未列出的文件（含 `mvp/`、`decisions/ADR-*`、`collaboration/TASK-001*`、`collaboration/ARV-001*`）不得修改。

## 禁止事项

- 不保存可识别儿童或家庭数据。
- 不把市场规模增长率直接等同于"Aurora 商业可行"。
- 不用单个产品定价推出普遍 WTP 结论。
- 不越过 ADR-001 打开 MVP 或原型工作。
- 不把获取样本数量或来源数量等同于结论强度。

## 完成定义

- 至少建立 6 个 EVD 记录，覆盖三条证据线、不同结果和至少两类可信替代解释（见上方竞争解释）。
- RES-002 包含证据、机制、反证、未知项和结论；重大主张均链接证据。
- HYP-002 状态根据证据更新（不得强制推进为支持或否定）。
- 各索引更新，TASK-002 状态改为 `done`。
- 两条验证命令均以退出码 0 完成。

## 升级条件

- 只有低可靠材料却需要支撑付费意愿结论。
- 触及真实家庭、学校或儿童联系方式材料。
- 证据清晰显示 ADR-001 停止阈值已触发（系统性不愿付费），需回项目负责人决策。
- 需要原始付费数据访谈、用户研究或产品实验才能验证。
