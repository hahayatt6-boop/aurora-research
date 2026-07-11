---
id: TASK-001
role: research-agent
status: done
allowed_files: evidence/**, research/RES-001-platform-gap.md, hypotheses/HYP-001-continuity-gap.md, collaboration/ARV-001-res-001.md, decisions/ADR-001-res-001-direction.md, evidence/README.md, research/README.md, hypotheses/README.md, decisions/README.md
forbidden_inputs: identifiable-child-family-school-contact-health-location-data
validation: python3 -m unittest discover -s tests -v && python3 scripts/validate_repository.py
---

# RES-001 公开证据收集与决策闭环

## 目标

用可追溯公开证据回答 RES-001：儿童 AI、机器人、STEAM、编程玩具和智能硬件较少形成长期平台，究竟代表可验证机会还是结构性警示；并根据证据更新 HYP-001、完成独立反方审阅和 ADR-001。

## 输入来源

- 公司官网、产品文档、公开生命周期公告、财务披露和归档页面。
- 同行评审的学习科学、儿童发展和教育技术研究。
- 权威监管机构、标准组织和儿童安全机构发布的公开指南。
- 可信的项目终止分析和从业者材料，但必须标注间接性与激励。

只允许公开来源和不可识别摘要。不得粘贴或转录任何可识别儿童、家庭、学校、联系方式、健康或精确位置材料。

## 研究问题与竞争解释

主要问题：平台缺口是否主要由跨项目、工具、关系和成长阶段的连续性不足造成？

必须同时比较：单位经济与硬件利润、获客与分发、家长信任与安全、年龄窗口和兴趣迁移、学习效果证据薄弱、学校或社区替代家庭连续性等解释。

## 证据线

1. **长期存在案例：**寻找没有完整成长档案却长期提供价值的产品或生态，以及支持连续性作用的案例。
2. **停滞或终止案例：**区分连续性不足与经济性、分发、信任、年龄窗口等机制。
3. **学习科学与儿童安全：**判断哪些指标能代表学习价值，哪些只是短期参与或新奇感。

每条证据线至少包含一个直接反驳 HYP-001 的候选来源。公司材料对产品功能可评为中高可靠，对学习效果或因果结论不得仅凭自述评高。

## 允许修改文件

- `evidence/**`
- `research/RES-001-platform-gap.md`
- `hypotheses/HYP-001-continuity-gap.md`
- `collaboration/ARV-001-res-001.md`
- `decisions/ADR-001-res-001-direction.md`
- `evidence/README.md`、`research/README.md`、`hypotheses/README.md`、`decisions/README.md`

未列出的产品代码、`mvp/` 和协作规范不得修改。

## 禁止事项

- 不保存可识别儿童或家庭数据，不执行访谈、招募或产品实验。
- 不把 AI 生成内容、搜索摘要或未核验二手转述当作事实。
- 不把估值、销量、活跃度、新奇感或公开存续年限直接等同于学习价值。
- 不用单个案例推出普遍因果结论。
- 不越过已接受且带审批证据的 ADR 打开 MVP 或原型工作。

## 完成定义

- 至少建立 8 个 EVD 记录，覆盖三条证据线、不同结果和至少两类可信替代解释；不得为满足数量拆分或重复同一来源。
- RES-001 的重大主张均链接证据，明确反证、未知项、置信度和决策建议。
- 独立反方审阅者挑战 HYP-001、核心发现、替代解释和决策建议。
- HYP-001 与 ADR-001 的状态和措辞与证据、ARV 处置一致。
- 四个索引更新，TASK-001 状态改为 `done`。
- 两条验证命令均以退出码 0 完成。

## 升级条件

- 任何来源疑似包含可识别儿童、家庭、学校、联系方式、健康或精确位置材料。
- 只有低可靠材料却需要支持方向性决策。
- 独立审阅得出 `unresolved`，或对证据可靠性和结论方向存在实质冲突。
- 结论需要真实参与者研究、外部发布、产品实验或 MVP 才能验证。

遇到升级条件时停止状态推进，保留证据缺口并选择继续研究、暂缓或收窄；不得用推测补齐。
