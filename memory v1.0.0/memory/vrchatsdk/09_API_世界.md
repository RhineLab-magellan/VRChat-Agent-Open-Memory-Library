---
source: https://vrchat.hexdocs.pm/VRChat.Worlds.html
date: 2026-06-10
SDK版本: vrchat v1.20.0 (Elixir)
---

# VRChat API 参考 - 世界模块

## 模块概述

API calls for all endpoints tagged `Worlds`.

## 函数列表

### get_world

Get World by ID - 获取特定世界的详细信息

**注意**：未认证时也能工作，但某些字段始终返回 `0`

```elixir
get_world(connection, world_id, opts \\ [])
```

### get_world_instance

Get World Instance - 返回世界的实例信息

```elixir
get_world_instance(connection, world_id, instance_id, opts \\ [])
```

### search_worlds

Search All Worlds - 搜索和列出世界

```elixir
search_worlds(connection, opts \\ [])
// 可选参数:
:n, :offset, :search, :tag, :notag
:releaseStatus, :maxUnityVersion, :minUnityVersion, :platform
:featured, :sort, :order, :user (设为 "me" 搜索自己的世界)
:userId, :fuzzy
```

### get_active_worlds

List Active Worlds - 搜索和列出当前活跃的世界

```elixir
get_active_worlds(connection, opts \\ [])
// 可选参数同上
```

### get_favorited_worlds

List Favorited Worlds - 搜索和列出收藏的世界

```elixir
get_favorited_worlds(connection, opts \\ [])
// 可选: :userId (admin-only)
```

### get_recent_worlds

List Recent Worlds - 搜索和列出最近访问的世界

```elixir
get_recent_worlds(connection, opts \\ [])
// 可选: :userId (admin-only)
```

### create_world

Create World - 创建新世界

**要求**：
- `assetUrl` 必须是 `.vrcw` 文件扩展名的有效 File 对象
- `imageUrl` 必须是有效图片文件扩展名的 File 对象

```elixir
create_world(connection, opts \\ [])
// 可选: :body (CreateWorldRequest)
```

### update_world

Update World - 更新特定世界的信息

```elixir
update_world(connection, world_id, opts \\ [])
// 可选: :body (UpdateWorldRequest)
```

### delete_world

Delete World - 删除世界

**注意**：世界永远不会真正"删除"，只是 `ReleaseStatus` 设为 `"hidden"` 且链接的文件被删除。WorldID 永久保留。

```elixir
delete_world(connection, world_id, opts \\ [])
```

### publish_world

Publish World - 发布世界

**限制**：每周只能发布一个世界

```elixir
publish_world(connection, world_id, opts \\ [])
```

### unpublish_world

Unpublish World - 取消发布世界

```elixir
unpublish_world(connection, world_id, opts \\ [])
```

### get_world_publish_status

Get World Publish Status - 返回世界的发布状态

```elixir
get_world_publish_status(connection, world_id, opts \\ [])
```

### get_world_metadata

Get World Metadata - 返回世界的自定义元数据

**注意**：据信目前未使用。元数据可通过 `updateWorld` 设置，可以是任意对象。

```elixir
get_world_metadata(connection, world_id, opts \\ [])
```

### 持久化数据管理

| 函数 | 说明 |
|------|------|
| `check_user_persistence_exists` | 检查用户是否有指定世界的持久化数据 |
| `delete_user_persistence` | 删除用户在指定世界的持久化数据 |