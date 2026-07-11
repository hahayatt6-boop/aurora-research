# Test Spec: Aurora RES-001 研究闭环

## Test Strategy

验证对象不是“结论是否乐观”，而是证据链、状态推进、隐私边界和决策强度是否满足仓库契约。

## Unit

- 运行 `python3 -m unittest discover -s tests -v`，现有 validator 测试全部通过。
- 若执行发现 schema 缺口，只在该缺口影响新增记录时增加最小回归测试。

## Integration

- 运行 `python3 scripts/validate_repository.py`，检查 EVD/RES/HYP/ADR/TASK/ARV 字段、链接、枚举、日期、隐私和独立审阅门。
- 对新增 URL 逐项打开核验标题、机构、发布日期和直接支持内容。
- 检查目录索引与实际记录状态一致。

## E2E

1. TASK-001 `active` -> EVD 登记 -> 先创建 ADR=`proposed` 草案和 HYP 拟定终态 -> 再将 RES 推进为 `review` -> 独立 ARV -> 处理挑战 -> RES=`complete` + HYP 终态 + ADR=`proposed` -> TASK `done`。ADR 草案必须先于 RES=`review` 和 HYP 终态存在。
2. 临时复制仓库到隔离目录，删除 ARV 或改为 `unresolved`，校验器必须退出非 0。
3. 在隔离目录制造 EVD 缺字段、错误 reports、失效链接，校验器必须退出非 0。
4. 使用 `mktemp -d` 在 Git 工作树外创建临时隔离目录，加入示例联系方式或儿童与学校组合，校验器必须退出非 0；无论通过、失败或中断处理，均用 trap / `rm -rf "$tmpdir"` 清理，不在真实仓库或固定临时路径保存该 fixture。
5. 对正常仓库重复运行测试至少两次，排除偶然绿灯。

## Observability

- 每个命令记录退出码和关键输出。
- `RES=review` 且 ARV 尚未解决的中间 checkpoint 预期为 validator-red；它用于证明审阅门生效，不是最终失败。正式绿色验证只在 ARV 逐项处理完成、记录级 disposition 已解决之后运行。
- Ultragoal ledger 记录每个故事的文件、来源数量、状态和验证结果。
- Code review 输出 recommendation 与 architectural status。
- UltraQA 场景矩阵记录 setup、expected、actual、cleanup。

## Research Quality Checks

| 检查 | 通过条件 |
| --- | --- |
| 来源直接性 | 搜索摘要不作为事实；每个 EVD 有可打开来源 |
| 外链核验留痕 | 每个 EVD 记录 `retrieved`，并在正文保存标题、发布者、日期和关键主张的逐页核验摘要 |
| 事实/解释分离 | “来源直接支持的陈述”不包含未标注推断 |
| 可靠性 | 公司自述不单独支撑教育效果；限制写明 |
| 案例对照 | 包含不同结果，而非只选成功或失败案例 |
| 反证 | 每条证据线至少一个反对 HYP-001 的候选来源 |
| 决策强度 | ADR 动作不超过 RES 置信度和 ARV 处置 |
| 授权边界 | ADR-001 在项目负责人明确接受前保持 `proposed`；自动流程不得打开 MVP |
| ARV 状态 | 任一逐项挑战未决时记录级 `disposition=unresolved`；全部逐项解决后才允许 `accepted` 或 `rejected` |
| 隐私 | 无用户个案、评论截图、身份组合或原始访谈内容 |

## Acceptance Evidence

- `evidence/` 中 EVD 记录和索引。
- `research/RES-001-platform-gap.md`、`hypotheses/HYP-001-continuity-gap.md`。
- `collaboration/ARV-001-res-001.md`。
- `decisions/ADR-001-res-001-direction.md`。
- 两条验证命令输出、code review 报告和 UltraQA 报告。

## Stop Conditions

- 发现可识别儿童、家庭或学校材料：不入库并终止该来源处理。
- 关键结论只有低可靠来源：不得推进到方向性接受态，改为未知项或 inconclusive。
- ARV 为 unresolved：不得完成 RES/HYP 或接受 ADR，返回计划修订或记录阻塞。
- 自动流程结束前若 ADR-001 在没有项目负责人明确交互授权的情况下变为 `accepted`，视为硬阻塞并恢复为待负责人决定的 `proposed` 状态。
- 三次修订仍无法通过同一门：报告硬阻塞，不伪造完成。
