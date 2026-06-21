---
title: VRChat 数据模型 - CurrentUser
category: vrchatsdk

knowledge_level: applied
status: active

tags:
  - vrchatsdk
  - avatar
  - udonsharp

aliases:
  - "VRChat 数据模型 - CurrentUser"

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
---
---
source: https://vrchat.hexdocs.pm/VRChat.Model.CurrentUser.html
date: 2026-06-10
SDK版本: vrchat v1.20.0 (Elixir)
---

# VRChat 数据模型 - CurrentUser

## 类型定义

```elixir
@type t() :: %VRChat.Model.CurrentUser{
  # 身份信息
  id: String.t(),
  username: String.t() | nil,
  displayName: String.t(),

  # 头像信息
  currentAvatar: String.t(),
  currentAvatarImageUrl: String.t(),
  currentAvatarThumbnailImageUrl: String.t(),
  currentAvatarTags: [String.t()],
  fallbackAvatar: String.t() | nil,
  userIcon: String.t(),
  profilePicOverride: String.t(),
  profilePicOverrideThumbnail: String.t(),

  // 状态与位置
  state: UserState.t(),
  status: UserStatus.t(),
  statusDescription: String.t(),
  homeLocation: String.t(),
  queuedInstance: String.t() | nil,
  presence: CurrentUserPresence.t() | nil,

  // 平台信息
  platform_history: [CurrentUserPlatformHistoryInner.t()] | nil,
  last_login: DateTime.t(),
  last_activity: DateTime.t() | nil,
  last_platform: String.t(),
  last_mobile: DateTime.t() | nil,

  // 用户信息
  bio: String.t(),
  bioLinks: [String.t()],
  pronouns: String.t(),
  tags: [String.t()],
  date_joined: Date.t(),
  pastDisplayNames: [PastDisplayName.t()],
  contentFilters: [String.t()] | nil,

  // 账户信息
  emailVerified: boolean(),
  hasEmail: boolean(),
  hasPendingEmail: boolean(),
  obfuscatedEmail: String.t(),
  obfuscatedPendingEmail: String.t(),
  hasBirthday: boolean(),
  isAdult: boolean(),
  unsubscribe: boolean(),

  // 账户安全
  acceptedTOSVersion: integer(),
  acceptedPrivacyVersion: integer() | nil,
  twoFactorAuthEnabled: boolean(),
  twoFactorAuthEnabledDate: DateTime.t() | nil,

  // 账户删除
  accountDeletionDate: Date.t() | nil,
  accountDeletionLog: [AccountDeletionLog.t()] | nil,

  // 好友相关
  isFriend: boolean(),
  friends: [String.t()],
  activeFriends: [String.t()] | nil,
  offlineFriends: [String.t()] | nil,
  onlineFriends: [String.t()] | nil,
  friendKey: String.t(),
  friendGroupNames: [String.t()],

  // 开发者与验证
  developerType: DeveloperType.t(),
  ageVerified: boolean(),
  ageVerificationStatus: AgeVerificationStatus.t(),

  // 语言设置
  userLanguage: String.t() | nil,
  userLanguageCode: String.t() | nil,

  // 其他
  allowAvatarCopying: boolean(),
  badges: [Badge.t()] | nil,
  statusFirstTime: boolean(),
  statusHistory: [String.t()],

  // 第三方账户
  steamId: String.t(),
  steamDetails: map(),
  oculusId: String.t(),
  picoId: String.t() | nil,
  viveId: String.t() | nil,
  googleId: String.t() | nil,
  googleDetails: map() | nil,

  // 客户端信息
  hasLoggedInFromClient: boolean(),
  receiveMobileInvitations: boolean() | nil,
  isBoopingEnabled: boolean() | nil,
  hideContentFilterSettings: boolean() | nil,

  // 认证
  authToken: String.t() | nil,

  // 更新时间
  updated_at: DateTime.t() | nil
}
```

## 与 User 模型的差异

CurrentUser 包含更多敏感信息和账户特定数据：

| 字段 | User | CurrentUser |
|------|------|-------------|
| currentAvatar | ❌ | ✅ |
| fallbackAvatar | ❌ | ✅ |
| homeLocation | ❌ | ✅ |
| friends | ❌ | ✅ |
| emailVerified | ❌ | ✅ |
| twoFactorAuthEnabled | ❌ | ✅ |
| authToken | ❌ | ✅ |
| friendKey | ✅ | ✅ |
| statusHistory | ❌ | ✅ |