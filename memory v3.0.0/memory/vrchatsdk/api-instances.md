---
title: "VRChat API 参考 - 实例模块"
category: vrchatsdk
knowledge_level: applied
status: active
source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
tags:
  - vrchatsdk
  - udonsharp
  - reference
aliases:
  - "VRChat API 参考 - 实例模块"
  - 14_API_实例
related:
  - "api-authentication.md"
  - "api-users.md"
  - "api-worlds.md"
  - "api-friends.md"
  - "api-notifications.md"
---
---
source: https://vrchat.hexdocs.pm/VRChat.Instances.html
date: 2026-06-10
SDK版本: vrchat v1.20.0 (Elixir)
---

# VRChat API 参考 - 实例模块

## 模块概述

API calls for all endpoints tagged `Instances`.

## 函数列表

### get_instance

Get Instance - 返回实例信息

**说明**：如果提供无效的 instanceId，此端点将简单返回 "null"

```elixir
get_instance(connection, world_id, instance_id, opts \\ [])
```

### get_instance_by_short_name

Get Instance By Short Name - 通过短名称返回实例信息

```elixir
get_instance_by_short_name(connection, short_name, opts \\ [])
```

### create_instance

Create Instance - 创建实例

```elixir
create_instance(connection, create_instance_request, opts \\ [])
// body: CreateInstanceRequest
```

### close_instance

Close Instance - 关闭实例或更新关闭时间

**权限要求**：
- ownerId 是你自己，或
- 实例所有者是群组且你有 `group-instance-manage` 权限

```elixir
close_instance(connection, world_id, instance_id, opts \\ [])
// 可选参数:
:hardClose  // 是否硬关闭，默认 false
:closedAt   // 用户不允许加入的时间
```

### get_short_name

Get Instance Short Name - 返回实例短名称

```elixir
get_short_name(connection, world_id, instance_id, opts \\ [])
```