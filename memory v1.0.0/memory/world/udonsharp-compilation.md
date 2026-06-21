# UdonSharp 编译管线 ⚠️ 已迁移

> **状态**: 此文件已迁移到 `memory/world/udon/udonsharp/compilation.md`。
> **迁移日期**: 2026-06-15
> **保留原因**: 兼容旧引用路径。

---

## 📚 权威文档位置

> **请访问**: [`memory/world/udon/udonsharp/compilation.md`](udon/udonsharp/compilation.md)

---

## 关键要点（已覆盖在权威文档中）

UdonSharp 编译管线为**四阶段**:

```
Setup → Roslyn Compilation → Bind → Emit → Udon Interface Bridge
```

各阶段职责：
- **Setup**: 加载 C# 源文件到 Roslyn 语法树
- **Roslyn**: 标准 C# 编译流程（语义分析、类型检查、符号解析）
- **Bind**: 遍历语法树，生成 BoundNode 树（语义验证）
- **Emit**: 从 BoundNode 树生成 Udon Assembly 代码
- **Bridge**: 将 UASM 组装为 IUdonProgram 对象

详细数据结构、错误处理、调试方法见权威文档。

---

## 相关文档

- `memory/world/udon/udonsharp/compilation.md` — **权威文档**
- `memory/world/udon/udonsharp/index.md` — UdonSharp 总览
- `memory/rules/udonsharp-language-limits.md` — UdonSharp 语言限制
- `memory/rules/udon-vm-architecture.md` — Udon VM 架构
- `memory/api/udonsharp-runtime.md` — UdonSharpBehaviour 运行时系统
- `memory/world/udon/vm-and-assembly.md` — Udon 字节码规范

---

## 迁移审计

| 项 | 旧文件 | 新文件 | 覆盖度 |
|----|--------|--------|--------|
| 四阶段编译流程 | ✅ 有 | ✅ 有 | 100% |
| 关键数据结构 | ✅ 有 | ✅ 有 | 100% |
| 错误处理 | ✅ 有 | ✅ 有 | 100% |
| 对开发者意义 | ✅ 有 | ✅ 有 | 100% |

> **结论**: 内容完全保留并已整合到新位置。请更新引用。
