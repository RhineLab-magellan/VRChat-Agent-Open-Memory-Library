# Position Sync(位置同步)

> Domain: World / Examples / Persistence
> Source: https://creators.vrchat.com/worlds/examples/persistence/position-sync
> 索引日期: 2026-06-15
> SDK Version: 3.4.x+
> 关联底层: `memory/api/persistence.md`

## 数据层选择

| 类型 | **PlayerObject** |
|------|------------------|
| 关键组件 | `VRCPlayerObject` + `UdonBehaviour` + `VRCEnablePersistence` |
| 同步模式 | 0.5s 周期 + `OnPlayerRestored` |

## 概述

一个简单的 PlayerObject prefab,保存每个玩家的位置和旋转,然后在玩家重新加入 World 时恢复它们。

## 使用方法

### VRChat Client
1. 加入 World,移动到远离 Spawn 点的位置
2. 重新加入 World,你应该在相同的位置和旋转

### Unity Editor
将 prefab `PositionSync` 添加到场景中,完成。

## 技术分解

### 保存逻辑
- 当玩家站在地面上时,脚本每 **0.5 秒** 保存一次位置和旋转
- 在从服务器接收持久化数据时(`OnPlayerRestored`),将玩家返回到原始位置

### 核心代码(推断)

```csharp
public class PositionSync : UdonSharpBehaviour
{
    [UdonSynced] private Vector3 syncedPosition;
    [UdonSynced] private Quaternion syncedRotation;
    
    private void Update()
    {
        if (!Networking.IsOwner(Networking.LocalPlayer, gameObject)) return;
        
        // 每 0.5 秒保存一次
        if (Time.time - lastSaveTime > 0.5f)
        {
            syncedPosition = transform.position;
            syncedRotation = transform.rotation;
            RequestSerialization();  // VRCEnablePersistence 自动持久化
            lastSaveTime = Time.time;
        }
    }
    
    public override void OnPlayerRestored(VRCPlayerApi player)
    {
        if (player != Networking.LocalPlayer) return;
        transform.position = syncedPosition;
        transform.rotation = syncedRotation;
    }
}
```

### Inspector 参数

| 类型 | 名称 | 说明 |
|------|------|------|
| `string` | Synced Rotation key | PlayerData 中用于旋转的 key 名 |
| `string` | Synced Position key | PlayerData 中用于位置的 key 名 |

> **注意**:Inspector 中暴露的是 PlayerData key,但实际数据存储使用 PlayerObject 的 `[UdonSynced]` 字段(由 `VRCEnablePersistence` 自动持久化)。

## 数据流

```text
玩家移动 → 站立在地面
    ↓
每 0.5 秒:
    - 读取 transform.position/rotation
    - 写入 [UdonSynced] 字段
    - RequestSerialization() → 网络同步
    - VRCEnablePersistence 自动持久化到服务端
    ↓
玩家离开 World
    ↓
玩家重新加入 → OnPlayerRestored
    ↓
transform.position = syncedPosition(立即传送)
```

## 与 Networking 的关系

可与 `memory/api/networking.md` 中的同步机制互链:
- 此示例使用 **Manual 同步模式** + 0.5s 周期
- 替代方案:Continuous 同步(每帧序列化,带宽高)或 NetworkCallable(事件驱动)

## 限制

- **100 KB/player/world**(PlayerObject 配额)
- 位置和旋转数据小(~28 bytes = Vector3 + Quaternion)
- 远未触及上限
- ⚠️ 0.5s 间隔 → 玩家可能丢失最多 0.5s 的移动(快速移动时可见)

## Key 命名空间建议

```text
推荐前缀: PositionSync-
示例:
- PositionSync-SyncedPosition    (Vector3)
- PositionSync-SyncedRotation    (Quaternion)
```

## Changelog

- **0.0.2**: Added in-world instructions, swapped to OnPlayerRestored
- **0.0.1**: Initial Publish

## 验证清单

✅ 数据层:PlayerObject
✅ 关键组件:VRCPlayerObject + UdonBehaviour + VRCEnablePersistence
✅ 引用 100 KB 限制
✅ 0.5s 周期机制说明
✅ 引用 OnPlayerRestored 时机
✅ Key 命名空间前缀建议
✅ 与 networking.md 互链
