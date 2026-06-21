---
source: https://vrchat.hexdocs.pm/VRChat.Authentication.html
date: 2026-06-10
SDK版本: vrchat v1.20.0 (Elixir)
---

# VRChat API 参考 - 认证模块

## 模块概述

API calls for all endpoints tagged `Authentication`.

## 函数列表

### get_current_user

Login and/or Get Current User Info

此端点执行两个操作：
1. 检查是否已登录（查找有效的 `auth` cookie）。如果未登录，则使用 `Authorization` header 登录并设置 `auth` cookie
2. 如果已登录，返回 CurrentUser 对象

**认证方式**：`Authorization: Basic {base64(urlencode(username):urlencode(password))}`

**警告：会话限制** 每次使用登录凭据进行身份验证都会算作一个单独的会话，数量有限。务必保存并重用 `auth` cookie。

```elixir
get_current_user(connection, opts \\ [])
```

### login

```elixir
login(options)
```

### logout

Logout - 使登录会话失效

```elixir
logout(connection, opts \\ [])
```

### verify_auth_token

Verify Auth Token - 验证当前提供的 Auth Token 是否有效

```elixir
verify_auth_token(connection, opts \\ [])
```

### verify_login_place

Verify Login Place - 验证用户的登录尝试

```elixir
verify_login_place(connection, token, opts \\ [])
```

### check_user_exists

Check User Exists - 检查用户名、displayName 或 email 是否已存在

**必需参数**：`username`、`displayName` 或 `email`（至少一个）

```elixir
check_user_exists(connection, opts \\ [])
# 可选: :email, :displayName, :username, :excludeUserId
```

### register_user_account

Register User Account - 注册新用户账户

**已弃用**：自动创建账户没有合法的公共第三方用例，违反 ToS §13.2

```elixir
register_user_account(connection, register_user_account_request, opts \\ [])
```

### delete_user

Delete User - 删除账户

- 普通用户只能删除自己的账户
- 账户删除需要 14 天
- VRC+ 订阅会**立即**取消
- **方法注意**：尽管是 Delete 操作，但需要 PUT 方法

```elixir
delete_user(connection, user_id, opts \\ [])
```

### confirm_email

Confirm Email - 确认用户邮箱地址

```elixir
confirm_email(connection, id, verify_email, opts \\ [])
```

### resend_email_confirmation

Resend Email Confirmation - 请求重新发送邮箱确认邮件

```elixir
resend_email_confirmation(connection, opts \\ [])
```

### 2FA 相关

| 函数 | 说明 |
|------|------|
| `enable2_fa` | 启用基于时间的 2FA 代码 |
| `disable2_fa` | 禁用当前账户的 2FA |
| `verify2_fa` | 使用 2FA 生成的代码完成登录 |
| `verify2_fa_email_code` | 使用 2FA 邮件代码完成登录 |
| `verify_pending2_fa` | 完成启用 2FA 的序列 |
| `verify_recovery_code` | 使用 OTP 恢复代码完成登录 |
| `get_recovery_codes` | 获取 OTP 恢复代码 |
| `cancel_pending2_fa` | 取消待处理的 2FA 启用 |