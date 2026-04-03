# Roles-Skill 原生语言 + 翻译系统设计方案

## 概述

为 roles-skill 项目设计原生语言 + 翻译系统，使每个角色都能用自己的"母语"表达，同时提供同声传译效果。

## 设计目标

1. 每个角色有自己的**原生语言**（比如：梅西 → 西班牙语，孔子 → 古汉语/文言文，爱因斯坦 → 德语，莎士比亚 → 古英语）
2. 输出时，**原生原文 + 用户设置的翻译语言 同时输出**，就像同声传译
3. 用户可以设置目标翻译语言（默认中文）

---

## 1. meta.json 新增字段

在 `meta.json` 中添加以下字段来定义角色的语言属性：

```json
{
  "name": "孔子",
  "slug": "confucius",
  "created_at": "2026-04-04T00:00:00Z",
  "updated_at": "2026-04-04T00:00:00Z",
  "version": "v1",
  "profile": {
    "role_type": "哲学家、教育家",
    "field": "伦理学、教育",
    "mbti": "INFJ",
    "native_language": "文言文",
    "native_language_code": "lzh"
  },
  "language_settings": {
    "default_translation_language": "中文",
    "default_translation_language_code": "zh-CN",
    "supported_translation_languages": ["中文", "英文", "日文", "韩文"]
  },
  "tags": {
    "personality": ["温和", "坚定", "好学", "谦逊", "有教无类"],
    "style": ["循循善诱", "重视礼仪", "言传身教", "因材施教"]
  },
  "description": "中国古代伟大的思想家、教育家，儒家学派创始人，倡导仁、义、礼、智、信，强调个人修养和社会伦理",
  "knowledge_sources": [],
  "corrections_count": 0
}
```

### 字段说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `profile.native_language` | string | 角色的原生语言名称 | "文言文", "德语", "古英语" |
| `profile.native_language_code` | string | ISO 639-3 语言代码 | "lzh", "deu", "enm" |
| `language_settings.default_translation_language` | string | 默认翻译语言 | "中文" |
| `language_settings.default_translation_language_code` | string | 默认翻译语言代码 | "zh-CN" |
| `language_settings.supported_translation_languages` | string[] | 支持的翻译语言列表 | ["中文", "英文"] |

---

## 2. SKILL.md 新增运行规则

在 `SKILL.md` 的 **运行规则** 部分新增以下规则：

```markdown
## 运行规则

### 语言输出规则（新增）

1. **原生语言优先**：
   - 首先用角色的原生语言（`profile.native_language`）生成回答
   - 确保原生语言的表达符合角色的时代背景和身份特点
   - 例如：孔子用文言文，莎士比亚用古英语，爱因斯坦用德语

2. **同声传译输出格式**：
   - 输出时采用「原生原文 + 翻译」的同声传译格式
   - 默认翻译为用户设置的目标语言（`language_settings.default_translation_language`）
   - 支持用户临时切换翻译语言（如："用英文翻译"）

3. **翻译语言设置**：
   - 用户可以通过 `/set-language {lang}` 命令设置全局翻译语言
   - 支持语言：中文（zh-CN）、英文（en-US）、日文（ja-JP）、韩文（ko-KR）
   - 未设置时默认使用 `language_settings.default_translation_language`

### 现有规则（保留）

1. 先由 PART B 判断：用什么风格/语气回答这个问题？
2. 再由 PART A 执行：用专业知识给出回答
3. 输出时始终保持 PART B 的表达风格
4. PART B Layer 0 的规则优先级最高，任何情况下不得违背
```

---

## 3. persona.md 中语言规则的位置

在 `persona.md` 的 **Layer 2: Communication Style** 部分添加语言相关规则：

```markdown
## Layer 2: Communication Style

### 语言风格（新增子节）

- **原生语言**：文言文
- **语言特点**：简洁凝练，常用警句格言，引用经典文献（如《诗经》《尚书》）
- **表达习惯**：使用"子曰"、"诗云"等句式，注重礼仪和道德教化
- **翻译原则**：翻译时保留原文韵味，避免过于现代化的表达

### 沟通风格（保留）

- 说话简洁而意味深长，常用警句格言
- 善于用日常事物打比方，"近取譬"，从身边小事说起
- 语气温和而庄重，既有威严又不失亲切
- 常以"吾闻之"、"诗云"等方式引用古人言语
- 避免长篇大论，点到为止，让听者自己体会
- 喜欢用问句引导对方思考，而非直接给出答案
```

### 语言规则位置总结

| 文件 | 位置 | 内容 |
|------|------|------|
| persona.md | Layer 2: Communication Style | 新增"语言风格"子节 |
| knowledge.md | 新增"语言知识"节 | 原生语言特点、翻译策略 |

---

## 4. knowledge.md 新增内容

在 `knowledge.md` 中添加语言相关的知识：

```markdown
## 语言知识（新增节）

### 原生语言特点

- **语言体系**：文言文（Classical Chinese）
- **语法特点**：省略主语、宾语，常用虚词，注重对仗和节奏
- **常用词汇**：仁、义、礼、智、信、忠、孝、悌
- **引用文献**：《诗经》《尚书》《易经》《礼记》《春秋》

### 翻译策略（新增节）

- **翻译原则**：信达雅兼顾，保留原文的文化内涵
- **难点处理**：对于古代典故和概念（如"仁"、"义"），需添加必要的解释
- **语气调整**：根据目标语言的表达习惯调整语气，但保留角色的身份特点
```

---

## 5. 完整的数据结构和 Prompt 规则

### 数据结构总结

```javascript
// 角色语言属性数据结构
{
  profile: {
    native_language: string,        // 原生语言名称
    native_language_code: string    // 语言代码（用于翻译 API）
  },
  language_settings: {
    default_translation_language: string,        // 默认翻译语言
    default_translation_language_code: string,    // 默认翻译语言代码
    supported_translation_languages: string[]    // 支持的翻译语言列表
  },
  // 其他现有字段...
}
```

### Prompt 规则设计

在生成角色回答时的 Prompt 规则：

```
你现在要扮演 {role_name}，你的原生语言是 {native_language}。

要求：
1. 首先用 {native_language} 生成回答
2. 确保语言风格符合角色的身份和时代背景
3. 然后将回答翻译成 {target_language}
4. 输出格式：
   【原生语言】: {native_response}
   【{target_language}】: {translated_response}

回答内容要求：
- 符合 Layer 0 硬规则
- 体现 Layer 1-4 的性格特点
- 专业知识来自 PART A
```

---

## 6. 输出格式示例

### 示例 1：孔子回答问题

**用户问题**："什么是仁？"

**输出格式**：

```markdown
【文言文】: 樊迟问仁。子曰："爱人。" 问知。子曰："知人。" 樊迟未达。子曰："举直错诸枉，能使枉者直。"

【中文翻译】: 樊迟问什么是仁。孔子说："爱人。" 樊迟又问什么是智。孔子说："了解人。" 樊迟还不明白。孔子说："选拔正直的人，罢黜邪恶的人，这样就能使邪恶的人变得正直。"
```

### 示例 2：莎士比亚回答问题

**用户问题**："什么是爱情？"

**输出格式**：

```markdown
【古英语】: Love is not love
Which alters when it alteration finds,
Or bends with the remover to remove:
O no! it is an ever-fixed mark
That looks on tempests and is never shaken;
It is the star to every wandering bark,
Whose worth's unknown, although his height be taken.

【中文翻译】: 爱不是爱
若是遇到变化就改变，
或是被移除就屈服：
哦不！爱是永恒的标记
它注视着暴风雨，却永远不会动摇；
它是每艘漂泊船只的星星，
它的价值无人知晓，尽管它的高度已被测量。
```

### 示例 3：爱因斯坦回答问题

**用户问题**："什么是相对论？"

**输出格式**：

```markdown
【德语】: Die Relativitätstheorie besteht aus zwei Teilen: der speziellen und der allgemeinen Relativitätstheorie. Die spezielle Relativitätstheorie handelt von Raum und Zeit bei konstanter Geschwindigkeit, während die allgemeine Relativitätstheorie Gravitation als Krümmung von Raum-Zeit durch Materie und Energie beschreibt. Ein einfaches Beispiel: Wenn du dich in einem beschleunigten Fahrstuhl befindest, kannst du die Gravitationskraft nicht von der Beschleunigung unterscheiden.

【中文翻译】: 相对论由两部分组成：狭义相对论和广义相对论。狭义相对论研究匀速运动时的时空，而广义相对论将引力描述为时空因物质和能量而弯曲。一个简单的例子：如果你在一个加速的电梯里，你无法区分引力和加速度。
```

### 示例 4：苏格拉底回答问题

**用户问题**："什么是智慧？"

**输出格式**：

```markdown
【古希腊语】: Ὁ οἶδα ὅτι οὐδὲν οἶδα. Αὕτη ἡ σοφία μου ἐστίν. Ὁ γὰρ ἄλλος οἴεται εἰδέναι τι, οὐκ εἰδώς, ἐγὼ δέ, ὥσπερ οὐκ οἶδα, οὕτως οὐδὲ οἴομαι. Τοῦτο ἄρα ἐσμὲ καὶ σμικρῷ τινι τούτῳ σοφώτεροί εἰμεν, ὅτι τὰ μὴ εἰδότα οὐδὲ οἰόμεθα εἰδέναι.

【中文翻译】: 我知道我一无所知。这就是我的智慧所在。因为别人以为自己知道一些其实并不知道的事情，而我既然不知道，就不认为自己知道。在这一点上，我确实比他们稍微聪明一点：凡是我不知道的事情，我就不认为自己知道。
```

---

## 7. 系统架构建议

### 新增组件

#### 1. 语言检测模块
- 检测用户的语言偏好
- 支持临时切换翻译语言

#### 2. 翻译模块
- 集成翻译 API（如 OpenAI, Google, DeepL）
- 支持多语言翻译

#### 3. 语言风格适配器
- 确保原生语言输出符合角色的身份特点
- 处理古代语言（文言文、古英语等）的特殊表达

#### 4. 配置管理
- 存储用户的语言偏好设置
- 支持 `/set-language` 命令

### 工作流程

```
用户提问 → 语言检测 → 角色原生语言生成 → 风格适配 → 翻译 → 同声传译输出
```

---

## 8. 扩展建议

### 1. 支持更多语言
- 增加对法语、德语、俄语、阿拉伯语等的支持

### 2. 方言和时代语言
- 支持地区方言（如粤语、四川话）
- 更精细的时代语言（如明清白话、中世纪拉丁语）

### 3. 语音合成
- 结合 TTS 技术实现语音输出
- 支持角色原声（如卓别林的伦敦口音）

### 4. 文化背景注释
- 为古代语言或生僻词汇添加注释
- 解释文化典故和历史背景

---

## 附录：常用语言代码参考

### 原生语言代码（ISO 639-3）

| 语言 | 代码 | 适用角色示例 |
|------|------|--------------|
| 文言文 | lzh | 孔子、李白、苏轼 |
| 古英语 | enm | 莎士比亚 |
| 德语 | deu | 爱因斯坦、贝多芬、康德 |
| 法语 | fra | 伏尔泰、拿破仑、德彪西 |
| 西班牙语 | spa | 毕加索、弗里达、加西亚·马尔克斯 |
| 意大利语 | ita | 达芬奇、米开朗基罗、伽利略 |
| 古希腊语 | grc | 苏格拉底、柏拉图、亚里士多德 |
| 日语 | jpn | 黑泽明、村上春树、宫本武藏 |
| 俄语 | rus | 托尔斯泰、柴可夫斯基、普希金 |

### 翻译语言代码（ISO 639-1）

| 语言 | 代码 |
|------|------|
| 中文（简体） | zh-CN |
| 英文 | en-US |
| 日文 | ja-JP |
| 韩文 | ko-KR |
| 法语 | fr-FR |
| 德语 | de-DE |
| 西班牙语 | es-ES |
| 俄语 | ru-RU |

---

## 总结

本设计方案完整地满足了以下需求：

1. ✅ 每个角色有自己的原生语言定义
2. ✅ 原生原文 + 翻译同声传译输出
3. ✅ 用户可以设置目标翻译语言
4. ✅ meta.json 新增字段设计完成
5. ✅ SKILL.md 新增运行规则设计完成
6. ✅ knowledge.md 和 persona.md 新增内容设计完成
7. ✅ 完整的数据结构和输出格式示例
