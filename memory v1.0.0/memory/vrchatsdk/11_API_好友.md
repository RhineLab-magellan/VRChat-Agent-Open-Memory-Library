---
source: https://vrchat.hexdocs.pm/VRChat.Friends.html
date: 2026-06-10
SDK版本: vrchat v1.20.0 (Elixir)
---

# VRChat API 参考 - 好友模块

## 模块概述

API calls for all endpoints tagged `Friends`.

## 函数列表

### get_friends

List Friends - 列出好友信息

```elixir
get_friends(connection, opts \\ [])
// 可选参数:
:offset     // 分页偏移
:n          // 返回数量
:offline    // true: 仅离线用户, false: 仅在线/活跃用户
```

### get_friend_status

Check Friend Status - 检查与用户的好友关系状态

**说明**：检查用户是否是好友、是否有发出的好友请求、是否有收到的好友请求

**正确接收和接受好友请求的方式**：
1. 检查是否有类型为 `friendRequest` 的传入 `Notification`
2. 然后接受该通知

```elixir
get_friend_status(connection, user_id, opts \\ [])
```

### friend

Send Friend Request - 发送好友请求

```elixir
friend(connection, user_id, opts \\ [])
```

### delete_friend_request

Delete Friend Request - 删除发出的待处理好友请求

**注意**：要删除收到的请求，请使用 `deleteNotification` 端点

```elixir
delete_friend_request(connection, user_id, opts \\ [])
```

### unfriend

Unfriend - 解除好友关系

```elixir
unfriend(connection, user_id, opts \\ [])
```