# Example Central

> 来源: VRChat 官方文档 (creators.vrchat.com/sdk/example-central/)
> 置信度: High
> SDK: 3.7.2+
> Last Updated: 2026-06-10

---

## Overview

Example Central 是 VRChat SDK 内置的示例中心，提供可浏览、下载和修改的示例项目，用于学习和实践 VRChat 开发。

---

## 访问方式

```
Unity Editor Menu → VRChat SDK → 🏠 Example Central
```

---

## 界面结构

### 左侧面板: 示例列表
- 可浏览和选择示例
- 支持搜索和标签过滤

### 右侧面板: 示例详情
- 缩略图
- 标题和版本
- 标签
- 描述
- 指南链接
- 示例场景

---

## 示例功能

### Version Tracking (语义版本)
```
Major.Minor.Patch
- Major: 重大变更，可能需要重新实现
- Minor: 新功能，向后兼容
- Patch: 修复和改进
```

⚠️ **限制**: 导入后无法查看示例版本，目前没有机制检查是否使用最新版本。

### Documentation Guides
每个示例包含详细文档：
- 示例用途
- 工作原理
- 自行实现方法
- 重要代码概念和组件

### 跨平台支持
大多数示例标注支持的平台（PC/Android/iOS）。

---

## 设置

点击 ⚙️ 图标打开设置：
- **Show Creator Economy Examples**: 默认为关闭（Beta 功能）
  - 需要 Beta tester 权限才能正常工作

---

## 示例分类

### World Examples
- 含发布的世界 ID
- 可直接在 VRChat 中体验

### Avatar Examples
- Avatar 相关示例
- 可能包含示例 Avatar 资源

### Creator Economy Examples (Beta)
- 需要特殊权限
- 商店、订阅等产品示例

---

## 常用示例列表

| 示例 | 说明 |
|------|------|
| Udon Example Scene | Udon 基础示例 |
| Minimap | VRCGraphics.Blit 使用示例 |
| Persistence Examples | PlayerData/PlayerObject 示例 |
| Video Player | 视频播放系统 |
| Image Loading | 图片加载 |
| Creator Economy SDK | 创作者经济集成 |

---

## 导入流程

1. 从列表中选择示例
2. 点击 "Import" 按钮
3. UnityPackage 导入到项目
4. (可选) 点击 "Docs" 查看详细文档

---

## VCC Package 管理

Example Central 示例通过 VRChat Package Manager (VPM) 分发：

```
Unity Editor Menu → VRChat SDK → Manage Packages
```

### 添加新包
1. 选择项目
2. 点击版本旁边的 "+" 或 "Latest Version"
3. 自动安装最新版本

### 更新包
1. 检测可用更新
2. 点击 "Latest Version" 下载

---

## 相关文档

- `memory/sources/official-docs.md` - 官方文档入口
- `memory/world/media-systems.md` - 媒体系统（视频/图片）
- `memory/api/persistence.md` - 持久化系统
- `memory/world/clientsim/index.md` - ClientSim 使用文档(World 调试工具)