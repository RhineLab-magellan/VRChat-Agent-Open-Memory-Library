---
title: Hybrid Domain — Knowledge Base
category: hybrid

knowledge_level: applied
status: active

tags:
  - misc
  - index
  - navigation

aliases:
  - "Hybrid Domain — Knowledge Base"

related:
  - osc-protocol.md
  - audio-link.md
  - udon-world-plugins.md
  - FACT.md
  - sources/open-source-projects.md
  - api/player-api.md

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
---
# Hybrid Domain — Knowledge Base


---

## 核心文档

| 文档 | 说明 | 来源 |
|------|------|------|
| **[osc-protocol.md](osc-protocol.md)** | OSC 完整协议数据库、消息格式、路由规则 | VRChat 官方文档 |
| **[audio-link.md](audio-link.md)** | 音频同步系统 API 与使用指南、纹理编码数据传递、时间同步 | 源码验证 |
| **[udon-world-plugins.md](udon-world-plugins.md)** ⭐NEW 2026-06-20 | **推荐 Udon 世界插件索引**(创作者安装 / 玩家识别) | 源码验证 + 案例研究 |

---

## 子域

| 子域 | 内容 | 状态 |
|------|------|------|
| **OSC** | Open Sound Control 协议集成 | ✅ 已完成 |
| **音频同步系统(参考工程)** | 音频可视化核心系统架构 + API 使用指南 | ✅ 已完成 |
| **推荐 Udon 世界插件** | 创作者安装的工业级插件索引(TLP UdonVoiceUtils + VizVid VVMW) | ✅ 已完成 (2026-06-20) |
| Avatar↔World | Contact 驱动 World 逻辑 | 待建设 |
| Tracking | VRCPlayerApi 追踪数据交互 | 待建设 |
| External | 第三方系统联动（MIDI, Web, etc.） | 待建设 |

---

## 核心设计模式（已验证）

### 1. Shader-Centric 数据传递
**原理**：高频变化数据编码为纹理，Shader 直接采样，零网络同步开销

### 2. Master 权威时间锚点
**原理**：Master 写入实例加入时间，其他客户端本地计算 elapsed time

### 3. 位域压缩同步
**原理**：单个 byte/bit 字段存储多个布尔值，减少序列化带宽

### 4. 漂移校正算法
**原理**：本地时间与网络时间差值缓慢收敛，避免瞬时抖动

---

## 待收录内容

- Avatar Contact → World UdonBehaviour 通信模式
- 跨域架构设计模式
- 外部系统集成案例（MIDI、Web 等）
- 多机位导演系统(参考工程)中的 Hybrid 模式参考

---

## 相关知识

- `memory/FACT.md` → 核心设计模式 section
- `memory/sources/open-source-projects.md` → 开源参考工程
- `memory/api/player-api.md` → VRCPlayerApi 追踪接口
