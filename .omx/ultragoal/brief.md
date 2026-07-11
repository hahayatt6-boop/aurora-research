# PRD: Aurora RES-001 研究闭环

## Requirements Summary

完成 `RES-001` 的公开证据研究、反方审阅和决策闭环，最终输出一个不会越过证据的方向性结论。研究范围、方法和退出标准已由 `research/RES-001-platform-gap.md:12-75` 定义；HYP-001 的四种判定阈值见 `hypotheses/HYP-001-continuity-gap.md:23-28`；隐私、独立审阅和 MVP 门见 `docs/agents/MULTI_AGENT_COLLABORATION.md:17-72`。

执行来源是 `.omx/specs/deep-interview-aurora-res-001-research.md` 和 `collaboration/TASK-001-res-001-evidence-collection.md:10-74`。

## RALPLAN-DR Summary

### Principles

1. 公开来源可追溯，来源事实与研究者解释分离。
2. 反证和竞争解释与支持证据同等重要。
3. 儿童与家庭隐私在检索和落库前阻断。
4. 结论强度不超过来源直接性、透明度和相互印证。
5. 研究完成不自动授权 MVP。

### Decision Drivers

1. 能否区分连续性机制与经济性、分发、信任、年龄窗口和学习效果等解释。
2. 能否形成跨不同结果案例、不同来源类型的证据链。
3. 能否把结论转化为可执行但可逆的 ADR，同时保持 `mvp/` 门关闭。

### Viable Options

| 方案 | 做法 | 优点 | 缺点 |
| --- | --- | --- | --- |
| A. 机制判定并收窄后续研究 | 收集多类公开证据，允许 HYP-001 为 weakened/inconclusive，再由 ADR 只授权更窄研究 | 与现有证据质量匹配；可保留学习价值 | 不能立即验证真实用户需求；结论较保守 |
| B. 建议负责人评估有限验证 | 若 RES complete、HYP 获强支持、ARV 已解决且安全门完整，则提出 ADR 草案供项目负责人决定 | 可为后续行为证据建立明确门槛 | 当前公开证据很可能不足；代理无权自行授权 MVP，且容易把参与度当学习价值 |
| C. 终止平台假设 | 若跨案例反复显示结构性经济/信任/年龄问题压倒连续性，则停止 | 避免沉没成本和过早产品化 | 公开资料的缺失可能导致假阴性 |

优先方案为 A，但代理只能形成证据结论和 `proposed` ADR。任何改变 Aurora 方向或打开 MVP 的决定均由项目负责人接受；B 不是默认路径，C 也必须先以可逆建议进入负责人决策。

## Acceptance Criteria

1. 至少 8 个 EVD 记录，覆盖长期存在、停滞/终止、学习科学/儿童安全三条证据线。
2. 至少 3 个长期存在/生态案例和 2 个停滞或终止案例；至少 2 个同行评审或权威安全来源。
3. 每个 EVD 包含来源、背景、直接支持陈述、解释、可靠性和局限，并以 `retrieved` 日期及正文中的标题、发布者、日期、关键主张留下逐页核验痕迹；发布时间未知时使用 `unknown`。
4. RES-001 包含案例选择依据、机制对比、证据、反证与替代解释、未知项和结论，并给出 `low|medium|high` 置信度。
5. HYP-001 状态只按既有阈值进入 `supported|weakened|rejected|inconclusive`。
6. 独立 ARV 覆盖进入 `review` 的 RES-001、HYP-001 拟定终态和已写出的 `proposed` ADR-001 草案。ARV 记录级 `disposition` 使用 `accepted|rejected|unresolved`：所有逐项挑战均已处理后才可为 `accepted` 或 `rejected`，任一挑战未决则必须为 `unresolved`；`unresolved` 阻止 RES/HYP 终态与 ADR 接受。
7. ADR-001 草案明确建议继续、收窄、转向、暂缓或停止；代理保持其为 `proposed`，项目负责人未明确接受前不得授权 MVP。
8. 目录索引和 TASK-001 状态同步更新。
9. 单元测试与仓库校验均退出 0；隐私、缺失链接、错误状态和未审阅门的对抗场景均失败得符合预期。

## Implementation Steps

1. **启动任务与状态。** 保留 `collaboration/TASK-001-res-001-evidence-collection.md` 为写入边界，把 `research/RES-001-platform-gap.md:4` 改为 `active`，更新研究索引。
2. **建立公开证据集。** 按 `templates/evidence-note.md` 新建 EVD；优先一手公司生命周期/功能材料、同行评审综述或实验、监管和儿童安全指导。每个来源单独核验网页，不使用搜索摘要作为事实。
3. **综合而非堆砌。** 在 RES-001 中建立案例矩阵和机制矩阵，把来源事实、推断、局限、反证和未知项分开；按 `research/RES-001-platform-gap.md:57-71` 检查退出标准。
4. **形成可审草案。** 完成证据综合后把 RES-001 推进到 `review`，按既有阈值为 HYP-001 拟定终态，并先写 `decisions/ADR-001-res-001-direction.md`，状态保持 `proposed`；不把“有连续性功能”误写成“连续性导致长期成功”。
5. **独立反方审阅。** 由未参与证据综合、使用独立上下文且只接收 RES/HYP/ADR 成品的审阅代理，同时检查 RES-001、HYP-001 拟定终态和 ADR-001 草案的最强反证、替代解释、来源薄弱点和建议越界；审阅结果写入 `collaboration/ARV-001-res-001.md`。
6. **处理审阅并收口研究。** 逐项处置使用 `accepted|rejected|unresolved`：`accepted` 表示原作者接受挑战并已修改权威记录；`rejected` 表示挑战经证据化说明后不采纳；任一逐项挑战未决时，ARV 记录级 `disposition` 必须为 `unresolved`。只有全部挑战已解决，记录级 disposition 才可按总体处置设为 `accepted` 或 `rejected`。`unresolved` 必须阻止终态；处理完成后才把 RES 从 `review` 推进到 `complete` 并更新 HYP 终态，ADR 仍保持 `proposed`，等待项目负责人决定。
7. **验证与负责人门。** 更新四个索引和 TASK 状态，运行单元测试、仓库校验、独立代码审阅和 UltraQA。若建议改变方向或 MVP 准入，只报告建议与证据，不自动把 ADR 改为 `accepted`。

## Pre-mortem

| 失败场景 | 早期信号 | 缓解 |
| --- | --- | --- |
| 宣传材料被误当学习效果证据 | 主要结论只链接公司官网，可靠性仍标 high | 对功能与效果分开评级；效果结论必须由同行评审或多源印证 |
| 案例存续被误当平台成功 | 机制矩阵只有成立年份、销量或活跃度 | 强制区分存续、商业可持续、学习价值、生态互补和跨项目连续性 |
| 反方审阅成为形式检查 | ARV 只复述 RES，没有最强反证或替代解释 | 使用独立代理；要求逐项挑战 HYP、核心发现、替代解释和 ADR |
| 公开案例指标不可比却被强行排序 | 不同案例只有口径不一的存续、销量、使用或学习指标 | 不生成综合分数或伪精确排名；按机制和证据可得性分层，无法比较时明确 `unknown` / `inconclusive` |
| 公开资料稀缺导致假阴性或误停 | 反证线只有单一候选源，或关键机制大多为 `unknown` | 证据不足时强制选择 `inconclusive`、暂缓或继续研究，不以资料缺失判定 `rejected` / stop |
| 审阅者并不真正独立 | 审阅者参与原始综合、继承作者推理链或在同一会话自审 | 使用独立代理和独立上下文；只提供 RES/HYP/ADR 成品及公开证据，不提供作者隐含推理 |

## Risks and Mitigations

- **公开资料选择偏差：**记录检索范围、纳入理由和缺失数据，不声称市场穷尽。
- **因果过度推断：**把跨案例模式写成机制线索，不写成已证实因果。
- **地区和年龄异质性：**标注地区、年龄和分发情境；不可迁移时降低可靠性。
- **证据陈旧：**记录 published/retrieved，并用当前官方页面核验生命周期状态。
- **外链与归档漂移：**仓库校验器只验证本地链接；每个外部来源必须在研究执行时逐页打开核验标题、发布者、日期和关键主张，记录获取日期，无法打开则降级或排除。
- **隐私风险：**只采公开机构或产品层资料，不采用户个案、评论截图或可识别叙述。

## ADR

### Decision

采用“公开证据机制判定 + 先写 proposed ADR 草案 + 独立反方审阅 + 项目负责人接受”的闭环。代理阶段始终保持 MVP 关闭；即使证据支持有限验证，也只能提交建议和准入条件。

### Drivers

- 当前仓库没有 RES-001 证据，不能直接产品化。
- 研究问题需要区分多个竞争机制。
- 儿童安全和家庭信任要求高于推进速度。

### Alternatives considered

- 立即原型化以获得行为数据。
- 只做市场全景，不做机制判定。
- 直接停止平台假设。

### Why chosen

该方案能在不接触真实儿童数据的前提下，最大化现有公开证据的决策价值，并保留停止和转向选项。

### Consequences

- 最终结论可能是 `inconclusive` 或收窄研究，而不是产品授权。
- 公开证据的长期留存和经济性缺口必须保留为未知项。
- 后续真实参与者研究仍需仓库外正式审批。
- ADR-001 在本自动流程结束时保持 `proposed`；方向变更和 MVP 授权必须由项目负责人明确接受。

### Follow-ups

- 若 ADR-001 仅授权继续研究，后续另立 RES，不创建 MVP 文件。
- 若出现不可区分的关键机制，设计不涉及可识别数据的二级研究方案。

## Available Agent Types and Staffing

- 研究/检索：`researcher`，高推理，按证据线分工；只返回来源和局限。
- 主控整合：当前主代理，高推理，串行写入 EVD/RES/HYP/ADR。
- 独立审阅：`critic` 或独立 review agent，高推理，不参与原始综合。
- 校验：`verifier`，高推理，检查 schema、链接、隐私和状态门。

Team 不作为默认执行器：主要风险在判断一致性和共享研究记录冲突。若外部检索吞吐成为瓶颈，可在 Ultragoal 故事内并行 2-3 个只读 researcher，主控仍串行落库。

## Goal-Mode Follow-up Suggestions

Autopilot 当前应使用 `$ultragoal` 维护故事和证据账本；研究检索可借鉴 `$autoresearch-goal` 的评估思路，但不替换 Autopilot 的既定 Ultragoal 阶段。`$team` 仅用于互不重叠的只读来源线。

## Launch Hints and Team Verification

- Ultragoal: `omx ultragoal create-goals --brief-file .omx/plans/prd-aurora-res-001-research.md`
- 如启用 Team：每个 researcher 只返回公开 URL、直接支持陈述、局限和建议可靠性，不直接修改共享 RES/HYP/ADR。
- Team 退出前证明：来源已打开核验、证据线覆盖、没有可识别数据；主控再将证据写入 Ultragoal checkpoint。

## Changelog

- 初版纳入隐私前门、证据强度约束、独立审阅门、MVP 非默认终点和 deliberate 预演。
- 根据 Architect gate 修订研究与授权状态机：ADR 草案先于 ARV，代理不接受方向/MVP 决策，并补公开指标不可比和外链核验风险。
