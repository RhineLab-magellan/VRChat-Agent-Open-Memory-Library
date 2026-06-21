# VRCGraphics & VRCShader API ⚠️ 已迁移

> **状态**: 此文件已被整合到 `memory/world/udon/vrc-graphics/` 子目录。
> **迁移日期**: 2026-06-15
> **保留原因**: 兼容旧引用路径；内容已完全覆盖在下方链接的文档中。

---

## 📚 权威文档位置

> **请访问以下文档获取完整内容**：

| 主题 | 权威文档 |
|------|---------|
| VRCGraphics/VRCShader 总览 | [`memory/world/udon/vrc-graphics/index.md`](udon/vrc-graphics/index.md) |
| VRCAsyncGPUReadback 详细 | [`memory/world/udon/vrc-graphics/asyncgpureadback.md`](udon/vrc-graphics/asyncgpureadback.md) |
| `_VRChat*` 全局变量 | [`memory/world/udon/vrc-graphics/vrchat-shader-globals.md`](udon/vrc-graphics/vrchat-shader-globals.md) |
| VRCCameraSettings | `memory/world/vrc-camera-settings.md` |
| VRCQualitySettings | `memory/world/vrc-quality-settings.md` |

---

## 关键要点（已覆盖在权威文档中）

- **VRCShader 属性名必须以 `_Udon` 为前缀**，否则 `SetGlobal` 静默失败
- **VRCGraphics.Blit 在 Quest GPU 上不工作**，除非 Shader 加 `ZTest Always` 或关闭 RT depth
- **`_VRChat*` 是受保护命名空间**，不要在自定义 Shader 中使用
- 详细 API 列表、Quest 兼容、性能考量见权威文档

---

## 迁移审计

| 项 | 旧文件 | 新文件 | 覆盖度 |
|----|--------|--------|--------|
| VRCShader API | ✅ 简表 | ✅ 完整 | 100% |
| VRCGraphics API | ✅ 简表 | ✅ 完整 | 100% |
| VRChat Shader Globals | ✅ 部分 | ✅ 完整 | 100% |
| Quest GPU 限制 | ✅ 有 | ✅ 详细 | 100% |
| 性能考量 | ✅ 简述 | ✅ 详细 | 100% |

> **结论**: 旧文件内容已 100% 覆盖，无信息损失。请更新引用以指向权威文档。
