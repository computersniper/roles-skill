---
name: add-role
description: Add a new role to the current group chat. 添加角色到当前多角色群聊。
argument-hint: role-slug
version: 1.0.0
user-invocable: true
allowed-tools: Read
---

# 添加角色到群聊

用户想要添加一个新角色到当前进行中的多角色群聊。

## 工作流程

1. 检查角色 slug 是否存在：`roles/{slug}/meta.json`
2. 如果不存在：告知用户，列出可用角色让用户选择
3. 如果存在：读取角色信息（meta + knowledge + persona）
4. 告知用户角色已添加，请继续讨论，新角色会在接下来的发言中参与讨论

## 输出格式

成功示例：
```
✅ 角色「{name}」已添加到群聊。
下次发言他就会参与讨论了。
```

现在处理用户请求：`{full_input}`
