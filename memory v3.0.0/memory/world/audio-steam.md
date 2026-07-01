---
title: Steam Audio 默认音频空间化 (2025.4.2+)
category: world

knowledge_level: applied
status: active

tags:
  - audio
  - steam-audio
  - onsp
  - spatialization
  - migration
  - 2025

aliases:
  - Steam Audio
  - "Steam Audio 空间化"
  - ONSP 替代
  - "Audio Spatializer"

related:
  - udon/world-debug-views.md
  - whitelisted-world-components.md
  - supported-assets.md
  - ../patterns/unorthodox-patterns.md

source: VRChat 2025.4.2 / 2025.4.2p1 / 2025.4.2 Open Beta Release Notes
source_type: official
version: 1.0
last_review: 2026-06-30
confidence: High
---

# Steam Audio 默认音频空间化 (2025.4.2+)

> **🔴 重大变更**:2025.4.2 起,VRChat **全面替代 ONSP** 为 Steam Audio,作为所有平台(PC/Quest/Android/iOS)的默认音频空间化器。
>
> **影响范围**:所有 `VRC_SpatialAudioSource` 组件、所有 `AudioSource` 的 3D 行为、Voice 音量滑块范围。

---

## 1. 上线时间线

| 版本 | 变更 |
|------|------|
| 2025.4.2 Open Beta | Steam Audio 公开测试 |
| 2025.4.2 正式 | **正式上线**,全面替代 ONSP |
| 2025.4.2p1 | 重大修复:Mono 扬声器、Doppler、Audio from Camera、ILD Nudging、近场缩放 |
| 2025.4.2p1 起 | 服务端音频微调系统启用 |

> **设计动机**(来自官方):
> - 摆脱 ONSP 工程瓶颈与跨平台不一致
> - 在拥挤实例中表现更好
> - 灵活,允许创作者调优
> - 为未来创作者功能开路

---

## 2. ⚠️ Voice 音量滑块范围变更(必读)

> **🔴 关键警告**:Steam Audio 改变了 **Voice 音量滑块**的范围。

| 系统 | 100% 滑块值 | 等价于旧系统 |
|------|------------|-------------|
| **ONSP(旧)** | 100% = 100% | 100% |
| **Steam Audio(新)** | 100% = 约 150% 旧值 | ⚠️ **65%** |

**实际影响**(2025.4.2p1 官方警告原文):
> "We have heard some feedback that people set it right back to 100% - this will now be *very loud*! For comparison, 100% on the old audio system is now approximately 65%."

**用户行动**:
1. 更新到 2025.4.2p1 后,Voice 滑块保持原值
2. 实际感受太响 → 调到约 65%
3. 实际感受太轻 → 调到约 150% (最大)

**创作者行动**:
- 教学用户调整 Voice 滑块
- 检查 World 内语音相关功能是否仍然舒适

---

## 3. 2025.4.2p1 关键修复

### 3.1 已修复问题

| 问题 | 修复内容 |
|------|----------|
| **部分 Mono 扬声器设置** | 空间化(包括语音)失效 → ✅ 已修复 |
| **Doppler 错误启用** | 没有适当 VRC 组件的 AudioSource 错误启用 Doppler → ✅ 已修复 |
| **"Audio from Camera" 模式** | 空间化失效(Stream Mode + Drone FPV) → ✅ 已修复 |
| **视角修正** | 即使在 VR 中也基于相机输出尺寸适配(非视口) → ✅ 已修复 |
| **聊天通知音量** | 异常 → ✅ 已修复 |
| **语音音频衰减/压缩** | 重新调音 → ✅ 已应用更多调优 |
| **ILD Nudging(左右耳分离)** | 改善近场音频立体声分离 → ✅ 已改进 |
| **近场缩放** | 基于 Avatar 眼睛高度调整 → ✅ 已改进 |
| **额外增益** | 非常近距离时减少 → ✅ 已降低 |

### 3.2 服务端音频微调系统(新增)

> **2025.4.2p1 引入**:
> "We have added a system that allows us to tweak some parts of the audio experience server-side, without needing a new update."

- **影响**:玩家可能听到"微妙变化",无需客户端更新
- **追踪**:官方根据社区反馈持续微调
- **创作者影响**:音频行为可能随时间微变

---

## 4. 调试工具:Audio Sources 页面

> **新增** Debug 页面(2025.4.2)。

### 4.1 访问方式

1. Quick Menu → Settings 标签 → 底部 **"Toggle Debug UI"** 按钮
2. 启用 World Debugging 权限(或自有 World)
3. 找到 **"Audio Sources"** 标签

> 也可使用旧路径:`RShift-Tilde-0`(`VRC_UiShape` debugger)

### 4.2 显示字段

详见 `memory/world/udon/world-debug-views.md` §2.6 Audio Sources 章节:

| 字段 | 含义 |
|------|------|
| **VRC/SAS** | 是否有 `VRC_SpatialAudioSource`,**是否转换为 Steam Audio** |
| **Dist** | 物理距离 + **虚拟距离**(受 Avatar 缩放影响) |
| **lG/rG dB** | 近场左右耳音量偏移 |
| **d** | 方向性因子 |
| **PPC°** | 视角校正偏移 |

> **新字段**(2025.4.2 起):"是否转换为 Steam Audio" 状态可视化。

---

## 5. 创作者迁移指南

### 5.1 检查清单

| 检查项 | 状态 |
|--------|------|
| World 使用 `VRC_SpatialAudioSource` | ✅ 自动转换为 Steam Audio,无需改动 |
| World 使用裸 `AudioSource` 3D | ⚠️ 检查 Doppler 行为 |
| Voice 滑块教学 | 📢 提醒用户 65% ≈ 旧 100% |
| 语音衰减参数 | 📏 基于 Avatar 眼睛高度,可能需要重新平衡 |
| Mirror 中音频 | 🔄 视角修正已自动处理 |
| Stream Mode / Drone FPV | ✅ "Audio from Camera" 已修复 |

### 5.2 已知参数变更

| 参数 | 旧(ONSP) | 新(Steam Audio) |
|------|----------|-----------------|
| 语音音量滑块 100% | 100% | ≈ 65% |
| 近场效果范围 | 固定 | 基于 Avatar 眼睛高度 |
| ILD Nudging | 简单 | 改进(更自然的耳间分离) |
| 视角修正 | 仅 PC | 全平台 + VR 适配 |

### 5.3 Udon 端影响

> **FACT**:Steam Audio 是 **运行时音频空间化**,对 Udon 脚本**透明**。
>
> - 不需要改 Udon 代码
> - 不需要重新编译 World
> - 但需要测试音频行为是否符合设计

---

## 6. 替代方案现状(2025.4.2 后)

| 空间化方案 | 状态 |
|------------|------|
| **Steam Audio** | ✅ **默认** |
| **ONSP** | ❌ **已弃用**,不再支持 |
| **Meta XR Audio** | ❌ 未启用 |
| **自定义 spatializer** | ❌ 未在白名单(Unity Asset/Script 限制) |

> **白名单参考**:`memory/world/whitelisted-world-components.md`
> 历史问题 U-5(2026 审计):"是否支持其他空间音频方案(如 Steam Audio、Meta XR Audio)?"→ **部分解决**:Steam Audio 是,Meta XR Audio 仍未。

---

## 7. 故障排查

| 症状 | 可能原因 | 修复 |
|------|---------|------|
| Voice 太响 | 旧 100% 滑块在新系统 = 150%(新 100% ≈ 旧 150%) | 调到约 65%(等效旧 100%) |
| Voice 太轻 | 旧值映射未更新 | 调到约 150%(等效旧 100% 的反向) |
| Mono 扬声器无空间化 | < 2025.4.2p1 客户端 | 升级到 2025.4.2p1+ |
| AudioSource Doppler 异常 | < 2025.4.2p1 客户端 | 升级 |
| Stream Mode 无空间化 | < 2025.4.2p1 客户端 | 升级 |
| 近场耳间分离不自然 | 客户端版本过低 | 升级 |
| 服务端音频变化 | 官方微调(预期) | 等待稳定 |

---

## 8. 未来展望

> **官方原话**(2025.4.2):
> "While we aren't quite opening that can of worms yet, it at least gives us the option."

- Steam Audio 为未来创作者功能铺路
- 可能:创作者端音频参数自定义
- 可能:空间化区域配置
- 可能:环境声学烘焙(类似光子映射)

---

## 9. 参考资料

- **VRChat 2025.4.2 Release Notes**(Build 1768) - Steam Audio 上线
- **VRChat 2025.4.2 Open Beta Notes**(Build 1761) - Beta 阶段
- **VRChat 2025.4.2p1 Release Notes**(Build 1769) - 重大修复
- 相关:`memory/world/udon/world-debug-views.md` §2.6
- 相关:`memory/world/whitelisted-world-components.md` - 音频组件白名单
- 相关:`memory/patterns/unorthodox-patterns.md` - `OnAudioFilterRead` 音频线程(仍有效)
- 相关:https://issteamaudiooutyet.com/(官方梗站)

---

**最后更新**:2026-06-30 | **状态**:✅ 知识库收录 | **来源**:VRChat 官方 Release Notes
