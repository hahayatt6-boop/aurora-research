# RES-003-EXP 儿童验证实验执行包

版本：2026-07-12

用途：在 [ARV-006](../collaboration/ARV-006-wtp-waiver-ruling.md) 裁定跳过 RES-003-WTP 问卷后，将下一步推进到 [RES-003-EXP](RES-003-EXP-validation-experiment.md) 的执行准备。本文件用于交给研究执行负责人、原型负责人和伦理/安全负责人，明确可执行材料、原型范围、儿童安全边界、数据回流和停止条件。

## 执行边界

| 项目 | 要求 |
| --- | --- |
| 目标 | 验证原则 3（空白画布启动）、原则 4（依赖监控与干预）、原则 5（去同质化儿童适用性） |
| 人群 | 中国 5-8 岁儿童；家长书面知情同意；儿童可随时退出 |
| 样本 | 计划 n=48，每组 n=12；至少 2 个城市或合作机构来源 |
| 时长 | 4 周，8 次交互，每次 25-35 分钟 |
| 原型 | 研究原型，不是 MVP，不上线，不开放公开注册 |
| 仓库内数据 | 只保存聚合统计、评分分布、效应量、去标识主题摘要 |
| 仓库外数据 | 原始录音、作品、行为日志和同意材料必须留在受控存储 |
| 禁止入库 | 儿童姓名、家长联系方式、学校标识、照片、录音、精确位置、健康信息、逐字可识别材料 |

## 当前决策状态

| 门槛 | 当前处理 |
| --- | --- |
| WTP 条件 2 | ARV-006 裁定跳过问卷，作为低置信度定性通过假设；不作为实证证据 |
| 儿童机制验证 | 继续推进，成为下一项最关键验证 |
| MVP | 仍未授权；本执行包只服务研究验证 |
| HYP-003 | 保持 `testing`，等待 RES-003-EXP 结果 |
| RES-003 | 保持 `active`，儿童验证后再进入 review 判断 |

## 角色分工

| 角色 | 责任 |
| --- | --- |
| 研究负责人 | 锁定实验方案、停止条件、聚合输出和 RES/HYP 更新规则 |
| 伦理/安全负责人 | 完成仓库外正式研究方案审批、家长同意、儿童退出机制、数据删除流程 |
| 原型负责人 | 实现只满足实验所需的研究原型，不做产品化功能 |
| 执行协调人 | 招募合作机构、安排 8 次交互、记录缺席和退出 |
| 评估负责人 | 组织双评估者盲评、计算 ICC、汇总创造力评分和行为编码 |
| 数据负责人 | 仓库外清洗原始数据，生成只含聚合统计的回传表 |

## 发放前必备材料

| 材料 | 状态要求 |
| --- | --- |
| 仓库外伦理审批或等效研究方案批准 | 未完成不得招募 |
| 家长知情同意书 | 明确数据类型、用途、退出、删除、非产品化 |
| 儿童口头/图示同意脚本 | 用儿童能理解的语言说明可以拒绝和停止 |
| 合作机构确认 | 不记录具体学校标识到仓库 |
| 研究原型说明 | 说明原型仅用于研究，不是产品 |
| 数据最小化清单 | 明确哪些数据必须采集，哪些不得采集 |
| 紧急停止规则 | 儿童不适、家长撤回、原型异常、内容安全异常 |

## 原型最低范围

研究原型只做实验必要功能：

| 功能 | 必须有 | 不做 |
| --- | --- | --- |
| AI 引导人 | 开放式提问、反思性问题、按组别控制介入时机 | 长期账号、成长档案、商业订阅 |
| 创作区 | 简单绘画或口语故事记录入口 | 公开作品展示、社交分享 |
| 组别控制 | 空白画布介入 vs 全程介入；视觉化去同质化 vs 无去同质化 | 个性化推荐系统 |
| 依赖干预 | 检测连续请求、复制建议、拒绝自主创作等依赖行为后进入自主思考模式 | 惩罚性提示、羞辱性反馈 |
| 日志 | 只记录实验所需事件、时间戳和组别匿名编号 | 姓名、学校、精确位置、设备指纹 |
| 内容安全 | 儿童适龄输出过滤、人工终止开关 | 开放域无限聊天 |

## 实验配置

| 组别 | 空白画布启动 | 去同质化 | n |
| --- | --- | --- | ---: |
| A | 是 | 视觉化去同质化 | 12 |
| B | 是 | 无去同质化 | 12 |
| C | 全程介入 | 视觉化去同质化 | 12 |
| D | 全程介入 | 无去同质化 | 12 |

实验 2 的依赖干预采用被试内序列：第 1-4 次关闭干预，第 5-8 次启用干预。

## 每次执行流程

| 阶段 | 时长 | 操作 |
| --- | ---: | --- |
| 到场确认 | 3 分钟 | 确认儿童愿意继续，若拒绝则停止 |
| 热身 | 3-5 分钟 | 非评分小游戏或简单聊天，降低紧张 |
| 创作任务 | 15-20 分钟 | 按组别执行 AI 引导和创作 |
| 回顾 | 5 分钟 | AI 或执行员引导儿童描述作品 |
| 退出检查 | 2 分钟 | 记录儿童情绪、疲劳和是否愿意下次继续 |

执行员不得现场暗示“哪个组更好”，不得用奖励诱导儿童继续。

## 数据字典（仓库外明细）

以下字段可在仓库外明细中存在，但不得以个体级形式进入仓库：

| 字段 | 说明 |
| --- | --- |
| `participant_code` | 随机编号，不含姓名、学校、班级或联系方式 |
| `group_assignment` | A/B/C/D |
| `session_index` | 1-8 |
| `age_band` | 5-6 或 7-8 |
| `city_tier` | 城市层级，不保存城市名到仓库 |
| `ai_request_count` | 儿童主动请求 AI 次数 |
| `independent_idea_count` | 无提示自主提出新想法次数 |
| `dependency_event_count` | 依赖行为事件次数 |
| `intervention_triggered` | 是否触发自主思考模式 |
| `recovery_after_intervention` | 干预后 60 秒内是否恢复自主创作 |
| `creativity_score_rater_1` | 盲评评分 |
| `creativity_score_rater_2` | 盲评评分 |
| `diversity_score` | 去同质化评分 |
| `engagement_score` | 观察评分 |

## 仓库内聚合回传表

只允许以下聚合表进入仓库：

### `exp_sample_summary`

| column | type | definition |
| --- | --- | --- |
| total_consented | integer | 家长同意样本数 |
| total_started | integer | 至少完成 1 次交互 |
| total_completed | integer | 完成 8 次交互 |
| withdrawal_n | integer | 中途退出 |
| effective_n | integer | 主分析有效样本 |
| group_a_n | integer | A 组有效样本 |
| group_b_n | integer | B 组有效样本 |
| group_c_n | integer | C 组有效样本 |
| group_d_n | integer | D 组有效样本 |

### `exp_principle_outcomes`

| principle | metric | condition_a | condition_b | effect_size | p_value | status |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| blank_canvas | creativity_score |  |  |  |  | pending |
| blank_canvas | independent_idea_rate |  |  |  |  | pending |
| dependency_intervention | dependency_rate_change |  |  |  |  | pending |
| dependency_intervention | recovery_rate |  |  |  |  | pending |
| dehomogenization | diversity_score |  |  |  |  | pending |
| dehomogenization | creativity_score |  |  |  |  | pending |

### `exp_safety_summary`

| metric | n | notes |
| --- | ---: | --- |
| child_stop_requested |  |  |
| parent_withdrawal_requested |  |  |
| content_safety_intervention |  |  |
| adverse_event |  |  |
| data_deletion_requested |  |  |

### `exp_open_feedback_themes`

| source | theme_code | theme_label | n_mentions | paraphrased_example |
| --- | --- | --- | ---: | --- |
| child_exit_check |  |  |  |  |
| parent_feedback |  |  |  |  |
| facilitator_notes |  |  |  |  |

开放反馈只保存 paraphrase，不保存儿童逐字话语或家庭事件细节。

## 判定规则

| 原则 | 支持阈值 | 削弱/停止阈值 |
| --- | --- | --- |
| 原则 3：空白画布启动 | 空白画布组创造力不低于全程介入组，且自主发起率更高 | 空白画布组创造力显著更低 |
| 原则 4：依赖干预 | 依赖行为率下降 > 30%，且恢复率 > 60% | 依赖行为率不降或恢复率 < 40% |
| 原则 5：去同质化 | 视觉化去同质化组多样性显著更高，且创造力不下降 | 多样性无差异，或多样性提升以创造力明显下降为代价 |

若任一原则触发停止阈值，不得把 HYP-003 升级为 supported。

## 停止条件

- 伦理/同意材料未完成或无法落实删除权。
- 原型无法稳定执行组别控制，导致条件污染。
- 内容安全异常无法由人工终止开关及时处理。
- 儿童表现出明显不适、压力或持续拒绝。
- 合作机构要求收集可识别信息且无法隔离在仓库外。
- 有效样本低于 n=36，且无法补样。
- 评估者间信度 ICC < 0.70，且无法复核评分。

## 完成后的仓库更新

1. 新增 EVD 记录，保存聚合结果、效应量、局限和反证。
2. 更新 [RES-003](RES-003-ai-guide-efficacy.md) 的原则 3/4/5 状态。
3. 更新 [HYP-003](../hypotheses/HYP-003-ai-guide-efficacy.md) 为 supported、weakened 或 rejected。
4. 若结果支持，进入 MVP 准入门审查；若不支持，重新评估 [ADR-003](../decisions/ADR-003.md)。
5. 任何情况下都不得提交原始儿童数据。
