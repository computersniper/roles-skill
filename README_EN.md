<div align="center">

<img src="./images/首图.jpg" alt="Banner" width="75%">

# roles.skill /众生.skill

> *"All roles in the world, AI preserves them for you."*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)

<br>

Can't find the right person to talk to?<br>
Want to discuss philosophy with ancient sages but history books feel cold?<br>
Need professional advice but don't know who to ask?<br>
Want a personal trainer/psychiatrist/interviewer available 24/7?<br>

**Put the whole world into Claude. Summon anyone you want, instantly.**<br>
**Any person, any thing, can be a skill — learn from anyone, anything.**

[Installation](#installation) · [Usage](#usage) · [Examples](#examples) · [**中文**](README.md) · [**古文**](README_GUWEN.md)

</div>

---

### 🌟 Series Projects:

This project architecture is inspired by:

- **[colleague-skill](https://github.com/titanwings/colleague-skill)** by [titanwings](https://github.com/titanwings) - Invented the "distill a person into AI Skill"双层 architecture
- **[ex-skill](https://github.com/therealXiaomanChu/ex-skill)** by [therealXiaomanChu](https://github.com/therealXiaomanChu) - Extended the distillation architecture to relationships

Use **colleague-skill** when your colleague leaves, use **[ex-skill](https://github.com/therealXiaomanChu/ex-skill)** when your ex leaves, use **roles.skill** when you want **the whole world** 🌟 Complete cyber immortality solution!

If you find this interesting, please Star both projects!

---

## ✨ What It Does

Put the whole world into Claude Code. Create an AI Skill for **any person/thing**, summon them anytime you want to chat or work with them.

- 👤 **Any person** - historical figure, celebrity, professional, anyone
- 📦 **Any thing** - a book, a product, a place, anything can converse with you
- 🌍 **72 pre-built roles** ready to use out of the box
- 🎯 **Automatic tool code generation** - if your role needs external APIs, we generate Python code scaffolding automatically
- 📈 **Continuous evolution** - append knowledge, correct responses, version control included

---

## 📦 Installation

### Claude Code

> **Important**: Claude Code looks for skills in `.claude/skills/` from **git repo root**. Please execute in the correct location.

```bash
# Install to current project (execute in git repo root)
mkdir -p .claude/skills
git clone https://github.com/computersniper/roles-skill .claude/skills/create-role

# Or install globally (available in all projects)
git clone https://github.com/computersniper/roles-skill ~/.claude/skills/create-role
```

### OpenClaw

```bash
git clone https://github.com/computersniper/roles-skill ~/.openclaw/workspace/skills/create-role
```

### Dependencies (optional)

```bash
pip3 install -r requirements.txt
```

---

## 🚀 Usage

In Claude Code, enter:

```
/create-role
```

Follow the prompts:
1. **Role Name** (required)
2. **Basic Info** (one sentence: profession, field, characteristics)
3. **Personality Profile** (one sentence: MBTI, style traits, your impression)
4. **Unique Abilities & Tools** (any unique capabilities this role has, needs any external APIs/tools?)
5. **Native Language** (what language does this character native speak)

All fields except name can be skipped. Generate even with just manual description.

When done, invoke with `/{slug}` to start chatting.

### Management Commands

| Command | Description |
|------|-------------|
| `/list-roles` | List all created roles |
| `/{slug}` | Invoke full Skill (Knowledge + Persona) |
| `/{slug}-knowledge` | Knowledge only |
| `/{slug}-persona` | Persona only |
| `/role-rollback {slug} {version}` | Rollback to historical version |
| `/delete-role {slug}` | Delete role |

### Group Chat Commands

| Command | Description |
|------|-------------|
| `/group-chat {topic} {role1} {role2}...` | Start a group chat with multiple roles |
| `/set-translation {language}` | Set default translation language |
| `/add-role {slug}` | Add another role to current group chat |

### Tool Learning Commands

| Command | Description |
|------|-------------|
| `/configure-tool {role-slug} {tool-name}` | Configure API credentials for a tool |
| `/learn-tool {role-slug} {tool-name}` | Let the role autonomously learn how to use the tool |

---

## 👥 Multi-Role Group Chat

You can select multiple created roles and let them chat together about any topic. **Put the whole world in Claude, let ancients talk with modern people, let masters from different fields碰撞思想**.

### Example Scenarios

| Scenario | Command Example |
|------|----------|
| **Confucius vs Socrates** on wisdom | `/group-chat What is true wisdom confucius socrates` |
| **Einstein vs Hawking** on black holes | `/group-chat What's inside a black hole albert_einstein stephen_hawking` |
| **Li Bai vs Du Fu** on poetry | `/group-chat What matters most in poetry libai dufu` |

> 💡 **Tip**: The more roles, the more interesting! You can have 3, 5, even more roles discussing together.

---

## 🎯 Features

### Generated Skill Structure

Each role Skill consists of two parts that work together to drive output:

| Part | Content |
|------|------|
| **Part A — Role Knowledge** | Domain expertise, core capabilities, methodology, key principles |
| **Part B — Persona** | 5-layer personality structure: Hard Rules → Basic Identity → Communication Style → Decision Pattern → Interaction Pattern |

Execution logic: `Receive question → Persona decides what style/attitude → Role Knowledge executes → Output in Persona's style`

### Native Language + Translation

Every role defines its `native_language`. Output in native language first, then translate to user's target language. Users can switch target language anytime.

- Li Bai writes in **Classical Chinese** → automatically translated to modern Chinese
- Messi speaks **Spanish** → automatically translated to your language
- Keep it authentic, learn something new along the way!

### Autonomous Tool Learning

- User provides API configuration → we generate Python code scaffolding → role autonomously learns how to use it
- Singers learn to call music APIs to sing, painters learn to call image APIs to paint
- No need for you to write code — AI does all the learning
- Continuous evolution, gets better with use

### Automatic Tool Generation

**Automatically generate Python tools based on role type, so your role gets real computation capabilities!**

| Role Type | Auto-generated Tool |
|-----------|---------------------|
| Data Scientist | Data analysis & statistical testing toolkit |
| Climate Scientist | Climate data API client |
| Aerospace Engineer | Orbital mechanics calculator |
| Weather Forecaster | Weather API client |
| Financial Analyst | Stock price API client |
| ... | ... AI will automatically determine based on role type |

Workflow: When creating a role → AI determines what tools are needed → automatically generates complete Python scaffolding → role gets tool capability immediately

Supports multiple authentication methods: API Key / Bearer Token / OAuth 2.0 / Basic Auth / No authentication

### Evolution Mechanism

- **Append knowledge** → automatically analyze incremental content → merge without overwriting existing conclusions
- **Conversation correction** → say "they wouldn't say that, they should be like this" → write to Correction layer, takes effect immediately
- **Version management** → automatically archive on each update, supports rollback to any historical version

---

## 📚 Pre-built Roles

> 🎯 **Project Vision**: **Put every role in the world into this repository**. Currently **72** built-in roles, still growing...

This repo already comes with **72 popular roles** ready to use. Clone and invoke directly. You can also use `/create-role` to create more.

### 📖 [View Complete ROLLECALL → ROLLECALL.md](./ROLLECALL.md)

Current statistics:

| Category | Count |
|------|------|
| 🔬 Science & Tech | 15 |
| 👳 Chinese Ancients | 10 |
| 👔 All Professions | 31 |
| 🌟 World Sports | 5 |
| 🎬 Literature & Film | 19 |

**Usage**: After cloning, just invoke by slug in Claude Code:
```
/albert_einstein        # Einstein - full mode
/product_manager         # Product Manager - product Q&A
/confucius               # Confucius - discuss philosophy
```

---

## 🗺️ Project Structure

This project follows the [AgentSkills](https://agentskills.io) open standard, the entire repo is one skill:

```
create-role/
├── SKILL.md              # skill entry (official frontmatter)
├── prompts/              # Prompt templates
│   ├── intake.md         #   conversational info collection
│   ├── knowledge_analyzer.md # domain knowledge extraction
│   ├── persona_analyzer.md    # personality extraction (with tag translation table)
│   ├── knowledge_builder.md   # knowledge.md generation template
│   ├── persona_builder.md     # 5-layer persona template
│   ├── merger.md          # incremental merge logic
│   └── correction_handler.md # conversation correction handling
├── tools/                # Python tools
│   ├── skill_writer.py   # Skill file management
│   ├── version_manager.py # version archive and rollback
│   └── tool_generator.py # automatic tool code generation
├── roles/                # generated role Skills
├── docs/
├── requirements.txt
└── LICENSE
```

---

## 📝 Notes

- **Quality depends on source material**: textbooks/notes > manual description
- We recommend providing: what problems this role solves, what methods they commonly use, what characterizes their speech
- This project generates AI roles based on your description, does not represent real person's views

---

## 🤝 Contributing

Our goal is **put every role in the world into this repository**, we have 72 now and still growing!

All forms of contribution are welcome:

- **👤 Contribute a role**: If you think a role should be here, welcome PR adding it
- **💻 Contribute code**: Improve tools, fix bugs, add features
- **💡 Contribute ideas**: What new feature do you want? open an issue to discuss
- **👥 Invite friends**: Bring your buddies here and create together!

### How to contribute a role

1. Fork this repo
2. Run `/create-role` in Claude Code following prompts to create new role
3. Verify the role works correctly
4. Submit Pull Request
5. After merge, your role will be here for everyone to use!

### Contribution Checklist

- [ ] `native_language` is correctly set in `meta.json`
- [ ] `knowledge.md` and `persona.md` structure is complete
- [ ] `SKILL.md` is correctly generated (automatically when creating)
- [ ] Role can be invoked correctly, format is correct

Looking forward to your PR!

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
