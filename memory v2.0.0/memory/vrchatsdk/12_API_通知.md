---
title: VRChat API 参考 - 通知模块
category: vrchatsdk

knowledge_level: applied
status: active

tags:
  - vrchatsdk
  - udonsharp
  - reference

aliases:
  - "VRChat API 参考 - 通知模块"

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
---
---
source: https://vrchat.hexdocs.pm/VRChat.Notifications.html
date: 2026-06-10
SDK版本: vrchat v1.20.0 (Elixir)
---

# VRChat API 参考 - 通知模块

## 模块概述

API calls for all endpoints tagged `Notifications`.

## 函数列表

### get_notifications

List Notifications - 获取当前用户的所有通知

```elixir
get_notifications(connection, opts \\ [])
// 可选参数:
:type      // 已弃用，不再起作用
:sent      // 返回用户发送的通知，必须为 false 或省略
:hidden    // true 仅允许在 type 为 friendRequest 时
:after     // 仅返回此日期后发送的通知（type 为 friendRequest 时忽略）
:n         // 返回数量
:offset    // 分页偏移
```

### get_notification

Show notification - 通过通知 ID 获取通知

```elixir
get_notification(connection, notification_id, opts \\ [])
```

### accept_friend_request

Accept Friend Request - 通过通知 `frq_` ID 接受好友请求

**说明**：好友请求可通过 `getNotifications` 过滤 `type=friendRequest` 找到

```elixir
accept_friend_request(connection, notification_id, opts \\ [])
```

### mark_notification_as_read

Mark Notification As Read - 标记通知为已读

```elixir
mark_notification_as_read(connection, notification_id, opts \\ [])
```

### delete_notification

Delete Notification - 删除通知

```elixir
delete_notification(connection, notification_id, opts \\ [])
```

### clear_notifications

Clear All Notifications - 清除**所有**通知

```elixir
clear_notifications(connection, opts \\ [])
```