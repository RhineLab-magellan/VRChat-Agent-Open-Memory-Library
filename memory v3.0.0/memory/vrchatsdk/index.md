---
title: "VRChatSDK 知识库索引"
category: vrchatsdk
knowledge_level: applied
status: active
source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
tags:
  - misc
  - index
  - navigation
aliases:
  - "VRChatSDK 知识库索引"
  - index
related:
  - homepage.md
  - typescript-sdk.md
  - websocket-api.md
  - instances.md
  - tags.md
  - faq.md
  - api-authentication.md
  - api-users.md
  - api-worlds.md
  - api-avatars.md
  - api-friends.md
  - api-notifications.md
  - api-favorites.md
  - api-instances.md
  - api-files.md
---
# VRChatSDK 知识库索引

**Domain**: VRChatSDK (HTTP API / 外部应用)
**Type**: External Integration
**本地化日期**: 2026-06-10
**文件数**: 18

---

## 概述

**重要**: VRChatSDK 与 UdonSharp **不在同一阶层**
- **UdonSharp**: 在 VRChat **游戏内** 的 Udon VM 上运行
- **VRChatSDK**: 在 **VRChat 外**(外部应用、Editor 工具)与 VRChat 服务器通信

**VRChatSDK** 是 VRChat 提供的 **HTTP API + WebSocket**,允许外部应用、Unity Editor 工具、第三方服务与 VRChat 服务器通信。


| 维度 | UdonSharp | VRChatSDK |
|------|-----------|-----------|
| 运行位置 | VRChat 客户端 Udon VM | 外部应用 / Editor / 服务器 |
| 通信对象 | 世界内其他玩家 | VRChat 服务器 API |
| 功能范围 | 游戏逻辑、网络同步、UI 交互 | 用户数据、世界数据、文件管理、实时事件 |
| 延迟 | 游戏内实时(~50-200ms)| HTTP 请求(~100-500ms)|

---

## 文档分类

### 总览与多语言支持(2)

| 文档 | 说明 |
|------|------|
| [homepage.md](homepage.md) | 层级概览 + 数据源说明 |
| [typescript-sdk.md](typescript-sdk.md) | SDK 多语言支持(JavaScript/Python/.NET/Dart/Java/Rust/Elixir)|

### 实时与实例(3)

| 文档 | 说明 |
|------|------|
| [websocket-api.md](websocket-api.md) | WebSocket 实时事件订阅(friend-online, notification, user-update)|
| [instances.md](instances.md) | 实例查询、创建、关闭 |
| [tags.md](tags.md) | 标签系统 |

### FAQ(1)

| 文档 | 说明 |
|------|------|
| [faq.md](faq.md) | 常见问题 |

### API 端点(11)

| 文档 | 端点类别 | 说明 |
|------|---------|------|
| [api-authentication.md](api-authentication.md) | Authentication | 登录/登出/2FA |
| [api-users.md](api-users.md) | Users | 用户查询/更新/标签 |
| [api-worlds.md](api-worlds.md) | Worlds | 世界 CRUD/发布/搜索 |
| [api-avatars.md](api-avatars.md) | Avatars | Avatar CRUD/切换 |
| [api-friends.md](api-friends.md) | Friends | 好友列表/请求 |
| [api-notifications.md](api-notifications.md) | Notifications | 通知管理 |
| [api-favorites.md](api-favorites.md) | Favorites | 收藏分组管理 |
| [api-instances.md](api-instances.md) | Instances | 实例查询/创建/关闭 |
| [api-files.md](api-files.md) | Files | 文件上传/下载/分析 |
| [api-groups.md](api-groups.md) | Groups | 群组完整管理 |

### 数据模型(2)

| 文档 | 模型 | 说明 |
|------|------|------|
| [model-user.md](model-user.md) | User | 公开用户数据结构 |
| [model-current-user.md](model-current-user.md) | CurrentUser | 当前登录用户扩展数据 |

---

## 重要限制

| 限制 | 说明 |
|------|------|
| **会话限制** | 每次登录凭据认证算作一个会话,数量有限。生产环境务必保存并重用 auth cookie |
| **限流(429)** | 必须实现指数退避(1s → 2s → 4s → ...)|
| **非官方 API** | VRChat 不官方支持此 API,端点可能随时变更 |
| **滥用后果** | 可能导致账户终止 |

---

## SDK 多语言支持

| 语言 | 安装命令 / 包 |
|------|--------------|
| **JavaScript** | `npm install vrchat`(vrchat.js)|
| **Python** | `pip install vrchat` |
| **.NET** | `dotnet add package VRChat.API |
| **Dart** | pub: `vrchat` |
| **Java** | Maven / Gradle |
| **Rust** | crates.io: `vrchat` |
| **Elixir** | Hex: `vrchat`(v1.20.0)|

---

## 使用场景

| 场景 | 端点 |
|------|------|
| **World Manager 工具** | Worlds / Instances / 发布流程 |
| **Avatar 批量审核** | Avatars / Tags |
| **Bot / 通知系统** | WebSocket / Notifications |
| **第三方客户端** | Users / Friends / Auth |
| **群组管理工具** | Groups |

---

## 与其他知识库的关系

- **`hybrid/osc-protocol.md`**:OSC 协议(游戏内外部通信,**不同协议**)
- **`hybrid/audio-link.md`**:AudioLink 音频系统
- **`world/creator-economy.md`**:VRChat 创作者经济(SDK 内 Store/Product API)
- **`FACT.md`**:VRChatSDK 与 UdonSharp 区别

---

## 数据来源

| 来源 | 类型 | 备注 |
|------|------|------|
| [vrchat.community](https://vrchat.community) | 社区维护 | 非官方 |
| [vrchat.hexdocs.pm](https://vrchat.hexdocs.pm) | 官方 Elixir SDK | v1.20.0 |
| [VRChat API Docs](https://hello.vrchat.com/) | 官方主页 | 入门 |

---