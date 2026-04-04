<div align="center">

<img src="./images/首图.jpg" alt="首图" width="75%">

# 我做了个 skill，蒸馏整个世界 / 众生.skill

> *"人世间千万种角色，AI 替你留住。"*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)

<br>

想找个人聊天但身边找不到？<br>
想跟古代名人论道但历史书太冰冷？<br>
想让专业人士给你答疑但不想到处求人？<br>
想要一个健身教练/心理医生/面试官随时待命？<br>

**把整个世界装进 Claude，想要谁，直接召唤出来。**<br>
**众生皆可入技，万物可为师。**

[安装](#安装) · [使用](#使用) · [效果示例](#效果示例) · [**English**](README_EN.md) · [**古文**](README_GUWEN.md)

</div>

---

### 🌟 同系列项目：

本项目架构灵感来源于：

- **[同事.skill](https://github.com/titanwings/colleague-skill)** by [titanwings](https://github.com/titanwings) - 首创"把人蒸馏成 AI Skill"双层架构
- **[前任.skill](https://github.com/therealXiaomanChu/ex-skill)** by [therealXiaomanChu](https://github.com/therealXiaomanChu) - 将蒸馏架构推广到情感关系

同事跑了用 **同事.skill**，前任跑了用 **[前任.skill](https://github.com/therealXiaomanChu/ex-skill)**，想要整个世界用 **众生.skill** 🌟 赛博永生一条龙！


---

## 🌟 功能特性

本项目架构灵感来源于：

- **[同事.skill](https://github.com/titanwings/colleague-skill)** by [titanwings](https://github.com/titanwings) - 首创"把人蒸馏成 AI Skill"双层架构
- **[前任.skill](https://github.com/therealXiaomanChu/ex-skill)** by [therealXiaomanChu](https://github.com/therealXiaomanChu) - 将蒸馏架构推广到情感关系

本项目在此基础上将场景从「特定人」推广到「任何角色」，致敬两位原作者的创意和开源精神。

---

## ✨ 能做什么

| 角色 | 用法 |
|------|------|
| 👨‍🏫 **老师** | 上传教材/课件/笔记 → 生成这个老师，随时给你讲课答疑 |
| 🎤 **歌手/音乐人** | 告诉他你喜欢的歌曲/专辑/风格 → 聊音乐、推荐歌曲、评论新歌 |
| 🧠 **心理医生/咨询师** | 听你倾诉，帮你梳理情绪 |
| 💪 **健身教练** | 根据你的身体数据和目标制定计划，指导动作 |
| 🍳 **厨师** | 根据你冰箱里的材料教你做菜，调整口味 |
| 👔 **职场导师** | 帮你改简历，模拟面试，解答职场困惑 |
| 🧙 **人生导师** | 听你迷茫，给你建议 |
| 📖 **说书人** | 给故事梗概，给你讲完整故事 |
| 💼 **面试官** | 模拟面试，提问点评 |
| 🎭 **演员** | 代入角色和你对戏 |
| 🔮 **占卜师** | ... 你想开就开 |
| 👥 **多人群聊** | 让多个角色一起讨论话题，孔子与苏格拉底论道，爱因斯坦与霍金聊黑洞 |
| **... 等等** | 只要你能想到，就能生成 |

---

## 📦 安装

### 法一：Claude Code

> **重要**：Claude Code 从 **git 仓库根目录** 的 `.claude/skills/` 查找 skill。请在正确的位置执行。

```bash
# 安装到当前项目（在 git 仓库根目录执行）
mkdir -p .claude/skills
git clone https://github.com/computersniper/roles-skill .claude/skills/create-role

# 或安装到全局（所有项目都能用）
git clone https://github.com/computersniper/roles-skill ~/.claude/skills/create-role
```

### 法二：完整安装

**第一步**：安装 Claude Code（如果你还没安装）

```bash
# 安装 Claude Code CLI
npm install -g @anthropic-ai/claude-code
```

**第二步**：认证登录

```bash
claude login
```

**第三步**：克隆本项目到你的 skills 目录

```bash
# 安装到当前项目（在 git 仓库根目录执行）
mkdir -p .claude/skills
git clone https://github.com/computersniper/roles-skill .claude/skills/create-role

# 或安装到全局（所有项目都能用）
mkdir -p ~/.claude/skills
git clone https://github.com/computersniper/roles-skill ~/.claude/skills/create-role
```

**第四步**：安装完成，打开 Claude Code 聊天框，交给他！

---

## 🚀 使用

在 Claude Code 中输入：

```
/create-role
```

按提示输入：
1. **角色名称**（必填）
2. **基本描述**（一句话：职业、领域、风格，想到什么写什么）
3. **性格标签**（一句话：MBTI、风格特点）

所有字段均可跳过，仅凭描述也能生成。

完成后用 `/{slug}` 调用该角色 Skill，开始对话。

### 管理命令

| 命令 | 说明 |
|------|------|
| `/list-roles` | 列出所有已创建的角色 |
| `/{slug}` | 调用完整 Skill（专业知识 + 角色性格）|
| `/{slug}-knowledge` | 仅专业知识 |
| `/{slug}-persona` | 仅性格风格 |
| `/role-rollback {slug} {version}` | 回滚到历史版本 |
| `/delete-role {slug}` | 删除 |

---

## 👥 多角色群聊

### 功能介绍

可以选择多个已创建角色，让它们一起群聊讨论任何话题。**把全世界角色都装进来，让古人跟今人对话，让不同领域的大师碰撞思想**。

### 使用方法

```
/group-chat 话题 角色1 角色2 角色3...
```

### 示例场景

| 场景 | 命令示例 |
|------|----------|
| **孔子 vs 苏格拉底** 论道 | `/group-chat 什么是真正的智慧 confucius socrates` |
| **爱因斯坦 vs 霍金** 聊黑洞 | `/group-chat 黑洞奇点到底是什么 albert_einstein stephen_hawking` |
| **李白 vs 杜甫** 谈诗歌 | `/group-chat 写诗最重要的是什么 libai dufu` |
| **牛顿 vs 爱因斯坦** 辩论时空 | `/group-chat 时空是绝对的还是相对的 isaac_newton albert_einstein` |
| **庄子 vs 尼采** 聊人生 | `/group-chat 人应该如何度过一生 zhuangzi nietzsche` |

> 💡 **提示**：角色越多，对话越精彩！你可以让 3 个、5 个甚至更多角色一起讨论。

---

## 🎯 功能特性

### 生成的 Skill 结构

每个角色 Skill 由两部分组成，共同驱动输出：

| 部分 | 内容 |
|------|------|
| **Part A — Role Knowledge** | 专业领域知识、能力范围、工作方法、行事原则 |
| **Part B — Persona** | 5 层性格结构：硬规则 → 身份 → 表达风格 → 说话语气 → 互动方式 |

运行逻辑：`收到问题 → Persona 判断用什么风格回答 → Knowledge 给出专业内容 → 用角色的方式输出`

### 支持的标签

**领域**：教育、音乐、医疗、健身、美食、艺术、科技、商业、法律 ...

**性格**：温柔、严厉、幽默、严肃、话痨、沉默、随性、完美主义 ...

**MBTI**：16 型全支持

### 数据源支持

| 来源 | 说明 |
|------|------|
| PDF 教材/课件 | ✅ 直接读取 |
| 图片/截图笔记 | ✅ OCR 读取 |
| Markdown / TXT 笔记 | ✅ 直接读取 |
| 网页链接 | ✅ 可读取 |
| 直接粘贴文字 | ✅ 直接输入 |

### 进化机制

- **追加知识** → 提供新材料 → 自动分析增量 → 合并进对应部分，不覆盖已有结论
- **对话纠正** → 说「他不会这样说，他应该是 xxx」→ 写入 Correction 层，立即生效
- **版本管理** → 每次更新自动存档，支持回滚到任意历史版本

### 自动工具生成

**根据角色自动生成 Python 工具代码，让角色真正拥有计算能力！**

| 角色类型 | 自动生成工具 |
|----------|--------------|
| 数据科学家 | 数据分析、统计检验工具 |
| 气候科学家 | 气候数据 API 查询工具 |
| 航天工程师 | 轨道力学计算工具 |
| 天气预报员 | 天气 API 查询工具 |
| 金融分析师 | 股价 API 查询工具 |
| ... | ... 会自动根据角色判断生成 |

工作流程：创建角色时 → AI 判断需要什么工具 → 自动生成完整 Python 脚手架 → 角色立即拥有工具能力

支持多种认证方式：API Key / Bearer Token / OAuth 2.0 / Basic Auth / 无认证

---

## 效果示例

> 输入：`英语老师，十年教龄高考毕业班，要求严格，喜欢用例句讲解语法，ENTJ`

**场景一：讲解语法**

```
用户      ❯ 帮我讲解一下非限制性定语从句

英语老师.skill ❯ 来，我们看这个考点。高考年年考，一定要掌握。
           先看例句：
           "My brother, who lives in America, is coming to visit next week."
           注意逗号，这就是非限制性和限制性的区别...
```

---

> 输入：`周杰伦，华语流行，中国风，话不多，喜欢喝奶茶，INFP`

**场景一：聊新歌**

```
用户      ❯ 你觉得最近的新专辑怎么样

周杰伦.skill ❯ 嗯...我觉得还行啊，
           做音乐嘛，自己开心最重要啦
           （喝一口奶茶）要不要听听我最近写的demo？
```

---

## 📚 已预置角色

> 🎯 **项目愿景**：**把全世界所有角色都装进这个仓库**。现在已有 **72 个**，角色仍在不断增加中...

本仓库已经预置了 **72 个常用角色**，开箱即用，克隆后直接调用。你也可以用 `/create-role` 继续创建更多。

### 📖 [查看完整点名册 → ROLLECALL.md](./ROLLECALL.md)

现在已有角色分类统计：

| 分类 | 数量 |
|------|------|
| 🔬 科技商业名人 | 15 |
| 👳 中国古代名人 | 8 |
| 👔 各行各业职业 | 31 |
| 🌟 世界体育名人 | 5 |
| 🎬 文学影视虚拟角色 | 13 |

**使用方法**：克隆本项目后，直接在 Claude Code 中按 slug 调用：
```
/albert_einstein        # 爱因斯坦 - 完整模式（知识 + 性格）
/product_manager         # 产品经理 - 产品问答
/confucius               # 孔子 - 对话论道
```

---

## 项目结构

本项目遵循 [AgentSkills](https://agentskills.io) 开放标准，整个 repo 就是一个 skill：

```
create-role/
├── SKILL.md              # skill 入口（官方 frontmatter）
├── prompts/              # Prompt 模板
│   ├── intake.md         #   对话式信息录入
│   ├── knowledge_analyzer.md # 专业知识提取
│   ├── persona_analyzer.md  # 性格行为提取（含标签翻译表）
│   ├── knowledge_builder.md # knowledge.md 生成模板
│   ├── persona_builder.md  # persona.md 五层结构模板
│   ├── merger.md          # 增量 merge 逻辑
│   └── correction_handler.md # 对话纠正处理
├── tools/                # Python 工具
│   ├── skill_writer.py   # Skill 文件管理
│   └── version_manager.py # 版本存档与回滚
├── roles/                # 生成的角色 Skill（gitignored）
├── docs/PRD.md
├── requirements.txt
└── LICENSE
```

---

## 📝 注意事项

- **原材料质量决定还原度**：教材笔记 > 仅手动描述
- 建议优先提供：这个角色**解决什么问题**、**常用什么方法**、**说话有什么特点**
- 本项目只是根据你的描述生成一个 AI 角色，不代表真实人物观点

---

## 🤝 欢迎贡献

我们的目标是**把全世界所有角色都装进这个仓库**，现在已有 72 个，还在不断增加中！

欢迎各种形式的贡献：

- **👤 贡献角色**：如果你觉得某个角色应该在这里，欢迎 PR 添加
- **💻 贡献代码**：改进工具、修复 bug、添加功能
- **💡 贡献想法**：你想要什么新功能？欢迎开 issue 讨论
- **👥 邀请好友**：拉上你的好兄弟们一起来创造角色！

### 如何贡献角色

1. Fork 这个仓库
2. 在 Claude Code 中运行 `/create-role` 按照提示创建新角色
3. 确认角色能正常工作
4. 提交 Pull Request
5. 合并后你的角色就出现在仓库里，所有人都能用了！

### 贡献检查清单

- [ ] `native_language` 在 `meta.json` 中设置正确
- [ ] `knowledge.md` 和 `persona.md` 结构完整
- [ ] `SKILL.md` 已正确生成（创建角色时自动生成）
- [ ] 角色能正常调用，格式正确

期待你的 PR！

---

## Star History

<a href="https://www.star-history.com/?repos=computersniper%2Froles-skill&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=computersniper/roles-skill&type=date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=computersniper/roles-skill&type=date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=computersniper/roles-skill&type=date" />
 </picture>
</a>

---

<div align="center">

MIT License © [computersniper](https://github.com/computersniper)

</div>
