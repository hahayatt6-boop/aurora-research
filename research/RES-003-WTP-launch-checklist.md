# RES-003-WTP 发放与聚合交接清单

版本：2026-07-12

用途：把 [RES-003-WTP](RES-003-WTP-pricing-experiment.md) 从仓库内准备推进到仓库外问卷执行，并确保回流到仓库的只有聚合统计。

## 发放前

| 检查项 | 要求 | 状态 |
| --- | --- | --- |
| 问卷文本 | 使用 [RES-003-WTP-questionnaire](RES-003-WTP-questionnaire.md) 最新版本 | pending |
| 概念卡 | 保留“早期概念、未验证效果、安全不完全保证”边界 | pending |
| 价格题 | PSM 四问 + 19/39/69 元价格锚定购买确定性均已录入 | pending |
| 招募渠道字段 | `recruitment_channel` 已录入，且不保存具体群名/账号/链接 | pending |
| 平台技术字段 | 关闭不必要的 IP、地理位置或设备指纹采集；无法关闭时仓库外删除 | pending |
| 开放题提示 | 明确要求不要填写姓名、联系方式、学校、具体地点或家庭可识别信息 | pending |
| 样本目标 | 有效样本 n >= 200；记录渠道配额和实际来源 | pending |
| 低时长阈值 | 固定为 120 秒，并计划报告敏感性分析 | pending |

## 仓库外数据处理

| 步骤 | 操作 | 禁止事项 |
| --- | --- | --- |
| 1 | 从问卷平台导出原始数据到仓库外安全位置 | 不提交原始导出 |
| 2 | 删除或隔离平台技术字段、开放题可识别内容 | 不把 hash、IP、设备指纹、具体渠道链接入库 |
| 3 | 执行筛选、理解检查、PSM 顺序一致性和低时长标记 | 不手动调整剔除规则以迎合结果 |
| 4 | 生成聚合 PSM 计数表 | 不保留个体级行 |
| 5 | 对开放题做主题编码和 paraphrase | 不保存逐字短摘 |
| 6 | 对所有聚合表做 small-cell suppression | 不发布 n < 10 单元格 |

## 聚合数据回流

只允许以下聚合文件或结果进入仓库：

| 文件/结果 | 说明 |
| --- | --- |
| `RES-003-WTP-psm-distribution-template.csv` 的填充副本 | 只含 scenario/question/price_code/n 聚合计数 |
| `RES-003-WTP-demand-scenario-template.csv` 的填充副本 | 只含锚定价格、有效样本、高确定性样本和折减率 |
| PSM 脚本输出价格点 | `pmc_cny`、`opp_cny`、`pme_cny` 与 status |
| 需求量折减输出 | `high_certainty_pct` 与 `conservative_demand_index` |
| 主题编码表 | 只含主题、频次、比例、paraphrase |

建议先在仓库外生成结果文件，人工复核后再选择是否将聚合结果入库。

## 计算命令

```bash
python3 scripts/calculate_wtp_psm.py \
  --psm-input <聚合PSM计数.csv> \
  --price-output <价格点输出.csv> \
  --demand-input <需求量输入.csv> \
  --demand-output <需求量输出.csv>
```

空模板 smoke test：

```bash
python3 scripts/calculate_wtp_psm.py \
  --psm-input research/RES-003-WTP-psm-distribution-template.csv \
  --price-output /tmp/res-003-wtp-price-points.csv \
  --demand-input research/RES-003-WTP-demand-scenario-template.csv \
  --demand-output /tmp/res-003-wtp-demand-scenario.csv
```

预期：空模板输出 `no_data` 价格点和零需求量折减，不得出现假 OPP/PMC/PME。

## EVD-035 更新步骤

1. 打开 [EVD-035 pending scaffold](../evidence/EVD-035-china-parent-wtp-pricing-experiment.md)。
2. 确认真实聚合数据已通过隐私复核。
3. 将 pending 表格替换为真实聚合结果。
4. 在“来源直接支持的陈述”中只写数据直接支持的事实。
5. 在“研究者解释”中单独写 Aurora 的解释，不把解释伪装成事实。
6. 在“局限与反证”中保留“非真实支付行为”的限制。
7. 更新 [evidence/README](../evidence/README.md)、[RES-003](RES-003-ai-guide-efficacy.md) 和相关 HYP 记录。

## 停止或回退条件

- 原始数据中出现可识别儿童、家庭、学校或联系方式，且无法可靠删除。
- 有效样本 n < 200。
- 单一渠道占比过高且无法补样。
- 目标价格下高确定性样本占比 < 20%。
- 聚合表存在 n < 10 单元格且无法合并。
- PSM 曲线无可解释交点，或结果完全依赖右删失顶格。

这些情况不代表研究失败，但必须阻止把 EVD-035 写成支持性证据。
