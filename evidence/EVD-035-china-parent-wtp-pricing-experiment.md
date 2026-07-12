---
id: EVD-035
title: "中国家长 WTP 定价实验（skipped scaffold）"
source_type: primary-research
published: unknown
retrieved: 2026-07-12
reliability: low
reports: RES-003
related_hypotheses: [HYP-002, HYP-003]
related_research: [RES-003, RES-003-WTP]
tags: [wtp, china, pricing, psm, skipped, primary-research]
---

# 来源

Skipped Aurora primary research scaffold for [RES-003-WTP](../research/RES-003-WTP-pricing-experiment.md).

**当前状态：skipped。** 项目负责人已在 [ARV-006](../collaboration/ARV-006-wtp-waiver-ruling.md) 裁定跳过 RES-003-WTP 问卷，并以低置信度定性通过假设推进下一步。本记录尚未包含真实问卷结果、真实 OPP/PMC/PME、购买确定性比例或需求量折减结果。不得将本记录引用为 ARV-005 条件 2 已满足的证据。

## 背景

原计划执行一项中国 4-8 岁儿童家长 WTP 定价实验：

- 方法：Van Westendorp 价格敏感度测试（PSM）+ 19/39/69 元/月价格锚定购买确定性 + 需求量折减
- 样本：n >= 200 有效样本
- 数据边界：仓库内只保存聚合统计，不保存原始问卷导出或清洗后个体级数据
- 问卷文本：[RES-003-WTP-questionnaire](../research/RES-003-WTP-questionnaire.md)
- 分析口径：[RES-003-WTP-analysis-tables](../research/RES-003-WTP-analysis-tables.md)
- 聚合模板：[PSM 分布模板](../research/RES-003-WTP-psm-distribution-template.csv)、[需求量折减模板](../research/RES-003-WTP-demand-scenario-template.csv)

## 来源直接支持的陈述

当前无真实来源结果，且问卷已被裁定跳过。以下字段保持未产生：

| 字段 | 当前状态 |
| --- | --- |
| 总完成样本 | not collected |
| 主分析有效样本 | not collected |
| 19 元/月高确定性样本占比 | not collected |
| 39 元/月高确定性样本占比 | not collected |
| 69 元/月高确定性样本占比 | not collected |
| stated preference OPP/PMC/PME | not collected |
| high certainty OPP/PMC/PME | not collected |
| conservative demand index | not collected |
| top trust requirements | not collected |
| value driver ranking | not collected |

## 研究者解释

当前解释仅限于方法准备和项目负责人裁定记录：

- 本 scaffold 说明 EVD-035 原本应如何记录结果，不提供任何已发生的 WTP 结论。
- ARV-006 的“定性通过假设”是项目排序和风险接受，不是实证结果。
- 空白聚合模板和 PSM 脚本已验证：无数据输入时输出 `no_data` 和零需求量折减，不会生成假价格点。
- 若未来结果显示目标价格下高确定性样本占比低于 20%，或高确定性 PSM 无法覆盖最低可行月费，RES-003 的 WTP 判断必须继续保持低置信度或下调。

## 可靠性

当前可靠性为 `low`，因为真实问卷未发放且未产生可验证聚合结果。本记录只能说明问卷被跳过和保留未来可恢复框架，不能单独支持任何重大决策。

若未来重新执行问卷，可靠性最多可在以下条件满足后提升至 `medium`：

1. 有 n >= 200 的有效聚合样本；
2. 聚合表通过 small-cell suppression 和隐私复核；
3. PSM 价格点和需求量折减由仓库脚本生成并可复现；
4. 结果章节明确标注陈述偏好不等于真实支付行为。

## 局限与反证

- PSM 仍是陈述性偏好，不能替代真实支付行为。
- 19/39/69 元价格锚定购买题测量的是概念条件下的购买可能性，不是真实付费转化。
- 样本来源若集中于单一渠道，WTP 可能被高估。
- 若家长信任门槛主要依赖线下老师、机构背书或免费试用，家庭直付路径仍然脆弱。

## 更新条件

只有在未来重新执行问卷且真实聚合数据完成后，才允许把本记录从 skipped scaffold 更新为结果证据。更新时必须：

1. 不提交原始或个体级问卷数据；
2. 填入聚合样本、PSM 价格点、需求量折减和信任门槛结果；
3. 更新 [evidence/README](README.md) 中 EVD-035 的主要用途；
4. 更新 [RES-003](../research/RES-003-ai-guide-efficacy.md) 的 ARV-003 条件 2 状态；
5. 若结果不可行，更新 HYP-002/HYP-003 的商业约束影响。
