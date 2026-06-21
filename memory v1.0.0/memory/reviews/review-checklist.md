# Review Checklist: UdonSharp Script Review

> Type: CHECKLIST
> Confidence: High
> Last Updated: 2026-06-04

---

Agent 审查 UdonSharp 脚本时必须逐项检查以下 15 点：

## 1. 基础身份

- [ ] 是否继承 `UdonSharpBehaviour`？
- [ ] `BehaviourSyncMode` 是什么？（NoVariableSync / Manual / Continuous）
- [ ] 该 SyncMode 是否匹配脚本的实际需求？

## 2. 语言合规

- [ ] 是否使用了 `List<T>`？
- [ ] 是否使用了 `Dictionary<TKey, TValue>`？
- [ ] 是否使用了 LINQ / lambda？
- [ ] 是否使用了 `async`/`await`？
- [ ] 是否使用了 `try`/`catch`/`throw`？
- [ ] 是否使用了 Coroutine？
- [ ] 是否使用了复杂泛型或委托？

## 3. API 合规

- [ ] 所有 API 调用是否被 Udon 暴露？
- [ ] 是否使用了 `GameObject.Find()` 在热路径中？
- [ ] 是否使用了 `GetComponent<T>()` 在热路径中？
- [ ] 是否有不确定可用性的 API？

## 4. 网络同步

- [ ] `[UdonSynced]` 变量是否都由 owner 写入？
- [ ] Manual Sync 修改后是否调用了 `RequestSerialization()`？
- [ ] 是否有 owner 检查保护非 owner 写入？
- [ ] Network Event 使用是否合适（仅用于瞬时效果）？
- [ ] 是否存在 late joiner 无法恢复的状态？

## 5. Late Joiner 正确性

- [ ] 晚加入玩家能否通过 `[UdonSynced]` 恢复所有必须状态？
- [ ] `OnDeserialization()` 是否正确处理了所有状态恢复？
- [ ] 是否存在仅靠 Network Event 传输但 late joiner 需要的状态？

## 6. Ownership Path

- [ ] owner 离开后对象行为是否正确？
- [ ] `OnOwnershipTransferred()` 是否处理了必要的重置或继续？
- [ ] 非 owner 修改状态的流程是否正确？

## 7. 数据结构

- [ ] 是否有可本地派生却被同步的数据？
- [ ] 多个 bool 是否可以合并为 bit flags？
- [ ] 是否用 int/enum 代替了字符串状态？
- [ ] 数组大小是否合理？

## 8. 性能：代码执行步骤

- [ ] 是否有不必要的 `Update()`？
- [ ] `Update()` 中是否有早期 return 或节流？
- [ ] 是否有不必要的数组遍历？
- [ ] 高频路径中是否有字符串操作？
- [ ] 引用是否在 `Start()` 中缓存？

## 9. 性能：网络带宽

- [ ] 同步变量数量是否最小化？
- [ ] Continuous Sync 使用是否恰当？
- [ ] 同步字段大小是否合理（避免大数组、长字符串）？
- [ ] `RequestSerialization()` 调用频率是否受控？

## 10. 性能：多 VM 协作

- [ ] 是否拆分过多 UdonBehaviour？
- [ ] 是否频繁跨 Behaviour 调用热路径？
- [ ] 是否有链式 `SendCustomEvent` 派发？
- [ ] 高频相关逻辑是否可以合并？

## 11. 冲突处理

- [ ] 多人同时操作是否有防护？
- [ ] 重复快速点击是否有 debounce？
- [ ] 是否存在竞态条件？

## 12. 错误处理

- [ ] 数组越界是否有检查？
- [ ] 空引用是否有 null 检查？
- [ ] 是否有防御性的边界条件处理？

## 13. 可维护性

- [ ] `[SerializeField]` 是否公开了必要的 Unity 绑定？
- [ ] 变量命名是否清晰？
- [ ] 关键数字是否用 const 或 SerializeField 代替魔法数字？
- [ ] 代码结构是否清晰？

## 14. 测试覆盖

脚本是否在以下场景合理：
- [ ] 单人使用
- [ ] 双人测试
- [ ] owner 转移
- [ ] late joiner
- [ ] 重进房间

## 15. 总体风险

按以下等级给出总体评分：
- **严重**: 会导致编译失败、运行时崩溃、网络状态错误、late joiner 数据丢失
- **中等**: 性能问题、不必要的同步开销、潜在的竞态条件
- **轻微**: 代码风格、可读性、轻微浪费
