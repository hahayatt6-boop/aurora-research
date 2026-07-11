# Aurora 儿童创造力教育研究

Aurora 是一个研究项目，用于判断：在 AI 时代，儿童创造力教育是否存在值得长期投入的机会，以及什么干预方式真正有助于儿童形成创造力、思维能力、项目能力、主体性和终身学习能力。

本项目不预设 AI 导师、机器人、智能硬件、创作工具或成长档案就是答案。研究可以得出继续、转向、收窄、暂缓或停止的结论。

## 方法来源

本项目使用 [Research OS](https://github.com/hahayatt6-boop/researchos) 的研究结构和校验工具。当前项目副本来自拆分基准 `504367d23681f0101e521a2d6ffad0a9cfa13662`；详细来源见[迁移记录](MIGRATION.md)。

## 研究工作流

1. [研究宪章](docs/charter/RESEARCH_CHARTER.md)定义使命、伦理和边界。
2. [假设库](hypotheses/README.md)记录可被证伪的判断。
3. [证据库](evidence/README.md)记录来源、可靠性和局限。
4. [研究报告](research/README.md)综合事实、反证和未知项。
5. [决策日志](decisions/README.md)解释项目如何根据证据行动。
6. [研究路线图](docs/roadmap/RESEARCH_ROADMAP.md)安排八个研究主题。
7. [MVP 准入门](mvp/README.md)防止在研究支持前进入产品开发。
8. [多智能体协作规程](docs/agents/MULTI_AGENT_COLLABORATION.md)约束代理分工、隐私前门、反方审阅和落库验证。

## 当前重点

- [RES-001：儿童 AI 与 STEAM 产品的平台缺口](research/RES-001-platform-gap.md)
- [HYP-001：跨项目连续性是主要平台缺口](hypotheses/HYP-001-continuity-gap.md)
- [ADR-000：先研究，再选择产品形态](decisions/ADR-000-research-before-product.md)

## 质量检查

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_repository.py
```

仓库不得保存任何可识别儿童身份的数据。儿童福祉始终高于活跃度、增长和商业化目标。
