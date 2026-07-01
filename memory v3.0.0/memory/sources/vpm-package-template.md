---
title: "VPM Package Template"
category: sources
knowledge_level: applied
status: active
source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-10
confidence: Medium
tags:
  - sources
  - shader
  - udonsharp
  - avatar
aliases:
  - "VPM Package Template"
  - vpm-package-template
related:
  - udonvoiceutils.md
  - vrcx.md
  - community-notes.md
  - example-central.md
  - official-docs.md
---
# VPM Package Template


---

## 概述

VPM Package Template 是 VRChat 官方提供的 Package 开发模板，用于创建、打包和分发 VPM 兼容的 Package。

**核心功能**:
- 一键创建基于模板的新仓库
- 自动构建 .zip 和 .unitypackage
- 自动生成 VPM Repo Listing
- 自动部署到 GitHub Pages

**适用场景**:
- 分享 UdonSharp 工具库
- 分发 Avatar 组件/Shader
- 创建可被 VPM 安装的第三方 Package

---

## 使用流程

### 1. 创建新仓库

1. 访问 https://github.com/vrchat-community/template-package
2. 点击 **"Use This Template"** 按钮
3. 填写仓库名称和描述
4. 选择 Public/Private 可见性
5. 不需要勾选 "Include all branches"

### 2. 克隆到本地

```bash
git clone https://github.com/username/your-package.git
cd your-package
```

### 3. 在 Unity 中打开

1. Unity Hub → Add → 选择仓库文件夹
2. 等待 VPM Resolver 下载并安装
3. 获得 VPM Package Maker 和 Package Resolver 工具

### 4. 开发 Package

**选项 A**: 删除示例 Package，重新创建
```bash
rm -rf Packages/com.vrchat.demo-template
```

**选项 B**: 复用示例 Package 并重命名
```bash
# 重命名文件夹
mv Packages/com.vrchat.demo-template Packages/com.username.packagename

# 更新 .gitignore
# 编辑 Packages/.gitignore
# 将 !com.vrchat.demo-template 改为 !com.username.packagename
```

### 5. 配置自动化

1. 在 GitHub 仓库 Settings 中创建变量:
   - 名称: `PACKAGE_NAME`
   - 值: `com.username.packagename`

2. 配置 GitHub Pages:
   - Settings → Pages → Source: GitHub Actions

---

## 项目结构

```
template-package/
├── .github/
│   └── workflows/
│       ├── release.yml        # 构建 Release
│       └── build-listing.yml   # 构建 Repo Listing
├── Packages/
│   └── com.vrchat.demo-template/  # 示例 Package
│       ├── package.json
│       ├── Editor/
│       └── Runtime/
├── Website/
│   └── index.html             #  Landing Page
└── ProjectSettings/           # Unity 项目设置
```

---

## package.json 格式

### 必需字段

| 字段 | 类型 | 示例 | 说明 |
|------|------|------|------|
| `name` | string | `com.vrchat.base` | 反向域名命名，必须唯一 |
| `displayName` | string | `VRChat Worlds` | VPM 中显示的名称 |
| `version` | string | `3.4.2` | 语义版本 (Major.Minor.Patch) |
| `unity` | string | `2022.3` | Unity 版本要求 |
| `vrchatVersion` | string | `2022.1.1` | VRChat SDK 版本要求 |
| `author` | object | 见下方 | 作者信息 |

### 示例

```json
{
  "name": "com.vrchat.demo-template",
  "displayName": "VRChat Example Package",
  "version": "0.0.7",
  "unity": "2022.3",
  "description": "Simple Package for testing Automation",
  "vrchatVersion": "2022.1.1",
  "author": {
    "name": "Momo the Monster",
    "email": "momodmonster@gmail.com",
    "url": "https://mmmlabs.com"
  }
}
```

### 可选字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `description` | string | Package 描述 |
| `dependencies` | object | 其他 VPM 包依赖 |
| `vpmDependencies` | object | VRChat SDK 依赖 |
| `url` | string | Package 远程 URL（发布后由系统填充） |

### 完整示例（带依赖）

```json
{
  "name": "com.example.my-package",
  "displayName": "My Example Package",
  "version": "1.0.0",
  "unity": "2022.3",
  "description": "An example VPM package",
  "vrchatVersion": "2022.1.1",
  "author": {
    "name": "Your Name",
    "email": "you@example.com"
  },
  "vpmDependencies": {
    "com.vrchat.worlds": ">=3.4.0"
  }
}
```

---

## GitHub Actions 工作流

### release.yml

**触发方式**: 手动 (`workflow_dispatch`)

**功能**:
1. 验证 `PACKAGE_NAME` 仓库变量
2. 从 package.json 读取版本号
3. 创建 .zip 压缩包
4. 创建 .unitypackage 文件
5. 生成 Git Tag
6. 发布 GitHub Release

**输出文件**:
- `{PACKAGE_NAME}-{version}.zip`
- `{PACKAGE_NAME}-{version}.unitypackage`
- `package.json`

### build-listing.yml

**触发方式**:
- 手动 (`workflow_dispatch`)
- Build Release 完成后自动触发
- Release 发布/编辑/删除时触发

**功能**:
1. 检出 package-list-action (Nuke 项目)
2. 构建 VPM Repo Listing JSON
3. 部署到 GitHub Pages

**输出**:
- VPM 兼容的 index.json
- Landing Page (Website/)

---

## Repo Listing 格式

VPM Repo Listing 是 VPM 识别 Package 源的索引文件。

### JSON 结构

```json
{
  "name": "My Package Listing",
  "id": "com.username.my-packages",
  "url": "https://username.github.io/repo-name/index.json",
  "author": "you@example.com",
  "packages": {
    "com.username.my-package": {
      "versions": {
        "1.0.0": {
          "name": "com.username.my-package",
          "displayName": "My Package",
          "version": "1.0.0",
          "unity": "2022.3",
          "vrchatVersion": "2022.1.1",
          "url": "https://github.com/username/repo/releases/download/1.0.0/com.username.my-package-1.0.0.zip",
          "author": {
            "name": "Your Name",
            "email": "you@example.com"
          }
        }
      }
    }
  }
}
```

### URL 格式

```
https://username.github.io/repo-name/
```

---

## Package Maker Tool

用于将现有的 .unitypackage 迁移为 VPM Package。

### 使用步骤

1. **准备**: 创建 VPM Package Template 仓库
2. **导入**: 将现有的 .unitypackage 导入到 Assets 目录
3. **启动**: `VRChat SDK / Utilities / Package Maker`
4. **配置**:
   - Target Folder: 选择 Package 的父文件夹
   - Package ID: 输入唯一标识符（如 `com.username.packagename`）
   - Related VRChat Package: 选择相关 SDK（World/Avatar）
5. **转换**: 点击 "Convert Assets to Package"
6. **确认**: 确认迁移对话框
7. **清理**: 删除 Package Maker Tool 和相关文件

### 迁移后结构

```
Packages/com.username.packagename/
├── package.json
├── Editor/           # UnityEditor 代码
│   └── *.cs
└── Runtime/          # Runtime 代码
    ├── *.cs
    └── **/*.cs
```

### 路径修复

#### 方式 1: 转换为 Resources

```csharp
// 旧代码 (不工作)
var styleSheet = AssetDatabase.LoadAssetAtPath<StyleSheet>(
    "Assets/MyPackage/Editor/MyPackageStyle.uss");

// 新代码 (使用 Resources)
var styleSheet = Resources.Load<StyleSheet>("MyPackageStyle");
```

#### 方式 2: 使用 GUID

```csharp
string path = AssetDatabase.GUIDToAssetPath("de965059f7f21034b8c112bfc7a0dc5f");
var styleSheet = AssetDatabase.LoadAssetAtPath<StyleSheet>(path);
```

---

## VPM CLI 命令

```bash
# 全局安装
dotnet tool install --global vrchat.vpm.cli

# 更新
dotnet tool update --global vrchat.vpm.cli

# 卸载
dotnet tool uninstall --global vrchat.vpm.cli
```

### 项目管理

| 命令 | 说明 |
|------|------|
| `vpm new <name> [template]` | 创建新项目（template: Base/World/Avatar/UdonSharp） |
| `vpm add project <path>` | 添加项目到列表 |
| `vpm remove project <name>` | 从列表移除项目 |
| `vpm list projects` | 列出所有项目 |
| `vpm resolve project` | 恢复项目包依赖 |
| `vpm migrate legacy [path]` | 从 Legacy SDK 迁移 |
| `vpm migrate 2022 [path]` | 从 Unity 2019 迁移到 2022 |

### 包管理

| 命令 | 说明 |
|------|------|
| `vpm add package <name>` | 添加包 |
| `vpm add package <name>@<version>` | 添加指定版本 |
| `vpm remove package <name>` | 移除包 |
| `vpm check package <name>` | 检查包信息 |

### 仓库管理

| 命令 | 说明 |
|------|------|
| `vpm list repos` | 列出所有仓库源 |
| `vpm add repo <url>` | 添加远程仓库 |
| `vpm add repo <path> --headers "key:value"` | 带 Header 添加仓库 |
| `vpm new repo [path] --name "Name" --author "email"` | 创建新仓库 |
| `vpm remove repo <id>` | 移除仓库 |

### 系统

| 命令 | 说明 |
|------|------|
| `vpm check hub` | 检查 Unity Hub |
| `vpm install hub` | 安装 Unity Hub |
| `vpm check unity` | 检查 Unity 安装 |
| `vpm install unity` | 安装 Unity 2022.3.22f1 |
| `vpm list unity` | 列出已安装的 Unity |

---

## 自定义 Landing Page

Website/index.html 使用 Scriban 模板引擎，支持动态填充。

### 可用变量

| 变量 | 说明 |
|------|------|
| `{{ this }}` | 最新 release 的 manifest |
| `{{ this.name }}` | Package 名称 |
| `{{ this.displayName }}` | 显示名称 |
| `{{ this.description }}` | 描述 |
| `{{ this.version }}` | 版本号 |

### 示例

```html
<h1>{{ this.displayName }}</h1>
<p>Version: {{ this.version }}</p>
<p>{{ this.description }}</p>
```

---

## 故障排除

### 1. Workflow 未触发

检查:
- 仓库变量 `PACKAGE_NAME` 是否设置
- GitHub Pages Source 是否设为 GitHub Actions

### 2. Release 未生成

检查:
- package.json 是否存在于 `Packages/{PACKAGE_NAME}/`
- `PACKAGE_NAME` 变量值是否与文件夹名匹配

### 3. Listing 未更新

检查:
- release 是否已发布
- workflow 是否完成

---

## 相关文档

- [VRChat Creator Docs - VPM](https://vcc.docs.vrchat.com/vpm/)
- [VRChat Creator Docs - CLI](https://vcc.docs.vrchat.com/vpm/cli/)
- [Converting Assets to VPM Package](https://vcc.docs.vrchat.com/guides/convert-unitypackage/)
- [template-package-listing](https://github.com/vrchat-community/template-package-listing)
- [package-list-action](https://github.com/vrchat-community/package-list-action)

---