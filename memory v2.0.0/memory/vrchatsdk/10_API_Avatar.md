---
title: VRChat API 参考 - Avatar 模块
category: vrchatsdk

knowledge_level: applied
status: active

tags:
  - vrchatsdk
  - avatar
  - udonsharp

aliases:
  - "VRChat API 参考 - Avatar 模块"

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
---
---
source: https://vrchat.hexdocs.pm/VRChat.Avatars.html
date: 2026-06-10
SDK版本: vrchat v1.20.0 (Elixir)
---

# VRChat API 参考 - Avatar 模块

## 模块概述

API calls for all endpoints tagged `Avatars`.

## 函数列表

### get_avatar

Get Avatar - 获取特定 Avatar 的信息

```elixir
get_avatar(connection, avatar_id, opts \\ [])
```

### get_own_avatar

Get Own Avatar - 获取用户的当前 Avatar

**限制**：只能获取登录用户自己的当前 Avatar

```elixir
get_own_avatar(connection, user_id, opts \\ [])
```

### search_avatars

Search Avatars - 搜索和列出 Avatar

**限制**：只能搜索自己的或精选的 Avatar。普通用户无法搜索其他人的 Avatar。

```elixir
search_avatars(connection, opts \\ [])
// 可选参数:
:n, :offset, :tag, :notag
:releaseStatus, :maxUnityVersion, :minUnityVersion, :platform
:featured, :sort, :order
:user (设为 "me" 搜索自己的 Avatar)
:userId
```

### get_favorited_avatars

List Favorited Avatars - 搜索和列出收藏的 Avatar

```elixir
get_favorited_avatars(connection, opts \\ [])
// 可选: :userId (admin-only)
```

### get_licensed_avatars

List Licensed Avatars - 列出授权的 Avatar

```elixir
get_licensed_avatars(connection, opts \\ [])
// 可选: :n, :offset
```

### create_avatar

Create Avatar - 创建 Avatar

**注意**：可以可选指定 ID。尝试创建已使用的 ID 会导致数据库错误。

```elixir
create_avatar(connection, opts \\ [])
// 可选: :body (CreateAvatarRequest)
```

### update_avatar

Update Avatar - 更新特定 Avatar 的信息

```elixir
update_avatar(connection, avatar_id, opts \\ [])
// 可选: :body (UpdateAvatarRequest)
```

### delete_avatar

Delete Avatar - 删除 Avatar

**注意**：Avatar 永远不会真正"删除"，只是 `ReleaseStatus` 设为 `"hidden"` 且链接的文件被删除。AvatarID 永久保留。

```elixir
delete_avatar(connection, avatar_id, opts \\ [])
```

### select_avatar

Select Avatar - 切换到该 Avatar

```elixir
select_avatar(connection, avatar_id, opts \\ [])
```

### select_fallback_avatar

Select Fallback Avatar - 切换到该 Avatar 作为备用 Avatar

```elixir
select_fallback_avatar(connection, avatar_id, opts \\ [])
```

### Impostor 相关

| 函数 | 说明 |
|------|------|
| `enqueue_impostor` | 排队生成该 Avatar 的 Impostor |
| `delete_impostor` | 删除生成的 Impostor |
| `get_impostor_queue_stats` | 获取排队 Impostor 的服务统计 |