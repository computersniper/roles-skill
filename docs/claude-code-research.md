# Claude Code 源代码研究报告

## 研究概述

本报告深入研究了 D:/study/vibe-coding/reference/claude-code-cli-master/ 目录下的 Claude Code 源代码，重点分析了：
1. 整体架构和 Skill 系统工作原理
2. 输出流程机制
3. 双语输出实现方案

## 1. 整体架构与 Skill 系统

### 1.1 核心架构概览

Claude Code 是一个基于 TypeScript/TSX 的 CLI 应用，使用 **Ink**（React for CLI）作为 UI 框架，**Bun** 作为运行时。

**关键模块**：
- `commands/` - 斜杠命令实现（`/commit`, `/review` 等）
- `skills/` - Skill 系统实现
- `outputStyles/` - 输出样式系统
- `components/` - UI 组件（基于 Ink React）
- `tools/` - 工具实现（Read, Edit, Bash 等）
- `constants/` - 常量定义（包括输出样式、系统提示等）

### 1.2 Skill 系统工作原理

**Skill 加载流程** (`skills/loadSkillsDir.ts:638-804`)：

```
启动 → getSkillDirCommands()
  ├─ 从多个来源并行加载 Skills：
  │   ├─ managedSkills (policySettings)
  │   ├─ userSkills (userSettings)
  │   ├─ projectSkills (projectSettings)
  │   ├─ additionalSkills (--add-dir)
  │   └─ legacyCommands (/commands 目录，已弃用)
  ├─ 去重（通过 realpath 解析文件）
  ├─ 分离条件 Skills (paths 前置) 和无条件 Skills
  └─ 返回无条件 Skills
```

**Skill 类型** (`types/command.ts:25-217`)：

1. **PromptCommand** (`type: 'prompt'`)
   - 基于文本提示的 Skill
   - `getPromptForCommand(args, context)` 返回内容块
   - 可以来自文件系统或 bundled 内置

2. **LocalCommand** (`type: 'local'`)
   - 本地执行的命令
   - 加载模块并调用

3. **LocalJSXCommand** (`type: 'local-jsx'`)
   - 本地执行并渲染 UI 的命令

**Skill 目录结构**：
```
.claude/skills/
└── skill-name/
    └── SKILL.md  (必需，不能是单独的 .md 文件)
```

**Bundled Skills** (`skills/bundledSkills.ts:53-100`)：
- 内置 Skill 通过 `registerBundledSkill()` 注册
- 编译在二进制中，对所有用户可用
- 可以包含附加文件 (`files` 字段)

## 2. Skill 触发后的输出流程

### 2.1 完整流程链

```
用户输入 /skill-name
    ↓
命令检测 (isSlashCommand)
    ↓
Skill 调用
    ↓
getPromptForCommand() 执行
    ↓
返回 ContentBlockParam[] (文本内容块)
    ↓
插入对话历史
    ↓
查询模型 (query.ts)
    ↓
系统提示组装 (constants/prompts.ts)
    ├─ getSimpleIntroSection()
    ├─ getSimpleSystemSection()
    ├─ getSimpleDoingTasksSection()
    ├─ getLanguageSection(settings.language)  ← 语言设置
    ├─ getOutputStyleSection()  ← 输出样式
    └─ ...更多 section
    ↓
模型响应
    ↓
消息渲染 (components/Message.tsx)
    ├─ AssistantTextMessage
    ├─ AssistantToolUseMessage
    └─ ...
```

### 2.2 输出样式系统

**Output Style 定义** (`constants/outputStyles.ts:11-23`)：
```typescript
type OutputStyleConfig = {
  name: string
  description: string
  prompt: string           // 样式提示文本
  source: SettingSource | 'built-in' | 'plugin'
  keepCodingInstructions?: boolean
  forceForPlugin?: boolean
}
```

**内置样式**：
- `default` - 无特殊样式
- `Explanatory` - 提供教育性解释
- `Learning` - 交互式学习模式

**自定义样式**：
- 位置：`.claude/output-styles/*.md` 或 `~/.claude/output-styles/*.md`
- 格式：Markdown 文件，frontmatter 配置

**输出样式集成** (`constants/prompts.ts`)：
```typescript
function getOutputStyleSection(outputStyleConfig): string | null {
  if (outputStyleConfig === null) return null
  return `# Output Style: ${outputStyleConfig.name}
${outputStyleConfig.prompt}`
}
```

### 2.3 语言设置

**语言 Section** (`constants/prompts.ts`)：
```typescript
function getLanguageSection(languagePreference): string | null {
  if (!languagePreference) return null
  return `# Language
Always respond in ${languagePreference}. Use ${languagePreference} for all explanations, comments, and communications with the user. Technical terms and code identifiers should remain in their original form.`
}
```

**语言选择器** (`components/LanguagePicker.tsx`)：
- 用户可通过 `/config` 设置首选语言
- 存储在设置中

## 3. 双语输出可行性分析

### 3.1 可能的方案对比

| 方案 | 修改层面 | 难度 | 灵活性 | 侵入性 |
|-----|---------|------|--------|--------|
| **方案 A: Output Style** | 用户配置 | 低 | 中 | 无 |
| **方案 B: Skill 模板** | Skill 层 | 低 | 高 | 无 |
| **方案 C: 核心代码** | 核心层 | 高 | 最高 | 高 |
| **方案 D: 混合方案** | Skill + Output Style | 中 | 高 | 低 |

## 4. 详细方案设计

### 方案 A: Output Style 实现双语（推荐用于全局效果）

**优点**：
- 无需修改核心代码
- 全局生效
- 用户可切换

**实现方式**：

在 `.claude/output-styles/bilingual.md`：

```markdown
---
name: Bilingual
description: Output in both English and Chinese
keep-coding-instructions: true
---

# Output Style: Bilingual

You must output ALL your responses in TWO languages simultaneously:
1. First in English (primary language)
2. Then in Chinese (translation)

## Format Requirements

For every section of text you output, use this exact format:

```
[English content here]

---

[Chinese content here (中文翻译)]
```

## Specific Rules

1. **Always provide both versions** - never skip one language
2. **Keep the same structure** in both versions (same headings, same bullet points, etc.)
3. **Code blocks only need one version** - put code in the English section, no need to duplicate code
4. **Tool use planning and explanations** - provide both languages
5. **File edits and summaries** - provide both languages

## Example

```
I'll help you implement the user authentication feature. Let me start by examining the current project structure.

---

我来帮你实现用户认证功能。让我先查看当前项目结构。
```

Remember: Always output in both languages, separated by `---` on its own line.
```

### 方案 B: Skill 模板实现双语（推荐用于特定 Skill）

**优点**：
- 精确控制单个 Skill 的输出
- 无需修改核心代码
- Skill 可以自包含双语模板

**实现方式**：

在 `.claude/skills/my-bilingual-skill/SKILL.md`：

```markdown
---
name: my-bilingual-skill
description: A skill that demonstrates bilingual output
when_to_use: When you need to provide bilingual responses
user-invocable: true
---

# My Bilingual Skill

## Skill Purpose
This skill demonstrates how to provide bilingual output.

## Bilingual Output Instructions

YOU MUST OUTPUT IN BOTH ENGLISH AND CHINESE FOR EVERY RESPONSE.

Follow this format strictly:

1. First, write everything in English
2. Then, write a separator line: `---`
3. Then, write everything in Chinese

### Example Output:

```
Let me help you with this task. First, I'll examine the files.

---

让我帮你完成这个任务。首先，我会查看相关文件。
```

## Your Task

[Insert your actual skill task here]

[Rest of your skill prompt...]
```

### 方案 C: 核心代码修改（不推荐，除非需要深度集成）

**需要修改的文件**：
- `constants/prompts.ts` - 添加新的双语 Section
- `constants/outputStyles.ts` - 可添加内置双语样式
- `components/Message.tsx` - 可添加渲染时的双语格式识别

**优点**：
- 可以实现最深度的集成
- 可以支持切换功能

**缺点**：
- 需要维护 fork
- 升级困难
- 侵入性强

## 5. Skill 层 vs 核心代码控制能力

| 能力 | Skill 层 | Output Style | 核心代码 |
|-----|---------|-------------|---------|
| 控制输出格式 | ✓ | ✓ | ✓ |
| 全局生效 | ✗ | ✓ | ✓ |
| 单个 Skill 生效 | ✓ | ✗ | ✓ |
| 渲染层控制 | ✗ | ✗ | ✓ |
| 无需修改代码 | ✓ | ✓ | ✗ |
| 用户可配置 | ✓ | ✓ | ✗ |
| 复杂逻辑 | ✓ | ✗ | ✓ |

## 6. 最佳实践方案建议

### 推荐方案：混合方案（Skill + Output Style）

**架构**：
```
用户层
  ├─ /config output-style bilingual  ← 全局切换
  └─ /my-bilingual-skill             ← 特定 Skill 使用

实现层
  ├─ .claude/output-styles/bilingual.md  ← 全局双语样式
  └─ .claude/skills/xxx/SKILL.md         ← 可包含双语指令
```

**分步实施**：

**第一步：创建双语 Output Style**

```
.claude/output-styles/
└── bilingual.md
```

**第二步：创建双语 Skill 模板示例**

```
.claude/skills/
└── bilingual-demo/
    └── SKILL.md
```

**第三步：使用指南**

用户可以：
1. 全局启用：`/config output-style bilingual`
2. 或者单独使用双语 Skill：`/bilingual-demo`

## 7. 关键发现总结

1. **Skill 系统完全基于提示词** - Skill 本质是动态插入的提示模板
2. **Output Style 也是提示词** - 通过 system prompt section 工作
3. **无需修改核心代码** - 所有输出控制都可通过提示工程实现
4. **语言设置已有框架** - `getLanguageSection()` 已存在，可扩展
5. **渲染层是纯展示** - Markdown 组件直接渲染模型输出

## 8. 文件速查表

| 功能 | 文件路径 | 说明 |
|-----|---------|-----|
| Skill 加载 | `skills/loadSkillsDir.ts` | 从目录加载 Skill |
| 内置 Skill 注册 | `skills/bundledSkills.ts` | registerBundledSkill |
| Command 类型 | `types/command.ts` | PromptCommand/LocalCommand |
| 系统提示 | `constants/prompts.ts` | getSystemPromptSections |
| 输出样式 | `constants/outputStyles.ts` | OutputStyleConfig |
| 消息渲染 | `components/Message.tsx` | 主要消息组件 |
| 语言选择 | `components/LanguagePicker.tsx` | 语言设置 UI |
| 查询逻辑 | `query.ts` | 模型查询主循环 |

---

**结论**：在不修改核心代码的情况下，完全可以通过 **Output Style + Skill 模板** 的组合实现双语输出功能。推荐采用这种非侵入式方案。
