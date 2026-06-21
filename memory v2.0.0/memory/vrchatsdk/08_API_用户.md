---
title: VRChat API 参考 - 用户模块
category: vrchatsdk

knowledge_level: applied
status: active

tags:
  - vrchatsdk
  - udonsharp
  - reference

aliases:
  - "VRChat API 参考 - 用户模块"

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
---
---
source: https://vrchat.hexdocs.pm/VRChat.Users.html
date: 2026-06-10
SDK版本: vrchat v1.20.0 (Elixir)
---

# VRChat API 参考 - 用户模块

## 模块概述

API calls for all endpoints tagged `Users`.

## 函数列表

### get_user

Get User by ID - 使用 ID 获取用户的公开信息

```elixir
get_user(connection, user_id, opts \\ [])
```

### get_user_by_name

Get User by Username - 使用用户名获取用户信息

**已弃用**：VRChat API 不再返回其他用户的用户名。此端点现在需要 Admin Credentials。

```elixir
get_user_by_name(connection, username, opts \\ [])
```

### search_users

Search All Users - 按文本查询搜索和列出用户

```elixir
search_users(connection, opts \\ [])
// 可选: :search (displayName), :developerType, :n, :offset
```

### update_user

Update User Info - 更新用户信息（邮箱、生日等）

```elixir
update_user(connection, user_id, opts \\ [])
// 可选: :body (UpdateUserRequest)
```

### get_user_groups

Get User Groups - 获取用户的公开群组

```elixir
get_user_groups(connection, user_id, opts \\ [])
```

### get_user_group_instances

Get User Group Instances - 返回用户的群组实例列表

```elixir
get_user_group_instances(connection, user_id, opts \\ [])
```

### get_user_group_requests

Get User Group Requests - 返回用户请求加入的群组列表

```elixir
get_user_group_requests(connection, user_id, opts \\ [])
```

### get_user_represented_group

Get user's current represented group - 返回用户当前代表的群组

```elixir
get_user_represented_group(connection, user_id, opts \\ [])
```

### add_tags / remove_tags

Add/Remove User Tags - 添加/移除用户标签

```elixir
add_tags(connection, user_id, change_user_tags_request, opts \\ [])
remove_tags(connection, user_id, change_user_tags_request, opts \\ [])
```

### update_badge

Update User Badge - 更新用户徽章

```elixir
update_badge(connection, user_id, badge_id, update_user_badge_request, opts \\ [])
```

### get_user_notes / update_user_note

用户笔记管理

```elixir
get_user_notes(connection, opts \\ [])  // 可选: :n, :offset
get_user_note(connection, user_note_id, opts \\ [])
update_user_note(connection, update_user_note_request, opts \\ [])
```

### get_user_feedback

Get User Feedback - 获取用户提交的反馈

```elixir
get_user_feedback(connection, user_id, opts \\ [])
// 可选: :contentId, :n, :offset
```

### 持久化数据管理

| 函数 | 说明 |
|------|------|
| `check_user_persistence_exists` | 检查用户是否有指定世界的持久化数据 |
| `delete_user_persistence` | 删除用户在指定世界的持久化数据 |