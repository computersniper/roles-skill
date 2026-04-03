---
name: set-translation
description: Set default translation language for group chat. 设置多角色群聊的默认翻译语言。
argument-hint: language
version: 1.0.0
user-invocable: true
allowed-tools: Read, Write
---

# 设置默认翻译语言

用户想要更改多角色群聊的默认翻译语言。

当前设置存储在 `settings.json` 文件中。

## 工作流程

1. 读取用户参数，获取目标语言
2. 如果没有 settings.json，创建它
3. 更新 `group_chat.default_translation_language` 字段
4. 告知用户更改已生效
5. 说明效果：后续群聊翻译都会使用这个语言

## 示例

用户输入：`set-translation 英文`

输出：
```
✅ 默认翻译语言已更改为：英文
后续群聊翻译都会使用英文。
```

现在处理用户请求：`{full_input}`
