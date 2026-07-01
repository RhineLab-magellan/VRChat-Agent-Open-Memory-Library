---
title: "World Debug Views - VRChat Debug 视图"
category: world
subcategory: udon
knowledge_level: applied
status: active
source: "本地知识库整理 + VRChat 2026.1.1 / 2026.1.1 Open Beta Release Notes"
source_type: community
version: 1.1
last_review: 2026-06-30
confidence: Medium
tags:
  - world
  - udon
  - physbone
  - contact
  - networking
  - audio
aliases:
  - "World Debug Views - VRChat Debug 视图"
  - world-debug-views
related:
  - avatar-events.md
  - udon-moderation-tool-guidelines.md
  - ui-events.md
  - ai-navigation.md
  - animation-events.md
---
# World Debug Views - VRChat Debug 视图

> 来源:https://creators.vrchat.com/worlds/udon/world-debug-views/
> 本地化日期:2026-06-15
> 状态:FACT(VRChat 官方 Debug 工具)
> 关联:`memory/api/networking.md`(Network Stats API)

---

## 一、Debug 菜单访问

### 1.1 入口

> **FACT**:Debug 菜单按钮在 **Quick Menu → Settings** 页面底部。

### 1.2 键盘快捷键

> **FACT**:`Right Shift` + `~` + `< Number >` 直接打开对应 Debug 页。

| 数字 | 视图 |
|------|------|
| 1 | AssetBundle and Memory View |
| 2 | Version & Info |
| 3 | Log Viewer |
| 4 | Players |
| 6 | Net Objects |
| 7 | PhysBone & Contact Overlay |
| 8 | Network Object Info Overlay |
| 9 | Player Info Overlay |
| 0 | VRC_UiShape Debug Overlay |

> **非美式键盘注意**:`~` 键**位于 1 键左侧的物理位置**。若键盘布局 `~` 不在该位置,使用**1 键左侧第一个键**(物理位置优先,字符其次)。

### 1.3 受限视图

> **FACT**:部分 Debug 视图**仅世界创建者**默认可见。

**默认受限的视图**:
- Debug View 6(Net Objects)
- Audio Sources 页面
- 所有 Debug World Overlays

**开放给他人**:
1. 在 VRChat 网站**世界设置**中启用 **World Debugging**
2. 点击 **Save Changes**
3. 其他用户**需重新加入世界**才能访问

### 1.4 分享注意

> **FACT**:VRChat 工作人员可能在 Canny(用户支持)要求**Debug 视图截图**。**但不应**主动分享给其他用户,可能泄露内部信息。

### 1.5 Safe Mode 快捷键（安全相关）⭐

> **FACT** **Safe Mode** 是**安全相关**的快捷键，与 Debug 视图**不同**。
>
> 触发后立即**禁用所有用户的所有功能**（Avatar 显示、语音、动画等）。

| 平台 | 快捷键 |
|------|--------|
| **桌面** | `Shift + Esc` |
| **VR 控制器** | 同时拉**两个 Trigger** + 按**两个系统菜单按钮** |
| **Quest 控制器** | 同 VR 控制器（Both Triggers + Both Menu；源文档未单独说明 Quest，**【推断】**按 VR 控制器处理）|

> **FACT** **Safe Mode 启用时**:
> - Safety System **切换到 Custom 模式**，**关闭所有 ranks 的所有设置**
> - 所有 Avatar **隐藏**，其他用户语音 **禁用**
> - 屏幕中间出现**文字**说明发生了什么
> - **覆盖**你之前的 Custom 设置（**会清空**你自定义的安全配置）

> **FACT** **关闭 Safe Mode**:
> - **手动**设置 Safety System **回原模式**
> - 如果之前用 **Custom 模式**，需**手动**重置之前设置（**不会自动恢复**）

> **FACT** **创作者应告知玩家**:
> - Safe Mode 是**紧急工具**（遇到恶意用户立即使用）
> - **不要**作为常规使用
> - VRChat 计划**未来**添加专用 "Safe" Shield Level（避免覆盖 Custom 设置）

> 详见 `avatar/safety-system.md` §5 (Safe Mode)

---

## 二、Debug 菜单页面(Debug Menu Pages)

### 2.1 AssetBundle and Memory View(1)

**显示内容**:
- VRChat 当前加载到内存的 Avatars
- Worlds
- Items
- 其他资源

**用途**:**主要用于 VRChat 故障排查**,世界开发中较少使用。

> **⚠️ 警告**:"Force GC" 和 "Force GC (full)" 按钮触发**内部 GC 通道**。
> - 看似减少内存使用
> - **不推荐**无完整理解时使用
> - **不会**真正改善性能或 RAM 使用
> - 反复使用**可能导致性能问题或不稳定**

### 2.2 Version & Info(2)

**显示内容**:
- Debug 视图系统帮助信息
- 当前 VRChat 构建版本
- 热键说明(红色)

**特殊功能**:
- 按钮可切换不同 **Debug World Overlays**
- 快捷键 `Right Shift`+`~`+`2` 首次按下**仅显示最小化 HUD**(基本信息)
- 再次按下打开**完整 Debug 视图**

### 2.3 Log Viewer(3)

**显示内容**:
- 输出日志
- **Udon Behaviour 崩溃信息** ⭐
- `Debug.Log` 输出
- Unity / VRChat 错误

**顶部按钮**:
- 启用/禁用特定日志类型
- 用作过滤器

**Background 选项**:
- 即使 Debug 菜单关闭也**收集日志**
- **重启后保留**
- 启动时**警告一次**(若激活)

> **⚠️ 警告**:后台收集日志**对性能有显著影响**。

**Udon 开发关键用途**:
```csharp
Debug.Log("Variable value: " + value);
Debug.LogError("Something went wrong");
Debug.LogWarning("Performance concern");
```

### 2.4 Players(4)

> **FACT**:Debug View 4 显示**其他玩家的各种统计**。

**每玩家列**:
| 列 | 含义 |
|----|------|
| **M** | 是否为 Instance Master |
| **L** | 是否为本地玩家 |
| **VR** | 是否在 VR 中 |
| **Group** | 当前所属组(内部网络系统,按距离组合对象) |
| **Intrvl** | 玩家发送自身同步数据的间隔时间 |
| **Fnl D** | 内部系统目标延迟(实际延迟频繁调整以平衡延迟与平滑) |

**顶部信息**:
- 当前实时网络状态
- **"Suffering"** 字段:世界 Udon Behaviour 是否发送**过多数据** ⭐

**底部按钮**:导出统计到 JSON 文件(同日志目录),主要用于**内部测试**。

> **FACT**:Udon 可通过 **Network Stats API** 检查大部分这些值。

### 2.5 Net Objects(6)

> **FACT**:Net Objects 页面显示**世界中所有网络对象**及其统计。

**每对象列**:
| 列 | 含义 |
|----|------|
| **Owner** | 对象所有者的 playerId |
| **Group** | 当前所属组(同 Players 页定义) |
| **Sleeping** | 对象是否休眠(仅 `VRCObjectSync` 可休眠,休眠后停止传输数据) |
| **Delay** | Owner 与查看者之间的当前延迟 |
| **Size** | 每次同步的字节数 |
| **Bps** | 该对象每秒约使用的字节数 |
| **Since Last** | 距上次发送数据的运行计数 |
| **Interval** | 该对象每秒约尝试同步的次数 |

> **⚠️ 警告**:对象多时,打开此页**可能导致性能下降**。

**性能优化关键**:
- **Size 大** = 单次同步负载大(检查 UdonSynced 变量数量/大小)
- **Bps 高** = 带宽消耗大(检查是否过度同步)
- **Since Last 持续增长** = 对象休眠良好(可接受)
- **Interval 过高** = 同步频率过高(可能需 Manual 模式 + 阈值触发)

### 2.6 Audio Sources

> **FACT**:显示世界所有活跃 `AudioSource` 组件的信息。

**每声源列**:
| 列 | 含义 |
|----|------|
| **Name** | GameObject 名称 |
| **Clip** | 分配的 `AudioClip` 名(不包含 `PlayOneShot`;未设置时为 ` `) |
| **Type** | 声源类型(World / Avatar / Internal;普通用户仅见 World) |
| **Vol** | Unity 设置的音量(**不**含 `VRC_SpatialAudioSource` 的 `Gain`) |
| **3D** | `spatialBlend` 值 |
| **Act/Prog** | 是否正在播放,及相对 `Clip` 的进度(无 Clip 时为 `-1.0%`) |
| **VRC/SAS** | 是否有 `VRC_SpatialAudioSource`,是否转换为 Steam Audio |
| **Dist** | 到声源的距离(物理单位),及**虚拟距离**(受 Avatar 缩放影响,用于近场计算) |
| **lG/rG dB** | 近场模拟的左右耳音量偏移(分贝) |
| **d** | 计算 lG/rG 的方向性因子 |
| **PPC°** | 透视校正偏移(度,物理位置与透视校正后位置的夹角) |

**排序方式**:
- **Scene**(加载顺序)
- **距离**(从声源到听者)

**额外功能**:
- 切换显示附近 `AudioSource` 的**基本射线和位置信息**(主要供内部使用)
- **需 World Debugging 权限**

---

## 三、Debug World Overlays(世界内叠加层)

> **FACT**:Overlays **不是 Debug 菜单页面**,而是**直接在世界内显示数据**。

**启用方式**:
1. 快捷键(`Right Shift`+`~`+`< Number >`)
2. 从 **Version & Info (2)** 页面切换

**通用要求**:
- **World Debugging 启用** 或 **当前世界由你上传**
- World Debugging 状态在 Debug 菜单**左下角**显示

### 3.1 PhysBone & Contact Overlay(7)

> **FACT**:Debug View 7 高亮世界中**附近的 PhysBones 和 Contacts**。

**用途**:调试 PhysBone / Contact 组件行为不符合预期时。

### 3.2 Network Object Info Overlay(8)

> **FACT**:在**每个同步对象上**显示**信息面板**。

**每对象面板**:
| 字段 | 含义 |
|------|------|
| **P** | 所有者的 Ping |
| **Q** | 数据质量(100% = 无丢包) |
| **O** | 对象所有者的 PlayerID |
| **G** | 当前所属组(同前定义) |
| **Held** | 是否被持有(若是 Pickup) |
| **Status** | 对象正在做什么(如 `Should Sleep` / `Player` / `Held` / `Discontinuity`) |

### 3.3 Player Info Overlay(9)

> **FACT**:与 Net Object Info Overlay 类似,但在**每个玩家脚下**显示**信息面板**。

**用途**:实时观察玩家网络状态、Owner 关系等。

### 3.4 VRC_UiShape Debug Overlay(0)

> **FACT**:`VRC_UiShape` Debug Overlay 显示世界中**每个 VRC_UiShape 的轮廓**。

**额外功能**:
- **屏幕**(桌面模式)或**手部**(VR 模式)显示**当前指向对象**的文本叠加
- 用于**诊断 UI 交互问题**

**典型调试场景**:
- UI 点击不响应 → 确认 VRC_UiShape 覆盖范围
- 桌面模式手部射线与 UI 区域对齐问题
- 多人 UI 焦点切换异常

---

## 四、Network Stats API(Udon 可读)

> **FACT**:Udon 可通过 **Network Stats API** 检查 Players (4) 视图显示的大部分值。

### 4.1 关键 API

参考 `memory/api/networking.md` 完整列表,核心 API:

| API | 用途 |
|-----|------|
| `Networking.GetServerTimeInMilliseconds()` | 服务器时间 |
| `Networking.CalculateServerDeltaTime()` | 时间差计算 |
| `Networking.IsMaster` | 是否 Master |
| `Networking.LocalPlayer` | 本地玩家 |
| `Networking.GetOwner(gameObject)` | 对象所有者 |
| `Networking.IsOwner(gameObject)` | 本地是否 Owner |

### 4.2 "Suffering" 字段的自检模式

```csharp
public class NetworkHealthMonitor : UdonSharpBehaviour
{
    void Update()
    {
        // 检查是否在 Master 上
        if (!Networking.IsMaster) return;
        
        // 计算"健康度"(示例)
        float totalBps = CalculateTotalBytesPerSecond();
        if (totalBps > 9000)  // 接近 ~11KB/s 限制
        {
            Debug.LogWarning("Network usage high: " + totalBps + " B/s");
        }
    }
    
    float CalculateTotalBytesPerSecond()
    {
        // 遍历所有网络对象并累计
        // (实际实现需枚举游戏对象)
        return 0f;
    }
}
```

---

## 五、典型调试工作流

### 5.1 网络同步问题排查

```
1. Build & Test 多客户端(2-4)
   ↓
2. 一名玩家操作 UI 触发同步
   ↓
3. 另一名玩家看不到同步?
   ↓
4. 打开 Debug View 6(Net Objects)
   ↓
5. 检查目标对象的:
   - Owner 是否正确
   - Size(每次同步字节数)
   - Bps(带宽)
   - Interval(同步频率)
   ↓
6. 打开 Debug View 4(Players)
   ↓
7. 检查双方玩家:
   - Group(应在同一组)
   - Delay(延迟是否过高)
   - Suffering(整体网络是否过载)
```

### 5.2 UI 交互问题排查

```
1. UI 点击不响应
   ↓
2. 打开 Debug View 0(VRC_UiShape Debug Overlay)
   ↓
3. 确认 VRC_UiShape 覆盖 UI 区域
   ↓
4. 桌面/VR 模式下查看指向提示
   ↓
5. 检查 UI Events 白名单(`ui-events.md`)
   ↓
6. 确认 OnClick 配置正确
```

### 5.3 PhysBone 行为异常

```
1. PhysBone 不按预期摆动/抓取
   ↓
2. 打开 Debug View 7(PhysBone & Contact Overlay)
   ↓
3. 确认 PhysBone 范围
   ↓
4. 检查碰撞体设置
   ↓
5. 检查 Avatar 是否在 PhysBone 影响范围内
```

### 5.4 Udon 性能问题

```
1. 世界运行卡顿
   ↓
2. 打开 Debug View 3(Log Viewer)
   ↓
3. 查找 Udon Behaviour 崩溃或警告
   ↓
4. 检查 Debug.LogError / Debug.LogWarning 输出
   ↓
5. 打开 Debug View 6(Net Objects)
   ↓
6. 检查网络对象是否过多或 Size 过大
   ↓
7. 使用 Network Stats API 自检
```

---

## 六、性能开销

> **FACT**:打开 Debug 视图本身**有性能开销**。

| 视图 | 性能影响 |
|------|----------|
| AssetBundle and Memory View (1) | 低 |
| Version & Info (2) | 极低 |
| Log Viewer (3) | 低(Background 模式高) |
| Players (4) | 低 |
| Net Objects (6) | **🟡 对象多时高** |
| Audio Sources | 低 |
| PhysBone & Contact Overlay (7) | 中 |
| Network Object Info Overlay (8) | **🟡 同步对象多时高** |
| Player Info Overlay (9) | 低 |
| VRC_UiShape Debug Overlay (0) | **🟡 VRC_UiShape 多时高** |

> **【推断】** 调试时建议**仅开启需要的视图**。

---

## 七、与其他文档的关系

| 相关文档 | 用途 |
|----------|------|
| `memory/api/networking.md` | Network Stats API 完整参考 |
| `memory/world/udon/using-build-test.md` | Build & Test 多客户端 |
| `memory/world/udon/vm-and-assembly.md` | 字节码级调试 |
| `memory/avatar/physbone.md`(待补充) | PhysBone 调试 |

---

## 八、检查清单(调试前)

- [ ] 已启用 **World Debugging**(如需受限视图)
- [ ] 已记忆**快捷键**或知道**菜单路径**
- [ ] 已准备好**Log Viewer 截图工具**
- [ ] 已规划**多客户端测试场景**
- [ ] 已记录**问题前后的关键数据**(Size, Bps, Delay)
- [ ] 已**关闭不相关的 Debug 视图**以减少开销

---

## 九、Missing Information

> **【未确认】** 以下信息需要查询 VRChat 官方补充文档:
>
> - Network Stats API 完整列表(文档未提供)
> - "Suffering" 字段的具体阈值
> - Net Objects 视图的"Sleeping" 触发条件
> - VRC_UiShape Debug Overlay 的具体渲染细节
> - 各 Debug 视图在 Quest 平台的可用性

---

## 十、Performance Debug Dashboard (2026.1.1+) ⭐NEW

> **FACT** (2026.1.1 Build 1781 起,2026.1.1 Open Beta 已包含):Debug 菜单新增 **Performance** 标签,允许创建和自定义性能仪表盘。

### 访问方式

```
Right shift + ~ + 1
```

或:Quick Menu → Settings 标签 → 底部 **"Toggle Debug UI"** 按钮 → 进入 Debug 菜单 → **Performance** 标签

### 功能

- **创建自定义仪表盘**
- **图表展示**多种性能指标
- 实时采样

### 2026.1.1p1 变更(Open Beta Build 1783)

| 变更 | 详情 |
|------|------|
| **Performance sampling 默认关闭** | 减少开销 |
| **可手动切换** | 在 Performance Debugging UI 中直接启用 |
| **数据字段显示当前值** | 调试菜单的 Performance 标签数据字段显示**最新采样值 (Cur)** |
| **Min/Max 字段语义** | 显示**显示数据的限制**(非图边缘) |

### 已知问题

| 版本 | 问题 |
|------|------|
| 2026.1.1 Open Beta | 调试时偶发卡顿(framerate hitches,逐渐加重) |
| 2026.1.1p1 | 修复卡顿(尤其 Quest),sampling 默认关闭 |

### 创作者用例

| 场景 | 用途 |
|------|------|
| **性能调优** | 监控特定 World/Avatar 帧率趋势 |
| **带宽诊断** | 观察网络流量峰值 |
| **帧时间分析** | 定位 GC spike 或物理负载 |
| **玩家体验模拟** | 用同一指标对比不同 Avatar/World 性能 |

详见 `memory/world/audio-steam.md` §4(Steam Audio Debug 字段)与本章节配合使用。
