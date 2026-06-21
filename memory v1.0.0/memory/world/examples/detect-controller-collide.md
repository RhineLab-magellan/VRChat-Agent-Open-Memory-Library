# Detect Controller Collide

> 来源: VRChat 官方文档 (creators.vrchat.com/worlds/examples/detect-controller-collide)
> 抓取日期: 2026-06-15
> 原始 URL: https://creators.vrchat.com/worlds/examples/detect-controller-collide
> 文档版本: Last updated Nov 15, 2024
> SDK: 3.0+

## Example Central Package

> ✅ **需要 Example Central Package**
> 通过 `VRChat SDK → 🏠 Example Central` 导入
> 包含 CharacterController 胶囊、UI Canvas、检测逻辑 Prefab

### Example World
- **World ID**: `wrld_7da557ad-3584-4b0a-bf61-6cbba33701d4`
- **URL**: https://vrchat.com/home/world/wrld_7da557ad-3584-4b0a-bf61-6cbba33701d4

---

## 概述

演示 VRChat **独有的玩家碰撞检测事件** `OnControllerColliderHitPlayer`。
- Unity 基础事件: `OnControllerColliderHit` (检测非玩家物体)
- VRChat 扩展: `OnControllerColliderHitPlayer` (检测玩家)
- 返回结构体: `ControllerColliderPlayerHit` 包含 `VRCPlayerApi` 引用

**典型场景**: 推箱子游戏、NPC 撞到玩家、玩家之间碰撞反馈。

---

## 关键 Udon API

| API | 类型 | 触发条件 | 返回结构 |
|-----|------|----------|----------|
| `OnControllerColliderHit(ControllerColliderHit hit)` | Unity Event | CharacterController 撞到非玩家物体 | `ControllerColliderHit` |
| `OnControllerColliderHitPlayer(ControllerColliderPlayerHit hit)` | VRChat 扩展事件 | CharacterController 撞到玩家 | `ControllerColliderPlayerHit` |

**`ControllerColliderPlayerHit` 关键字段**:
- `VRCPlayerApi player` - 被撞到的玩家 API 引用

---

## Graph 程序: OnCharacterControllerHitExampleGraph

### 公共变量(Inspector 暴露)

| 名称 | 类型 | 说明 |
|------|------|------|
| `CharacterController` | `CharacterController` | 引用自身 CC,用于 `Update` 中调用 `Move()` |
| `moveSpeed` | `float` | 移动速度(内部乘以 `Time.deltaTime`) |
| `hitNameText` | `TextMeshProUGUI` | 命中时更新的 UI 文本 |
| `characterControllerStartPos` | `Transform` | 重置时的起始位置 |

### 四个事件

| 事件 | 触发 | 行为 |
|------|------|------|
| `Update()` | 每帧 | 调用 `Move()` 让 CC 向前移动 |
| `OnControllerColliderHit(hit)` | 撞到非玩家 | 从 `hit` 提取物体名,设置到 `hitNameText` |
| `OnControllerColliderHitPlayer(hit)` | 撞到玩家 | 从 `hit.player` 提取玩家名,设置到 `hitNameText` |
| `__ResetCharacterController()` | 自定义事件 | CC 重置回起始位置(由两个碰撞事件触发) |

### 行为演示

胶囊在玩家与墙之间反复冲撞:
1. 撞到玩家 → UI 显示玩家名
2. 玩家走开 → 撞到墙 → UI 显示 "Wall"
3. 重复循环

---

## 关键实现细节

### CharacterController 的使用

```csharp
// 必须在 Update 中显式调用 Move(),CC 不会自动移动
private void Update()
{
    Vector3 forward = transform.TransformDirection(Vector3.forward);
    CharacterController.Move(forward * moveSpeed * Time.deltaTime);
}
```

### 重置策略

```csharp
public void __ResetCharacterController()
{
    transform.position = characterControllerStartPos.position;
    transform.rotation = characterControllerStartPos.rotation;
}
```

碰撞后立即重置 → 持续向同一方向冲撞 → 形成可观察的"撞-重置-撞"循环。

---

## 与其他碰撞事件对比

| 事件 | 适用 | 性能 |
|------|------|------|
| `OnPlayerTriggerEnter/Exit` | Trigger 区域(无物理) | 最低 |
| `OnControllerColliderHit` | 物理碰撞(非玩家) | 中 |
| `OnControllerColliderHitPlayer` | 物理碰撞(玩家) | 中 |

**性能考量**:
- Trigger 事件: 玩家进入/离开区域时触发
- Controller 碰撞: 物理引擎每帧检测,**有持续成本**
- 选择依据: 是否需要物理阻挡 + 碰撞响应

---

## 二次开发建议

- 撞到不同玩家触发不同反馈(伤害计算、积分等)
- 撞到特定物体触发剧情
- 用 `hit.gameObject.tag` 区分物体类型

---

## 与知识库互补

- **Player Collisions 完整 API**: `memory/api/events-reference.md` 中的 Player Collisions 章节
- **VRCPlayerApi**: `memory/api/player-api.md`(待建)
- **Trigger 事件**: `memory/world/components/trigger.md`(待建)

## 相关 Udon 文档链接

- [Player Collisions - Physics](/worlds/udon/players/player-collisions#physics)
- [Unity OnControllerColliderHit](https://docs.unity3d.com/2022.3/Documentation/ScriptReference/MonoBehaviour.OnControllerColliderHit.html)
- [Unity CharacterController](https://docs.unity3d.com/2022.3/Documentation/ScriptReference/CharacterController.html)
