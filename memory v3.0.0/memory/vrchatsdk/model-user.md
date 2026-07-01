---
title: "VRChat 数据模型 - User"
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
  - avatar
  - udonsharp
aliases:
  - "VRChat 数据模型 - User"
  - 16_模型_User
related:
  - "tags.md"
  - "api-avatars.md"
  - "api-favorites.md"
  - "model-current-user.md"
  - "typescript-sdk.md"
---
---
source: https://vrchat.hexdocs.pm/VRChat.Model.User.html
date: 2026-06-10
SDK版本: vrchat v1.20.0 (Elixir)
---

# VRChat 数据模型 - User

## 类型定义

```elixir
@type t() :: %VRChat.Model.User{
  # 身份信息
  id: String.t(),
  username: String.t() | nil,        // 已弃用
  displayName: String.t(),

  # 头像信息
  userIcon: String.t(),
  currentAvatarImageUrl: String.t(),
  currentAvatarThumbnailImageUrl: String.t(),
  currentAvatarTags: [String.t()],
  profilePicOverride: String.t(),
  profilePicOverrideThumbnail: String.t(),

  // 状态与位置
  state: UserState.t(),
  status: UserStatus.t(),
  statusDescription: String.t(),
  location: String.t() | nil,
  worldId: String.t() | nil,
  instanceId: String.t() | nil,
  travelingToLocation: String.t() | nil,
  travelingToWorld: String.t() | nil,
  travelingToInstance: String.t() | nil,

  // 平台信息
  platform: String.t() | nil,
  last_platform: String.t(),
  last_login: String.t(),
  last_activity: String.t(),
  last_mobile: String.t() | nil,

  // 用户信息
  bio: String.t(),
  bioLinks: [String.t()],
  pronouns: String.t(),
  tags: [String.t()],
  note: String.t() | nil,
  date_joined: Date.t(),

  // 好友相关
  isFriend: boolean(),
  friendKey: String.t(),
  friendRequestStatus: String.t() | nil,

  // 开发者与验证
  developerType: DeveloperType.t(),
  ageVerified: boolean(),
  ageVerificationStatus: AgeVerificationStatus.t(),

  // 其他
  allowAvatarCopying: boolean(),
  badges: [Badge.t()] | nil
}
```

## UserStatus 枚举

定义用户的当前状态（"ask me"、"join me" 或 "offline"）

## UserState 枚举

用户状态，指示在线活动和隐私偏好

## DeveloperType 枚举

| 值 | 说明 |
|----|------|
| `"none"` | 普通用户 |
| `"trusted"` | 未知 |
| `"internal"` | VRChat 开发者 |
| `"moderator"` | VRChat 主持人 |

**注意**：主持人可以随意隐藏他们的 developerType。