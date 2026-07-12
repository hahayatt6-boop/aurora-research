---
id: ARV-006
reviewer_role: project-lead-ruling
reviewer_id: project-lead-20260712
original_author_or_source: user-directive
original_author_id: project-lead-chat-20260712
claims_reviewed: ARV-005 condition 2 execution requirement, RES-003-WTP
disposition: accepted
impact_on_confidence: WTP 问卷不执行；条件 2 不作为当前下一步排序阻断，但不能记录为实证满足；RES-003 的市场可行性置信度保持 low
owner_next_step: 跳过 RES-003-WTP 发放，按定性通过假设推进 RES-003-EXP 儿童验证执行准备；MVP 仍需 RES-003-EXP 和后续准入门审查
---

# 项目负责人裁定：跳过 RES-003-WTP 问卷并以定性通过假设推进下一步

裁定人：项目负责人
日期：2026-07-12
裁定对象：[ARV-005](ARV-005-conditions-ruling.md) 中条件 2 的执行要求，以及 [RES-003-WTP](../research/RES-003-WTP-pricing-experiment.md) 的发放计划。

## 裁定

项目负责人决定：**跳过 RES-003-WTP 问卷发放，暂不执行中国家长 WTP 定价实验；在路线排序上假设 WTP 定性可通过，并继续推进下一步儿童验证实验准备。**

该裁定的含义是：

1. `RES-003-WTP` 从 planned 改为 superseded，不再作为当前顺序的阻断项。
2. ARV-005 对条件 2 的严格解读不被改写为“已由实证满足”，而是被项目负责人豁免为“当前下一步排序不阻断”。
3. `EVD-035` 不得更新为支持性证据；它只记录“问卷未执行/无真实结果”的事实。
4. RES-003 的 WTP 置信度保持 `low`，不得升级为 `medium` 或 `high`。
5. 本裁定不授权 MVP，不允许创建产品蓝图或进入实现。

## 理由

- 项目负责人选择将当前资源优先投入儿童端核心机制验证，而不是继续做家长 WTP 定价实验。
- 现有公开证据已经足以形成定性风险假设：家长 WTP 路径存在但脆弱，信任界面和价格可及性是必要条件。
- 对当前阶段而言，儿童端原则 3/4/5 是否成立更可能改变方向选择；若儿童端验证失败，WTP 定价实验即使通过也无法支持产品推进。

## 证据边界

本裁定不是新证据，不改变以下事实：

| 项目 | 状态 |
| --- | --- |
| 是否有真实 RES-003-WTP 问卷结果 | 否 |
| 是否有 Aurora 场景 OPP/PMC/PME | 否 |
| 是否量化意向-行为差距 | 否 |
| 是否证明 19/39/69 元价格可行 | 否 |
| 是否满足“非学术 WTP 实证数据”的严格证据标准 | 否 |
| 是否允许继续下一步排序 | 是，基于项目负责人风险接受 |

## 对 RES-003 推进路径的影响

```
ARV-005 原路径:
RES-003-WTP 真实定价实验 + RES-003-EXP 儿童验证
    -> 两项均通过后 RES-003 可进入 review

ARV-006 裁定后路径:
WTP 问卷跳过，作为低置信度定性通过假设
    -> 继续 RES-003-EXP 儿童验证执行准备
    -> 若儿童验证不通过，重新评估 ADR-003
    -> 若儿童验证通过，再进入 MVP 准入门审查而非直接开发
```

## 后续要求

1. [RES-003-WTP](../research/RES-003-WTP-pricing-experiment.md) 标记为 `superseded`，说明“未执行，因项目负责人裁定跳过”。
2. [EVD-035](../evidence/EVD-035-china-parent-wtp-pricing-experiment.md) 保持 `low` 可靠性，并标注无真实结果。
3. [RES-003](../research/RES-003-ai-guide-efficacy.md) 更新条件 2 评估：实证未满足，但排序上由 ARV-006 豁免。
4. [RES-003-EXP](../research/RES-003-EXP-validation-experiment.md) 推进到执行准备，优先补齐执行包、伦理/同意清单、原型需求和聚合回传结构。
5. `mvp/` 保持关闭；任何 MVP 蓝图仍须另行通过准入门。

## 不能做的事

- 不能把“假设定性通过”写成“WTP 已验证”。
- 不能引用 EVD-035 支持商业可行性。
- 不能将 RES-003-WTP 空模板输出解释为结果。
- 不能因为 WTP 被豁免就删除家长信任界面、数据删除、价格可及性或真实支付风险。
- 不能越过 RES-003-EXP 直接进入 MVP。
