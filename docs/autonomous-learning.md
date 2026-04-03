# 角色自主技能学习功能设计

## 功能概述

每个角色根据自身身份，**自主学习如何使用外部工具/API** 扩展能力。用户只需要提供 API 配置，角色自己研究使用方法。

**示例场景：**
- 歌手角色 → 想要唱歌 → 自主学习如何调用音乐生成大模型 API 生成歌声
- 画家角色 → 想要画画 → 自主学习如何调用图像生成 API 作画
- 摄影师角色 → 想要修图 → 自主学习如何调用图像编辑 API
- 厨师角色 → 想要找菜谱 → 自主学习如何调用菜谱搜索 API
- 程序员角色 → 想要分析代码 → 自主学习如何调用代码审查 API

## 设计理念

**核心思想**：角色不是静态的，它知道自己能做什么，想要做到什么，当有工具可用时，它会**主动学习如何使用**。

这使得角色真正"活"起来：它会根据自己的身份和需求，主动扩展能力边界。

## 数据结构设计

### 1. meta.json 新增字段

```json
{
  "name": "周杰伦",
  "slug": "jay_chou",
  ...
  "capabilities": {
    "tools": [
      {
        "name": "text-to-music",
        "description": "生成歌曲音乐",
        "provider": "suno",
        "required_config": ["api_key", "base_url"],
        "status": "needs_config"  // needs_config | configured | learning | ready
      }
    ],
    "autonomous_learning": true,
    "learning_history": [
      {
        "tool": "text-to-music",
        "learned_at": "2026-04-04T00:00:00Z",
        "notes": "学会了如何调用 API 生成歌词和旋律"
      }
    ]
  },
  "user_provided_config": {
    "text-to-music": {
      "api_key": "user-provided-key",
      "base_url": "https://api.suno.ai"
    }
  }
}
```

### 字段说明：

| 字段 | 说明 |
|------|------|
| `capabilities.tools[]` | 该角色需要/可以使用的工具列表 |
| `capabilities.tools[].name` | 工具名称 |
| `capabilities.tools[].description` | 工具用途描述 |
| `capabilities.tools[].provider` | 服务商 |
| `capabilities.tools[].required_config` | 需要哪些配置项 |
| `capabilities.tools[].status` | 当前状态：需要配置 → 已配置 → 学习中 → 就绪 |
| `capabilities.autonomous_learning` | 是否开启自主学习 |
| `capabilities.learning_history[]` | 学习历史记录 |
| `user_provided_config` | 用户提供的 API 配置 |

### 2. knowledge.md 新增章节

```markdown
## 工具与能力扩展

### 原生能力
- 作词作曲
- 唱歌
- 聊音乐

### 可扩展工具
- `text-to-music` - AI 音乐生成
- `image-generation` - 专辑封面设计

### 自主学习状态
- text-to-music: `ready` - 已学会调用 API
```

## 工作流程设计

### 流程：用户提供 API → 角色自主学习 → 开始使用

```
用户：我给你添加了 Suno API，key 是 xxx，地址是 yyy
    ↓
系统：读取 user_provided_config 保存配置
    ↓
角色：阅读 API 文档（如果用户提供）→ 理解认证方式 → 理解请求格式 → 学习如何调用 → 记录学习笔记 → 更新 status → ready
    ↓
用户：帮我写一首关于爱情的中国风歌曲
    ↓
角色：根据需求构建 API 请求 → 调用工具 → 获取结果 → 呈现给用户
```

### 触发命令

**新增命令：** `/configure-tool {role-slug} {tool-name}`

```
/configure-tool jay_chou text-to-music
> API key: xxx
> Base URL: https://api.suno.ai
```

**学习命令：** `/learn-tool {role-slug} {tool-name}`

角色会：
1. 重新阅读 API 文档
2. 总结调用方法
3. 测试理解是否正确
4. 更新学习笔记

## 提示词设计

### 在角色 SKILL.md 中新增规则

```
## 工具使用规则

1. **自主学习原则**
   - 你知道自己身份和能力边界，当有工具可以帮助你更好完成工作时，你应该主动学习使用它
   - 用户提供 API 配置后，你要自己研究如何调用，不需要用户教你每一步
   - 如果 API 认证失败或格式错误，你要尝试调试修正

2. **用户提供配置**
   - 用户只需要给你 API key 和地址
   - 剩下的认证方式、请求格式、错误处理，你自己摸索

3. **调用规则**
   - 使用 Claude Code 的 `Bash` 工具调用 API
   - 按照 API 要求构造请求
   - 获取结果后整理呈现

## 自主学习流程

当用户给你配置了新工具：
1. 阅读 API 文档（如果提供）
2. 理解认证方式（Bearer token? API key in query?）
3. 理解请求格式（JSON body? form data?）
4. 做一个简单测试调用
5. 记录学习笔记
6. 告诉你学会了，可以开始用了
```

### 系统提示注入

每次角色回答前，系统提示会加入：
```
你是 {role_name}, 你有这些工具可用：{tools list}
你已经学会如何使用这些工具，遇到需要工具的场景主动调用。
```

## 用户交互设计

### 1. 用户触发配置

```
/configure-tool jay_chou text-to-music
API key: sk-xxx
Base URL: https://api.suno.ai
```

### 2. 角色自主学习

角色会：
- 保存配置到 `meta.json`
- 分析这个 API 是做什么的
- 研究认证方式
- 尝试理解请求格式
- 写下学习笔记
- 告诉你"我学会了，现在可以帮你生成歌曲了"

### 3. 使用工具

用户："帮我写一首关于春天的歌"

角色：
- 构建符合 API 要求的请求
- 使用 `Bash curl` 调用 API
- 获取返回结果
- 整理结果给用户

### 4. 遇到错误

如果 API 返回错误：
- 角色自己阅读错误信息
- 尝试修正请求格式
- 重试
- 如果还是错，告诉你问题在哪里，需要你修正配置

## 优点分析

1. **真正自主** - 角色根据自身需求主动学习，不是用户手把手教
2. **极度灵活** - 任何 API 都可以接入，不限定服务商
3. **无需框架修改** - 纯提示层实现，不需要修改 Claude Code 核心
4. **持续进化** - 角色可以不断学习新工具，能力越来越强
5. **用户友好** - 用户只需要给 API key，剩下的角色搞定

## 贡献邀请设计

在 README 末尾添加"欢迎贡献"章节：

```markdown
## 🤝 欢迎贡献

我们的目标是**把全世界所有角色都装进这个仓库**，现在已有 {N} 个，还在不断增加中！

欢迎各种形式的贡献：

- **贡献角色**：如果你觉得某个角色应该在这里，欢迎 PR 添加
- **贡献代码**：改进工具、修复 bug、添加功能
- **贡献想法**：你想要什么新功能？欢迎开 issue 讨论
- **邀请好友**：拉上你的好兄弟们一起来创造角色！

### 如何贡献角色

1. Fork 这个仓库
2. 创建新角色：`/create-role` 按照提示创建
3. 提交 PR
4. 合并后你的角色就出现在仓库里了，所有人都能用！

### 贡献指南

请确保：
- `native_language` 设置正确
- `knowledge.md` 和 `persona.md` 结构完整
- 所有文件都按照模板生成
- 能正常工作

期待你的 PR！
```

## 总结

这个设计实现了"角色自主学习新技能"的愿景：

✅ 角色根据自身身份主动识别需要什么工具
✅ 用户只需要提供 API 配置，不需要教使用方法
✅ 角色自主研究 API 调用方法，自己调试
✅ 学会之后就能持续使用，能力持续进化
✅ 纯 Skill 层实现，不需要修改 Claude Code 核心
✅ 完全开放，欢迎所有人贡献角色和代码
