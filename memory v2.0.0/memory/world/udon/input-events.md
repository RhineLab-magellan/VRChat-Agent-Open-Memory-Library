---
title: Input Events - 玩家输入事件
category: world
subcategory: udon

knowledge_level: applied
status: active

tags:
  - world
  - udon
  - event

aliases:
  - "事件"

related:
  - https://github.com/vrchat-community/osc/blob/main/docs/Input.md

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
---
# Input Events - 玩家输入事件

> 来源: https://creators.vrchat.com/worlds/udon/input-events/
> 抓取日期: 2026-06-15
> 状态: ✅ FACT (官方文档)

---

## 概述

可通过 **Udon Input Events** 以**统一方式**读取玩家控制器输入,**跨平台一致**(VR / Desktop / Mobile)。

> **关键优势**: 玩家重映射按键时,这些事件**仍正常工作**。

有两种事件类型:
- **Button 事件** - `bool` 值
- **Axis 事件** - `float` 值

每个事件还包含 **`UdonInputEventArgs`** 对象(包含额外元数据)。

> 也可直接用 [Unity 输入方法和属性](#unity-input-methods-and-properties)。

---

## Button 事件(bool)

`bool` 值 = **true** 按下,**false** 释放。

### 完整事件列表

| 事件 | Desktop | 控制器 |
|---|---|---|
| `InputJump` | Spacebar | 控制器上的 face 按钮(通常) |
| `InputUse` | **Left-Click** | 控制器 **trigger** 按钮(通常) |
| `InputGrab` | **Left-Click** | VR 控制器 **grip** 按钮 |
| `InputDrop` | **Right-Click** | Vive Wand / WMR: 按下 grip;其他: 释放 grip |

### 签名

```csharp
public override void InputJump(bool value, UdonInputEventArgs args);
public override void InputUse(bool value, UdonInputEventArgs args);
public override void InputGrab(bool value, UdonInputEventArgs args);
public override void InputDrop(bool value, UdonInputEventArgs args);
```

### 与 `Interact()` 关系

> **🔴 关键区别**: `Interact()` 是**对象级事件**(需要 Collider),`InputUse` 是**全局玩家事件**(玩家按 Use 触发)

- `Interact()` → 玩家点击特定 Collider
- `InputUse(true)` → 玩家**任何时候**按 Use 键(即使没指向物体)

---

## Axis 事件(float)

`float` 值通常在 **[-1, 1]** 范围。

> **频率**: 控制器模拟摇杆时,每次值变化都触发(0 → 0.1 → 0.2 ...)。Desktop 输出**整数**(-1, 0, 1 ...)。

### 完整事件列表

| 事件 | Desktop | 控制器 |
|---|---|---|
| `InputMoveHorizontal` | A / D | 左侧 stick/pad 左右 |
| `InputMoveVertical` | W / S | 左侧 stick/pad 上下 |
| `InputLookVertical` | 鼠标上下 | 右侧 stick/pad 上下 |
| `InputLookHorizontal` | 鼠标左右 | VR: 右侧 stick/pad 左右(**无 Comfort Turning**);手柄: 右侧 stick 左右 |

### 签名

```csharp
public override void InputMoveHorizontal(float value, UdonInputEventArgs args);
public override void InputMoveVertical(float value, UdonInputEventArgs args);
public override void InputLookHorizontal(float value, UdonInputEventArgs args);
public override void InputLookVertical(float value, UdonInputEventArgs args);
```

---

## UdonInputEventArgs

每个输入事件都包含此对象,持有**额外的输入元数据**。

> **官方预留**: 未来可能添加更多数据字段(欢迎反馈建议)

### 完整字段

| 字段 | 类型 | 说明 |
|---|---|---|
| `UdonInputEventType` | enum | `BUTTON` 或 `AXIS` |
| `boolValue` | `bool` | **Button 事件**时为 true/false;**Axis 事件**时为 false(默认值) |
| `floatValue` | `float` | **Axis 事件**时为 [-1, 1] 数值;**Button 事件**时为 0(默认值) |
| `handType` | enum | `LEFT` 或 `RIGHT`。**键盘和鼠标用户也包含**: 鼠标 = RIGHT,键盘 = LEFT |

---

## OnInputMethodChanged 事件

> **触发时机**: 用户切换输入方式时(Keyboard → Mouse / Controller / Touchscreen)

### 签名

```csharp
public override void OnInputMethodChanged(VRCInputMethod inputMethod);
```

`VRCInputMethod` 枚举详见 [Type Nodes 文档](/worlds/udon/graph/type-nodes/#vrcsdkbasevrcinputmethod)。

> **Vive 歧义警告**:
> - `VRCInputMethod.Vive` = 通过 SteamVR 运行的 Vive 控制器
> - `VRCInputMethod.ViveXr` = 通过 OpenXR 运行的 Vive XR Elite 控制器

---

## Unity Input 方法和属性

Udon 可访问 [`UnityEngine.Input`](https://docs.unity3d.com/ScriptReference/Input.html) 命名空间中的**部分**方法和属性。

### 完整可用 API 列表

| API | 用途 |
|---|---|
| `Input.anyKey` | 任意键是否按下 |
| `Input.anyKeyDown` | 任意键首次按下(本帧) |
| `Input.inputString` | 本帧输入的字符 |
| `Input.imeIsSelected` | IME 是否激活 |
| `Input.GetAxis()` | 虚拟轴值 |
| `Input.GetAxisRaw()` | 虚拟轴原始值 |
| `Input.GetButton()` | 虚拟按钮状态 |
| `Input.GetButtonDown()` | 虚拟按钮首次按下 |
| `Input.GetButtonUp()` | 虚拟按钮释放 |
| `Input.GetMouseButton()` | 鼠标按钮状态 |
| `Input.GetMouseButtonDown()` | 鼠标按钮首次按下 |
| `Input.GetMouseButtonUp()` | 鼠标按钮释放 |
| `Input.GetJoystickNames()` | 已连接手柄名称 |
| `Input.GetKey()` | 键盘按键状态 |
| `Input.GetKeyDown()` | 键盘按键首次按下 |
| `Input.GetKeyUp()` | 键盘按键释放 |

> **不在 Udon 中的 Unity Input API**: `Input.mousePosition`, `Input.touchCount`, `Input.touches` 等不直接可用。**`UdonInputEventArgs.handType` 等提供了更高级的输入信息**。

---

## VRChat 菜单与输入检测(关键!)

> **🔴 关键**: Udon **无法**在**任何 VRChat 菜单打开时**检测输入!

### 阻止输入检测的菜单

- **Main menu**(主菜单)
- **Quick menu**(快捷菜单,Desktop / Mobile)
- **Text input popup**(文本输入弹窗)

### 打开菜单时(释放输入)

> VRChat 打开菜单时,Udon **释放**所有按住的输入,**即使玩家仍按住**。

```csharp
// 示例: 玩家按住方向键 → 打开菜单
// 行为: Input.GetButtonUp() 返回 true(模拟"释放")
// 行为: InputJump(false) 被触发(模拟"释放跳跃")
```

### 关闭菜单时(Unity Input 自动按下)

> VRChat 关闭菜单时,Udon **自动按下**所有按住的 **Unity 输入**。

```csharp
// 示例: 玩家按住右方向键 → 关闭菜单
// 行为: Input.GetButtonDown() 返回 true(模拟"按下")
// 行为: InputJump(true) 不会触发(只 Unity Input 自动补)
```

> **🔴 关键差异**: 只有 **Unity Input** (`Input.GetButton`) 自动补,**Udon Input 事件** (`InputJump`) **不**自动补。

---

## 典型用法

### 1. Jump Counter(跳跃计数)

```csharp
public class JumpCounter : UdonSharpBehaviour
{
    public int jumpCount = 0;

    public override void InputJump(bool value, UdonInputEventArgs args)
    {
        if (value)  // 按下瞬间
        {
            jumpCount++;
            Debug.Log($"Jumps: {jumpCount} (hand: {args.handType})");
        }
    }
}
```

### 2. Move Detection(移动检测)

```csharp
public override void InputMoveHorizontal(float value, UdonInputEventArgs args)
{
    if (Mathf.Abs(value) > 0.5f)
    {
        // 玩家在快速移动
    }
}
```

### 3. Cross-Platform Input Adapter

```csharp
public override void OnInputMethodChanged(VRCInputMethod method)
{
    switch (method)
    {
        case VRCInputMethod.Keyboard:
            ShowKeyboardHints();
            break;
        case VRCInputMethod.Mouse:
            ShowMouseHints();
            break;
        case VRCInputMethod.Controller:
            ShowControllerHints();
            break;
        case VRCInputMethod.Touchscreen:
            ShowTouchHints();
            break;
    }
}
```

---

## 风险与陷阱

| 风险 | 等级 | 说明 |
|---|---|---|
| 菜单打开时输入检测 | 🔴 严重 | **不会**触发;UI 状态变化 |
| `Input.GetButtonUp` 误触发 | 🟡 中等 | 打开菜单时模拟释放 |
| `Input.GetButtonDown` 自动补 | 🟡 中等 | 关闭菜单时模拟按下 |
| `UdonInputEventArgs.boolValue` 在 axis | 🟡 中等 | 永远 false |
| `UdonInputEventArgs.floatValue` 在 button | 🟢 低 | 永远 0 |
| Vive 输入方式歧义 | 🟢 低 | 注意 `Vive` vs `ViveXr` |
| UdonSharp 重载歧义 | 🟡 中等 | 同名方法需用 `public override` |

---

## 精确按键识别限制(2026-06-15 补充)

> **🔴 关键约束**: Udon Input Events 是**抽象动作层**,**无法识别具体 VR 硬件按键**(X/Y/A/B 等 face 按钮)

### 为什么抽象

Udon 只暴露 8 个**语义化动作事件**:
- 4 个 Button:`InputJump` / `InputUse` / `InputGrab` / `InputDrop`
- 4 个 Axis:`InputMoveHorizontal` / `InputMoveVertical` / `InputLookHorizontal` / `InputLookVertical`

`UdonInputEventArgs.handType` 仅能区分**左右手**(`LEFT`/`RIGHT`),**不能**识别是哪个 face 按钮触发。

### 官方描述(原文)

> `InputJump`: Spacebar on Desktop, **typically a face button** on controllers.
> `InputUse`: Left-Click on Desktop, typically a **trigger** button on controllers.
> `InputGrab`: Left-Click on Desktop, typically a **grip** button on VR controllers.
> `InputDrop`: Right-Click on Desktop, press grip button on Vive Wands and some WMR, release grip button on others.

注意:**"typically"** 表明官方未对每种控制器做精确枚举。

### 精确识别 X 键(Quest 左手柄)的方法

**必须**用 `Input.GetButton()` 走 **VRChat 预设的 InputManager 轴名**:

```csharp
// 左手 X 键(Quest Touch / Meta Touch)
bool xButtonHeld = Input.GetButton("Oculus_CrossPlatform_Button2");

// ⚠️ Unity 2022 中 GetButtonDown/GetButtonUp 有 bug(已损坏),需手动模拟
private bool _wasPressed = false;
private bool xDown = false;
private bool xUp = false;

private void Update()
{
    bool pressed = Input.GetButton("Oculus_CrossPlatform_Button2");
    xDown = pressed && !_wasPressed;
    xUp = !pressed && _wasPressed;
    _wasPressed = pressed;
}
```

### 常用轴名(Quest / Meta Touch)

| 物理按键 | 轴名(参考社区维护的 [VRChat Inputs Spreadsheet](https://docs.google.com/spreadsheets/d/1eygw_eZh2tFsBa9Tt7KI_-Pgl1GMcV3yyBPDjT0bFcU)) |
|---------|---------------------------------------------------------|
| 左手 X | `Oculus_CrossPlatform_Button2` |
| 左手 Y | `Oculus_CrossPlatform_Button3` |
| 右手 A | `Oculus_CrossPlatform_Button0` |
| 右手 B | `Oculus_CrossPlatform_Button1` |
| Trigger | `Oculus_CrossPlatform_Button9`(按)/ `Oculus_CrossPlatform_Trigger`(轴) |
| Grip | `Oculus_CrossPlatform_Button10`(按)/ `Oculus_CrossPlatform_Grip`(轴) |

> **【未确认】** 精确编号因 SDK 版本/平台差异可能不同,务必实测。

### ⚠️ 关键陷阱

| 陷阱 | 等级 | 说明 |
|------|------|------|
| **Unity 2022 下 `GetButtonDown/Up` 损坏** | 🔴 严重 | 需手动用 `GetButton + bool` 模拟(来源:[feedback.vrchat.com bug #unity-2022-missing-legacy-input-events](https://feedback.vrchat.com/bug-reports/p/unity-2022-missing-legacy-input-events)) |
| **ALCOM 项目 InputManager 不完整** | 🔴 严重 | ALCOM 创建的项目只有 18 个默认轴(无 VR 预设),直接使用失败(issue vrc-get/vrc-get#1899,2025-02 修复)。**必须用 VCC 创建 World 项目** |
| **Quest 2 上 X 键响应不一致** | 🟡 中等 | 社区报告 `Oculus_CrossPlatform_Button2` 在 Quest 2 上"every ~10 clicks"才触发,需实测 |
| **轴名跨厂商不通用** | 🟡 中等 | 上面是 Oculus 命名,SteamVR Index/Vive 等需不同名 |
| **玩家重映射后失效** | 🟡 中等 | `Input.GetButton("Oculus_CrossPlatform_Button2")` **不响应**玩家在 VRChat 设置中的重映射 |

### 推荐策略

| 场景 | 推荐方式 |
|------|---------|
| 仅需"跳跃"抽象动作 | `InputJump` (跨平台,响应重映射) |
| 需精确识别 X 键 | `Input.GetButton("Oculus_CrossPlatform_Button2")` (Quest) |
| Avatar 内精确识别 X 键 | Expression Parameters + VRChat InputDriver(参考 Avatar 域文档) |
| 外部应用监听 X 键 | 第三方 OSC 桥接程序(如 I5UCC/VRCThumbParamsOSC) |

---

## 与知识库互补

- **Udon 事件完整参考**: `memory/api/events-reference.md` ⭐ InputXxx 事件签名
- **Collision/Trigger 事件**: `memory/api/events-reference.md` ⭐ OnTriggerXxx/OnCollisionXxx
- **Interact 事件**: `memory/api/events-reference.md` ⭐ Interact()
- **UI Events**: `memory/world/udon/ui-events.md` ⭐ UI 事件白名单(不同机制)
- **Animation Events**: `memory/world/udon/animation-events.md` ⭐ Animator 事件白名单
- **OSC 输入控制**: `memory/hybrid/osc-protocol.md` ⭐ Input Control API(注意:官方 OSC 不暴露 X/Y/A/B)
- **Avatar Expression Parameters**: `memory/avatar/playable-layers.md` ⭐ Avatar 端 VR InputDriver 绑定

---

## 相关 VRChat 官方文档

- [Input Events](/worlds/udon/input-events) - 本页官方原版
- [Unity Input](https://docs.unity3d.com/ScriptReference/Input.html) - Unity 输入 API
- [VRChat OSC - Input Control](https://github.com/vrchat-community/osc/blob/main/docs/Input.md) - OSC Input Control 完整地址清单
- [VRC Inputs Spreadsheet](https://docs.google.com/spreadsheets/d/1eygw_eZh2tFsBa9Tt7KI_-Pgl1GMcV3yyBPDjT0bFcU) - 社区维护的 InputManager 轴名清单
