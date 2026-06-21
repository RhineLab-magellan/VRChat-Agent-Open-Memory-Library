---
source: https://vrchat.hexdocs.pm/VRChat.Groups.html
date: 2026-06-10
SDK版本: vrchat v1.20.0 (Elixir)
---

# VRChat API 参考 - 群组模块

## 模块概述

API calls for all endpoints tagged `Groups`.

## 函数列表

### 群组管理

| 函数 | 说明 |
|------|------|
| `get_group` | Get Group by ID - 通过 ID 获取单个群组 |
| `create_group` | Create Group - 创建群组（需要 VRC+ 订阅） |
| `update_group` | Update Group - 更新群组 |
| `delete_group` | Delete Group - 删除群组 |
| `search_groups` | Search Group - 按名称或 shortCode 搜索群组 |

### 成员管理

| 函数 | 说明 |
|------|------|
| `get_group_members` | List Group Members - 列出所有群组成员（不包含调用者） |
| `get_group_member` | Get Group Member - 获取特定成员 |
| `update_group_member` | Update Group Member - 更新成员信息 |
| `join_group` | Join Group - 加入群组 |
| `leave_group` | Leave Group - 离开群组 |
| `kick_group_member` | Kick Group Member - 踢出成员 |
| `ban_group_member` | Ban Group Member - 封禁成员 |
| `unban_group_member` | Unban Group Member - 解封成员 |
| `get_group_bans` | Get Group Bans - 获取封禁列表 |

### 角色管理

| 函数 | 说明 |
|------|------|
| `get_group_roles` | Get Group Roles - 获取群组角色 |
| `get_group_role_templates` | Get Group Role Templates - 获取角色模板 |
| `create_group_role` | Create GroupRole - 创建角色 |
| `update_group_role` | Update Group Role - 更新角色 |
| `delete_group_role` | Delete Group Role - 删除角色 |
| `add_group_member_role` | Add Role to GroupMember - 添加角色到成员 |
| `remove_group_member_role` | Remove Role from GroupMember - 移除成员角色 |

### 加入请求管理

| 函数 | 说明 |
|------|------|
| `get_group_requests` | Get Group Join Requests - 获取加入请求列表 |
| `respond_group_join_request` | Respond Group Join Request - 接受/拒绝请求 |
| `cancel_group_request` | Cancel Group Join Request - 取消发出的请求 |

### 邀请管理

| 函数 | 说明 |
|------|------|
| `create_group_invite` | Invite User to Group - 邀请用户加入群组 |
| `get_group_invites` | Get Group Invites Sent - 获取已发送的邀请列表 |
| `delete_group_invite` | Delete User Invite - 删除发出的邀请 |

### 相册管理

| 函数 | 说明 |
|------|------|
| `create_group_gallery` | Create Group Gallery - 创建相册 |
| `update_group_gallery` | Update Group Gallery - 更新相册 |
| `delete_group_gallery` | Delete Group Gallery - 删除相册 |
| `get_group_gallery_images` | Get Group Gallery Images - 获取相册图片列表 |
| `add_group_gallery_image` | Add Group Gallery Image - 添加图片到相册 |
| `delete_group_gallery_image` | Delete Group Gallery Image - 删除相册图片 |

### 公告与帖子

| 函数 | 说明 |
|------|------|
| `get_group_announcements` | Get Group Announcement - 获取群组公告 |
| `create_group_announcement` | Create Group Announcement - 创建公告 |
| `delete_group_announcement` | Delete Group Announcement - 删除公告 |
| `get_group_posts` | Get posts from a Group - 获取群组帖子 |
| `add_group_post` | Create a post in a Group - 创建帖子 |
| `update_group_post` | Edits a Group post - 编辑帖子 |
| `delete_group_post` | Delete a Group post - 删除帖子 |

### 其他

| 函数 | 说明 |
|------|------|
| `get_group_instances` | Get Group Instances - 获取群组实例 |
| `get_group_audit_logs` | Get Group Audit Logs - 获取审计日志 |
| `get_group_permissions` | List Group Permissions - 列出所有可用权限 |
| `update_group_representation` | Update Group Representation - 更新代表身份 |

## 关键说明

### 创建群组要求
- **需要 VRC+ 订阅**

### 成员列表
- `get_group_members` 永远不会返回调用端点的用户
- 关于调用者的信息必须在群组对象的 `myMember` 字段中查找

### 公告限制
- 创建公告会删除所有现有公告
- 如需正确公告，请使用帖子端点

### 代表身份
- 当 `isRepresenting` 设为 `true` 时，所有其他群组的此标志将设为 `false`