# VRCX — VRChat 伴侣应用

> 知识库索引: `sources/vrcx.md`
> 收录日期: 2026-06-11
> 分类: 社区工具 / VRChat API 客户端

---

## 基础信息

| 属性 | 值 |
|------|-----|
| **项目名** | VRCX (VRChat Cross) |
| **GitHub** | github.com/vrcx-team/VRCX |
| **官网** | vrcx.app |
| **Discord** | vrcx.app/discord |
| **语言** | JavaScript (47.1%), Vue (36.2%), C# (13.6%) |
| **许可证** | MIT |
| **Stars** | 1,772 |
| **最新版本** | v2026.05.03 (2026-05-03) |
| **首次发布** | 2019-08-16 |
| **贡献者** | 110 人 |
| **是否合规** | ✅ 不违反 TOS — 仅使用官方 VRChat API |

> ⚠️ **VRCX 不修改游戏**：仅使用 API 负责任地提供功能，不是 mod 或作弊工具。

---

## 核心功能总览

### 1. 社交管理
| 功能 | 说明 |
|------|------|
| 好友/世界/Avatar 列表 | 在 VRChat 外部管理社交列表 |
| 好友状态监控 | 实时追踪好友在线状态、位置、Avatar |
| 好友历史记录 | 记录添加日期、共度时间、昵称变更 |
| 备注/便签 | 记录与好友的相遇方式等备忘信息 |

### 2. 可自定义仪表盘
- 多面板布局（Feed / GameLog / Instance 组件）
- 创建多个仪表盘，每个配置独立的事件过滤器和列可见性

### 3. 搜索功能
- 全局搜索：用户、世界、Avatar、群组
- 粘贴 ID/URL 直接访问
- Quick Search：客户端模糊搜索（好友/Avatar/世界/群组）

### 4. 活动热力图
- 可视化用户在线活动模式（星期 × 小时）
- 显示峰值统计

### 5. 拍照地点记录
- 将世界数据存储在游戏内截图元数据中
- 6 个月后仍能回忆截图地点

### 6. 通知管理
- VRCX 内发送/接收邀请和好友请求
- 查看邀请的实例信息

### 7. 实例信息
- 查看当前实例的统计和玩家列表
- 查看世界中播放的视频链接

### 8. 社交状态预设
- 保存并快速应用状态 + 状态描述组合

### 9. VRChat 服务器状态
- 状态栏指示器
- 登录页警报（实时通知服务器问题/宕机）

### 10. Discord Rich Presence（增强版）
- 显示详细实例信息（世界缩略图、名称、玩家数）
- 公用大厅的加入按钮

### 11. VR Overlay
- 可配置的事件/通知实时馈送
- VR 内可见

### 12. 媒体管理
- 上传和管理 Avatar/世界图片（无需 Unity）

### 13. 自动化
- 启动 VRChat 时自动启动其他应用
- VRC 崩溃后自动重启并加入上一个实例

### 14. 数据导出/导入
- 导出：好友列表、Avatar 列表、Discord 名称、备注、收藏分组
- 导入：收藏分组和群组禁言记录

---

## 主题系统

VRCX 支持自定义主题，可在 GitHub Wiki 查看主题制作指南。

---

## 下载与安装

### Windows
下载最新安装程序：`VRCX_Setup.exe`
- 发布页: github.com/vrcx-team/VRCX/releases/latest
- Beta/Nightly: vrcx.app/github/nightly 或应用内 `Settings → General → Change build`

### macOS / Linux
参考: github.com/vrcx-team/VRCX/wiki/Running-VRCX-on-Linux

---

## 技术架构（推断）

| 层级 | 技术栈 |
|------|--------|
| 前端 | Vue.js (36.2%) |
| 核心逻辑 | JavaScript (47.1%) |
| 原生集成 | C# (.NET) — 用于桌面集成功能 |
| 通信 | VRChat HTTP API（非 UdonSharp） |
| 发布 | Electron 或类似框架（桌面应用） |

**【推断】** VRCX 很可能基于 Electron 构建，因为：
- Vue.js 前端 + JavaScript 核心
- C# 部分用于原生系统集成（.NET/WPF）
- 跨平台支持（Windows/macOS/Linux）

---

## 与 VRChatSDK 的关系

| 维度 | VRChatSDK (HTTP API) | VRCX |
|------|---------------------|------|
| **用途** | 外部应用 / Editor 工具 | 玩家伴侣应用 |
| **目标用户** | 创作者 / 开发者 | 普通玩家 |
| **运行位置** | Unity Editor / 外部脚本 | 独立桌面应用 |
| **功能范围** | 用户/世界/Avatar 数据管理 | 社交/通知/状态/Rich Presence |
| **API 访问** | 直接 HTTP 调用 | 直接 HTTP 调用 |

> **VRCX 是 VRChatSDK HTTP API 最成功的客户端实现之一**，展示了 API 的实际应用场景。

---

## 参考链接

| 资源 | URL |
|------|-----|
| GitHub | github.com/vrcx-team/VRCX |
| 官网 | vrcx.app |
| Discord | vrcx.app/discord |
| 下载 | github.com/vrcx-team/VRCX/releases |
| Nightly | vrcx.app/github/nightly |
| Wiki (Linux) | github.com/vrcx-team/VRCX/wiki/Running-VRCX-on-Linux |
| Wiki (Themes) | github.com/vrcx-team/VRCX/wiki/Themes |
| 构建指南 | github.com/vrcx-team/VRCX/wiki/Building-from-source |

---

## 相关知识库条目

- `memory/vrchatsdk/` — VRChat HTTP API 完整文档（18 个文件）
- `sources/open-source-projects.md` — 开源项目参考（待补充 VRCX）