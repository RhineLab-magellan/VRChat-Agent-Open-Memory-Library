---
title: VRChat API 参考 - 收藏模块
category: vrchatsdk

knowledge_level: applied
status: active

tags:
  - vrchatsdk
  - avatar
  - udonsharp

aliases:
  - "VRChat API 参考 - 收藏模块"

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
---
---
source: https://vrchat.hexdocs.pm/VRChat.Favorites.html
date: 2026-06-10
SDK版本: vrchat v1.20.0 (Elixir)
---

# VRChat API 参考 - 收藏模块

## 模块概述

API calls for all endpoints tagged `Favorites`.

## 收藏组类型

| 类型 | 组名格式 |
|------|----------|
| 好友 | `group_0` 到 `group_3` |
| Avatar | `avatars1` 到 `avatars4` |
| World | `worlds1` 到 `worlds4` |

**限制**：无法将非好友添加为收藏。删除好友关系会同时从双方移除收藏。

## 函数列表

### get_favorites

List Favorites - 返回收藏列表

```elixir
get_favorites(connection, opts \\ [])
// 可选参数:
:n      // 返回数量
:offset // 分页偏移
:type   // 收藏类型 (FavoriteType)
:tag    // 标签过滤
```

### get_favorite_groups

List Favorite Groups - 返回用户拥有的收藏组列表

```elixir
get_favorite_groups(connection, opts \\ [])
// 可选参数:
:n, :offset, :userId (admin-only), :ownerId
```

### get_favorite_group

Show Favorite Group - 获取特定收藏组的信息

```elixir
get_favorite_group(connection, favorite_group_type, favorite_group_name, user_id, opts \\ [])
```

### add_favorite

Add Favorite - 添加新收藏

```elixir
add_favorite(connection, opts \\ [])
// 可选: :body (AddFavoriteRequest)
```

### remove_favorite

Remove Favorite - 从收藏列表中移除收藏

```elixir
remove_favorite(connection, favorite_id, opts \\ [])
```

### update_favorite_group

Update Favorite Group - 更新特定收藏组的信息

```elixir
update_favorite_group(connection, favorite_group_type, favorite_group_name, user_id, opts \\ [])
// 可选: :body (UpdateFavoriteGroupRequest)
```

### clear_favorite_group

Clear Favorite Group - 清除特定收藏组的**所有**内容

```elixir
clear_favorite_group(connection, favorite_group_type, favorite_group_name, user_id, opts \\ [])
```

### get_favorite_limits

Get Favorite Limits - 返回收藏限制信息

```elixir
get_favorite_limits(connection, opts \\ [])
```