---
title: "VRChat API 参考 - 文件模块"
category: vrchatsdk
knowledge_level: applied
status: active
source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
tags:
  - vrchatsdk
  - udonsharp
  - reference
aliases:
  - "VRChat API 参考 - 文件模块"
  - 15_API_文件
related:
  - "api-authentication.md"
  - "api-users.md"
  - "api-worlds.md"
  - "api-friends.md"
  - "api-notifications.md"
---
---
source: https://vrchat.hexdocs.pm/VRChat.Files.html
date: 2026-06-10
SDK版本: vrchat v1.20.0 (Elixir)
---

# VRChat API 参考 - 文件模块

## 模块概述

API calls for all endpoints tagged `Files`.

## 概念说明

- **File**：文件对象，每个 File 可以有多个 Version
- **Version**：文件版本，每个 Version 可以有多个 Data blobs
- **Version 0**：始终是文件创建时的时间戳，实际数据通常在 version 1 及以上

## 函数列表

### get_files

List Files - 返回文件列表

```elixir
get_files(connection, opts \\ [])
// 可选参数:
:tag     // 标签，如 "icon" 或 "gallery"
:userId  // 会导致 500 权限错误
:n, :offset
```

### get_file

Show File - 显示文件对象的一般信息

```elixir
get_file(connection, file_id, opts \\ [])
```

### create_file

Create File - 创建新文件对象

```elixir
create_file(connection, opts \\ [])
// 可选: :body (CreateFileRequest)
```

### create_file_version

Create File Version - 创建新文件版本

创建 Version 后，需要调用 `/file/{fileId}/{versionId}/file/start` 开始文件上传

```elixir
create_file_version(connection, file_id, opts \\ [])
// 可选: :body (CreateFileVersionRequest)
```

### delete_file

Delete File - 删除文件对象

```elixir
delete_file(connection, file_id, opts \\ [])
```

### delete_file_version

Delete File Version - 删除特定版本的文件

**限制**：只能删除最新版本

```elixir
delete_file_version(connection, file_id, version_id, opts \\ [])
```

### download_file_version

Download File Version - 下载指定版本的文件

**版本注意**：Version 0 是文件创建时间，实际数据通常在 version 1 及以上
**扩展名注意**：文件不保证有扩展名，UnityPackage 文件通常有扩展名

```elixir
download_file_version(connection, file_id, version_id, opts \\ [])
```

### 文件上传流程

```elixir
# 1. 开始上传 - 获取 AWS URL
start_file_data_upload(connection, file_id, version_id, file_type, opts \\ [])
// 可选: :partNumber

# 2. 检查上传状态
get_file_data_upload_status(connection, file_id, version_id, file_type, opts \\ [])

# 3. 完成上传
finish_file_data_upload(connection, file_id, version_id, file_type, opts \\ [])
// 可选: :body (FinishFileDataUploadRequest)
// 注意：上传 Avatar 和 World 的 file 后还需要上传 signature 文件
```

### get_file_analysis

Get File Version Analysis - 获取上传资源的性能分析

```elixir
get_file_analysis(connection, file_id, version_id, opts \\ [])
get_file_analysis_security(connection, file_id, version_id, opts \\ [])
get_file_analysis_standard(connection, file_id, version_id, opts \\ [])
```

### 图片上传

```elixir
upload_image(connection, file, tag, opts \\ [])
// tag: icon, gallery, sticker, emoji, emojianimated
// 可选: :frames, :framesOverTime, :animationStyle, :maskTag

upload_icon(connection, file, opts \\ [])
upload_gallery_image(connection, file, opts \\ [])
```