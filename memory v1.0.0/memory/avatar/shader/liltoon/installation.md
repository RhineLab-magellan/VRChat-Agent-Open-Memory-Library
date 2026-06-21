# lilToon 安装与配置

---

## 安装方式

### 方式一：VCC (推荐)

```
1. 打开 VRChat SDK > Settings > Download VCC
2. 或直接访问: vcc://vpm/addRepo?url=https://lilxyzw.github.io/vpm-repos/vpm.json
3. 在 VCC 中添加仓库
4. 在 Manage Project 中找到 lilToon 并安装
```

**优点**：
- 自动更新
- 依赖管理
- 版本控制

### 方式二：BOOTH 下载

```
1. 访问 https://lilxyzw.booth.pm/items/3087170
2. 下载 ZIP 文件
3. 解压后找到 .unitypackage 文件
4. 拖入 Unity Project 窗口
```

### 方式三：Unity Package Manager

```
1. Unity 菜单 > Window > Package Manager
2. 点击 + > Add package from git URL...
3. 粘贴仓库 URL
```

---

## 初始设置流程

### STEP 1: 安装着色器

选择一个安装方式完成安装。

### STEP 2: 创建材质

```
1. Project 窗口右键 > Create > Material
2. 或 Assets > Create > Material
3. 在 Inspector 中选择 lilToon 着色器
```

### STEP 3: 切换编辑模式

lilToon 提供两种编辑模式：

| 模式 | 适用场景 |
|------|---------|
| **简易设置** | 预设模型、仅修改颜色 |
| **详细设置** | 新建设置、迁移着色器、精细调整 |

```
Inspector > 编辑モード > 詳細設定
```

> ⚠️ 部分环境默认不显示日语，需要在 Language 设置中切换为 Japanese

### STEP 4: 分配纹理

根据纹理类型分配到对应位置：

| 纹理类型 | 分配位置 |
|---------|---------|
| **主纹理** | 基本色设置 > メインカラー > テクスチャ |
| **法线贴图** | ノーマルマップ設定 > ノーマルマップ |
| **轮廓线遮罩** | 輪郭線設定 > 輪郭線 > マスクと太さ |
| **阴影遮罩** | 影設定 > 影 > マスクと強度 |
| **MatCap** | マットキャップ設定 > マットキャップ |
| **MatCap 遮罩** | マットキャップ設定 > マットキャップ > マスク |
| **RimLight 遮罩** | リムライト設定 > リムライト > 色/マスク |
| **发光（遮罩）** | 発光設定 > 発光テクスチャ > 色 |

### STEP 5: 设置渲染模式

透明纹理需要修改渲染模式：

| 模式 | 适用场景 |
|------|---------|
| **不透明** | 无透明需求 |
| **カットアウト** | 镂空效果、无半透明 |
| **半透明** | 头发、表情等半透明 |

```
Inspector > 描画モード > カットアウト / 半透明
```

### STEP 6: 应用预设（可选）

使用预设快速配置：

```
1. 编辑モード > プリセット
2. 选择目的对应的预设
3. 点击应用
```

---

## 安装后验证

### 检查着色器是否正确安装

```
1. 创建一个材质球
2. Inspector > Shader > lilToon
3. 确认参数面板正常显示
```

### 常见问题

| 问题 | 解决方案 |
|------|---------|
| 材质选择后无 UI | 可能混入了旧版本，执行 Refresh Shaders |
| 无法选择着色器 | 检查 Editor 错误，尝试重新导入 |
| 参数显示异常 | 切换编辑模式或重启 Unity |

---

## 菜单项

安装后会在 Unity 菜单添加以下工具：

### GameObject 菜单
```
GameObject/lilToon/[GameObject] Fix lighting
```
- 修复多 Mesh 物体亮度不一致

### Assets 菜单
```
Assets/lilToon/[Shader] Refresh shaders
Assets/lilToon/[Material] Remove unused properties
Assets/lilToon/[Material] Run migration
Assets/lilToon/[Texture] Convert normal map (DirectX <-> OpenGL)
Assets/lilToon/[Texture] Pixel art reduction
Assets/lilToon/[Texture] Convert Gif to Atlas
Assets/lilToon/[Model] Setup from FBX
```

---

## 卸载/更新

### 更新
```
VCC: 直接更新包
BOOTH: 重新下载并导入覆盖
```

### 完全卸载
```
1. 删除 lilToon 文件夹
2. 重新导入
```

> ⚠️ 建议先备份项目

---

## 相关文档

- [概述与特性](overview.md) — lilToon 四大特性
- [渲染模式](render-modes.md) — 各模式详解
- [基本设置](basic-settings.md) — 基础参数
- [故障排除](troubleshooting.md) — 常见问题
