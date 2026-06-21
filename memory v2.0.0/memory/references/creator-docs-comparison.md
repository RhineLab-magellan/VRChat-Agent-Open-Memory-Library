---
title: VRChat Creator Docs 对比记录
category: references

knowledge_level: applied
status: active

tags:
  - references
  - shader
  - physbone
  - networking
  - sync
  - audio

aliases:
  - "VRChat Creator Docs 对比记录"

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
---
# VRChat Creator Docs 对比记录

> 来源: https://deepwiki.com/vrchat-community/creator-docs
> 索引日期: 2026-06-04 (commit 8be404)
> 原始文档: https://github.com/vrchat-community/creator-docs

---

## 待用户判定的冲突项

### 1. Avatar 性能排名 - PhysBone 元件数定义

**官方文档描述**:
| Metric | Excellent | Good | Medium | Poor |
| --- | --- | --- | --- | --- |
| PhysBones Affected Transforms | 16 | 64 | 128 | 256 |

**当前知识库记录** (`memory/avatar/performance-rank.md`):
| 指标 | Excellent | Good | Medium | Poor |
|------|-----------|------|--------|------|
| **PB 影响骨头数** | 16 | 64 | 128 | 256 |

✅ **一致** - 无冲突

---

### 2. VRCShader.SetGlobal 属性前缀要求

**官方文档描述**:
> Note that the property name must be prefixed with "_Udon", or be the literal string "_AudioTexture" in order to be used with VRCShader.SetGlobal

**当前知识库**: 
- 知识库中未记录此限制
- 建议：添加此限制到 `VRCGraphics` 相关文档

---

### 3. Networking Specs 带宽限制

**官方文档描述**:
- Udon scripts 可发送约 **11 KB/s**
- Manual sync 限制约 **280,496 bytes/serialization**
- Continuous sync 限制约 **200 bytes/serialization**

**当前知识库**:
- `memory/api/networking.md` 未记录这些具体数值
- 需要更新

---

### 4. [NetworkCallable] 版本要求

**官方文档描述**:
> [NetworkCallable] was introduced in SDK 3.8.1

**当前知识库**:
- FACT.md 记录了带参网络同步语法
- 未记录版本要求

---

### 5. Persistence 压缩行为

**官方文档描述**:
> VRChat stores User Data in a compressed format. If your world's data is easy to compress, you may be able to store more than 300 KB (compressed into 100 KB by VRChat).

**当前知识库** (`memory/api/persistence.md`):
- 记录了 100KB per player per world 限制
- 未记录压缩行为和 300KB 原始数据上限

---

## 新增内容（知识库未覆盖）

### 1. VRCGraphics / VRCShader API
- `VRCGraphics.Blit()` - Quest GPU 特殊要求（ZTest Always 或关闭 depth）
- `VRCShader.PropertyToID()` - 必须使用 `_Udon` 前缀
- `VRCShader.SetGlobal()` - 全局着色器变量设置

### 2. Shader Globals
- `_VRChatCameraMode` - 0=正常, 1=VR手持相机, 2=Desktop手持相机, 3=截图
- `_VRChatMirrorMode` - 0=正常, 1=VR镜子, 2=Desktop镜子
- `_VRChatFaceMirrorMode` - 面部镜子
- `_VRChatMirrorCameraPos` - 镜子相机世界坐标
- `_VRChatScreenCameraPos` / `_VRChatPhotoCameraPos` - 屏幕/照片相机位置
- `_VRChatScreenCameraRot` / `_VRChatPhotoCameraRot` - 屏幕/照片相机旋转

### 3. Data Containers
- VRCJson 序列化/反序列化 API
- Data Lists / Data Dictionaries / Data Tokens
- JSON 同步方法（通过字符串序列化）

### 4. Example Central
- 内置示例中心，Unity Menu: VRChat SDK > Example Central
- Semantic Versioning 版本管理
- 标签过滤系统
- Creator Economy examples (Beta)

### 5. Creator Economy SDK
- Store API: OpenWorldStore, OpenListing, OpenGroupPage
- Product API: DoesPlayerOwnProduct, GetPlayersWhoOwnProduct
- 事件: OnPurchaseConfirmed, OnPurchaseExpired

### 6. Cross-Platform Development
- Android 与 PC avatar 必须保持相同 armature 路径
- root bone (Hips) 的 scale 和 rotation 必须相同
- 平台切换: Unity Build Settings > Android

### 7. Mobile UI Optimization
- VRC_UIShape component 配置 Canvas
- "Focus View" 功能允许用户缩放 UI
- OnScreenUpdateEvent 获取屏幕方向和分辨率
- 屏幕空间 UI 优于世界空间 UI

---

## 知识库完整性评估

| 领域 | 知识库覆盖 | 新增需求 |
|------|----------|---------|
| Networking (基本) | ✅ 完整 | - |
| Networking (Specs) | ⚠️ 缺失具体数值 | 需要更新 |
| Persistence (基本) | ✅ 完整 | - |
| Persistence (压缩) | ❌ 未记录 | 需要新增 |
| Avatar Performance | ✅ 完整 | - |
| VRCGraphics | ❌ 未记录 | 需要新增 |
| Data Containers | ❌ 未记录 | 需要新增 |
| Example Central | ❌ 未记录 | 需要新增 |
| Creator Economy | ❌ 未记录 | 需要新增 |
| Cross-Platform | ⚠️ 部分 | 需要更新 |
| Mobile UI | ❌ 未记录 | 需要新增 |

---

## 后续行动

- [x] 用户确认冲突项后更新知识库
- [x] 创建新知识库文件补充缺失内容
- [x] 更新 FACT.md 添加新参考工程

---

## 完成状态 ✅

### 已创建文件
| 文件 | 状态 |
|------|------|
| `参考文献/creator-docs-对比记录.md` | ✅ 已创建 |
| `memory/world/udon/vrc-graphics/index.md` | ✅ 已创建 |
| `memory/world/data-containers.md` | ✅ 已创建 |
| `memory/world/creator-economy.md` | ✅ 已创建 |
| `memory/platform/android-development.md` | ✅ 已创建 |
| `memory/platform/cross-platform-content.md` | ✅ 已创建 |
| `memory/platform/mobile-ui-optimization.md` | ✅ 已创建 |
| `memory/sources/example-central.md` | ✅ 已创建 |

### 已更新文件
| 文件 | 更新内容 |
|------|---------|
| `memory/api/networking.md` | 带宽限制 + [NetworkCallable] |
| `memory/api/persistence.md` | 压缩行为 |
| `memory/FACT.md` | 新增工程记录 |
| `memory/index.md` | 新增入口 + 文件清单 |

### 无冲突项
检查后未发现与现有知识库的实质性冲突。所有差异已记录为新增内容而非冲突。