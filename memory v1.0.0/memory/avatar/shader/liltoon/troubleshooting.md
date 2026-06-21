# lilToon 故障排除

---

## 编辑器错误

### 编辑器错误处理流程

```
1. 更新 lilToon 到最新版本
2. 删除 lilToon 文件夹后重新导入
3. 对 lilToon 文件夹执行 Reimport
4. 如仍有问题，提交错误报告
```

### 错误报告模板

```
バグ: 
再現方法: 

# 可选信息
Unity版本: 
lilToon版本: 
VRChat世界: 
スクリーンショット: 
コンソールログ:
```

---

## 材质问题

### 材质选择后无 UI

**原因**：旧版本混合

**解决方案**：
```
Assets/lilToon/[Shader] Refresh shaders
```

### 材质错误

**解决方案**：
```
1. 检查 Console 错误
2. 更新/重新导入 lilToon
3. 刷新着色器
```

### 透明度显示异常

**检查项**：
- 描画モード 是否为半透明
- 纹理是否包含透明度
- Render Queue 设置

**解决方案**：
```
提高前景物体 Render Queue 值
```

---

## 渲染问题

### 半透明物体重叠消失

**原因**：绘制顺序问题

**解决方案**：
```
调整 Render Queue：
前景物体使用较高值（2500+）
```

### 亮度不一致

**原因**：多 Mesh 物体

**解决方案**：
```
1. 右键对象 > lilToon/[GameObject] Fix lighting
2. 统一材质设置
3. 检查顶点光强度
```

### 阴影过强/过弱

**原因**：环境光影响

**解决方案**：
```
降低 影色への環境光影響度
使用遮罩隔离面部
使用 ライト方向のオーバーライド
```

---

## 轮廓线问题

### 轮廓线不整洁

**解决方案**：
```
1. 使用 マスクと太さ 遮罩调整
2. 顶点颜色烘焙（硬边模型）
```

### 轮廓线无法平滑

**原因**：硬边模型限制

**解决方案**：
```
1. 准备光滑法线模型
2. 使用顶点颜色烘焙工具
3. 分配到轮廓线着色器
```

---

## VRChat 相关问题

### 上传画面无法打开

**原因**：脚本错误

**解决方案**：
```
1. 更新/重新导入 lilToon
2. 刷新着色器
3. 检查其他可能冲突的脚本
```

### Safety 表现异常

**检查项**：
- Custom Safety Fallback 设置
- 纹理 Alpha 通道
- 描画モード 设置

---

## 性能问题

### 负荷过高

**优化建议**：
```
1. 降低渲染模式负荷
2. 减少遮罩数量
3. 烘焙纹理
4. 合并相似材质
```

### Build 尺寸过大

**优化建议**：
```
1. 移除未使用纹理
2. 使用烘焙功能
3. 关闭不需要的功能
```

---

## 纹理问题

### 纹理设置无效

**原因**：SamplerState 限制

**说明**：
部分纹理使用固定 SamplerState，导入设置可能被忽略。

### 纹理命名问题

**Setup from FBX 失败**：

检查纹理命名是否符合规则，排除关键词列表。

---

## 其他问题

### Unity 项目无法打开

**解决方案**：
```
1. 删除 Library 和 Temp 文件夹
2. 重新打开项目
3. 备份 Library 文件夹
```

### SRP 版本错误

**原因**：旧版本 SRP 标识不完整

**解决方案**：
在 `lilToon/Shader/Includes/lil_common_macro.hlsl` 中指定版本：

```hlsl
#define SHADER_LIBRARY_VERSION_MAJOR 4
#define SHADER_LIBRARY_VERSION_MINOR 8
```

---

## 常用修复命令

| 命令 | 用途 |
|------|------|
| **Refresh shaders** | 修复着色器错误 |
| **Remove unused properties** | 清理材质属性 |
| **Run migration** | 版本迁移 |
| **Fix lighting** | 修复亮度问题 |
| **Convert normal map** | 法线格式转换 |

---

## 相关文档

- [基本设置](basic-settings.md) — 基础参数
- [VRChat 配置](vrchat-specific.md) — VRChat 特定问题
- [优化指南](optimization.md) — 性能优化
- [着色器变体](variations.md) — 版本说明
