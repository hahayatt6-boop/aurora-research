# RES-003-WTP 数据分析表结构

版本：2026-07-11

用途：定义 [RES-003-WTP](RES-003-WTP-pricing-experiment.md) 的数据字段、清洗标记、聚合表和决策输出。仓库内只保存聚合表和去标识主题摘要，不保存原始可识别材料。

## 数据文件边界

| 文件 | 是否入库 | 说明 |
| --- | --- | --- |
| 原始问卷导出 | 否 | 仓库外保存，可能含平台技术字段和开放题原文 |
| 清洗后个体级数据 | 否 | 即使去除联系方式，也仍可能形成家庭画像，不入库 |
| 聚合统计表 | 是 | 只含分组统计、比例、均值、中位数和价格点 |
| 开放题主题编码表 | 是 | 只保存主题、频次和去标识短摘；不得保存可识别内容 |
| EVD-035 证据记录 | 是 | 定价实验结论、方法、样本、局限 |

## 价格区间编码

PSM 价格选项用区间中点进行计算；敏感性分析同时报告下界和上界。

| code | label | lower_cny | midpoint_cny | upper_cny |
| --- | --- | ---: | ---: | ---: |
| P00_09 | 0-9 元/月 | 0 | 5 | 9 |
| P10_19 | 10-19 元/月 | 10 | 15 | 19 |
| P20_29 | 20-29 元/月 | 20 | 25 | 29 |
| P30_49 | 30-49 元/月 | 30 | 40 | 49 |
| P50_79 | 50-79 元/月 | 50 | 65 | 79 |
| P80_119 | 80-119 元/月 | 80 | 100 | 119 |
| P120_199 | 120-199 元/月 | 120 | 160 | 199 |
| P200_PLUS | 200 元/月及以上 | 200 | 240 | 280 |

说明：`P200_PLUS` 的上界不是事实价格，只用于敏感性分析。主分析不得把开放上界解释为真实上限。

## 原始字段字典

该表用于从问卷平台导出字段映射到分析字段。原始个体级数据不入库。

| field_name | type | allowed_values | required | analysis_use |
| --- | --- | --- | --- | --- |
| response_id_hash | string | platform-generated hash | yes | 去重；仓库内不保存 |
| submitted_at_date | date | YYYY-MM-DD | yes | 质量检查；仓库内最多保存日期聚合 |
| duration_seconds | integer | >= 0 | yes | 低时长标记 |
| decision_role | categorical | primary, shared, no | yes | 筛选 |
| child_age_band | multi | age_4_5, age_6_8, none | yes | 筛选与分层 |
| city_tier | categorical | tier1, new_tier1, tier2, tier3_lower, unsure | yes | 分层 |
| monthly_child_spend | categorical | 0_99, 100_299, 300_599, 600_999, 1000_1999, 2000_plus, unsure | yes | 分层 |
| paid_child_app_history | categorical | current, past, never, unsure | yes | 分层 |
| comprehension_ai_role | categorical | guide, replace, course, unsure | yes | 理解检查 |
| comprehension_parent_view | categorical | summary_boundary, full_transcript, test_score, unsure | yes | 理解检查 |
| comprehension_product_type | categorical | software, hardware, offline_course, unsure | yes | 理解检查 |
| psm_too_cheap | price_code | price codes | yes | PSM |
| psm_cheap | price_code | price codes | yes | PSM |
| psm_expensive | price_code | price codes | yes | PSM |
| psm_too_expensive | price_code | price codes | yes | PSM |
| purchase_certainty | integer | 1-10 | yes | 高确定性校准 |
| budget_source | categorical | interest_class, books_materials, toys_entertainment, app_subscription, new_budget, would_not_buy, unsure | yes | 支付来源 |
| expected_retention | categorical | trial_1m, 2_3m, 4_6m, 7_12m, 12m_plus, would_not_subscribe, unsure | yes | 续费预期 |
| trust_requirements | multi | privacy_delete, parent_report, no_ai_completion, content_safety, visible_growth, expert_endorsement, low_price, child_likes, free_trial, other | yes | 信任门槛 |
| ai_trust_level | integer | 1-5 | yes | 信任分层 |
| value_top3 | multi | start_creation, richer_expression, reduce_short_video, parent_report, no_ai_completion, data_control, weekly_tasks, portfolio | yes | 价值排序 |
| primary_value_driver | categorical | same as value_top3 | yes | 主要购买理由 |
| main_concern_text | text | optional | no | 仓库外主题编码 |
| desired_feature_text | text | optional | no | 仓库外主题编码 |

## 清洗标记表

表名：`wtp_cleaning_summary`

| column | type | definition |
| --- | --- | --- |
| total_started | integer | 打开并进入问卷的样本数 |
| total_completed | integer | 完成问卷的样本数 |
| invalid_screening_n | integer | 筛选不合格样本数 |
| failed_comprehension_n | integer | 理解检查失败样本数 |
| invalid_psm_order_n | integer | PSM 顺序不一致样本数 |
| low_duration_n | integer | 低时长样本数 |
| duplicate_response_n | integer | 重复样本数 |
| contains_identifier_n | integer | 开放题疑似包含可识别信息的样本数 |
| effective_n_main | integer | 主分析有效样本数 |
| effective_n_high_certainty | integer | 购买确定性 8-10 分有效样本数 |

## 样本结构表

表名：`wtp_sample_profile`

| segment_dimension | segment_value | n | pct |
| --- | --- | ---: | ---: |
| city_tier | tier1 |  |  |
| city_tier | new_tier1 |  |  |
| city_tier | tier2 |  |  |
| city_tier | tier3_lower |  |  |
| child_age_band | age_4_5 |  |  |
| child_age_band | age_6_8 |  |  |
| monthly_child_spend | 0_99 |  |  |
| monthly_child_spend | 100_299 |  |  |
| monthly_child_spend | 300_599 |  |  |
| paid_child_app_history | current |  |  |
| paid_child_app_history | past |  |  |
| paid_child_app_history | never |  |  |
| ai_trust_level | 1_2_low |  |  |
| ai_trust_level | 3_mid |  |  |
| ai_trust_level | 4_5_high |  |  |

说明：若任一关键分层 n < 30，只报告描述性统计，不做强比较。

## PSM 分布表

表名：`wtp_psm_distribution`

| scenario | psm_question | price_code | n | pct | cumulative_pct |
| --- | --- | --- | ---: | ---: | ---: |
| stated_preference | too_cheap | P00_09 |  |  |  |
| stated_preference | cheap | P00_09 |  |  |  |
| stated_preference | expensive | P00_09 |  |  |  |
| stated_preference | too_expensive | P00_09 |  |  |  |
| high_certainty | too_cheap | P00_09 |  |  |  |
| conservative_30pct | too_cheap | P00_09 |  |  |  |

三种场景：

- `stated_preference`：主分析有效样本
- `high_certainty`：`purchase_certainty >= 8` 的有效样本
- `conservative_30pct`：高确定性样本按 30% 转化率折减；用于收入和可行性，不改变价格分布形状

## PSM 价格点输出表

表名：`wtp_psm_price_points`

| scenario | n | pmc_cny | opp_cny | pme_cny | acceptable_range_cny | notes |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| stated_preference |  |  |  |  |  | 上限估计 |
| high_certainty |  |  |  |  |  | 中性估计 |
| conservative_30pct |  |  |  |  |  | 只用于需求规模折减 |

计算口径：

- `PMC`：`too_cheap` 曲线与 `expensive` 曲线交点
- `OPP`：`too_cheap` 曲线与 `too_expensive` 曲线交点
- `PME`：`cheap` 曲线与 `too_expensive` 曲线交点
- 若使用区间数据，先以中点计算；再用上下界做敏感性分析

## 分层价格点表

表名：`wtp_segment_price_points`

| segment_dimension | segment_value | scenario | n | opp_cny | pmc_cny | pme_cny | high_certainty_pct |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| city_tier | tier1 | high_certainty |  |  |  |  |  |
| city_tier | new_tier1 | high_certainty |  |  |  |  |  |
| child_age_band | age_4_5 | high_certainty |  |  |  |  |  |
| child_age_band | age_6_8 | high_certainty |  |  |  |  |  |
| monthly_child_spend | 300_599 | high_certainty |  |  |  |  |  |
| paid_child_app_history | current | high_certainty |  |  |  |  |  |
| ai_trust_level | 4_5_high | high_certainty |  |  |  |  |  |

解释规则：分层结果只用于发现价格敏感人群，不得用小样本分层替代总体结论。

## 付费确定性表

表名：`wtp_purchase_certainty`

| score_band | n | pct | median_psm_cheap_cny | median_psm_expensive_cny |
| --- | ---: | ---: | ---: | ---: |
| 1_3_low |  |  |  |  |
| 4_7_mid |  |  |  |  |
| 8_10_high |  |  |  |  |

关键输出：

- `high_certainty_pct = n(8_10_high) / effective_n_main`
- 若 `high_certainty_pct < 20%`，WTP 判断必须降级，不能把 PSM 上限作为商业可行证据。

## 支付来源和续费预期表

表名：`wtp_payment_behavior_proxy`

| metric | option | n | pct |
| --- | --- | ---: | ---: |
| budget_source | interest_class |  |  |
| budget_source | books_materials |  |  |
| budget_source | toys_entertainment |  |  |
| budget_source | app_subscription |  |  |
| budget_source | new_budget |  |  |
| budget_source | would_not_buy |  |  |
| expected_retention | trial_1m |  |  |
| expected_retention | 2_3m |  |  |
| expected_retention | 4_6m |  |  |
| expected_retention | 7_12m |  |  |
| expected_retention | 12m_plus |  |  |

解释规则：

- `new_budget` 占比低，说明产品主要挤占既有教育/娱乐预算。
- `trial_1m` 和 `would_not_subscribe` 占比高，说明首购和续费风险不可忽略。

## 信任门槛表

表名：`wtp_trust_requirements`

| requirement | n_selected | pct_selected | rank |
| --- | ---: | ---: | ---: |
| privacy_delete |  |  |  |
| parent_report |  |  |  |
| no_ai_completion |  |  |  |
| content_safety |  |  |  |
| visible_growth |  |  |  |
| expert_endorsement |  |  |  |
| low_price |  |  |  |
| child_likes |  |  |  |
| free_trial |  |  |  |
| other |  |  |  |

决策用途：排名前 3 的信任门槛必须进入后续家长信任界面设计；否则价格实验不能直接解释为可购买需求。

## 价值主张表

表名：`wtp_value_drivers`

| value_driver | top3_n | top3_pct | primary_n | primary_pct | rank_primary |
| --- | ---: | ---: | ---: | ---: | ---: |
| start_creation |  |  |  |  |  |
| richer_expression |  |  |  |  |  |
| reduce_short_video |  |  |  |  |  |
| parent_report |  |  |  |  |  |
| no_ai_completion |  |  |  |  |  |
| data_control |  |  |  |  |  |
| weekly_tasks |  |  |  |  |  |
| portfolio |  |  |  |  |  |

解释规则：若 `parent_report`、`data_control` 或 `no_ai_completion` 排名高于儿童创作收益，说明家长购买理由主要是风险控制而非创造力收益。

## 开放题主题编码表

表名：`wtp_open_text_themes`

| source_question | theme_code | theme_label | n_mentions | pct_respondents | anonymized_quote_example |
| --- | --- | ---: | ---: | ---: | --- |
| main_concern | dependency | 依赖 AI |  |  |  |
| main_concern | content_safety | 内容安全 |  |  |  |
| main_concern | privacy | 数据隐私 |  |  |  |
| main_concern | effectiveness | 是否真的有效 |  |  |  |
| desired_feature | parent_control | 家长控制 |  |  |  |
| desired_feature | trial | 免费试用 |  |  |  |

开放题处理规则：

1. 先在仓库外删除任何可识别片段。
2. 再进行主题编码。
3. 仓库内只保存主题频次和短摘。
4. 短摘不得包含姓名、联系方式、学校、具体地点、罕见身份组合或家庭事件细节。

## 决策矩阵表

表名：`wtp_decision_matrix`

| condition | threshold | observed_value | status | decision_impact |
| --- | --- | --- | --- | --- |
| high_certainty_pct | >= 20% |  | pending | 低于阈值则 WTP 判断降级 |
| conservative_opp_vs_19 | >= 19 CNY |  | pending | 不支持最低订阅价则停止消费级路径 |
| conservative_opp_vs_39 | >= 39 CNY |  | pending | 支持轻量订阅价 |
| conservative_opp_vs_69 | >= 69 CNY |  | pending | 支持较高服务成本 |
| pme_vs_min_viable_fee | >= locked_min_fee |  | pending | 覆盖单位经济上限 |
| trust_top3_covered_by_design | true |  | pending | 未覆盖则需先做家长信任界面 |
| effective_n_main | >= 200 |  | pending | 不足则不能满足 ARV-005 |

`status` 取值：

- `pass`
- `partial`
- `fail`
- `pending`

## EVD-035 结果摘要模板

执行完成后，新增 `evidence/EVD-035-china-parent-wtp-pricing-experiment.md`，至少写入以下结果：

| 字段 | 内容 |
| --- | --- |
| 样本 | 总样本、有效样本、高确定性样本 |
| 方法 | PSM + 付费确定性校准 |
| 价格点 | stated preference、high certainty、conservative 三种情景 |
| 核心结论 | 条件 2 是否满足 |
| 反证 | 高确定性占比、价格不足、信任门槛过高等 |
| 局限 | 陈述偏好、概念卡、非真实支付 |

不得把 PSM 结果表述为真实购买行为。若没有真实支付，可靠性不得高于 `medium`。
