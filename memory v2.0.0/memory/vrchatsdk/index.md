---
title: VRChatSDK 知识库索引
category: vrchatsdk

knowledge_level: applied
status: active

tags:
  - misc
  - index
  - navigation

aliases:
  - "VRChatSDK 知识库索引"

related:
  - 01_首页.md
  - 02_TypeScript_SDK.md
  - 03_Websocket_API.md
  - 04_Instances.md
  - 05_Tags.md
  - 06_FAQ.md
  - 07_API_认证.md
  - 08_API_用户.md
  - 09_API_世界.md
  - 10_API_Avatar.md
  - 11_API_好友.md
  - 12_API_通知.md
  - 13_API_收藏.md
  - 14_API_实例.md
  - 15_API_文件.md

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
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
| [01_首页.md](01_首页.md) | 层级概览 + 数据源说明 |
| [02_TypeScript_SDK.md](02_TypeScript_SDK.md) | SDK 多语言支持(JavaScript/Python/.NET/Dart/Java/Rust/Elixir)|

### 实时与实例(3)

| 文档 | 说明 |
|------|------|
| [03_Websocket_API.md](03_Websocket_API.md) | WebSocket 实时事件订阅(friend-online, notification, user-update)|
| [04_Instances.md](04_Instances.md) | 实例查询、创建、关闭 |
| [05_Tags.md](05_Tags.md) | 标签系统 |

### FAQ(1)

| 文档 | 说明 |
|------|------|
| [06_FAQ.md](06_FAQ.md) | 常见问题 |

### API 端点(11)

| 文档 | 端点类别 | 说明 |
|------|---------|------|
| [07_API_认证.md](07_API_认证.md) | Authentication | 登录/登出/2FA |
| [08_API_用户.md](08_API_用户.md) | Users | 用户查询/更新/标签 |
| [09_API_世界.md](09_API_世界.md) | Worlds | 世界 CRUD/发布/搜索 |
| [10_API_Avatar.md](10_API_Avatar.md) | Avatars | Avatar CRUD/切换 |
| [11_API_好友.md](11_API_好友.md) | Friends | 好友列表/请求 |
| [12_API_通知.md](12_API_通知.md) | Notifications | 通知管理 |
| [13_API_收藏.md](13_API_收藏.md) | Favorites | 收藏分组管理 |
| [14_API_实例.md](14_API_实例.md) | Instances | 实例查询/创建/关闭 |
| [15_API_文件.md](15_API_文件.md) | Files | 文件上传/下载/分析 |
| [18_API_群组.md](18_API_群组.md) | Groups | 群组完整管理 |

### 数据模型(2)

| 文档 | 模型 | 说明 |
|------|------|------|
| [16_模型_User.md](16_模型_User.md) | User | 公开用户数据结构 |
| [17_模型_CurrentUser.md](17_模型_CurrentUser.md) | CurrentUser | 当前登录用户扩展数据 |

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