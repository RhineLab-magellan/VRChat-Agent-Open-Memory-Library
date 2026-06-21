# Debugging Udon Projects

> 来源: https://creators.vrchat.com/worlds/udon/debugging-udon-projects
> 抓取日期: 2026-06-15
> 状态: ✅ FACT (官方调试指南)

---

## 概述

**Debugging** 是了解 VRChat、世界和 Udon 代码"在做什么"的关键技能。

> **🔴 关键**: **发布世界前必须在 VRChat 中测试**!大多数错误可在 Unity Editor 中修复,但**有些 Udon 程序只能在 VRChat 中调试**。

---

## VRChat Debug Log 入门

### 1. 在 VRChat 中查看日志

启动 VRChat 时**启用 Debug GUI**(详见下文),在 **Desktop** 和 **VR** 模式下均可打开 Debug 覆盖层。

**快捷键**:`Right Shift + Backtick + 3`

更多快捷键: [VRChat Keyboard and Mouse](https://docs.vrchat.com/docs/keyboard-and-mouse)

### 2. 在文本编辑器中查看日志

VRChat 日志文件位置:

```
C:\Users\YourName\AppData\LocalLow\VRChat\VRChat
```

文件命名:

```
output_log_08-55-48.txt  (每次启动 VRChat 生成新文件)
```

---

## 启用 Udon 调试(3 种方式)

> **🔴 默认 VRChat 日志不包含 Udon 详细信息**!必须显式启用。

### 方式 1: VRC Quick Launcher ⭐ 推荐

- [VRC Quick Launcher](https://vcc.docs.vrchat.com/tools/vrc-quick-launcher/) 允许选择启用哪些调试功能
- 在 **Creator Companion → Tools** 标签找到
- **最简单的方式**(避免手写批处理)

### 方式 2: 批处理文件

在 `VRChat.exe` 同级目录创建 `debug.bat`:

```bat
VRChat.exe --no-vr --enable-debug-gui --enable-sdk-log-levels --enable-udon-debug-logging
```

**3 个 Flag 解释**:

| Flag | 作用 |
|---|---|
| `--no-vr` | 强制 Desktop(调试时不需要 VR) |
| `--enable-debug-gui` | 启用 Debug GUI 覆盖层 |
| `--enable-sdk-log-levels` | 启用 SDK 日志详细级别 |
| `--enable-udon-debug-logging` | **启用 Udon 调试日志**(最关键) |

**高级示例**(使用第 2 个 profile + 720p 分辨率):

```bat
VRChat.exe --profile=1 --no-vr --enable-debug-gui --enable-sdk-log-levels --enable-udon-debug-logging -screen-width 1280 -screen-height 720
```

更多 Flag:

- [VRChat Launch Options](https://docs.vrchat.com/docs/launch-options)
- [Unity Standalone Player 命令行参数](https://docs.unity3d.com/2022.3/Documentation/Manual/CommandLineArguments.html)

### 方式 3: Steam 启动选项

1. Steam Library → 右键 VRChat → Properties
2. **General** 标签 → **Set Launch Options**
3. 输入:
   ```
   --enable-debug-gui --enable-udon-debug-logging
   ```

> **⚠️ 性能警告**: 调试会**降低 VRChat 性能**并**增加日志文件大小**!**不要在生产环境保持启用**。

---

## 添加日志到 Udon 程序

> **核心调试技巧**: 在可疑位置插入 `Debug.Log` 节点,带**唯一文本**

### UdonSharp 示例

```csharp
using UdonSharp;
using UnityEngine;
using VRC.Udon.Common;

public class JumpDetector : UdonSharpBehaviour
{
    public override void InputJump(bool value, UdonInputEventArgs args)
    {
        Debug.Log("Local player jumped!");
    }
}
```

### 调试策略

1. **在关键操作前/后添加日志**
2. **日志消息要唯一**(便于在大量日志中 grep)
3. **观察日志看脚本是否到达某点**
4. **识别是否在某 `Debug.Log` 之前就停止执行**

---

## 理解 Udon 错误

### 行为

> **🔴 关键**: 当 UdonBehaviour 遇到严重错误时,**会自动 disable 自己**!

错误日志(在 VRChat 客户端可见):

```
[UdonBehaviour] An exception occurred during Udon execution, this UdonBehaviour will be halted.
```

**找到详细信息**: 在日志文件中搜索单词 **"halted"**。

### 错误示例解析

```
2020.08.28 17:40:51 Error      -  [UdonBehaviour] An exception occurred during Udon execution, this UdonBehaviour will be halted.
VRC.Udon.VM.UdonVMException: An exception occurred in an UdonVM, execution will be halted.
---> VRC.Udon.VM.UdonVMException: An exception occurred during EXTERN to 'VRCSDK3VideoComponentsBaseBaseVRCVideoPlayer.__GetTime__SystemSingle'.
---> System.NullReferenceException: Object reference not set to an instance of an object.
  at VRC.SDK3.Internal.Video.Components.AVPro.AVProVideoPlayerInternal.GetTime () [0x00000] in :0
  at VRC.Udon.Wrapper.Modules.ExternVRCSDK3VideoComponentsBaseBaseVRCVideoPlayer.__GetTime__SystemSingle (VRC.Udon.Common.Interfaces.IUdonHeap heap, System.UInt32[] parameterAddresses) [0x00000] in :0
```

### 关键信息(第二行)

```
An exception occurred during EXTERN to 'VRCSDK3VideoComponentsBaseBaseVRCVideoPlayer.__GetTime__SystemSingle'.
---> System.NullReferenceException: Object reference not set to an instance of an object.
```

| 信息 | 解读 |
|---|---|
| `EXTERN to '...'` | Udon **VM 外部调用**失败 |
| `Object reference not set to an instance of an object` | **空引用** (NullReferenceException) |
| `VRCSDK3VideoComponentsBaseBaseVRCVideoPlayer` | **VRCVideoPlayer** 组件 |
| `__GetTime__SystemSingle` | 调用了 `GetTime` 方法 |

**结论**: 脚本尝试访问 `VRCVideoPlayer.GetTime()`,但 **VRCVideoPlayer 未赋值**(null)。

**修复**: 找到调用 `VRCVideoPlayer.GetTime` 的 Graph,确保有 `VRCVideoPlayer` 连接。

### Udon VM 异常的层级

```
Outer Exception
  └─ UdonVMException (Udon VM 中异常)
      └─ EXTERN Exception (具体哪个 EXTERN 调用)
          └─ Actual .NET Exception (如 NullReferenceException)
```

**关注最内层**的 `.NET Exception`,那才是**根本原因**。

---

## 关键调试模式

### 模式 1: "哨兵"日志

在 UdonBehaviour 的关键路径添加独特日志:

```csharp
public class PlayerTracker : UdonSharpBehaviour
{
    public override void OnPlayerJoined(VRCPlayerApi player)
    {
        Debug.Log($"[PlayerTracker] OnPlayerJoined: {player.displayName}");
        // ...
    }

    public override void OnPlayerLeft(VRCPlayerApi player)
    {
        Debug.Log($"[PlayerTracker] OnPlayerLeft: {player.displayName}");
    }
}
```

然后在日志中 grep `[PlayerTracker]`,**完整看到该脚本的活动**。

### 模式 2: 计数器

```csharp
private int _interactCount = 0;

public override void Interact()
{
    _interactCount++;
    Debug.Log($"[Counter] Interact called {_interactCount} times");
}
```

识别**重复触发**或**未触发**问题。

### 模式 3: 状态快照

```csharp
private void LogState(string context)
{
    Debug.Log($"[State] {context} | Owner={Networking.IsOwner(gameObject)} | " +
              $"isMaster={Networking.IsMaster} | " +
              $"syncedA={_syncedA} | syncedB={_syncedB}");
}
```

---

## 在 Unity 中查看 UdonSharp 日志

> **UdonSharp 运行时异常监听器**: 监听 VRChat 输出日志,定位 UdonSharp 脚本**具体哪一行**出错

- **默认启用**,可在 Project Settings 中禁用
- 在 VRChat 中抛出的任何错误会显示在**编辑器 Console** 中
- 显示格式: `script FullBodyPlayerTracker.cs encountered an error in line 92 at the 86th character`

> **核心价值**: 看到**原始 UdonSharp 代码**的错误位置,而不是编译后的 VM 指令位置。

---

## ⚠️ 关键工程注意事项

### 1. Debug.Log 本身是 EXTERN(昂贵!)

> **🔴 关键**: 每次 `Debug.Log` 都是 **EXTERN 调用**,在 Udon VM 中**非常昂贵**

- 详见 `memory/rules/udon-vm-architecture.md`
- 不要在 `Update()` 中无脑 `Debug.Log`
- 生产代码中应**移除调试日志**或用 `#if UNITY_EDITOR` 包裹

```csharp
#if UNITY_EDITOR
    Debug.Log("[DEBUG] 调试信息");
#endif
```

### 2. Behaviour halted = 永久停止

> UdonBehaviour halt 后**不会自动恢复**!必须**重新启用** GameObject 或**重新进入世界**。

### 3. 日志文件位置是 Per-User

- 不同用户日志文件位置不同
- 多人调试时需要**明确告知路径**

---

## 调试资源

| 资源 | 用途 |
|---|---|
| `[UdonBehaviour] An exception` | grep 此字符串找到 halt 事件 |
| `--enable-udon-debug-logging` | **必加** flag |
| UdonSharp 运行时异常监听 | 定位 UdonSharp 代码行号 |
| `Halted` 关键词搜索 | 找到所有 halt 事件 |
| 错误嵌套链 | **最内层**是根本原因 |

---

## 与知识库互补

- **Udon VM 架构**: `memory/rules/udon-vm-architecture.md` ⭐ EXTERN 机制
- **Udon 性能规则**: `memory/rules/performance-rules.md` ⭐ Debug.Log 成本
- **UdonSharp 运行时**: `memory/api/udonsharp-runtime.md` ⭐ 异常监听机制
- **Udon 编译管线**: `memory/world/udonsharp-compilation.md` ⭐ Build 错误排查

---

## 相关 VRChat 官方文档

- [Debugging Udon Projects](/worlds/udon/debugging-udon-projects)
- [VRChat Launch Options](https://docs.vrchat.com/docs/launch-options)
- [VRC Quick Launcher](https://vcc.docs.vrchat.com/tools/vrc-quick-launcher/)
- [Keyboard and Mouse](https://docs.vrchat.com/docs/keyboard-and-mouse)
