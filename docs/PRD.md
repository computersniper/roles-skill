# Product Requirements Document: 众生.skill / roles.skill

## 问题描述

现在已经有：
- `colleague.skill`: 把同事蒸馏成 AI Skill
- `ex.skill`: 把前任蒸馏成 AI Skill

但是，这两个都是针对**特定的具体的人**。我们需要一个更通用的框架：**让用户可以创建任何角色，无论是具体的人还是抽象的职业/身份**。

## 目标

创建一个 Claude Code Skill，允许用户：
1. 创建任何人类角色（职业、身份、真实人物虚构人物均可）
2. 提供原材料（教材、笔记、文字）
3. 系统自动提取 `Role Knowledge` + `Persona` 双层结构
4. 用户可以随时追加新材料，纠正错误，支持版本回滚
5. 完全兼容现有的 AgentSkills / Claude Code Skill 标准

## 用例

### 用例 1：创建个人老师
> 用户：我要高考了，把我的英语笔记都给你，帮我创建一个我的高三英语老师角色。
>
> [上传笔记 PDF]
>
> AI 提取：知识体系 → 教学风格 → 创建 Skill
>
> 用户：每天让这个老师抽我语法填空，讲解题目。

### 用例 2：创建歌手角色
> 用户：帮我创建周杰伦，华语流行，中国风，话不多，喜欢喝奶茶。
>
> AI 创建：用户可以随时和他聊音乐，聊人生。

### 用例 3：创建心理咨询师
> 用户：帮我创建一个温和的人本主义心理咨询师。
>
> 用户心情不好的时候可以随时来找他倾诉。

### 用例 4：创建健身教练
> 用户：帮我创建一个健身教练，我 175cm 70kg 体脂 20% 目标增肌。
>
> 帮我制定计划，监督我。

## 架构设计

延续 `colleague.skill` → `ex.skill` 的双层架构：

```
每个角色 Skill:
  PART A: Role Knowledge (专业领域知识)
  PART B: Persona (性格/风格/说话方式)

运行逻辑:
  收到问题 → Persona 决定用什么风格 → Knowledge 给出专业内容 → 输出
```

## 目录结构

```
create-role/
├── SKILL.md              # 主入口（create-role 命令）
├── README.md             # 项目说明
├── prompts/              # Prompt 模板
│   ├── intake.md         # 信息录入问题序列
│   ├── knowledge_analyzer.md # 知识提取
│   ├── persona_analyzer.md  # 性格提取
│   ├── knowledge_builder.md # 知识文件生成
│   ├── persona_builder.md  # 性格文件生成
│   ├── merger.md          # 增量合并
│   └── correction_handler.md # 纠正处理
├── tools/                # Python 工具
│   ├── skill_writer.py   # 列表管理
│   └── version_manager.py # 版本备份回滚
├── roles/               # 生成的角色（gitignore）
├── docs/PRD.md
├── requirements.txt
└── LICENSE
```

## 功能特性

### 必须有
- [x] 创建新角色（三个问题收集信息）
- [x] 支持多种原材料导入（PDF、图片、链接、粘贴）
- [x] 双层提取（Knowledge + Persona）
- [x] 生成完整 Skill 文件
- [x] 支持追加新材料
- [x] 支持对话纠正
- [x] 版本备份和回滚
- [x] 列出所有角色 / 删除角色
- [x] 兼容 Claude Code / AgentSkills 标准

### 标签支持
- 职业领域：任何领域都可以
- 性格标签：通用翻译表
- MBTI：全 16 型支持
- 可以仅凭描述生成，不需要材料

## 致谢

- 架构灵感来自 [colleague-skill](https://github.com/titanwings/colleague-skill) by [titanwings](https://github.com/titanwings)
- 进一步推广灵感来自 [ex-skill](https://github.com/therealXiaomanChu/ex-skill) by [therealXiaomanChu](https://github.com/therealXiaomanChu)

本项目遵循相同的开源精神，继续推广这个"把人/角色蒸馏成 AI Skill"的想法。
