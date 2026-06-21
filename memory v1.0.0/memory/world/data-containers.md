# Data Containers & VRCJson ⚠️ 已迁移

> **状态**: 此文件已迁移到 `memory/world/udon/data-containers/` 子目录。
> **迁移日期**: 2026-06-15
> **保留原因**: 兼容旧引用路径。

---

## 📚 权威文档位置

> **请访问以下文档**：

| 主题 | 权威文档 |
|------|---------|
| **Data Containers 总览** | [`memory/world/udon/data-containers/index.md`](udon/data-containers/index.md) |
| **Byte/Bit Operations（位域压缩）** | [`memory/world/udon/data-containers/byte-and-bit-operations.md`](udon/data-containers/byte-and-bit-operations.md) |
| **位域压缩 Pattern** | `memory/patterns/bit-packed-flags.md` |

---

## 关键要点（已覆盖在权威文档中）

- **DataToken 类型**: Null/Boolean/Byte/Int/Float/String/DataList/DataDictionary/Reference/DataError
- **DataList / DataDictionary**: 基础操作、克隆、JSON 序列化
- **JSON 限制**: 仅字符串键、根只能是 List/Dict、不支持 Reference、不支持 NaN/Infinity
- **位域压缩**: 8 个 bool → 1 个 byte，节省 87.5% 序列化空间
- **核心工具**: `DataToken.Bitcast()` / `System.BitConverter` / `System.Buffer`

---

## 相关文档

- `memory/world/udon/data-containers/index.md` — **总览**
- `memory/world/udon/data-containers/byte-and-bit-operations.md` — **位/字节操作**
- `memory/api/networking.md` — 网络同步模式
- `memory/patterns/bit-packed-flags.md` — 位域压缩 Pattern
- `memory/rules/udonsharp-language-limits.md` — 集合类型限制（List/Dictionary 禁用）

---

## 迁移审计

| 项 | 旧文件 | 新文件 | 覆盖度 |
|----|--------|--------|--------|
| DataToken 类型表 | ✅ 有 | ✅ 有 | 100% |
| DataList/Dictionary API | ✅ 有 | ✅ 有 | 100% |
| VRCJson 序列化 | ✅ 有 | ✅ 有 | 100% |
| JSON 限制 | ✅ 有 | ✅ 有 | 100% |
| 性能考虑 | ✅ 有 | ✅ 有 | 100% |
| Byte/Bit 工具 | 🔗 引用 | ✅ 完整 | 100% |

> **结论**: 内容完全保留并已整合到新位置。请更新引用。
