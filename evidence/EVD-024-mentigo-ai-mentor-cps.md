---
id: EVD-024
title: "Mentigo: AI Mentor Agent for Creative Problem Solving in Middle School"
source_type: peer-reviewed
published: 2025-04-01
retrieved: 2026-07-11
url: "https://doi.org/10.1145/3706598.3713952"
reliability: medium
reports: RES-003
related_hypotheses: [HYP-001]
related_research: [RES-003]
tags: [ai-mentor, cps, llm, adaptive-scaffolding, middle-school]
---

# 来源

Zha, S., Liu, Y., Zheng, C., et al. (2025). Mentigo: An Intelligent Agent for Mentoring Students in the Creative Problem Solving Process. CHI 2025.

## 背景

研究团队开发了 Mentigo，一个基于 LLM 的 AI 导师代理，用于指导中学生完成创意问题解决（CPS）过程。系统通过六阶段 CPS 过程运行，动态识别和响应 23 种不同的学生状态（如"目标不明确""思维过于发散""浅层思维"等），提供适应性指导策略。

## 来源直接支持的陈述

- Mentigo 在学生参与度、创造力和任务表现方面均优于基线系统
- 系统可用性量表（SUS）得分为 88.54
- 在目标清晰度（p = 0.051）、综合指导策略（p = 0.032）、知识与技能获取（p = 0.019）方面显著优于基线
- 学生反馈："系统 A（Mentigo）更像项目导师，提供更多引导，一步步带领你，几乎像老师引导你完成过程"
- 系统能动态识别 23 种学生状态并调整指导策略

## 研究者解释

Mentigo 是目前最接近 Aurora "AI 引导人"概念的系统之一。它证明了：
1. LLM 可以作为创意项目导师运行
2. 适应性指导策略比固定提示更有效
3. 学生将 AI 导师感知为"项目导师"而非工具

但局限明显：样本仅 12 名学生，无长期追踪，且基于特定 CPS 框架而非开放创作场景。

## 可靠性

**Medium**——同行评审发表（CHI 2025），但样本极小（12 名学生），专家评审仅 5 人。系统的"适应性"依赖预编码的状态-策略数据库而非真正的 LLM 自适应推理。

## 局限与反证

- 样本量极小（12 名学生），无法推广
- 无长期追踪，仅测量单次会话效果
- 系统依赖手工编码的学生状态库（23 种），而非 LLM 自主识别
- CPS 是结构化问题解决，不同于 Aurora 的开放创作场景
- 无对照组的长期留存数据
