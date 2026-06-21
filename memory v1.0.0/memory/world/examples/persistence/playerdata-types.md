# Player Data Types(PlayerData 数据类型)

> Domain: World / Examples / Persistence
> Source: https://creators.vrchat.com/worlds/examples/persistence/playerdata-types
> 索引日期: 2026-06-15
> SDK Version: 3.4.x+
> 关联底层: `memory/api/persistence.md`

## 数据层选择

| 类型 | **PlayerData** |
|------|----------------|
| 关键 API | 18 种支持数据类型演示 |

## 概述

一个精简示例,演示 **PlayerData 接口支持的所有数据类型**。

## 支持的数据类型(18 种)

| 分类 | 数据类型 |
|------|----------|
| **布尔/字节** | `bool`, `byte`, `byte[]` |
| **整数** | `int`, `uint`, `long`, `ulong`, `short`, `sbyte`, `ushort` |
| **浮点** | `float`, `double` |
| **字符串** | `string` |
| **向量** | `Vector2`, `Vector3`, `Vector4` |
| **四元数** | `Quaternion` |
| **颜色** | `Color`, `Color32` |

## 使用方法

### 客户端
1. 进入 World
2. 点击 "Set Test Data" 按钮
3. 观察显示更新为测试数据

### Editor(ClientSim)
1. 打开 `VRChat SDK > ClientSim Player Data` 编辑器窗口
2. 在 Play Mode 中按下按钮时,观察测试数据也在此更新
3. 可以清除并重新设置测试数据
4. 可以打开包含测试数据的 JSON 文件,手动更新,然后在编辑器窗口中点击 Refresh 显示更新后的测试数据

## 技术分解

### PlayerDataController
具有 `SetTestData` 方法,设置一些示例 player data,由场景中的按钮触发。

### 数据流

```text
按钮点击 → SetTestData()
    ↓
PlayerData.Set*(Networking.LocalPlayer, "key_*", value)
    ↓
OnPlayerDataUpdated 触发
    ↓
检查本地玩家数据是否更改 → 如果是,获取新数据
    ↓
格式化为可读字符串(包括数据类型和值)
    ↓
使用 TextMeshProUGUI 显示在屏幕上
```

### PlayerDataToString 帮助函数
检查特定 key 下存储的数据类型并将其转换为字符串以便显示。此函数支持 **所有可持久化数据类型**。

如果 player data 类型无法识别,会输出错误消息指示类型未知。

## 容量估算

| 数据类型 | 单条数据大小 | 100 KB 可存储 |
|----------|--------------|---------------|
| bool | 1 byte | ~100,000 条 |
| byte | 1 byte | ~100,000 条 |
| int | 4 bytes | ~25,000 条 |
| float | 4 bytes | ~25,000 条 |
| double | 8 bytes | ~12,500 条 |
| Vector3 | 12 bytes | ~8,300 条 |
| Quaternion | 16 bytes | ~6,200 条 |
| string(~50 chars) | ~50 bytes | ~2,000 条 |
| byte[] | 可变 | 灵活分配 |

## 限制

- **100 KB/player/world**(PlayerData 配额,已压缩)
- **String max ~50 chars**(建议值)
- **Key max 128 chars**(建议值)
- ⚠️ 大型 `byte[]` 容易快速填满配额

## Key 命名空间建议

```text
推荐前缀: PlayerDataTypes-  (或具体场景名)
示例:
- PlayerDataTypes-TestInt
- PlayerDataTypes-TestFloat
- PlayerDataTypes-TestVector3
- PlayerDataTypes-TestString
- PlayerDataTypes-TestByteArray
```

## Changelog

- Last updated on **Jan 31, 2025**

## 验证清单

✅ 数据层:PlayerData
✅ 18 种数据类型完整列举
✅ 引用 100 KB 限制
✅ Key 命名空间前缀建议
✅ 容量估算表
