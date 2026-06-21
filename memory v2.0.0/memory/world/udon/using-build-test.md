---
title: Using Build & Test - 本地测试流程
category: world
subcategory: udon

knowledge_level: applied
status: active

tags:
  - world
  - udon
  - animator
  - avatar

aliases:
  - "Using Build & Test - 本地测试流程"

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
---
# Using Build & Test - 本地测试流程

> 来源:https://creators.vrchat.com/worlds/udon/using-build-test/
> 本地化日期:2026-06-15
> 状态:FACT(VRChat 官方测试流程)
> 关联:`memory/sources/clientsim.md` - 替代的编辑器内模拟方案

---

## 一、核心定位

> **FACT**:简单功能(鼠标事件、计时器)用 Unity **Play 模式**即可;但**需要 Avatar 交互或网络同步**的功能,**必须**用 Build & Test。

### 1.1 Play 模式 vs Build & Test

| 功能 | Play 模式 | Build & Test |
|------|-----------|--------------|
| 鼠标事件 | ✅ | ✅ |
| 计时器 | ✅ | ✅ |
| Animator | ✅ | ✅ |
| UdonBehaviour.OnTriggerEnter | ✅ | ✅ |
| **Avatar 交互** | ❌ | ✅ |
| **网络同步** | ❌ | ✅ |
| **VR 模式** | ❌ | ✅ |
| **PlayerData 持久化** | ❌ | ✅ |

### 1.2 ClientSim 替代方案

> **FACT**:在 Edit 模式直接运行 VRChat 客户端的开销较大,**ClientSim** 提供轻量级模拟。

参考 `memory/sources/clientsim.md` 获取详细信息。

---

## 二、设置流程

### 2.1 创建项目

1. 新建 Unity 项目
2. 导入 VRChat Worlds SDK
3. 菜单栏 → **VRChat SDK → Show Control Panel**

### 2.2 Authentication 标签

```text
Control Panel → Authentication → Sign In
输入 VRChat 账号凭据
```

> **FACT**:Build & Test 需要有效的 VRChat 登录凭据。

### 2.3 Settings 标签 - 设置 VRChat Client 路径

菜单:**Settings → VRChat Client → Edit**

| 安装源 | 默认路径 |
|--------|----------|
| **Steam** | `C:\Program Files (x86)\Steam\steamapps\common\VRChat\VRChat.exe` |
| **Oculus** | `C:\Program Files\Oculus\Software\Software\vrchat-vrchat\VRChat.exe` |
| **Viveport** | `C:\Viveport\ViveApps\469fbcbb-bfde-40b5-a7d4-381249d387cd\1597468388\VRChat.exe` |

> **FACT**:未设置正确路径,Build & Test 可能启动失败或启动错误的客户端。

### 2.4 Builder 标签 - 设置 Layer 和 Collision Matrix

1. 点击 **Setup Layers for VRChat** → 弹出确认 → **Do it!**
2. 点击 **Set Collision Matrix** → 弹出确认 → **Do it!**

> **FACT**:VRChat 使用自定义 Layer 和 Collision Matrix,缺失此步骤会导致构建失败。

---

## 三、第一次 Build & Test

### 3.1 步骤

1. 切换到 **Builder** 标签
2. **勾选 Force Non-VR**(桌面模式首次测试推荐)
3. 点击 **Build & Test** 按钮

### 3.2 预期结果

- VRChat 客户端启动
- 自动登录
- 自动进入**本地实例**(仅你一人)
- 可以走动、交互、测试

---

## 四、Multiple Clients(多客户端测试)

### 4.1 为什么需要

> **FACT**:测试 **Synced Variables** 和 **Custom Network Events** 需要多个玩家在同实例。

### 4.2 步骤

1. 关闭当前已启动的 VRChat 客户端
2. **Number of Clients** 设为 **2**(或更多)
3. 点击 **Build & Test**
4. Unity 会启动 **2 个** VRChat 客户端
5. 两个客户端使用**相同 Avatar**
6. 可切换窗口控制**两个 Avatar**

### 4.3 Master 与权限

> **FACT**:**第一个加载的 Avatar 是 Master**,因此是**网络对象 Owner**,可**更新 UI 元素**。
> 第二个 Avatar 只能**看到**同步更新。

#### 4.3.1 测试模式

| 测试目标 | 所需客户端数 |
|----------|-------------|
| 单一玩家 UI 交互 | 1 |
| Synced Variables 同步 | 2 |
| Custom Network Events 触发 | 2 |
| 所有权转移(谁拿到 Owner) | 2 |
| Master 切换行为 | 2-3 |
| 大实例(>10 玩家)性能 | 4+ |

### 4.4 所有权转移测试示例

> UdonExampleScene 提供 **SyncButtonAnyone** 示例:**谁点击就转移所有权**。

```csharp
public override void Interact()  // 玩家点击
{
    // 转移所有权给点击者
    Networking.SetOwner(Networking.LocalPlayer, gameObject);
    // 之后该玩家可同步修改
}
```

---

## 五、Build & Reload(热重载)

### 5.1 设计动机

> **FACT**:多客户端测试时,每次修改世界都要重新登录 VRChat,**耗时且需要重排窗口**。

### 5.2 启用方式

设置 **Number of Clients = 0**,然后点击 **Build & Test**(此时变为 **Build & Reload**)。

### 5.3 行为

- 构建新版本世界
- **所有已打开的客户端自动进入新本地实例**
- **跳过 VRChat 启动和登录流程**
- 大幅缩短迭代时间

### 5.4 命令行启用(自启动客户端)

VRChat 新增 `--watch-worlds` 标志,开启热重载监听:

```shell
VRChat.exe --watch-worlds --profile=0 --no-vr --enable-debug-gui --enable-sdk-log-levels --enable-udon-debug-logging -screen-width 1920 -screen-height 1080
```

**参数说明**:

| 参数 | 说明 |
|------|------|
| `--watch-worlds` | 监听世界构建,自动重载 |
| `--profile=0` | 使用 Profile 索引 0(默认账号) |
| `--no-vr` | 桌面模式 |
| `--enable-debug-gui` | 启用 Debug GUI |
| `--enable-sdk-log-levels` | 启用 SDK 日志级别 |
| `--enable-udon-debug-logging` | 启用 Udon Debug 日志 |
| `-screen-width 1920` | 屏幕宽度 1920 |
| `-screen-height 1080` | 屏幕高度 1080 |

### 5.5 多 Profile 测试

> **FACT**:可启动多个 VRChat 客户端使用不同 Profile 模拟多玩家。

```shell
# 终端 1:Profile 0(Master)
VRChat.exe --watch-worlds --profile=0 --no-vr

# 终端 2:Profile 1(普通玩家)
VRChat.exe --watch-worlds --profile=1 --no-vr
```

---

## 六、EditorOnly 物体自动删除

> **FACT**:Build & Test 构建过程会**自动剔除 EditorOnly 标签的物体**。

### 6.1 用途

- 测试用辅助物体(灯光、调试面板)
- 不应进入 Build 的标记
- 节约运行时开销

### 6.2 用法

```csharp
// 在 Editor 中设置
GameObject testHelper = new GameObject("TestHelper");
testHelper.tag = "EditorOnly";
// 或:Inspector → Tag → EditorOnly
```

### 6.3 注意

> **🔴 编辑器内可见、Build 后自动移除**

适用于:
- 调试 Gizmo
- 开发控制台
- 测试用碰撞体
- 性能分析器

**不适用于**:
- 必备 UI(用 VRC_Only 区分,或彻底删除)
- 美术资源

---

## 七、模拟玩家加入/离开

### 7.1 OnPlayerJoined / OnPlayerLeft 事件

```csharp
public override void OnPlayerJoined(VRCPlayerApi player)
{
    Debug.Log("玩家加入: " + player.displayName);
    // 模拟 Master 同步
    if (Networking.IsMaster)
    {
        // 给新玩家发完整状态
        RequestSerialization();
    }
}

public override void OnPlayerLeft(VRCPlayerApi player)
{
    Debug.Log("玩家离开: " + player.displayName);
    // 清理与该玩家相关的数据
}
```

### 7.2 Build & Test 多客户端触发

| 步骤 | 行为 |
|------|------|
| Build & Test 启动 2 客户端 | 触发 `OnPlayerJoined` 2 次 |
| 关闭客户端 1 | 触发 `OnPlayerLeft` 1 次 |
| Build & Reload | 不触发 `OnPlayerLeft`(`--watch-worlds` 持续连接) |

### 7.3 Master 切换测试

```csharp
// 在 OnPlayerLeft 中检查 Master 转移
public override void OnPlayerLeft(VRCPlayerApi player)
{
    if (player == oldMaster)  // 原 Master 离开
    {
        // 等待 VRChat 自动选举新 Master
        // 选举完成会触发 OnPlayerJoined(由系统重发)
    }
}
```

> **FACT**:Master 转移由 VRChat 平台自动处理,新 Master 不会触发 `OnPlayerJoined`,但 `Networking.IsMaster` 值会变。

---

## 八、PlayerData 持久化测试

### 8.1 测试方法

1. Build & Test 进入世界
2. 设置 PlayerData:`PlayerData.Set("key", "value")`
3. **关闭客户端**
4. **Build & Test 重新启动** (再次进入相同世界)
5. 读取 PlayerData:`if (PlayerData.HasKey("key")) { var v = PlayerData.GetString("key"); }`

### 8.2 注意

- PlayerData 是**跨世界**的(同一账号所有世界共享)
- 持久化是**最终一致性**,修改后立即可见
- 测试时使用**唯一 Key** 避免污染

### 8.3 清理测试数据

```csharp
// 测试结束后清理
public void ClearTestData()
{
    if (Networking.IsMaster)  // 或本地玩家
    {
        if (PlayerData.HasKey("test_key"))
        {
            PlayerData.Delete("test_key");
        }
    }
}
```

---

## 九、SDK 校验(Build 前)

### 9.1 常见错误

> **【推断】** Build 失败通常由以下原因:

| 错误 | 原因 | 解决 |
|------|------|------|
| Missing Layers | 未设置 VRChat Layers | 点击 Setup Layers for VRChat |
| 碰撞矩阵未设置 | 默认 Unity 矩阵 | 点击 Set Collision Matrix |
| Script 编译错误 | UdonSharp 编译失败 | 查看 Console 错误 |
| 物体未设置 VRC_Only | 测试物体进入 Build | 改用 EditorOnly |
| Avatar 描述缺失 | 测试 Avatar 无描述 | 设置测试 Avatar |
| UdonBehaviour 未编译 | .cs 改动未保存 | 保存并重新编译 |

### 9.2 Build 前必检清单

- [ ] VRChat Layers 设置完成
- [ ] Collision Matrix 设置完成
- [ ] 所有 UdonSharp 脚本编译通过(无错误)
- [ ] 客户端路径已设置
- [ ] 已登录 SDK Control Panel

---

## 十、SDK Control Panel 工作流

### 10.1 完整流程图

```
1. 修改场景/脚本
   ↓
2. 保存(Ctrl+S)
   ↓
3. 打开 VRChat SDK Control Panel
   ↓
4. 切换到 Builder 标签
   ↓
5. (可选)设置 Number of Clients
   ↓
6. 点击 Build & Test / Build & Reload
   ↓
7. 等待 VRChat 启动(首次较慢,热重载较快)
   ↓
8. 在 VRChat 中测试
   ↓
9. 返回 Unity 修改
   ↓
10. (若已启用 Reload)重复步骤 2-8
```

### 10.2 Build & Test 性能参考

| 阶段 | 耗时 |
|------|------|
| 首次 Build & Test | 60-180 秒(含 VRChat 启动) |
| 后续 Build & Reload | 5-15 秒(仅世界重载) |
| 纯代码修改 Reload | 3-8 秒 |
| Shader 重新编译 Reload | 20-60 秒 |

---

## 十一、与其他文档的关系

| 相关文档 | 用途 |
|----------|------|
| `memory/sources/clientsim.md` | Edit 模式内模拟(轻量替代) |
| `memory/world/udon/ui-events.md` | UI 事件测试 |
| `memory/world/udon/world-debug-views.md` | Debug 视图 |
| `memory/api/persistence.md` | PlayerData 完整 API |
| `memory/api/networking.md` | 网络同步测试 |

---

## 十二、Missing Information

> **【未确认】** 以下信息需要查询 VRChat 官方补充文档:
>
> - `--watch-worlds` 标志的具体实现机制
> - 多个 Profile 同时启动的稳定性
> - Build & Test 的具体性能数据(取决于硬件)
> - EditorOnly 删除的完整规则(是否递归子物体)

---

## 十三、风险与限制

### 13.1 Build & Test 限制

| 限制 | 说明 |
|------|------|
| 仅本机 | 无法模拟真实网络延迟 |
| 相同 Avatar | 多客户端使用同一 Avatar,无法测试 Avatar 兼容性 |
| 本地实例 | 无需好友列表,无法测试跨好友系统 |
| 单机性能 | 无法测试多机器负载 |

### 13.2 常见陷阱

- **忘记 Build & Reload**:直接关掉 VRChat 重新 Build & Test,会重新登录(慢)
- **EditorOnly 滥用**:必备 UI 被误删
- **PlayerData 污染**:测试 Key 与生产 Key 冲突
- **Master 误判**:测试时 Master 行为可能与生产环境不同
