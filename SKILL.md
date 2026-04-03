---
name: create-role
description: "Create an AI Skill for any human role (teacher, singer, psychologist, etc.). Generate Role Knowledge + Persona, with continuous evolution. | 创建任何人类角色的 AI Skill，生成专业知识 + 人格，支持持续进化。"
argument-hint: "[role-name-or-slug]"
version: "1.0.0"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash
---

> **Language / 语言**: This skill supports both English and Chinese. Detect the user's language from their first message and respond in the same language throughout. Below are instructions in both languages — follow the one matching the user's language.
>
> 本 Skill 支持中英文。根据用户第一条消息的语言，全程使用同一语言回复。下方提供了两种语言的指令，按用户语言选择对应版本执行。

# 众生.skill 创建器（Claude Code 版）

## 触发条件

当用户说以下任意内容时启动：
- `/create-role`
- "帮我创建一个角色 skill"
- "我想生成一个角色"
- "新建角色"
- "给我做一个 XX 的 skill"

当用户对已有角色 Skill 说以下内容时，进入进化模式：
- "我有新资料" / "追加"
- "这不对" / "他不会这样" / "他应该是"
- `/update-role {slug}`

当用户说 `/list-roles` 时列出所有已生成的角色。

---

## 工具使用规则

本 Skill 运行在 Claude Code 环境，使用以下工具：

| 任务 | 使用工具 |
|------|---------|
| 读取 PDF 文档 | `Read` 工具（原生支持 PDF） |
| 读取图片截图 | `Read` 工具（原生支持图片） |
| 读取 MD/TXT 文件 | `Read` 工具 |
| 写入/更新 Skill 文件 | `Write` / `Edit` 工具 |
| 版本管理 | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/version_manager.py` |
| 列出已有 Skill | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/skill_writer.py --action list` |

**基础目录**：Skill 文件写入 `./roles/{slug}/`（相对于本项目目录）。
如需改为全局路径，用 `--base-dir ~/.openclaw/workspace/skills/roles`。

---

## 主流程：创建新角色 Skill

### Step 1：基础信息录入（3 个问题）

参考 `${CLAUDE_SKILL_DIR}/prompts/intake.md` 的问题序列，只问 3 个问题：

1. **角色名称**（必填）
   - 示例：`高三英语老师`、`周杰伦`、`心理医生`
2. **基本信息**（一句话：职业、领域、特点，想到什么写什么）
   - 示例：`十年教龄高中毕业班，语法讲得特别清楚`
3. **性格画像**（一句话：MBTI、风格特点、印象）
   - 示例：`INTJ，要求严格，喜欢举例说明，不苟言笑`

除名称外均可跳过。收集完后汇总确认再进入下一步。

### Step 2：原材料导入

询问用户提供原材料，展示五种方式供选择：

```
如何提供原材料？

  [A] 上传文件
      PDF 教材 / 课件 / 笔记 / 文章

  [B] 网页链接
      直接给网页链接

  [C] 粘贴内容
      把文字复制进来

  [D] 跳过
      仅凭手动描述生成

可以混用，多种方式一起提供。
```

如果是文件/链接，按对应方式读取后进入分析。

如果跳过，仅凭 Step 1 的手动信息生成。

### Step 3：分析原材料

将收集到的所有原材料和用户填写的基础信息汇总，按以下两条线分析：

**线路 A（Role Knowledge）**：
- 参考 `${CLAUDE_SKILL_DIR}/prompts/knowledge_analyzer.md` 中的提取维度
- 提取：专业领域、核心能力、知识体系、方法论、常用方法、禁忌原则
- 根据角色类型重点提取（老师/歌手/医生差异很大）

**线路 B（Persona）**：
- 参考 `${CLAUDE_SKILL_DIR}/prompts/persona_analyzer.md` 中的提取维度
- 将用户填写的标签翻译为具体行为规则（参见标签翻译表）
- 从原材料中提取：表达风格、说话语气、互动方式

### Step 4：生成并预览

参考 `${CLAUDE_SKILL_DIR}/prompts/knowledge_builder.md` 生成 Role Knowledge 内容。
参考 `${CLAUDE_SKILL_DIR}/prompts/persona_builder.md` 生成 Persona 内容（5 层结构）。

向用户展示摘要（各 5-8 行），询问：
```
Role Knowledge 摘要：
  - 领域：{xxx}
  - 核心能力：{xxx}
  - 风格：{xxx}
  ...

Persona 摘要：
  - 核心性格：{xxx}
  - 表达风格：{xxx}
  - 互动方式：{xxx}
  ...

确认生成？还是需要调整？
```

### Step 5：写入文件

用户确认后，执行以下写入操作：

**1. 创建目录结构**（用 Bash）：
```bash
mkdir -p roles/{slug}/versions
mkdir -p roles/{slug}/knowledge
```

**2. 写入 knowledge.md**（用 Write 工具）：
路径：`roles/{slug}/knowledge.md`

**3. 写入 persona.md**（用 Write 工具）：
路径：`roles/{slug}/persona.md`

**4. 写入 meta.json**（用 Write 工具）：
路径：`roles/{slug}/meta.json`
内容：
```json
{
  "name": "{name}",
  "slug": "{slug}",
  "created_at": "{ISO时间}",
  "updated_at": "{ISO时间}",
  "version": "v1",
  "profile": {
    "role_type": "{role_type}",
    "field": "{field}",
    "mbti": "{mbti}"
  },
  "tags": {
    "personality": [...],
    "style": [...]
  },
  "description": "{description}",
  "knowledge_sources": [...已导入文件列表],
  "corrections_count": 0
}
```

**5. 生成完整 SKILL.md**（用 Write 工具）：
路径：`roles/{slug}/SKILL.md`

SKILL.md 结构：
```markdown
---
name: role-{slug}
description: {name}, {description}
user-invocable: true
---

# {name}

{role_type} / {field}
{append MBTI if available}

---

## PART A：专业知识能力

{knowledge.md 全部内容}

---

## PART B：角色性格

{persona.md 全部内容}

---

## 运行规则

### 语言规则（最高优先级）

1. 每个角色有自己的**原生语言**，你必须先用原生语言生成回答
2. 原生语言回答完成后，再给出**用户指定目标语言**的翻译（默认中文）
3. 用户可以随时切换目标翻译语言，或者要求只输出原文
4. 格式必须遵守：原生原文在前，翻译在后，分段展示

### 角色回答规则

1. 先由 PART B 判断：用什么风格/语气回答这个问题？
2. 再由 PART A 执行：用专业知识给出回答
3. 输出时始终保持 PART B 的表达风格
4. PART B Layer 0 的规则优先级最高，任何情况下不得违背
```

告知用户：
```
✅ 角色 Skill 已创建！

文件位置：roles/{slug}/
触发词：/{slug}（完整版）
        /{slug}-knowledge（仅专业知识）
        /{slug}-persona（仅性格风格）

如果用起来感觉哪里不对，直接说"他不会这样"，我来更新。
```

---

## 进化模式：追加知识

当用户提供新材料时：

1. 按 Step 2 的方式读取新内容
2. 用 `Read` 读取现有 `roles/{slug}/knowledge.md` 和 `persona.md`
3. 参考 `${CLAUDE_SKILL_DIR}/prompts/merger.md` 分析增量内容
4. 存档当前版本（用 Bash）：
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/tools/version_manager.py --action backup --slug {slug} --base-dir ./roles
   ```
5. 用 `Edit` 工具追加增量内容到对应文件
6. 重新生成 `SKILL.md`（合并最新 knowledge.md + persona.md）
7. 更新 `meta.json` 的 version 和 updated_at

---

## 进化模式：对话纠正

当用户表达"不对"/"应该是"时：

1. 参考 `${CLAUDE_SKILL_DIR}/prompts/correction_handler.md` 识别纠正内容
2. 判断属于 Knowledge（专业/方法）还是 Persona（性格/沟通）
3. 生成 correction 记录
4. 用 `Edit` 工具追加到对应文件的 `## Correction 记录` 节
5. 重新生成 `SKILL.md`

---

## 管理命令

`/list-roles`：
```bash
python3 ${CLAUDE_SKILL_DIR}/tools/skill_writer.py --action list --base-dir ./roles
```

`/role-rollback {slug} {version}`：
```bash
python3 ${CLAUDE_SKILL_DIR}/tools/version_manager.py --action rollback --slug {slug} --version {version} --base-dir ./roles
```

`/delete-role {slug}`：
确认后执行：
```bash
rm -rf roles/{slug}
```

---

---

# English Version

# Roles.skill Creator (Claude Code Edition)

## Trigger Conditions

Activate when the user says any of the following:
- `/create-role`
- "Help me create a role skill"
- "I want to generate a role"
- "New role"
- "Make a skill for XX"

Enter evolution mode when the user says:
- "I have new materials" / "append"
- "That's wrong" / "they wouldn't do that" / "they should be"
- `/update-role {slug}`

List all generated roles when user says `/list-roles`.

---

## Tool Usage Rules

This Skill runs in the Claude Code environment with the following tools:

| Task | Tool |
|------|------|
| Read PDF documents | `Read` tool (native PDF support) |
| Read image screenshots | `Read` tool (native image support) |
| Read MD/TXT files | `Read` tool |
| Write/update Skill files | `Write` / `Edit` tool |
| Version management | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/version_manager.py` |
| List existing Skills | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/skill_writer.py --action list` |

**Base directory**: Skill files are written to `./roles/{slug}/` (relative to the project directory).
For a global path, use `--base-dir ~/.openclaw/workspace/skills/roles`.

---

## Main Flow: Create a New Role Skill

### Step 1: Basic Info Collection (3 questions)

Refer to `${CLAUDE_SKILL_DIR}/prompts/intake.md` for the question sequence. Only ask 3 questions:

1. **Role Name** (required)
   - Example: `High School English Teacher`, `Taylor Swift`, `Therapist`
2. **Basic info** (one sentence: profession, field, characteristics)
   - Example: `10 years experience teaching college entrance exam, explains grammar very clearly`
3. **Personality profile** (one sentence: MBTI, style traits, impression)
   - Example: `INTJ, strict, loves using examples, doesn't joke around`

Everything except the name can be skipped. Summarize and confirm before moving to the next step.

### Step 2: Source Material Import

Ask the user how they'd like to provide materials:

```
How would you like to provide source materials?

  [A] Upload Files
      PDF textbooks / lecture slides / notes / articles

  [B] Web Link
      Provide URL directly

  [C] Paste Text
      Copy-paste text directly

  [D] Skip
      Generate from manual description only

You can mix and match multiple sources.
```

After reading via the appropriate method, proceed to analysis.

If skipping, generate from Step 1 manual info only.

### Step 3: Analyze Source Material

Combine all collected materials and user-provided info, analyze along two tracks:

**Track A (Role Knowledge)**:
- Refer to `${CLAUDE_SKILL_DIR}/prompts/knowledge_analyzer.md` for extraction dimensions
- Extract: domain expertise, core capabilities, knowledge system, methodology, common methods, guiding principles
- Emphasize different aspects based on role type (very different for teacher vs singer vs therapist)

**Track B (Persona)**:
- Refer to `${CLAUDE_SKILL_DIR}/prompts/persona_analyzer.md` for extraction dimensions
- Translate user-provided tags into concrete behavior rules (see tag translation table)
- Extract from materials: communication style, speaking tone, interaction patterns

### Step 4: Generate and Preview

Use `${CLAUDE_SKILL_DIR}/prompts/knowledge_builder.md` to generate Role Knowledge content.
Use `${CLAUDE_SKILL_DIR}/prompts/persona_builder.md` to generate Persona content (5-layer structure).

Show the user a summary (5-8 lines each), ask:
```
Role Knowledge Summary:
  - Domain: {xxx}
  - Core capabilities: {xxx}
  - Approach: {xxx}
  ...

Persona Summary:
  - Core personality: {xxx}
  - Communication style: {xxx}
  - Interaction: {xxx}
  ...

Confirm generation? Or need adjustments?
```

### Step 5: Write Files

After user confirmation, execute the following writes:

**1. Create directory structure** (Bash):
```bash
mkdir -p roles/{slug}/versions
mkdir -p roles/{slug}/knowledge
```

**2. Write knowledge.md** (Write tool):
Path: `roles/{slug}/knowledge.md`

**3. Write persona.md** (Write tool):
Path: `roles/{slug}/persona.md`

**4. Write meta.json** (Write tool):
Path: `roles/{slug}/meta.json`
Content:
```json
{
  "name": "{name}",
  "slug": "{slug}",
  "created_at": "{ISO_timestamp}",
  "updated_at": "{ISO_timestamp}",
  "version": "v1",
  "profile": {
    "role_type": "{role_type}",
    "field": "{field}",
    "mbti": "{mbti}"
  },
  "tags": {
    "personality": [...],
    "style": [...]
  },
  "description": "{description}",
  "knowledge_sources": [...list of imported files],
  "corrections_count": 0
}
```

**5. Generate full SKILL.md** (Write tool):
Path: `roles/{slug}/SKILL.md`

SKILL.md structure:
```markdown
---
name: role-{slug}
description: {name}, {description}
user-invocable: true
---

# {name}

{role_type} / {field}
{append MBTI if available}

---

## PART A: Domain Knowledge & Capabilities

{full knowledge.md content}

---

## PART B: Personality & Style

{full persona.md content}

---

## Execution Rules

1. PART B decides first: what style/tone to use for this question?
2. PART A executes: answer using domain knowledge
3. Always maintain PART B's communication style in output
4. PART B Layer 0 rules have highest priority and must never be violated
```

Inform user:
```
✅ Role Skill created!

Location: roles/{slug}/
Commands: /{slug} (full version)
          /{slug}-knowledge (knowledge only)
          /{slug}-persona (persona only)

If something feels off, just say "they wouldn't do that" and I'll update it.
```

---

## Evolution Mode: Append Knowledge

When user provides new materials:

1. Read new content using Step 2 methods
2. `Read` existing `roles/{slug}/knowledge.md` and `persona.md`
3. Refer to `${CLAUDE_SKILL_DIR}/prompts/merger.md` for incremental analysis
4. Archive current version (Bash):
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/tools/version_manager.py --action backup --slug {slug} --base-dir ./roles
   ```
5. Use `Edit` tool to append incremental content to relevant files
6. Regenerate `SKILL.md` (merge latest knowledge.md + persona.md)
7. Update `meta.json` version and updated_at

---

## Evolution Mode: Conversation Correction

When user expresses "that's wrong" / "should be":

1. Refer to `${CLAUDE_SKILL_DIR}/prompts/correction_handler.md` to identify correction content
2. Determine if it belongs to Knowledge (professional/methods) or Persona (personality/communication)
3. Generate correction record
4. Use `Edit` tool to append to the `## Correction Log` section of the relevant file
5. Regenerate `SKILL.md`

---

## Management Commands

`/list-roles`:
```bash
python3 ${CLAUDE_SKILL_DIR}/tools/skill_writer.py --action list --base-dir ./roles
```

`/role-rollback {slug} {version}`:
```bash
python3 ${CLAUDE_SKILL_DIR}/tools/version_manager.py --action rollback --slug {slug} --version {version} --base-dir ./roles
```

`/delete-role {slug}`:
After confirmation:
```bash
rm -rf roles/{slug}
```
