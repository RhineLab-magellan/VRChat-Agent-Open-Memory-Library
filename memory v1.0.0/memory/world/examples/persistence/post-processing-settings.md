# Post-Processing Settings(后处理设置)

> Domain: World / Examples / Persistence
> Source: https://creators.vrchat.com/worlds/examples/persistence/post-processing-settings
> 索引日期: 2026-06-15
> SDK Version: 3.4.x+
> 关联底层: `memory/api/persistence.md`

## 数据层选择

| 类型 | **PlayerData** |
|------|----------------|
| 关键 API | `OnPlayerDataUpdated` + Unity UI Slider 事件 |

## 概述

此场景通过将 **PostProcessing Volume 的权重** 保存到 PlayerData 来保存和加载其 Bloom 设置。

## 使用方法

### 客户端
1. 播放场景
2. 使用 "Post-Processing Weight" Slider 设置 Bloom 级别
3. 它应该作为名为 `"settings_pp_weight"` 的 float 出现在 ClientSim PlayerData 窗口中

## 技术分解

### UdonPostProcessing 脚本
有一个名为 "UdonPostProcessing" 的 UdonSharp 脚本,位于同名 GameObject 上。

### 数据流

```text
1. Slider 移动
    ↓
2. Unity UI Event 调用 UdonPostProcessing.SliderUpdated
    ↓
3. SliderUpdated():
    - PlayerData.SetFloat(Networking.LocalPlayer, "settings_pp_weight", value)
    ↓
4. PlayerData 更新
    ↓
5. OnPlayerDataUpdated 事件触发
    ↓
6. 触发两个操作:
    a) 设置目标 PostProcessingVolume 的权重(改变本地 Bloom 强度)
    b) 更新 Slider 的值和位置以匹配存储的权重
       (确保玩家首次加载实例并从服务器恢复值时,Slider 与值匹配)
```

### 核心代码(推断)

```csharp
public class UdonPostProcessing : UdonSharpBehaviour
{
    public Slider bloomSlider;
    public PostProcessingVolume targetVolume;
    
    private const string BLOOM_WEIGHT_KEY = "settings_pp_weight";
    
    public void SliderUpdated()
    {
        float value = bloomSlider.value;
        PlayerData.SetFloat(Networking.LocalPlayer, BLOOM_WEIGHT_KEY, value);
    }
    
    public override void OnPlayerDataUpdated(VRCPlayerApi player, string key)
    {
        if (player != Networking.LocalPlayer) return;
        if (key != BLOOM_WEIGHT_KEY) return;
        
        if (PlayerData.TryGetFloat(player, key, out float weight))
        {
            // 1. 设置 PostProcessingVolume 权重
            targetVolume.weight = weight;
            
            // 2. 更新 Slider 位置(首次加载时与服务器值匹配)
            bloomSlider.value = weight;
        }
    }
}
```

## Key 命名空间分析

⚠️ **本示例 Key 命名不当** —— `"settings_pp_weight"` 没有 Prefab 名前缀,易与其他 Post Processing 系统冲突。

### 改进建议

```text
原 Key: settings_pp_weight
改进 Key: PostProcessing-BloomWeight  (或 Momo-PPP-BloomAmount 等具体 Prefab 名前缀)
```

## 限制

- **100 KB/player/world**(PlayerData 配额)
- Bloom 权重是 float(4 bytes),远未触及上限
- ⚠️ **OnPlayerDataUpdated 对每个 key 变化都会触发** —— 应在回调内检查 key 匹配

## 跨 Prefab 引用风险

如果一个 World 中有多个 PostProcessing Volume 系统,使用通用 Key 会导致冲突。
**强烈建议**使用 Prefab 名作为前缀。

## Changelog

- 初始版本

## 验证清单

✅ 数据层:PlayerData
✅ 关键 API:OnPlayerDataUpdated + PlayerData.SetFloat/TryGetFloat
✅ 引用 100 KB 限制
✅ Key 命名空间风险警告(本示例 Key 不规范)
✅ 命名空间改进建议
