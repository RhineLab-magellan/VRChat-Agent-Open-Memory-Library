# Avatar 改模教学法 & 问题诊断框架

> 来源 A: vrnavi.jp 教程分析 (2026-06-17)
> 来源 B: vrcmaster.com 教程分析 (2026-06-17) ⭐NEW
>
> **定位**: 不是教"如何改模"，而是教"**如何教导别人改模**"以及"**如何给玩家提供有意义的问题解决方案**"
>
> **适用对象**: 面对"少量 Unity / 动画器 / Avatars3 基础"的玩家
>
> **双源互补**: A 来源偏"vrnavi 深度系列型"、B 来源偏"vrcmaster 工具链普及型"——两者结合可形成覆盖更广的教学技巧库
>
> **⭐NEW 2026-06-17**: 第三来源 **Kuriko**(HackMD 教程)风格分析已加入第三部分,与前两源形成 **"深度系列 + 工具链普及 + 工程实践百科"** 三足鼎立。
>
> **⭐NEW 2026-06-17 第四来源补充**: **MA Samples 页面**(现成 Prefab 拆解型教学) 学习加入"MA 官方教程风格分析"扩展,新增"用现成 Prefab 拆解教学"3 条新原则(原则 43-45);Samples 拆解内容独立入 `modular-avatar.md` §9.6。

---

## 一、教程核心结构（两篇范文）

| 维度 | dressup-ma（换装教程） | modular-avatar-komono（小物件教程） |
|------|------------------------|-------------------------------------|
| **结构** | 严格时间线 + 极细颗粒度 | 线性极简（5 步） |
| **目录深度** | 4 层嵌套（`2.1.3.1`） | 1 层 |
| **章节规则** | 1 节 = 1 个具体动作 | 1 篇 = 1 个完整流程 |
| **预估时间** | 顶部明示"45-90 分" | 无（流程简单） |
| **外链策略** | 假设 4 件事已完成的"前置门控" | 几乎所有上下文外链到 dressup-ma |

**核心结论**: 不要写"百科级单篇万字文"，要写"**主题级深度的系列文章**"。一个改模任务 = 一篇文章；通用 Unity 知识 = 另一篇。

---

## 二、10 条核心教学原则

### 原则 1 — 用"前置门控"假设读者水平

- **开篇明示**："本文是给已经完成 X、Y、Z 的人看的"
- 把基础门槛交给独立文章
- **避免每篇都从零讲起的水文感**

### 原则 2 — 目录颗粒度 = 1 节 1 动作

- 让读者可以"读完一节就停下做一节"
- 不要把 5 步塞进"大节"

### 原则 3 — 标注预估时间

- "45-90 分"比"需要一些时间"更减压
- 玩家会安排自己的时间

### 原则 4 — 创造"老手角色"插入口语化贴士

- 作者用 "たろ"、"いそ" 两个角色写短句吐槽
- 模拟"有经验的同事坐在旁边提醒你"
- **降低初学者孤独感** + 让冷冰冰 UI 步骤有温度

### 原则 5 — 术语放脚注，主流程保持纯净

- 主流程不被术语打断
- 脚注提供"深入查阅"的窗口
- **扫一眼脚注不会漏**，**跳过脚注不会卡**

### 原则 6 — 教"系统成功/失败状态的视觉特征"

新手最大障碍不是"不会做"，而是"**不知道现在算不算成功**"。

| 视觉信号 | 含义 | 教学时机 |
|----------|------|----------|
| **粉红 Prefab** | 缺失文件 | 衣装导入前 |
| **红框 Validation** | 上传阻塞 | 上传前 |
| **灰→白加粗** | MA 启用成功 | 项目设置时 |
| **Armature vs Mesh** | 区分骨骼与网格 | 微调时 |
| **细线状身体** | BlendShape 压缩 | 衣装穿戴前 |

### 原则 7 — 用"症状→原因→对策 checklist"代替"操作步骤"

- 尤其在**故障排查段**
- 例子：上传失败的 6 项 checklist
- **让读者学会"自己排查"而不是"只会照做"**

### 原则 8 — 诚实承认工具陷阱

- "Console 错误可能不指向真正出错的地方"（反直觉提醒）
- "一个滑块控制 8 个 keys"（控件与作用范围不一致）
- **承认工具的反直觉特性，反而建立信任**

### 原则 9 — 主动说"可以停在这里"

- "微调是无限深渊"
- 告诉读者"BlendShape 调完就够"
- 防 burnout

### 原则 10 — 形成"教学网络"而非"单篇文章"

- 本文末尾引下一篇，下一篇又引 Ex 菜单
- **让读者在每篇文章末尾都有"下一步可去哪"的方向感**

---

## 三、玩家常见踩坑点（教学时主动预防）

### 高频踩坑 1: 粉红 Prefab Asset

**症状**: Prefab 资源在 Unity 中显示为荧光粉色
**原因**: 必要文件缺失（材质/Shader/纹理）
**对策**:
- 教学时主动展示"正常 Prefab"vs"粉红 Prefab"对比图
- 引导查"衣装附带说明书"或"销售页"
- 提及 VRChat Creator 资源常见依赖：lilToon、SCSS、Poiyomi 等

### 高频踩坑 2: FBX vs Prefab 混淆

**症状**: 拖入 Avatar 的不是衣装，是 FBX
**原因**: Unity 中 FBX 和 Prefab 图标相似
**对策**:
- 教"看 Inspector 标签确认是 Prefab Asset"
- FBX 是 3D 模型原始文件，Prefab 是 Unity 内部格式
- **可以拖的是 Prefab，FBX 必须先转 Prefab**

### 高频踩坑 3: Hierarchy 放置位置错误

**症状**: 衣装位置错乱、动画不跟手
**原因**: Modular Avatar **以第一次配置的位置为基准**
**对策**:
- 必须直接拖到 Avatar 文件夹内
- 不要放在场景根目录
- 错放后要 Delete 再放，不能用 Move

### 高频踩坑 4: BlendShape 联动陷阱

**症状**: 调整一个 ShapeKey 时，多个部位连带变化
**原因**: 一个 ShapeKey 滑块可能同时控制 8-10 个子 ShapeKey
**对策**:
- 教"调整前先观察哪些部位会动"
- "先全归 0 再单独调"
- 列出"常用 ShapeKey 联动表"（Shrink_Stocking、Breast_xxx 等）

### 高频踩坑 5: 误删部件

**症状**: 删除了不该删的 Avatar 部件
**原因**: 不知道 Inspector 顶部"启用开关"和"删除"的区别
**对策**:
- **教"取消勾选"而不是"删除"** 作为临时隐藏
- 误删可以重新选 + 勾选回来
- 删除不可逆，隐藏可恢复

### 高频踩坑 6: 上传前 Validation 红框

**症状**: 红框三角形错误阻止上传
**原因**: 多种（材质缺失、性能超限、参数未声明等）
**对策**:
- 教"先看红框 AutoFix 按钮"
- Console 错误**可能不指向真正出错的地方**（重点提醒）
- 给出"症状-原因-对策"6 项 checklist

### 高频踩坑 7: 非专用衣装不会动

**症状**: 把衣装拖进 Avatar 后衣装不跟随身体
**原因**: 衣装 Prefab 内部没有 MA 组件（不是"MA 专用设置"）
**对策**:
- 教"看 Inspector 是否有 MA 组件"判断专用 vs 非专用
- 非专用的: 右键 → MA → Setup Outfit 自动添加
- 专用的: 直接放即可

---

## 四、玩家常见问题分类（给方案时使用）

| 类别 | 典型问题 | 方案焦点 |
|------|----------|----------|
| **A. 不会安装** | VCC 是什么？MA 怎么装？ | 工具链教学、前置门控 |
| **B. 衣装不显示** | 拖进去看不见 | 粉红 Prefab、FBX 误用、放置位置错 |
| **C. 衣装不跟随** | 衣装站桩不动 | MA 组件缺失、Setup Outfit 未执行 |
| **D. 身体穿模** | 手/脚从衣服穿出来 | BlendShape 调整、衣装微调 |
| **E. 上传失败** | 红框 Validation | 6 项 checklist、Console 排查 |
| **F. 动作奇怪** | 抬手变形、Bike Pose | Avatar Pose Matcher、原始 FBX 替换 |
| **G. 性能问题** | Poor 等级、卡顿 | AAO、NDMF 工具链、轻量化系列 |
| **H. 跨平台** | Quest 上看不到 | iOS/Android 对应、Impostor 设置 |

**回答时**: 先判断玩家在哪个类别 → 用"症状-原因-对策"框架给出具体方案 → 提供 1-2 个具体资源链接（VPM 链接、支援世界名、相关文档）

---

## 五、关键术语的口语化翻译

| 专业术语 | 通俗说法 | 教学时机 |
|----------|----------|----------|
| **Prefab Asset** | "設計図、Assets 内の素材から Unity 内でオブジェクトを組み立てるためのレシピ本" | 介绍 Prefab 时 |
| **Material Error（マテリアルエラー）** | "3D オブジェクトを構成する見た目関連のデータであるマテリアルが欠損、もしくは正常に動作しない状態" | 解释粉红 Prefab 时 |
| **Armature** | "3D モデル上で人の動きを再現するための人間の骨格を模した構造" | 教微调选 Bone 时 |
| **BlendShape** | "体の部位の形をスライダーで変形させる機能" | 教脱衣/微调时 |
| **Hierarchy** | "Unity 画面左侧的场景对象树状结构" | 教场景操作时 |
| **Inspector** | "Unity 画面右侧的属性面板" | 教属性调整时 |
| **VCC** | "VRChat 官方推出的包管理工具" | 介绍工具链时 |
| **MA** | "Modular Avatar 的缩写，让非程序也能做 Avatar 改模的工具" | 工具链介绍时 |

---

## 六、推荐资源（教学引导用）

### 测试支援世界

- **Avatar Testing Chamber by Ziggor** — 立体镜、简易舞蹈、改変支持功能
  - **特征**: 軽量（轻量）、改変初心者から上級者まで
  - **教学话术**: "改変时去这个 World 测，比直接在游戏里测效率高 10 倍"

### 桌面 vs VR 互补测试

- **桌面**: 手軽、效率高
- **VR**: 真实感强、能发现桌面看不到的破绽
- **教学话术**: "Desktop 跑一遍 + VR 跑一遍 = 完整测试"

---

## 七、推荐的下一步教学路径

```
[已掌握基础]
   ↓
1. 衣装换装（dressup-ma 范畴）
   ↓
2. 小物件/配饰（modular-avatar-komono 范畴）
   ↓
3. Ex 菜单做衣装切换（lilycalInventory 范畴）
   ↓
4. 表情改変（FaceEmo、FaceMixer 范畴）
   ↓
5. 优化（AAO、NDMF 工具链、Meshia）
   ↓
6. 跨平台（Quest/iOS 对应、Impostor）
   ↓
7. 高级（PhysBone、Constraint、Chimera 改変）
```

**教学策略**: 每篇文章都明确"下一步去哪"，形成学习路径网

---

## 八、回答玩家问题的 5 步流程

1. **归类**: 玩家问题属于 A-H 哪一类？
2. **追问**: 哪个具体症状？（避免直接给"完整教程"）
3. **最小可行方案**: 给"症状-原因-对策"中**最可能**的那一项
4. **验证步骤**: 教玩家"如何自己确认方案生效"
5. **下一步**: 引导到"如果没解决，看 X 文档"或"试试 Y 工具"

**反例**: 玩家说"衣装不显示" → 直接甩"VCC 教程"全 50 屏
**正例**: 玩家说"衣装不显示" → 问"是粉红色还是看不见？穿了但不跟手？" → 给具体检查项

---

## 九、自我检查清单（写教程/给方案前）

- [ ] 是否假设了读者的水平？是否明确写了"前置条件"？
- [ ] 章节是否 1 节 = 1 动作？
- [ ] 是否有预估时间？
- [ ] 是否教了"成功状态的视觉特征"？
- [ ] 是否主动提示"常见踩坑点"？
- [ ] 是否承认了"工具的反直觉特性"？
- [ ] 是否说"可以停在这里"？
- [ ] 末尾是否引导到下一篇/下一步？
- [ ] 故障排查是否用"checklist"而不是"叙述"？
- [ ] 是否避免了"先甩完整教程"的甩锅式回答？

---

## 来源

- 教程 1: https://vrnavi.jp/dressup-ma/ - "Modular Avatar を使った対応衣装の着せ替え方（改変の第1歩）"
- 教程 2: https://vrnavi.jp/modular-avatar-komono/ - "Modular Avatarで小物・アクセサリーの付け方"

---

# 第二部分:vrcmaster.com 教学风格分析 (2026-06-17)

> 与第一部分的"vrnavi 深度系列型"不同,vrcmaster 是"**工具链普及型**"——以"零基础也能搞定"为核心目标,文章数量大、覆盖广、单篇短小。
> 共有 10 篇相关教程,涵盖:Unity 装→VCC 装→Modular Avatar 装→Avatar 导入→衣装穿着→纹理替换→粉色修复→工具/资源推荐。

## A. vrcmaster 站点概览

| 类别 | 教程 | 字数 | 教学目标 |
|------|------|------|----------|
| **环境搭建链** | Unity 2022.3.22f1 安装 | 4500 | 装正确版本的 Unity |
| | VCC 安装 + 项目模板 | 3500 | 创建 Avatar 项目 |
| | Avatar 导入 + 上传 | 3300 | 把 .unitypackage 变可穿 Avatar |
| **核心改模** | Avatar 穿衣服 | 3550 | 5 STEP 走完穿衣流程 |
| | Modular Avatar 入门 | 3000 | 装 MA 并做 ON/OFF Toggle |
| **概念解释** | 什么是 Texture | 2200 | 幼儿园级讲清 Texture/Material/Shader |
| **故障排除** | 粉色 Avatar 修复 | 2200 | 解决 3 大原因 |
| | 纹理/PNG 替换 | 2550 | 2 种换图方法 |
| **工具 & 资源** | BOOTH Library Manager | 3400 | 资源管理工具 |
| | 免费 Avatar 资源 5 选 | 2950 | 推荐 5 个新手友好资源 |

**站点特征**:
- 标题统一带"【2026年最新版/2026年版】"强调时效
- 站内有"## カテゴリー"和"## 最近"两大导航,强调整站结构清晰
- 单篇 2000-4500 字符,**深度浅但入口多**,适合"看一眼就能上手"

## B. vrcmaster 的 12 条核心教学原则(可与第一部分互补)

### 原则 11 — "陪伴式"语气(いっしょに)

- 称呼读者 "**初心者さん**" / "**そんなあなた**",自称 "**いっしょにやっていきます**"
- 大量 "**〜してみましょう**"(一起来试试) "**〜ましょう**"(一起做吧) "**〜ね！**" 句尾
- 收尾必给"心理按摩":"**最初の『小さな成功体験』をしっかり積むことができましたね！**"
- **效果**: 把教程从"说明书"变成"朋友陪你做"

### 原则 12 — emoji 标题体系(可扫读)

- 标题段一律带 emoji:`🎯` 目标 / `🌸` 预备 / `👗` 分类 / `⚠️` 注意 / `🧰` 工具 / `💬` 补充 / `✅` 成功 / `🎉` 总结
- **效果**: 读者扫一眼就能定位自己关心的章节
- 配对使用 `🔰`(易错点) `❌`(失败) `💡`(提示) `📌`(备忘) `🔗`(链接)

### 原则 13 — 三段式拆解专业概念

- **先说"会出什么问题"**(动机会话) → **再命名"这叫 XXX"**(术语) → **再说"工具一键搞定"**(解法)
- 例子: "衣装がズレたり" → "这叫 Root Bone" → "Setup Outfit 一発で完了"
- **效果**: 把"为什么学这个"和"学了这个怎么解"连成一条线

### 原则 14 — 幼儿园级比喻系统

| 专业术语 | 比喻 | 教学时机 |
|----------|------|----------|
| **骨骼 (Bone)** | "骨組み(ボーン)"——身体里的骨架 | 教 Avatar 结构时 |
| **Texture** | "画了颜色/图案的"**布**"或"**シール(贴纸)**"" | 讲 Texture 概念时 |
| **Material** | "决定这块**布怎么呈现**" | 讲 Material 时 |
| **Shader** | "决定 Avatar 外观(髪や服の質感)的**机制**" | 讲 Shader 时 |
| **.unitypackage** | "Avatar 的**设计图和素材包**" | 解释导入时 |
| **Unity** | "**ゲーム制作ソフト**" | 解释 Unity 时 |
| **VCC** | "**包管理工具**" / "**必須級**"(必装级) | 解释 VCC 时 |
| **Modular Avatar** | "**救世主**" / "**強い味方**" | 解释 MA 时 |
| **Kisekae Prefab** | "**着せ替え用 Prefab**" | 解释换装时 |

**核心原则**: 比喻必须用读者**日常一定见过的物品**——布/贴纸/骨/布偶/设计图,而不是技术比喻。
**反例**: 不要说"Shader 是 GPU 上的程序"——初学者会卡在"GPU 是什么"上

### 原则 15 — 戏剧化开场(代入感)

- 用第二人称对话/惊呼切入:"「えっ！？アバターが全身ピンクに！？なんで…？」"
- 瞬间让读者代入"我遇到过"或"我害怕遇到"的场景
- **效果**: 拉近距离 + 制造"这个教程对我有用"的感觉
- **使用时机**: 故障排除类文章效果最好

### 原则 16 — 反复心理安抚(去焦虑)

- "**大丈夫!**" / "**直し方はとてもカンタン**" / "**初心者の方がほぼ必ず一度は通る壁**"
- 把"踩坑"正常化为"成长必经一步"
- **效果**: 显著降低初学者"这好难我不行"的心理门槛
- **使用时机**: 故障排除 + 概念解释 + 流程总结

### 原则 17 — "先修心,后修手"结构

- 每篇都遵循 "**问题 → 安心话 → 原理(比喻) → 步骤 → Q&A → 鼓励**" 流程
- 先让读者"不怕",再讲操作
- **效果**: 防止读者中途放弃

### 原则 18 — 跨文章互链(形成"概念网")

- Texture → Material → Shader 三篇互相链接
- Avatar 导入 ↔ 服装穿着 ↔ MA 入门 形成依赖链
- 读者随时可查
- **效果**: 站内无"信息孤岛"

### 原则 19 — 严守版本号(防踩坑核心)

- **Unity 版本: 2022.3.22f1**(VRChat 官方推荐,反复出现 5+ 次)
- **VCC 模板: "Unity 2022 Avatar Project"**(必须严格配套)
- **lilToon**(必装 Shader) / **Modular Avatar**(必装级) / **AMC**(Avatar Menu Creator,推荐)
- **效果**: 数字层面的硬性约束是改模最大踩坑来源之一
- **教学话术**: 反复强调"必须这个版本"+"为什么必须是这个版本"

### 原则 20 — 工具评测型 + 资源推荐型 固定模板

#### 工具评测型(BOOTH Library Manager 范本)
1. 个人痛点共鸣开篇
2. "こんな人におすすめ"读者画像
3. 一句话工具定义
4. 三大神功能分点
5. STEP 实践步骤
6. 进阶玩法
7. FAQ
8. 总结三句话卖点
9. 版权声明

#### 资源推荐型(免费 Asset 5 选 范本)
每个资源配:
- 风格定位
- ✅ 核心卖点(3 条内)
- 対応アバター列表
- 導入アドバイス(MA/AMC 用法)
- ⚠️ 特殊注意点(如 Trust Rank 截止条件)
- BOOTH 链接

文末附**导入前チェックリスト**(規約/対応/シェーダー/Unity 版本)

### 原则 21 — 工具的"反直觉"特性诚实承认

- 例子:"『Android SDK and NDK License Terms from Google』是正常画面,不是坑"
- 例子:"首次启动**不要点**"Install Unity Editor"——会装到非 VRChat 支持版本"
- **效果**: 反直觉提醒反而建立信任

### 原则 22 — 版权/合法改変声明(站尾)

- 几乎每篇都带"**著作権・改変に関するご案内**"
- 声明"使用官方 SDK 的合法步骤"+"图片经制作者许可"
- **效果**: 营造可信赖氛围 + 避免法律风险
- **建议**: 玩家问到"这样做会不会违规"时,主动引导到此声明

## C. vrcmaster 风格的"上手 5 步"主教程结构

以 `avatar-clothing-guide`(穿衣服主教程)为范本:

```
📦 STEP1: 导入
🧍‍♀️ STEP2: 拖入 Hierarchy
🛠 STEP3: 工具一键连接(Setup Outfit)
👚 STEP4: 整理原衣装
🚀 STEP5: 上传
```

**结构特点**:
- 每步 2-4 行,极简
- 5 步 = 5 个 emoji 标题 = 5 个"做完就前进一格"的奖励节点
- **零代码、零手动、零调试**(只点鼠标)

**回答玩家"怎么给 Avatar 穿衣服"时**: 直接套用这个 5 步结构,改用中文表达。

## D. 10 篇教程的"内容地图"

```
                       ┌─ Unity 安装 (unity-install-guide)
                       ├─ VCC 安装 (vcc-install-guide)
                       └─ Avatar 导入 (avatar-import-guide) ←━━┓
                                                              ┃
                       ┌─ 服装穿着 (avatar-clothing-guide) ←━━┫
                       ├─ MA 入门 (modular-avatar-install)   ←━━┛
                       │
    概念解释  ─────────┼─ 什么是 Texture (what-is-texture)
                       ├─ 纹理替换 (avatar-texture-replace)
                       └─ 粉色修复 (avatar-pink-fix)
                       
    工具 & 资源 ────────┼─ BOOTH Library Manager
                       └─ 免费 Asset 5 选
```

**关键依赖链**:
- Unity → VCC → Avatar 导入 → 服装穿着 → MA 入门(单向,不可跳)
- 概念解释 3 篇互相引用,可独立阅读
- 工具 & 资源 2 篇与其他篇无强依赖,可作为"扩展阅读"

## E. vrcmaster 风格与 vrnavi 风格对比

| 维度 | vrnavi(第一部分) | vrcmaster(第二部分) |
|------|------------------|---------------------|
| **核心目标** | 深度教程(单一任务讲透) | 普及教程(覆盖面广) |
| **目标读者** | 有基础,想精通 | 完全零基础,想上手 |
| **单篇长度** | 长(深度) | 短(浅入) |
| **目录深度** | 4 层(`2.1.3.1`) | 1 层(平铺) |
| **代码展示** | 较多 | 几乎无 |
| **比喻系统** | 较少(术语为主) | 极丰富(布/贴纸/布偶/设计图) |
| **语气** | 亲切但偏正式 | 极度口语+emoji |
| **故障排除** | 6 项 checklist | 3 大原因式 |
| **末尾** | "下一步"引导 | 心理按摩 + 流程图 |
| **适用场景** | "我想做 X,讲透" | "我想入门 X,先看看" |

**综合使用建议**:
- 玩家**第一次问"改模怎么做"** → 用 vrcmaster 风格的 5 步结构 + emoji 比喻
- 玩家**追到具体细节**(如"Setup Outfit 之后如何微调") → 切到 vrnavi 深度风格
- 玩家**报错/故障** → 用 vrcmaster 戏剧化开场 + vrnavi checklist 收尾

## F. 回答玩家问题的 5 步流程(升级版)

整合 vrcmaster 与 vrnavi 两套:

1. **归类**: 玩家问题属于 A-H 哪一类？
2. **戏剧化开场**(vrcmaster): "哎?这问题是不是 XX 引起的?" 拉近距离
3. **心理安抚**(vrcmaster): "这种坑新手基本都踩过,别慌"
4. **症状-原因-对策 checklist**(vrnavi + vrcmaster 3 大原因式)
5. **下一步**(vrnavi): 引导到"如果没解决,看 X 文档"或"试试 Y 工具"

**反例**: 玩家说"粉色 Avatar" → 直接甩"导入 lilToon"一句话(不够!)
**正例**: 玩家说"粉色 Avatar" → "「えっ！？ピンクになっちゃった！？それ、初めて改模する方がほぼ必ず通る道です💦」" → 3 大原因 → 一步一步对策

## G. vrcmaster 风格的"禁忌"

| 禁忌 | 反例 | 正例 |
|------|------|------|
| 不要说"专业术语"而不解释 | "先 Setup Root Bone" | "先把**腰の骨(Hips)** に衣装を接続します" |
| 不要"假设玩家知道" | "装 lilToon 就行" | "lilToon 是 VRChat 改模最常用的 **Shader**(画材)" |
| 不要"步骤过长" | 1 节塞 10 步 | 1 节 2-4 步 |
| 不要"忽略心理感受" | "导入完成" | "✅ **完了です！** 第一个小目标达成！" |
| 不要"无 emoji 长段" | 一屏黑字 | emoji 当路标 |
| 不要"假设读者会看完全文" | 不分段 | 段首 1 句话点出本段目标 |

## H. vrcmaster 来源的教程列表(本批次)

| 教程 | URL |
|------|-----|
| Avatar 穿衣服 | https://vrcmaster.com/avatar-clothing-guide/ |
| Unity 装 | https://vrcmaster.com/unity-install-guide-vrchat/ |
| VCC 装 | https://vrcmaster.com/vcc-install-guide-vrchat/ |
| Avatar 导入 | https://vrcmaster.com/vrchat-avatar-import-guide/ |
| MA 入门 | https://vrcmaster.com/modular-avatar-install/ |
| 什么是 Texture | https://vrcmaster.com/what-is-texture/ |
| 纹理替换 | https://vrcmaster.com/vrchat-avatar-texture-replace/ |
| 粉色修复 | https://vrcmaster.com/avatar-pink-fix-vrchat/ |
| BOOTH Library Manager | https://vrcmaster.com/booth-library-manager-usage/ |
| 免费 Asset 5 选 | https://vrcmaster.com/free-assets-vrc-avatar/ |

---

# 第三部分:Kuriko 风格分析 (2026-06-17)

> 与前两源不同的"**工程实践百科型**"——既不深(如 vrnavi 系列),也不短(如 vrcmaster 单篇),而是一篇**5.5 万字长文**涵盖 9 个工具 + 5 大类优化技术。**特征:可作为工具型参考长期翻阅**。
>
> 来源: https://hackmd.io/kUmtF6aTT4GhxkHRwNKSlQ
> 适用对象: 想"完整掌握 Avatar 最佳化体系"的玩家

## I. Kuriko 教学风格画像(与其他两源对比)

| 维度 | vrnavi(深度系列) | vrcmaster(普及) | **Kuriko(百科实践)** |
|------|------------------|-----------------|---------------------|
| **目标** | 单一任务讲透 | 覆盖面广 | 完整工具型参考 |
| **读者** | 有基础想精通 | 完全零基础 | 想"一文掌握全貌" |
| **篇幅** | 长(单任务) | 短(单工具) | **超长(全体系)** |
| **目录深度** | 4 层(`2.1.3.1`) | 1 层(平铺) | 2 层(章 + 节) |
| **情绪** | 亲切但正式 | 极度口语 + emoji | **温和 + 黑色幽默** |
| **故障排除** | 6 项 checklist | 3 大原因式 | **惨剧图示 + 经验外化** |
| **末尾** | "下一步"引导 | 心理按摩 | **"我们一起"的承诺** |

## J. Kuriko 独有的 12 条教学原则

### 原则 23 — 懒人包**置顶**(第一屏 5 分钟可执行)

- **位置**: 目录之后、正文之前的 `:::success` 框
- **目的**: 让"怕长文、赶时间"的玩家 5 分钟拿到 80% 优化收益
- **结构**: 5 步极简流程,每步对应后文章节
- **效果**: 留下浅度用户 → 引导深度用户读完
- **与 vrcmaster 区别**: vrcmaster 把摘要放在段落开头;Kuriko 直接独立成块,更醒目

### 原则 24 — 「代價-好處」对照框架(绝不只推优点)

每次介绍技术必说代價:
- "**唯一的代价是**,会无法开关其中某个特定物件"
- "**好处**,除了在 CPU 处理上可以降低负担,**一部分的 Material Slots 在这里也会同步合并**"
- **效果**: 让读者形成"凡操作必观代价"的工程思维

### 原则 25 — "💪 給挑戰者們" 等级挑战机制

每节末尾用 `:::warning` 包裹的进阶框:
> "想挑戰 Excellent,請把 `MergeMesh` 改成 `Body`。並將原本的 `Body` 一併扔進去"

- **基础内容**: 默认目标(Good 等级)
- **挑战者框**: 进阶玩家(Excellent 等级)
- **效果**: 难度分级,避免新手被吓退、避免老手觉得无聊

### 原则 26 — 内部锚链接"传送门"机制

- 用 `[合併 Skinned Mesh 在前面已經說過了,可以回去看看→傳送門](#Skinned-Mesh-Renderer-蒙皮網格)` 实现非线性导航
- **效果**: HackMD 相对于传统 PDF 的最大优势,读者可在概念间自由跳转

### 原则 27 — 数字具象化技巧

抽象数字 → 具体可感:
- **"4K 贴图 = 21MB VRAM"**(从抽象分辨率到具体容量)
- **"32×2 = 64 碰撞侦测数"**(从抽象公式到具体算式)
- **"Steam 統計: 8GB VRAM 是最大宗"**(从个人建议到市场数据)
- **效果**: 让玩家对"降 1 阶 = 1/4"有体感

### 原则 28 — "惨剧图"反例警示

- 教程保存"半透明材质球被合并后的慘剧"图片作为警示
- **原理**: 正向说理("请分类")易被忽略,反例展示("惨剧")被记住
- **效果**: "一次惨剧图胜过十句警告"
- **应用场景**: 合并 Skinned Mesh、Atlas 化、UV Tile 误用等

### 原则 29 — 社区贡献者显式致谢

- "感謝 **夜嵐蝶 Alma** 的知识补充"(Material Slot vs Material 概念)
- "感謝 **Touma** 分享的技巧"(liltoon 烘焙 + Merge Bone 经验)
- "感謝 **Vistanz** 的推荐这个工具"(Meshia 工具)
- **效果**:
  - 提升内容可信度
  - 营造健康的知识共享氛围
  - 鼓励其他贡献者参与

### 原则 30 — 工具维护状态明确标注

- `lilNDMFMeshSimplifier` 用 `:::warning` 标注"**已停止维护,请改用 Meshia**"
- **效果**: 对时效性负责,避免读者踩坑过时工具

### 原则 31 — 工具"作者名片"标准模板

每个工具都按统一结构介绍:
```
[工具名](官网链接) → [作者署名] → [一句话功能 + 评价] → [VCC/导入链接] → [重要提示框] → [与其他工具关系]
```

### 原则 32 — "复制 Avatar" 工作流作为安全网

- 懒人包第一步就是"**复制 Avatar 本身**"
- 让新手知道"最坏可以丢复制体",敢动手操作
- **教学心理学**: 风险预防优先于操作便利

### 原则 33 — 备份提醒 + GIF 双重置顶

- 在"开搞前"用 `:::warning` + `giphy.com` 备份 GIF 双重强化
- **效果**: 不只是文字提醒,还有视觉冲击
- **位置**: 不放文末免责声明,放正文最前

### 原则 34 — "作者未实测"诚实免责

- MA + VRCFury 共存方案标注 "⚠️ 自己沒實測過,如果出問題,或知道正確答案請告訴我"
- **教学伦理**: 标注不确定信息,反而建立信任
- **应用**: 任何引用第三方方案但未亲自验证的内容

## K. Kuriko 风格核心句式模板(可与 vrcmaster 互补)

| 句式 | 模板 | 使用场景 |
|------|------|----------|
| **承接式开场** | "X 這個東西,**沒事不要放**" | 介绍应避免的操作 |
| **懒人包开场** | "想追求更好?[把它看完。](#目錄)" | 引导深度阅读 |
| **痛点破题** | "每次跟別人對到眼,常聽到電腦好卡的哀號?" | 文章开头 |
| **风险免责声明** | "備份,Avatar 或專案炸了,頭痛的不是我,而是你哦~" | 操作前提醒 |
| **小激励收尾** | "搞定!" / "完成!" / "就這樣!" | 每步结束 |
| **进阶挑战引导** | "想挑戰 Excellent,請把..." | 章节末尾 |
| **经验外化** | "以我改裙子的心得,降低 Pull、Momentum、Immobile,效果好像比較明顯" | 主观建议 |
| **冷知识开场** | "無論原檔是 PNG、JPG、PSD,**最終的 VRAM 使用量,只會依 Unity 內的設定而改變**" | 概念澄清 |
| **并列式承诺** | "讓我們一起把 VRChat 變成性能友善的地方吧!" | 文章结尾 |

## L. Kuriko 风格的"禁忌"

| 禁忌 | 反例 | 正例 |
|------|------|------|
| **不要"只说好處"** | "合并 Skinned Mesh 让你的 Avatar 性能翻倍" | "**唯一的代价是**无法单独开关,好处是 CPU 负担降低 + Material Slot 合并" |
| **不要"假设读者看完全文"** | 长篇不分明细 | 章节 + 1-2 句目标段首 |
| **不要"隐藏不确定信息"** | 把未实测的方案直接当结论 | "⚠️ 自己沒實測過,如果出問題,請告訴我" |
| **不要"忽略社区贡献"** | 引用他人知识不署名 | "感謝 X 分享的技巧" |
| **不要"忽略工具时效"** | 推荐已停维护的工具 | 明确标注"已停止维护,请改用 X" |
| **不要"忽略备份提醒"** | 把备份放文末 | 开搞前 `:::warning` + GIF 双重置顶 |

## M. 三源融合的"综合使用指南"

面对不同类型的玩家问题,采用不同教学风格:

| 玩家问题类型 | 推荐风格 | 关键技巧 |
|--------------|----------|----------|
| **"我想改模,完全不会"** | **vrcmaster**(普及) | 5 步结构 + emoji 比喻 + 戏剧化开场 |
| **"我想做 X,讲透"** | **vrnavi**(深度) | 1 节 1 动作 + 前置门控 + 时间标注 |
| **"我想系统了解最佳化"** | **Kuriko**(百科) | 懒人包置顶 + 代價-好處 + 传送门 |
| **"我的 Avatar 哪里出问题?"** | **vrnavi checklist** | 6 项症状-原因-对策 |
| **"报错/故障"** | **vrcmaster 戏剧化 + vrnavi checklist** | "哎?踩坑很正常💦" + checklist |
| **"工具/版本怎么选"** | **Kuriko 工具名片** | 作者 + 功能 + VCC + 状态 + 维护情况 |
| **"我想长期参考"** | **Kuriko 传送门** | 内部锚链接 + 章节独立可读 |

## N. Kuriko 来源的教程(本次学习)

| 教程 | URL | 类型 |
|------|-----|------|
| **VRChat Avatar 究極輕量化、最佳化筆記 (繁中)** | https://hackmd.io/kUmtF6aTT4GhxkHRwNKSlQ | 工具型百科 |
| **VRChat Avatar Optimization Notes (英文版)** | https://hackmd.io/@kurikotw/AvatarOptimize_ENG | 翻译版(注: ChatGPT 辅助翻译,可能需勘误) |

**学习方式**: 6 个子 Agent 并行分析(工具链/性能指标/网格材质/动态骨骼/面数/教学法综合),然后由主 Agent 整合归纳。

---

## O. 自我检查清单(整合三源,2026-06-17 升级版)

写教程/给方案前:

- [ ] 玩家处于什么水平?(零基础/有基础/进阶)
- [ ] 玩家问的是哪类问题?(A-H 八类常见问题)
- [ ] 是否给出"症状-原因-对策"框架,而不是甩完整教程?
- [ ] 是否说明"代價-好處",而不仅说好處?
- [ ] 是否标注"工具维护状态"避免推荐过时工具?
- [ ] 是否引用社区贡献者时显式署名?
- [ ] 是否标注"未实测"内容避免误导?
- [ ] 是否给"懒人包 5 步"让急性子有收获?
- [ ] 是否给"挑战者框"让老手不无聊?
- [ ] 备份/不可逆操作前是否提醒?
- [ ] 故障排查是否用"checklist"或"惨剧图"?
- [ ] 末尾是否引导到"下一步去哪"?

---

# 第四部分:Modular Avatar 官方教程教学风格分析 (2026-06-17)

> **来源**:https://modular-avatar.nadena.dev/docs 的 6 个官方教程 + Samples + Component Reference
> **文档语言**: 英文(有日语翻译)
>
> **与前三源不同的"工具作者视角型"**——既不是零基础普及(vrcmaster),也不是单一任务深讲(vrnavi),更不是百科实践(Kuriko),而是**"工具作者直接教你用它"**。
> **特征:专业、克制、案例驱动、读者假设为有 Unity 基础的创作者**。

## P. MA 官方教程的 5 大风格特征

| 特征 | vrnavi (玩家创作者) | vrcmaster (普及) | Kuriko (百科) | **MA 官方 (工具作者)** |
|------|---------------------|-------------------|---------------|------------------------|
| **核心目标** | 单一任务讲透 | 覆盖广 | 完整工具型参考 | **教"如何使用我的工具"** |
| **目标读者** | 有基础想精通 | 完全零基础 | 想"一文掌握全貌" | **会装 MA + 有 Avatar 经验** |
| **篇幅** | 长(单任务深) | 短(单工具浅) | 超长(全体系) | **中短(单功能清晰)** |
| **目录深度** | 4 层 | 1 层 | 2 层 | **1-2 层** |
| **代码展示** | 较多 | 几乎无 | 较多(脚本) | **几乎无(全部 GUI 操作)** |
| **示例 Avatar** | 不用具体名 | 不用具体名 | 不用具体名 | **必用具体 BOOTH 商品** |
| **语气** | 亲切但偏正式 | 极度口语+emoji | 温和幽默 | **克制、技术、不讨好** |
| **故障排除** | 6 项 checklist | 3 大原因式 | 惨剧图 | **"已知限制"段落** |
| **末尾** | "下一步"引导 | 心理按摩 | 承诺式 | **"Edit this page"GitHub 链接** |

## Q. MA 官方教程独有的 8 条教学原则(可补充前三源)

### 原则 35 — **示例驱动 + 商品链接**(具象到具体商品)

- 每个教程都用**真实 BOOTH 商品**做示例:
  - 教程 1: "Capettiya 的 [Sailor Onepiece](https://capettiya.booth.pm/items/3795694)"
  - 教程 1: "Nagatoro Koyori 的 [Anon-chan](https://booth.pm/ja/items/3564947)"
  - 教程 2: "Lachexia 的 [Dress Lumi](https://lachexia.booth.pm/items/3763311)"
  - 教程 4: "Anon-chan 的连帽衫" (反复用同一素体)
- **效果**:
  - 读者可以直接买同样的东西复现
  - 教程"可验证性"拉满
  - **反例**: 我们写"用你的衣服"——读者无从对照
- **应用**: 教玩家时,**让玩家先用一个免费公开的 Avatar 复现**,再用自己的

### 原则 36 — **"What happened here?" / "How does it work?" 段落**(原理透明)

- 每个教程不仅说"怎么操作",还单独有:
  - "What happened here?" (教程 1, 2)
  - "How does it work?" (教程 6, Merge Armature 等)
  - "When should I use it?" / "When shouldn't I use it?" (组件参考)
- **效果**: 让读者**理解机制**,而不只是"按步骤点"
- **与 vrnavi 区别**: vrnavi 用"老手角色插嘴"讲原理;MA 用**独立段落**讲
- **应用**: 教玩家时,操作步骤之后**单独加一节"为什么这样"**(30-50 字即可)

### 原则 37 — **"Known limitations" / "When shouldn't I use it"**(主动告诉陷阱)

- 组件参考页**必带** "When shouldn't I use it?" 段
- 教程页**必带** "warning" / "tip" 提示框
- 例:
  - "This component should not be used to modify blendshapes that are also animated by other animations"
  - "In VRChat, it's not currently possible to adjust the avatar's height dynamically"
  - "due to a bug in the VCC, you might sometimes get this error when trying to add..."
- **效果**: 把"读者会踩的坑"**主动暴露**,而不是被踩了再回来看 FAQ
- **应用**: 我们教玩家时,**操作前先说"什么情况不能用"**

### 原则 38 — **"未来可能改变"诚实免责**(不假装稳定)

- MA 官方多次提到:
  - "The precise timing of reactive component activation is **subject to change in the future**"
  - "This component is still internally called `ModularAvatarMergeBlendTree` for API compatibility"
  - "Behavior might change in the future if it becomes possible to dynamically adjust the avatar's height"
- **效果**:
  - 诚实承认"我现在写的不一定是永远对的"
  - 玩家**不会因为变化而惊讶**
- **与 Kuriko 原则 34 "未实测免责" 类似,但 MA 更"前瞻性"**——主动承认未来会变
- **应用**: 我们说"目前是这样" / "MA 版本更新后可能变"

### 原则 39 — **"Why would you?" 反问句**(不替玩家做选择)

- 教程 6 (手动 Animator) 的核心句:
  > "You can also do this by building an animator manually, **but why would you?**"
- 教程 1 教完 Merge Armature 后:
  > "With Modular Avatar, **you don't need to unpack** the original avatar or outfit prefab"
- 教程 4 教完 Object Toggle 后,提示 Shape Changer:
  > "If you have any animatable toggles, Modular Avatar will automatically remove..."
- **效果**:
  - 不说"X 比 Y 好"
  - 让玩家**自己判断**什么场景用什么
- **与 vrnavi "前置门控"区别**: vrnavi 假设读者水平;MA 假设读者**有判断力**
- **应用**: 教玩家时,"你可以用 X,但更推荐 Y,理由是 Z"——不替玩家决定

### 原则 40 — **"Apply On Play" / "Compile 时机" 解释**(把工具行为说清)

- 玩家最常问的"为什么编辑器正常,VRChat 出问题",MA 官方在 "Dealing with problems" 直接说:
  - "Modular Avatar will automatically process your avatar; when you enter play mode or build..."
  - "Check that 'Apply On Play' is checked"
  - "Generated assets are saved in a folder named `ModularAvatarOutput`"
- **效果**:
  - 把"工具的运行时机"**明确告诉读者**
  - 玩家知道**什么时候看效果**、**什么时候重新处理**
- **应用**: 我们教玩家时,**明确说"现在去 Play 模式看效果"**

### 原则 41 — **"Debug 工具内置"**(给玩家自助能力)

- MA 提供**内置调试器**: Reaction Debugger
  - 打开方式: 右键 GameObject → Modular Avatar → Show Reaction Debugger
  - 可以虚拟改变状态,看 Reactive Components 行为
  - "Avoid the need to manually interact with your avatar"
- **Manual Bake Avatar** 也是自助工具:
  - "手动看 MA 编译后的最终结果"
- **效果**:
  - 不依赖 VRChat 也能调试
  - 玩家**自己就能排除问题**
- **应用**: 我们教玩家时,优先用"工具内的调试方式"而不是"进 Play 模式试"

### 原则 42 — **"`tip` 框 vs `warning` 框 vs `note` 框"** 分级提示

- 官方用 Docusaurus admonition 区分 4 种信息密度:
  - `tip` — 有用小贴士(可跳过)
  - `note` — 补充信息(可跳过)
  - `warning` — 操作注意事项(必看)
  - `caution` — 严重警告(必看)
- 例:
  - `tip`: "It's best to put the scene view into a side-on, isometric view when making this adjustment"
  - `warning`: "In VRChat, it's not possible to adjust the avatar's height dynamically. As such, if multiple Floor Adjusters are present, no adjustment will be made"
  - `caution`: "When you manually bake your avatar, Modular Avatar will generate a bunch of generated meshes and other assets, and they won't be cleaned up automatically"
- **效果**: 玩家根据提示框类型**自动判断信息重要性**
- **应用**: 我们教玩家时:
  - "**提示**" = 可选看
  - "**注意**" = 必看
  - "**警告**" = 不看会炸

## R. MA 官方教程风格的"禁忌"

| 禁忌 | 反例(我们常犯) | 正例(MA 官方) |
|------|----------------|----------------|
| **不要"承诺完美"** | "用这个 Avatar 一定不会出问题" | "**This behavior might change in the future**" |
| **不要"假设读者会 Play 模式"** | "现在你应该看到效果了" | "**Go into play mode**, we can see that..." |
| **不要"省略失败模式"** | 只讲成功路径 | "**What if it doesn't work?** Check X" |
| **不要"使用未具象的代词"** | "把它拖到那里" | "**Drag the avatar's right hand bone** into the 'Target' field" |
| **不要"省略组件字段名"** | "打开这个" | "Click the '**+**' icon to add a new entry" |
| **不要"忽略编辑器预览限制"** | "你应该看到..." | "Use **Avatar 3.0 Emulator or Gesture Manager** to test" |

## S. MA 官方教程的"句式模板"

| 句式 | 模板 | 例子 |
|------|------|------|
| **"绝大多数场景"开场** | "With modular avatar, **most X can be done with Y**" | "most simple outfits can be merged onto your avatar with one click" |
| **"什么时候用 / 不用"对仗** | "**When should I use it?** / **When shouldn't I use it?**" | 组件参考必带 |
| **"发生了什么"反思** | "**What happened here?**" | 教程 1, 2 结尾 |
| **"它如何工作"透明化** | "**How does it work?**" | 组件参考必带 |
| **"已知限制"诚实** | "**Limitations:**" / "**However, ...**" | 高级组件带 |
| **"Try X first"建议** | "**If you're not sure**, you can try both" | Quick Swap |
| **"Edit this page"开放** | "**[Edit this page](GitHub link)**" | 每个页面底部 |

## T. MA 教学风格与前三源的融合策略

| 玩家问题 | MA 风格应用 | 其他源补充 |
|---------|------------|------------|
| **"MA 是啥?"** | MA 风格: 列出 3 核心特性 | vrcmaster: "救世主" 比喻 |
| **"怎么装衣服?"** | MA 风格: 教程 1 简化版(3 步) | vrnavi: 加上预估时间 |
| **"装上没反应"** | MA 风格: 9 项诊断表 | vrcmaster: 戏剧化开场 + 心理安抚 |
| **"我想了解 X 组件"** | MA 风格: 组件参考 (When/How/Limitations) | Kuriko: 工具名片 + 维护状态 |
| **"我做了 X,出错了"** | MA 风格: 已知限制 + GitHub Issue | Kuriko: 惨剧图 + 经验外化 |
| **"MA + VRCFury 冲突?"** | MA 风格: 实验性功能 + 风险免责声明 | Kuriko 风格: "⚠️ 自己沒實測過" |

## U. MA 教程风格速记卡片(Agent 教学时用)

**用 MA 风格回答时,记住**:
- ✅ 给具体组件名(精确到字段)
- ✅ 给 "What happened here?" / "How does it work?" 反思
- ✅ 给 "When shouldn't I use it?" 反向提示
- ✅ 给 "未来可能改变" 免责
- ✅ 主动暴露"已知限制"
- ✅ 例子用具象商品(BOOTH 链接)
- ❌ 不用"保姆式"语气("你一定行!")
- ❌ 不用"假装完美"("100% 不会出错")
- ❌ 不用"省略字段名"("打开这个" → "点 + 按钮")

## V. 来源链接

- 官方文档主页: https://modular-avatar.nadena.dev/docs
- 教程索引: https://modular-avatar.nadena.dev/docs/tutorials
- 组件参考: https://modular-avatar.nadena.dev/docs/reference
- FAQ: https://modular-avatar.nadena.dev/docs/faq
- GitHub: https://github.com/bdunderscore/modular-avatar
- **Samples 页面**: https://modular-avatar.nadena.dev/docs/samples

## V.Samples Samples 拆解教学法 ⭐NEW 2026-06-17

> **新增子节**: 提炼 Samples 页面（Fingerpen + Clap）的教学法,补充 MA 官方教程分析
> **位置**: 完整拆解见 `modular-avatar.md` §9.6 Samples 实战案例
> **本节重点**: 抽象出 3 条"用现成 Prefab 拆解教学"的新原则(原则 43-45),可补充前三源教学法

### 原则 43 — "用现成 Prefab 拆解" > "从零搭建教学"

**官方 Samples 的核心教学价值不在"教你怎么造这个",而在"让你看一个**做好的东西长什么样**"**。这和教程 1-6 的"从零搭建"思路是**互补的**:

| 维度 | 从零搭建教程（1-6） | 现成 Prefab 拆解（Samples） |
|------|---------------------|---------------------------|
| 教学目标 | 学会做 | 学会看 |
| 玩家心理 | "我要造一个" | "我要懂这个" |
| 适合人群 | 创作者 | **所有玩家**(包括只想用别人 Prefab 的人) |
| 完成度 | 必须全程跟完 | 拖一下就能用,剩下的随便看 |

**应用到我们自己的教学**:
- 教玩家一个组件时,**优先展示一个真实 Prefab 里它的样子**
- 不要假设玩家会自己造——90% 玩家只想"看懂别人做了什么"
- **配套话术**:"这是 Fingerpen Prefab 内部的样子,你以后看到任何 MA 小组件,结构都长这样,只是组件组合不同"

### 原则 44 — "递进式 Sample" > "并列式 Sample"

**官方 Samples 不是"2 个独立例子",而是"Fingerpen → Clap"的递进**。Clap **没有重新发明轮子**——它在 Fingerpen 之上**只加了 1 个新知识点**(Internal Parameters + Contact)。

这种设计的好处:
- 玩家学 Clap 时,**70% 的内容已经会了**(Fingerpen 教的)
- 学习负担从"学 2 个独立的东西"降到"学 2 个东西 + 1 个差异点"
- 玩家的**信心增长是连续的**——"哦,Fingerpen 我会了,Clap 只是多了这一点"

**应用到我们自己的教学**:
- 设计多步骤教程时,**不要写 5 个完全独立的例子**
- 第 2 个例子应该是"在第 1 个之上 + 1 个新东西"
- **配套话术**:"这 30% 是你已经会的,只看新加的 70% 就行"

### 原则 45 — "展示完成效果" + "展示制作过程" 都要教,但分场景

**Samples 是"展示完成效果"型教学**——玩家拿到一个**已经做完的** Prefab,先看到"哦它能用"(完成效果),再去拆"哦原来是这样"(制作过程)。这和教程 6(手动 Animator)的"展示制作过程"形成对比:

| 维度 | 展示完成效果（Samples） | 展示制作过程（教程 6） |
|------|------------------------|----------------------|
| 第一步 | 看效果 | 搭结构 |
| 玩家心理 | "哦,原来是这样" | "我来做做看" |
| 失败成本 | 极低(看不会坏) | 高(搭错了要重来) |
| 适合谁 | **所有人** | 想自己造的创作者 |

**应用到我们自己的教学**:
- **入门阶段**:先给玩家一个"能用的 Prefab",让他体验完成效果
- **拆解阶段**:再打开 Prefab 讲内部结构("那个组件是干什么的")
- **创造阶段**:最后才是"从零搭一个"
- **配套话术**:"先玩 → 再拆 → 最后造"——这个顺序适合绝大多数玩家

### 一句话总结

**Samples 教学的核心洞察**: 官方文档把教学拆成了"**展示效果(Samples)→ 展示搭建(教程 1-6)→ 展示组件细节(Component Reference)**"三层。我们的教学文档也应该照这个分层来组织——**让新手从 Samples 进入,从 Prefab 内部"看穿"组件,而不是从组件定义开始**。

### Samples 在四源融合中的位置

| 源 | 教学类型 | Samples 是不是它的一部分? |
|----|---------|------------------------|
| **vrnavi** | 深度系列 | ❌ 不包含 Samples 拆解(它做的是"如何做"系列) |
| **vrcmaster** | 普及工具链 | ❌ 不包含 |
| **Kuriko** | 工程实践百科 | ⚠️ 部分包含(它会"拆一个真东西"但不会系统性覆盖) |
| **MA 官方** | 工具作者 | ✅ **核心载体**(Samples 是 MA 官方"完整 Prefab 长什么样"的唯一权威展示) |

**结论**: Samples 教学风格属于 **MA 官方** 的"完成效果型"分支,和我们之前总结的"MA 官方 = 工具作者视角"形成**双层结构**:
- **组件层**(When/How/Limitations): "用我的工具做 X"
- **Prefab 层**(Fingerpen/Clap 拆解): "看我的工具**做好的样子**"

---

# 第五部分:四源综合使用指南 (2026-06-17 升级)

> 整合 **vrnavi (深度系列) + vrcmaster (工具链普及) + Kuriko (工程实践百科) + MA 官方 (工具作者视角)** 四源,形成**完整的 Avatar 改模教学风格库**。

## W. 四源核心定位对比

| 源 | 定位 | 一句话 |
|----|------|--------|
| **vrnavi** | 深度系列 | "我要把 X 讲透" |
| **vrcmaster** | 普及工具链 | "零基础也能搞定" |
| **Kuriko** | 工程实践百科 | "系统掌握全貌" |
| **MA 官方** | 工具作者 | "用我的工具做 X" |

## X. 面对玩家的"教学风格选择决策树"

```
玩家提问
│
├─ 完全零基础,问"是什么"?
│   └─ vrcmaster 风格 (5 步 + emoji 比喻)
│
├─ 有基础,问"怎么做"?
│   └─ vrnavi 风格 (1 步 1 动作 + 时间)
│       ├─ 涉及具体工具
│       │   └─ MA 官方风格 (精确字段 + 已知限制)
│       └─ 涉及系统化理解
│           └─ Kuriko 风格 (懒人包 + 代價-好處)
│
├─ 报错/故障
│   └─ vrcmaster 戏剧化 + vrnavi checklist + MA "已知限制"
│
└─ 工具选型/版本决策
    └─ Kuriko 工具名片 + MA "When to use it"
```

## Y. 四源禁忌融合(回答时绝对不能)

1. ❌ **承诺完美**("一定不会出错") → MA 原则 38
2. ❌ **只推优点不推代价** → Kuriko 原则 24
3. ❌ **甩完整教程当回答** → vrnavi 原则 6
4. ❌ **术语不解释** → vrcmaster 原则 14
5. ❌ **忽略备份/不可逆提醒** → Kuriko 原则 33
6. ❌ **替玩家做工具选择** → MA 原则 39
7. ❌ **隐藏不确定信息** → Kuriko 原则 34 + MA 原则 38
8. ❌ **无视觉锚点长段黑字** → vrcmaster 原则 12

## Z. 四源融合的"黄金回答模板"

```
[戏剧化/陪伴式开场] (vrcmaster)
  "哎?你遇到 X 问题了?这坑新手基本都踩过 💦 别慌~"

[归类 + 简化定位] (vrnavi)
  "这是 MA 工具 X 的常见问题,先看是不是 Y 原因"

[症状-原因-对策 checklist] (vrnavi + MA "When not to use")
  □ 症状 1: ... → 原因 ... → 试 X
  □ 症状 2: ... → 原因 ... → 试 Y

[代價-好處提示] (Kuriko)
  "如果用方案 A,好处是 X,代价是 Y"

[未实测免责 / 未来变更免责] (Kuriko + MA)
  "⚠️ 这个我没亲自测过;或者 MA 版本更新后可能变"

[下一步引导] (vrnavi)
  "如果还没解决,看 X 文档 / 试试 Y 工具 / 加 Z 群问"
```

## AA. 最终:Avatar 教学"风格自检表"(Agent 回答前过一遍)

- [ ] 玩家处于什么水平?(零基础/有基础/进阶)
- [ ] 玩家问的是哪类问题?(A-H 八类)
- [ ] 选对风格了吗?(vrcmaster/vrnavi/Kuriko/MA 官方)
- [ ] 是否给出"症状-原因-对策"框架,而不是甩完整教程?
- [ ] 是否说明"代價-好處",而不仅说好處?
- [ ] 是否标注"工具维护状态"避免推荐过时工具?
- [ ] 是否引用社区贡献者时显式署名?
- [ ] 是否标注"未实测/未来变更"内容?
- [ ] 是否给"懒人包 5 步"让急性子有收获?
- [ ] 是否给"挑战者框"让老手不无聊?
- [ ] 备份/不可逆操作前是否提醒?
- [ ] 故障排查是否用"checklist"或"惨剧图"?
- [ ] 末尾是否引导到"下一步去哪"?
- [ ] **MA 专项**: 涉及具体组件时,是否给了精确字段名 + 已知限制?
- [ ] **MA 专项**: 涉及 X 是不是用 X 时,是否给了反向提示?
- [ ] **MA 专项**: 涉及"未来行为",是否诚实免责?

---

# 第六部分:MA 教程的具体技术提炼(2026-06-17 新增)

> **与 §R-§Z 的关系**：§R-§Z 是"教学风格"归纳,§BB 是"具体技术细节"提炼。
> **学习来源**:官方 6 个教程的原文精读,详见 `memory/avatar/modular-avatar-tutorials-detailed.md`

## BB. MA 教程的 5 大玩家友好设计

### BB.1 Default 复选框预览 ⭐⭐⭐

**官方原文**（教程 3）:
> "If you want to see it in action, click the `Default` box on the Menu Item, and you should see the hoodie disappear."

**原理**: 点 Inspector 的 `MA Menu Item` 上的 `Default` 复选框,**立即**在 Scene 视图看到物件出现/消失。

**为什么这是教学金矿**:
- **不需要进 Play 模式**就能验证
- 玩家最痛点:"我做了但不知道对不对" → 直接解决
- 降低"我做了什么破坏了 Avatar"的焦虑

**教学应用**:
```
✅ 教 Object Toggle 时,必教"点 Default 看效果"
✅ 任何"我做了 X 但没反应"问题 → 先让玩家点 Default 验证
❌ 不要让玩家"进 Play 模式再看"作为默认步骤
```

### BB.2 Overdraw 调试视图 ⭐⭐⭐

**官方原文**（教程 5）:
> "click on the debug overlay button, and select `Overdraw`, to get a see-through view of what's going on"

**原理**: Scene 视图左上角 Shaded 按钮 → 选 Overdraw → 场景变半透明,可以"透视"看穿模。

**具体操作步骤**:
1. 在 Scene 视图（非 Game 视图）左上角
2. 点 "Shaded" 下拉
3. 选 "Overdraw"
4. 场景变彩色半透明,重叠处颜色越深表示 overdraw 越严重

**为什么这是教学金矿**:
- 玩家痛点:"我不知道穿模程度" → 直接**看到**
- 比"截图 + 文字描述"直观 10 倍
- 适用所有"是否重叠"问题

**教学应用**:
```
✅ 调形态键时 → Overdraw 验证
✅ 调 Collider 时 → Overdraw 验证
✅ 任何"看起来穿模"问题 → Overdraw 调试
✅ 教"如何验证你的修改没破坏 Avatar"
```

### BB.3 MA Parameters 位置约束 ⭐⭐

**官方原文**（教程 6）:
> "Make sure that `MA Parameters` is on either the same object, or a parent of all your `Merge Animator`s and `Menu Installers`!"

**原理**: `MA Parameters` 必须在所有 `Merge Animator` 和 `Menu Installer` 的**同一对象或父级**。

**教学应用**:
- 教创作者时:**默认**把 MA Parameters 放在小组件根对象
- 出错排查:参数找不到 → 第一检查位置

### BB.4 Internal Checkbox ⭐⭐

**官方原文**（教程 6）:
> "If you set the internal checkbox, modular avatar will ensure that your `Cube` parameter doesn't interfere with anything else on the avatar using the same parameter name."

**原理**:
- 勾 Internal → MA 自动避免参数名冲突(用户看不见原始名)
- 不勾 Internal → 用户可手动改名,可能冲突

**教学应用**:
- 教创作者时:**默认**勾 Internal
- 例外:多个小组件需要共享参数(罕见)

### BB.5 Setup Outfit 自动机制 ⭐⭐

**官方原文**（教程 1）:
> "Modular Avatar will automatically locate the armature object under the outfit, and attach a [Merge Armature](/docs/reference/merge-armature) component to it."

**原理**: `Setup Outfit` 自动:
- 找 Armature 对象
- 加 Merge Armature 组件
- 处理 A-Pose/T-Pose 转换
- 创建 Mesh Settings

**教学应用**:
- 教玩家"**你不需要理解**这个,MA 帮你做了"
- 不讲"为什么能自动",只讲"它会自动"
- 高级概念(骨骼合并、A-Pose 转换)封装起来

---

## CC. MA 教程的"具体句式"清单

| 教程 | 关键句式 | 教学价值 |
|------|---------|---------|
| 1 | "**you don't need to unpack the original avatar or outfit prefab!**" | 永远不要拆 Prefab |
| 1 | "**merge the bone heirarchy with the original avatar's bones**" | 骨骼合并是 MA 的核心 |
| 2 | "**Attachment Mode will automatically update to 'As child; keep position'**" | 教"自动变更"机制 |
| 3 | "**click the `Default` box on the Menu Item**" | 见 BB.1 |
| 4 | "**click the arrow next to the parameter name box to search**" | 参数搜索按钮(▼) |
| 5 | "**select `Overdraw`**" | 见 BB.2 |
| 5 | "**Use Avatar 3.0 Emulator or Gesture Manager to test**" | 诚实告知限制 + 给绕过方法 |
| 6 | "**Make sure that `MA Parameters` is on...**" | 见 BB.3 |
| 6 | "**set the internal checkbox**" | 见 BB.4 |

---

## DD. MA 教程的"反面教材"(绝对不能教)

| ❌ 反面教材 | 原因 |
|------------|------|
| 教玩家"用 Animator 方式做开关"作为默认 | 官方原话 "why would you?" |
| 教玩家"拆开 Prefab" | "you don't need to unpack!" |
| 教玩家"如果不工作就重启 Unity" | 应该给具体诊断而非模糊建议 |
| 教玩家"设置 Bone Proxy 后没动是正常" | 应该给"自动变更 Attachment Mode"的具体预期 |
| 让玩家"猜"参数名 | 应该用 ▼ 按钮搜索 |
| 教玩家"编辑器能预览所有效果" | 形态键联动不可预览,要诚实告知 |
| 让玩家"猜"MA Parameters 放哪 | 官方明确"同一对象或父级" |

---

## EE. MA 教学的应用模板(Agent 用)

```
[开场 - vrcmaster 戏剧化]
"哎?你想装衣服但没反应?这坑太常见了 💦"

[归类 - 给出定位]
"这是装衣服流程的最常见 5 个问题之一,先看是不是 Y 原因"

[症状-原因-对策 - vrnavi + MA]
□ 症状 1: 装上没动 → 检查是否右键了 Setup Outfit
□ 症状 2: 装上了但穿模 → 加 Shape Changer + Overdraw 调试 (BB.2)
□ 症状 3: 调体型衣服不变 → 加 Blendshape Sync
□ 症状 4: 鞋子陷地 → 加 Floor Adjuster
□ 症状 5: 多个组件参数冲突 → MA Parameters 勾 Internal (BB.4)

[诚实免责 - MA + Kuriko]
"⚠️ 形态键联动效果编辑器无法预览,要用 Avatar 3.0 Emulator 测试"

[具体技术 - MA BB 节]
"调试时记得用 Overdraw 视图(Scene → Shaded → Overdraw)"

[下一步引导]
"如果还没解决,看 X 文档第 Y 节 / 试试 Z 工具"
```

---

## FF. 来源与配套

| 文档 | 内容 |
|------|------|
| `memory/avatar/teaching-methodology.md` (本文) | 教学风格 + 具体技术提炼 + Samples 拆解教学法(原则 43-45) |
| `memory/avatar/modular-avatar.md` | MA 主文档(组件 + 教学决策树 + **§9.6 Samples 实战案例** ⭐NEW) |
| **`memory/avatar/modular-avatar-tutorials-detailed.md`** | 6 个教程的原文精读 + 玩家视角操作分解 |
| `memory/avatar/avatar-modding-guide.md` | 改模完整流程 |

**官方教程**:
- https://modular-avatar.nadena.dev/docs/tutorials
- https://modular-avatar.nadena.dev/docs/samples (Fingerpen + Clap)

---

# 第七部分:MA 组件级"零基础 → 高级"语言转换案例库(2026-06-17 新增)

> **与 §BB-§FF 的关系**:§BB-§FF 是"教程技术提炼"(适用于教学整篇),§GG-§QQ 是"组件级语言转换"(适用于回答单个组件问题)
> **学习来源**:本次系统学习官方 Component Reference 27 个组件 + 4 个横切页的原文,详见 `memory/avatar/ma-component-cards.md`
> **目标**:让 Agent 在回答"X 组件怎么用"时,自动判断"用零基础语言还是专业语言",并给出**具体可复用的话术**

## GG. 总体转换原则

### GG.1 三级语言体系(基于 2026-06-17 vrcmaster + Kuriko 教学法)

| 级别 | 适用对象 | 语言特征 | 句长 | 句式 |
|------|---------|---------|------|------|
| **L0 零基础** | 完全没碰过 Unity | 比喻(布/骨/挂钩/裁缝) | 5-15 字 | "把 X 当成 Y" |
| **L1 入门** | 会装 Avatar | 步骤 + 字段名 | 15-25 字 | "拖 X 到 Y 字段" |
| **L2 进阶** | 懂 Animator + 表达式 | 概念 + 限制 | 25-50 字 | "X 通过 Y 实现 Z" |
| **L3 专业** | 创作者 / 工具作者 | 反射 / 编译 / NDMF | 50+ 字 | "在 OnEnable 阶段..." |

### GG.2 默认语言 = L1(入门)

**理由**:
- 玩家第一次问"X 怎么用"**通常有 Unity 基础**但**没装过 MA**
- L1 既能"直接照做"也能"理解原理"
- 零基础玩家会在追问时暴露 → 切 L0
- 进阶玩家在主动用专业词时暴露 → 切 L2/L3

### GG.3 切换信号(玩家用这些词,自动升级)

| 玩家说 | 切换到 | 理由 |
|--------|-------|------|
| "Animator Controller"、"Layer"、"State" | L2 | 懂 Animator |
| "NDMF"、"编译时"、"运行时" | L3 | 懂 NDMF 架构 |
| "Prefab Variant"、"嵌套 Prefab" | L2 | 懂 Unity 高级 |
| "Blendshape"、"Skinned Mesh Renderer" | L2 | 懂 Avatar 概念 |
| "Trigger"、"Condition"、"Transition" | L2 | 懂 Animator 状态机 |
| "PhysBone"、"Constraint" | L2 | 懂 Avatar Dynamics |

### GG.4 切换信号(玩家用这些词,降级到 L0)

| 玩家说 | 切换到 | 理由 |
|--------|-------|------|
| "什么是 XXX" | L0 | 完全没有概念 |
| "我完全不会 Unity" | L0 | 明示零基础 |
| "看不懂" | L0(回到上一步) | 失去跟随 |
| "Avatar 没动" | L1(检查) | 描述现象 |
| "为什么不工作" | L1(诊断) | 不知道原因 |

## HH. 27 个组件的语言转换案例(完整)

> 每个组件给 3 个语言级别的话术示例
> L0 = 零基础 / L1 = 默认入门 / L2 = 进阶

### HH.1 Merge Armature

| 级别 | 话术 |
|------|------|
| L0 | "把衣服拖到 Avatar 身上,右键选 Setup Outfit,搞定" |
| L1 | "组件加到衣服根对象,拖 Avatar 骨骼到 Merge Target,Prefix/Suffix 通常自动填" |
| L2 | "Merge Armature 通过 Bone Name 匹配 + Prefix/Suffix 去噪策略,合并时调用 SkinnedMeshRenderer.rootBone 重写并自动重构骨骼父子关系,PhysBone/Contact 的 target 字段也会被更新" |

### HH.2 Merge Animator

| 级别 | 话术 |
|------|------|
| L0 | "想让你的道具能动?加这个,它帮你把动画'贴'到 Avatar 上" |
| L1 | "Animator 拖入,Layer Type 选 FX,勾上 delete attached animator 和 match avatar write defaults" |
| L2 | "Match Avatar Write Defaults 在 OnEnable 阶段通过反射读取 Avatar Animator 的 WD 状态,如果 Avatar 不一致则跳过;Layer Priority 数字小的先应用,同优先级按 Hierarchy 顺序" |

### HH.3 Merge Motion (Blend Tree)

| 级别 | 话术 |
|------|------|
| L0 | "想做一直动的表情?用 Blend Tree 资产,加这个组件" |
| L1 | "Blend Tree 资产拖到 Motion 字段,搞定" |
| L2 | "Merge Motion 创建 Direct Blend Tree(参数恒为 1),会强制 rebase 所有子动画到相同长度,不适合随时间变化的动画" |

### HH.4 Object Toggle

| 级别 | 话术 |
|------|------|
| L0 | "右键 Avatar → Create Toggle,改个名,搞定" |
| L1 | "组件加到控制对象,点 + 添加目标,勾选=启用时启用" |
| L2 | "多个 Object Toggle 冲突时 Hierarchy 末位胜出;链式 A→B→C 关闭时,每级延迟 1 帧防止"瞬时空档"" |

### HH.5 Shape Changer

| 级别 | 话术 |
|------|------|
| L0 | "衣服把身体藏起来了?用 Shape Changer 把身体被盖住的部分也藏起来" |
| L1 | "Target Renderer 拖入身体,点 + 选形态键,模式选 Delete 省性能" |
| L2 | "Delete 模式调用 Mesh.SetTriangles 静态删除顶点(Always Active 时),Set 模式依赖 Animator 控制 blendshape 值(可能有动画时)" |

### HH.6 Material Setter

| 级别 | 话术 |
|------|------|
| L0 | "想换某个对象的样子?加这个,选新材质" |
| L1 | "Renderer 拖入,选槽位,目标材质拖入 Set material to" |
| L2 | "Material Setter 精确控制 Renderer 槽位;Material Swap 按 Material 资产名批量替换,二者互补" |

### HH.7 Material Swap

| 级别 | 话术 |
|------|------|
| L0 | "想换衣服颜色?加这个,准备几套颜色随时换" |
| L1 | "原材质 + 目标材质对应拖入,Quick Swap 模式选 Same Folder,Inspector 出现 ← → 切换" |
| L2 | "Quick Swap 在 Editor 通过 Material 资产路径扫描实现 Adjacent Folders 匹配,Adjacent Folders 算法基于父目录对比" |

### HH.8 Mesh Cutter

| 级别 | 话术 |
|------|------|
| L0 | "Mesh Cutter 是'裁剪刀',把不需要的多边形剪掉" |
| L1 | "加 Mesh Cutter,加 Vertex Filter(By Mask/Axis/Bone/Blendshape),Always active 时直接删多边形" |
| L2 | "Multiple Vertex Filter 支持 Combine/Intersect 模式;Always-active Mesh Cutter 编译时通过 Mesh.SetTriangles 静态裁剪,有 constraint 性能开销" |

### HH.9 Bone Proxy

| 级别 | 话术 |
|------|------|
| L0 | "想在手上挂个东西?用 Bone Proxy,挂哪个骨头都行" |
| L1 | "组件加到对象,拖目标骨骼到 Target,Attachment Mode 自动设置" |
| L2 | "Bone Proxy 重新父化对象(不合并骨骼),所以做通用 Prefab 时它跨 Avatar 通用;Merge Armature 反之——按骨骼名匹配所以只对特定 Avatar" |

### HH.10 Blendshape Sync

| 级别 | 话术 |
|------|------|
| L0 | "调身体形状衣服不变?加这个,选身体的形态键" |
| L1 | "组件加到衣服,点 + 选素体形态键(胸部大小等),自动同步" |
| L2 | "Blendshape Sync 不能链式 A→B→C;运行时只支持 Animator 控制的形态键(Viseme/EyeLook 同步有精度问题)" |

### HH.11 Parameters

| 级别 | 话术 |
|------|------|
| L0 | "VRChat 只给你 256 个参数格子,Internal 自动起名避免冲突" |
| L1 | "加组件,点 + 加参数,设类型(Bool/Int/Float),勾 Internal" |
| L2 | "Internal 参数通过 MA Build 阶段 UniqueName 解析自动避免冲突;Saved/Synced 控制是否占 Expression Parameters 槽位(Synced 耗 256 上限)" |

### HH.12 Menu Item

| 级别 | 话术 |
|------|------|
| L0 | "菜单按钮就是 Hierarchy 里的对象,改名=改菜单名" |
| L1 | "GameObject 改名,加 Menu Item 组件,选 Type,参数下拉选已定义的" |
| L2 | "Submenu Source = Children 让子级作菜单项,自动支持分页;自动参数创建在未声明时自动 + Saved/Synced" |

### HH.13 Menu Installer

| 级别 | 话术 |
|------|------|
| L0 | "把你做的开关挂到 Avatar 菜单里?加这个" |
| L1 | "默认装到顶级菜单,Select Menu 选目标,满了自动分页" |
| L2 | "Menu Installer + Menu Group 实现"扁平安装";Prefab Developer Options 用于创作者场景,通过资产引用而非 Hierarchy 关联" |

### HH.14 Menu Group

| 级别 | 话术 |
|------|------|
| L0 | "多个开关不想分页?用 Menu Group(高级)" |
| L1 | "加 Menu Group,默认包含所有直接子级 Menu Item" |
| L2 | "Menu Group 主要是 Extract Menu 系统的内部组件;新手推荐 Sub Menu 模式更清晰" |

### HH.15 Menu Install Target

| 级别 | 话术 |
|------|------|
| L0 | "如果看到 Inspector 有这个组件,别删——是 MA 自动生成的" |
| L1 | "通常不用手创建,MA 用 Select Menu 时自动加" |
| L2 | "Menu Install Target 通过引用覆盖 Menu Installer 目标菜单,实现基于对象位置的菜单重定向" |

### HH.16 PhysBone Blocker

| 级别 | 话术 |
|------|------|
| L0 | "想装饰不被头发甩动?加这个,装饰刚性附着" |
| L1 | "组件加到装饰,通常配 Bone Proxy 一起用" |
| L2 | "PhysBone Blocker 通过把子对象加入父 PhysBone Ignore 列表实现阻断;Bone Proxy + PhysBone Blocker 组合是标准的"刚性配件"模式" |

### HH.17 Scale Adjuster

| 级别 | 话术 |
|------|------|
| L0 | "衣服 X/Y/Z 比例不对?用这个单独调一轴" |
| L1 | "加组件到目标骨骼,Unity Scale 工具调整" |
| L2 | "Scale Adjuster 通过约束父子 scale 关系实现单骨骼 X/Y/Z 独立缩放;Adjust child positions 仅调位置不缩放" |

### HH.18 Floor Adjuster

| 级别 | 话术 |
|------|------|
| L0 | "鞋子陷地?加这个把 Avatar 抬高" |
| L1 | "新建 GameObject,加 Floor Adjuster,Y 对齐鞋底" |
| L2 | "VRChat **不能动态**调整 Avatar 高度,所以多个 Floor Adjuster 共存时**不调整**;这是已知限制,未来可能改变" |

### HH.19 Move Independently

| 级别 | 话术 |
|------|------|
| L0 | "想编辑时移动对象不影响子级?用这个,运行时无效" |
| L1 | "加组件,Objects to move together 勾几个一起动" |
| L2 | "Move Independently 纯 Editor 工具,运行时无效果;非均匀缩放各轴支持不完整,scale 用 Scale Adjuster" |

### HH.20 Platform Filter

| 级别 | 话术 |
|------|------|
| L0 | "想让 VRChat 专用道具在 Resonite 消失?加这个" |
| L1 | "组件加对象,Platform 选平台,Include/Exclude 选" |
| L2 | "Platform Filter 处于 NDMF Build 阶段末尾(平台分支),如果组件已自动处理平台(如 Merge Animator)不要重复加" |

### HH.21 Remove Vertex Color

| 级别 | 话术 |
|------|------|
| L0 | "头发变色了?加这个,可能就好了" |
| L1 | "组件加 root,所有子对象的顶点色都移除" |
| L2 | "Remove Vertex Color 在 Build 阶段通过 SkinnedMeshRenderer.colors 数组归零实现;VRChat Mobile Shader 容易触发顶点色"色偏"问题" |

### HH.22 Mesh Settings

| 级别 | 话术 |
|------|------|
| L0 | "如果你看到 Setup Outfit 自动加了这个,别动" |
| L1 | "Set or inherit 模式让 outfit prefab 的设置被 avatar 覆盖,推荐 outfit 用这个" |
| L2 | "Mesh Settings 的 4 种模式(Inherit/Set/Don't set/Set or inherit)控制父子级 mesh 配置的继承关系;Bounds 只对 SkinnedMeshRenderer 生效" |

### HH.23 Convert Constraints

| 级别 | 话术 |
|------|------|
| L0 | "VRChat 装上后自动加这个,别删——它帮你加速" |
| L1 | "装到 Avatar 根,自动转换 Unity Constraints 为 VRChat Constraints" |
| L2 | "VRChat Constraints 比 Unity Constraints 性能好;VRCSDK Auto Fix 装了 MA 后会自动加这个组件" |

### HH.24 Visible Head Accessory

| 级别 | 话术 |
|------|------|
| L0 | "想戴眼镜第一人称能看到?加这个" |
| L1 | "加在 Head 子级下,无配置;但不能是 PhysBone 子级" |
| L2 | "用 VRCHeadChop + proxy bone 权重调整实现,避免三角形穿过视角;找"部分顶点 visible bone、部分 hidden bone"的三角形加 proxy 骨骼" |

### HH.25 Global Collider

| 级别 | 话术 |
|------|------|
| L0 | "想让你的道具被别人头发甩到?加 Global Collider" |
| L1 | "组件加到对象,定义 Capsule/Sphere Collider,VRChat 会用它" |
| L2 | "Global Collider 实现策略因平台而异;VRChat 上**最多 6 个**,超过会**覆盖食指 Collider**;Manual Remap 可手动指定占用哪个" |

### HH.26 World Fixed Object

| 级别 | 话术 |
|------|------|
| L0 | "想悬浮剑?加这个,Avatar 动但剑不动" |
| L1 | "加到对象,无配置" |
| L2 | "World Fixed Object 在 Avatar 根生成 world-origin fixed GameObject,把你的对象移为子级;**只生成一个 constraint**,所以 1 个和多个性能相同" |

### HH.27 World Scale Object

| 级别 | 话术 |
|------|------|
| L0 | "复杂链子道具,不想被 Avatar 缩放影响?加这个" |
| L1 | "加到对象,无配置;但 Editor 不预览,游戏中才生效" |
| L2 | "World Scale Object 通过 VRC Scale Constraint 强制 scale = (1,1,1);编辑器不预览,因为 Constraint 行为在运行时由 VRC SDK 注入" |

### HH.28 Sync Parameter Sequence(高级,创作者向)

| 级别 | 话术 |
|------|------|
| L0 | "你做 PC + Quest 双版本?主版本加这个,先传 PC" |
| L1 | "组件加到 Avatar,选 primary platform(包含所有参数),先传 primary,再传其他" |
| L2 | "Sync Parameter Sequence 在 Build 阶段重排 Expression Parameters 槽位,确保跨平台 synced 参数顺序一致;与 VRCFury Parameter Compressor 不兼容" |

## II. 横切页的语言转换

### II.1 Manual processing

| 级别 | 话术 |
|------|------|
| L0 | "想看 MA 编译完的样子?右键 Avatar → Manual bake avatar" |
| L1 | "Tools → Modular Avatar → Manual bake avatar,生成 ModularAvatarOutput 文件夹" |
| L2 | "Manual bake 在 NDMF Build 阶段执行,生成的资源打包成单文件(避免 Unity bug + 加快处理),可在 Inspector 点 Unpack 拆开" |

### II.2 Dealing with problems

| 级别 | 话术 |
|------|------|
| L0 | "Avatar 没动?先检查 Apply On Play 勾没勾" |
| L1 | "Tools → Modular Avatar → Show Error Report,点对象名跳到 Hierarchy 选中" |
| L2 | "MA 错误窗口集成到 NDMF 编译流水线,自动随编辑更新;某些错误类型需要重新 build" |

### II.3 FAQ 经典问题

**Q: 能导出到 VRM 吗?**(零基础视角)
- L0: "不能直接,但可以先 Manual bake avatar,然后用 UniVRM 导出"
- L1: "Tools → Manual bake avatar → UniVRM 导出;不用时记得删 ModularAvatarOutput"
- L2: "Manual bake 在 NDMF 编译后导出处理后的 Avatar,UniVRM 不感知 NDMF 但能识别已处理的 Avatar" |

**Q: 衣服原本不是为我的 Avatar 设计的,能用吗?**
- L0: "可以,MA 会按名字匹配骨骼;装好后用 'Reset position to base avatar' 大致对齐再微调"
- L1: "Merge Armature 按名字匹配,装好后在 Inspector 点 'Reset position to base avatar' → 'Do It!',3 个选项(Also set rotation / local scale / Adjust outfit overall scale)"
- L2: "Reset Position 工具通过 arm length 算法计算整体 scale,然后做局部 transform 同步;三维建模软件轴向差异由 MA 自动处理" |

## JJ. 三个常见场景的"完整对话示范"

### JJ.1 场景:零基础玩家问"装衣服"

```
玩家: "我刚买的衣服怎么装?"

[L0 + vrcmaster 戏剧化]
Agent: "哎?你刚买的衣服不会动?这太常见了 💦 别慌,MA 帮你搞定"

[症状-原因-对策]
Agent: "先检查 3 件事:
  □ 你装 MA 了吗? VCC/ALCOM 装下,加项目
  □ 衣服拖到 Avatar 里了吗? 直接拖到 Avatar 的子级
  □ 你右键 → Setup Outfit 了吗? 这一步是关键!"

[下一步引导]
Agent: "做完进 Play 模式,衣服应该跟着身体动
  如果还不行,看 MA 错误窗口(顶部菜单 Tools → Modular Avatar → Show Error Report)
  实在不行来加群问"
```

### JJ.2 场景:入门玩家问"Blendshape Sync"

```
玩家: "调胸部大小,衣服不变形怎么办?"

[L1 + vrnavi 步骤]
Agent: "衣服和身体的形态键没关联,加 Blendshape Sync 就行:
  1. 选中衣服的 Mesh Renderer(衣服的,不身体的)
  2. Inspector → Add Component → 搜 'Blendshape Sync'
  3. 点 + 按钮
  4. 双击要同步的形态键(比如胸部的)
  5. 改基对象形态键,衣服自动跟"

[诚实免责 - MA 限制]
Agent: "⚠️ Blendshape Sync 不能链式(A→B→C 不行),而且 VRChat 的 Viseme/EyeLook 系统控制的形态键同步有精度问题"
```

### JJ.3 场景:进阶玩家问"MA + NDMF 性能"

```
玩家: "MA 处理在 NDMF 哪个 phase?性能开销如何?"

[L3 + 反射级别]
Agent: "MA 主要在 Generating phase(Resolving 之后):
  - Merge Armature:Pass 阶段重写 SkinnedMeshRenderer.rootBone + 骨骼对象再父化
  - Merge Animator:Layer Priority 数字小的先生成,同优先级按 Hierarchy
  - Reactive Components:OnEnable 阶段读取对象状态,1 帧延迟通过延迟 disable 实现

性能:大部分组件的运行时开销是 O(1) 的(Reactive 由 Animator 驱动)
  - 唯一高成本:Write Defaults 匹配(Avatar 不一致时反射读取所有 state)
  - Shape Changer Delete 模式:Always Active 时静态裁剪,运行时 O(1)
  - Global Collider:VRChat 限 6 个,超出会覆盖食指 Collider"
```

## KK. 与四源教学法的对应关系

| 本节(MA 组件级) | 对应源 | 互补 |
|------------------|--------|------|
| GG-HH 级别体系 | vrcmaster 原则 14(幼儿园比喻)+ Kuriko 原则 23(懒人包) | 把"语言分级别"具体到 27 个组件 |
| II 横切页 | MA 官方风格(BB-FF) | 已有 BB-FF 教程级,这里是组件级 |
| JJ 三个场景 | 四源融合"黄金回答模板"(Z 节) | 把模板实例化 |
| 切换信号表 GG.3 | vrcmaster 原则 11(陪伴式) | 量化"什么时候升级语言" |

## LL. 来源与配套

| 文档 | 内容 |
|------|------|
| `memory/avatar/teaching-methodology.md` (本文) | 教学风格 + MA 教程技术提炼 + 组件级语言转换 |
| `memory/avatar/ma-component-cards.md` ⭐NEW | 27 个组件的"教学卡"(When/How/Limitations) |
| `memory/avatar/modular-avatar.md` | MA 主文档(组件 + 教学决策树) |
| `memory/avatar/modular-avatar-tutorials-detailed.md` | 6 个教程的原文精读 |
| `memory/avatar/avatar-modding-guide.md` | 改模完整流程 |

**下一版待做**: 实验性功能(Resonite 支持 / Portable Avatar Components)精读

---

# 第七部分:问题诊断教学法(MA "Dealing with problems" 章节精读) ⭐NEW 2026-06-17

> **学习来源**: [Dealing with problems 主页](https://modular-avatar.nadena.dev/docs/problems) + [Installation issues](https://modular-avatar.nadena.dev/docs/problems/install)
> **核心洞察**: MA 官方 problems 章节**异常精简**(只 2 个问题),但**每个问题都遵循"症状→原因→3 步修复"模式**。这种"宁少勿滥"的设计哲学本身值得学习。

## MM. problems 章节的核心设计哲学

### MM.1 "分布式问题诊断"设计

**关键观察**: MA 官方 problems 章节**只覆盖 2 个问题**:
- 主页:Nothing is getting processed at all(Apply On Play 没勾)
- 子页 install:Failed to add Repo(VCC 已知 bug)

**为什么这么少**?——因为问题诊断的责任**分散到了多个地方**:

| 位置 | 责任范围 | 数量级 |
|------|---------|--------|
| **Dealing with problems** | 最高频、影响最大 | 2-3 个 |
| **Component Reference** | 组件级"Known limitations" | 每个组件 1 段 |
| **General Behavior** | MA 自动行为 + 平台行为 | 1-2 个 |
| **FAQ** | "能不能 X"类问题 | 5-10 个 |
| **GitHub Issues** | 实际 bug | 数百个 |
| **Discord** | 实时讨论 | 不计其数 |

**对 Agent 的启示**:
- ✅ **不要"假装权威"**——只覆盖知识库有的内容
- ✅ **主动告诉玩家**"这个问题可能要去 Discord / GitHub 问"
- ✅ **问题诊断是分布式责任**——一个文档不可能覆盖所有问题
- ✅ **教学最高优先级**:让玩家**自己学会查**这些渠道

### MM.2 官方 problems 章节的"三段式"模式

**官方每个问题都遵循这个结构**:

```
症状 (Symptom)        → 玩家看到了什么
原因 (Root Cause)     → 99% 是什么导致的
3 步修复 (Fix Steps)  → 精确到字段的操作
```

**示例(主页 Nothing is getting processed at all)**:

```
症状: 你做了操作(加了组件、点了 Setup Outfit)但什么都没发生
原因: Apply On Play 没勾选(99% 的情况)
修复: 选中 Avatar → Inspector → VRC Avatar Descriptor → Apply On Play 勾上
```

**示例(install Failed to add Repo)**:

```
症状: VCC 添加 MA 仓库时弹出 Failed to add Repo
原因: VCC 已知 bug(due to a bug in the VCC)
修复: 点 Cancel → 看 Community Repositories 列表 → 确认 bd_ 已勾选
```

### MM.3 8 条可复用的"问题诊断写作原则"

从 problems 章节提炼:

| # | 原则 | 官方做法 | 教学启示 |
|---|------|---------|---------|
| 1 | **只列最高频问题** | 整个章节就 2 个问题 | 不要"为了完整"列 20 个 |
| 2 | **错误窗口 > Console** | 专门有 Show Error Report | 教玩家"先看错误窗口" |
| 3 | **诚实告知工具 bug** | "due to a bug in the VCC" | 不掩饰工具问题 |
| 4 | **路径精确到字段** | "VRC Avatar Descriptor → Apply On Play" | 不写"勾上那个选项" |
| 5 | **错误自动更新提示** | "Most errors ... will update automatically" | 提前说"有些需重新 Build" |
| 6 | **给出绕过方案** | "Click Cancel, look in the list..." | 不只说"这是 bug" |
| 7 | **不假设完美** | "Usually this means..." | 用"99%"/"通常" |
| 8 | **错误窗口可重开** | 工具栏菜单明文 | 教玩家"出错关掉了也没事" |

### MM.4 玩家问题回答的"5 步问题诊断法" ⭐核心

> 整合官方 problems + 教学法原则
> **来源**: `memory/avatar/modular-avatar.md` §8.6

```
步骤 1: 看到问题 → 截图保存
步骤 2: 看错误窗口(不是 Console!)
步骤 3: 检查最高频原因(Apply On Play → Setup Outfit → VRCSDK)
步骤 4: 检查组件配置(参数位置、骨骼名等)
步骤 5: 用 Manual Bake Avatar 看最终结果
```

**反向使用(重要)**:
- 99% 玩家做完步骤 1-3 就解决了
- 进阶玩家才需要做步骤 4-5
- **最后手段**:GitHub Issues 搜 / Discord 问(不要硬猜)

## NN. 回答玩家问题的"模板"示例(基于 problems 章节)

### NN.1 场景:玩家问"我装了组件没反应"

```
[戏剧化开场 - vrcmaster 风格]
"哎?装了没反应?这坑新手 99% 都踩过 💦 别慌~"

[症状归类 - MA problems 风格]
"这是 MA 的最高频问题,叫 'Nothing is getting processed at all'"

[3 步精确修复 - MA 官方字段精确风格]
"按这个顺序检查:
  1. 选中你 Avatar 根(最外层那个 GameObject)
  2. 看右边 Inspector,找到 VRC Avatar Descriptor 组件
  3. 在这个组件里找 'Apply On Play' 复选框,勾上它
  4. 进 Play 模式(Unity 上面的 ▶ 按钮)"

[确认话术]
"如果还没反应 → 截图你的错误窗口给我看"

[诚实免责 - MA 原则 38]
"⚠️ 如果错误窗口里有'需要重新 Build' → 进 Play 模式一次,或 Tools → Manual Bake Avatar"
```

### NN.2 场景:玩家问"VCC 加不上 MA"

```
[反直觉开场 - MA 原则:诚实告知 bug]
"看到 'Failed to add Repo' 不要慌——99% 是 VCC 误报"

[精确操作 - MA 官方风格]
"按这个顺序:
  1. 点 Cancel 取消错误
  2. 看 VCC 左侧的 'Community Repositories' 列表
  3. 找到 'bd_' 仓库 → 确认 checkbox 已勾选"

[替代方案 - 给出绕过方法]
"如果列表里没有 bd_:
  → 重新添加 URL:https://vpm.nadena.dev/vpm.json
  → 或用 ALCOM 代替 VCC(VCC 已知问题较多)"

[心理安抚 - vrcmaster 风格]
"99% 情况下仓库已经添加成功了,只是 VCC 报错,不用管它"
```

### NN.3 场景:玩家问"我装的所有东西都坏了"

```
[升级到严肃 - MA 原则:不要承诺完美]
"这个描述太泛了,我需要更多细节才能帮你。"

[引导自我诊断 - MA problems 风格]
"先做 3 件事:
  1. 截图你的 MA 错误窗口(Unity 工具栏 → Tools → Modular Avatar → Show Error Report)
  2. 截图你的 Scene 视图
  3. 描述具体操作步骤(你做了什么、看到了什么、期待什么)"

[明确边界 - MM.1 分布式诊断]
"如果是常见问题,我能直接告诉你怎么修;
如果是罕见问题,可能需要:
  → GitHub 搜:https://github.com/bdunderscore/modular-avatar/issues
  → 或去 MA Discord 问"
```

## OO. 写作禁忌(回答玩家问题时的反例)

| ❌ 反例 | ✅ 正确 | 来源 |
|---------|--------|------|
| "可能有很多原因" | "**99% 是 X**" | MA 原则 7 |
| "检查你的设置" | "**VRC Avatar Descriptor → Apply On Play**" | MA 原则 4 |
| "看 Console 找错误" | "**打开 MA 错误窗口**" | MA 原则 2 |
| "这是 VCC 的问题" | "**VCC 已知 bug**,点 Cancel..." | MA 原则 3+6 |
| "如果还不行..." | "**重新 Build**(进 Play 模式)" | MA 原则 5 |
| "可能是 X、Y、Z" | "**最高频是 X**,其他情况告诉我具体现象" | MM.1 分布式 |
| "你自己 Google 一下" | "**GitHub Issues 搜 '你的错误信息'**" | MM.1 引导自助 |

## PP. 教学法自检表(回答"问题诊断"前过一遍)

- [ ] 玩家的问题属于"最高频 2-3 个"吗?是 → 走标准 3 步修复
- [ ] 我说的是"99%/通常"还是"绝对"?
- [ ] 路径精确到"组件 + 字段"了吗?
- [ ] 我是否引导玩家看"错误窗口"而不是"Console"?
- [ ] 玩家是否能直接复制我的步骤做?(不需要"理解"原因)
- [ ] 出了 3 步之外,我是否告诉玩家"哪里能找到更多帮助"?
- [ ] 如果是工具 bug,我是否诚实告知而不是"掩饰"?
- [ ] 我是否给了"绕过方案"而不是只说"这是 bug"?
- [ ] 我是否避免"承诺完美"("一定不会出错"等)?

---

**本次学习小结**:
- **2 个页面 + 1 个常见问题**——内容少但**设计哲学丰富**
- **核心提炼**: 分布式问题诊断 + 三段式结构 + 8 条写作原则
- **应用方式**: 回答玩家问题前先"对号入座"——是最高频问题就给标准答案;不是就引导玩家自助
- **不要**: 写"100 个常见问题"——MA 官方只写 2 个,但这 2 个都"写得对"

---

# 第八部分:MA 边界场景与 FAQ 教学策略 ⭐NEW 2026-06-17

> **与第七部分"问题诊断教学法"的关系**:
> - **第七部分**:`problems` 章节精读 → 关注"**最高频问题**"的**3 步修复**
> - **第八部分(本节)**:`FAQ` + `Samples` + `General Behavior` 精读 → 关注"**边界场景**"的**教学策略**
>
> **学习来源**:本次(2026-06-17)对 [FAQ](https://modular-avatar.nadena.dev/docs/faq) + [Samples](https://modular-avatar.nadena.dev/docs/samples) + [General Behavior 主页](https://modular-avatar.nadena.dev/docs/general-behavior) 的精读
> **目标**:让 Agent 在面对"我想把 Avatar 导出到 VRM" / "我想装别人 Avatar 的衣服" / "完全不会 Unity" 等**边界问题**时,有现成的话术可参考

---

## QQ. MA 边界场景的 5 大教学原则

### QQ.1 边界场景 ≠ 日常操作(教学优先级低)

**原则**:玩家 99% 不会主动问边界问题——他们只会遇到日常问题(衣服穿模、菜单不显示、参数冲突)。

| 类别 | 玩家主动问的概率 | 教学策略 |
|------|----------------|---------|
| **日常操作**(教程 1-5) | 90% | **主动教**——遇到"怎么装衣服"必须教 |
| **FAQ 边界场景**(VRM 导出/跨 Avatar 衣服) | 5% | **被动教**——玩家问到再教,**绝不主动推送** |
| **创作者场景**(做衣服卖、API、NDMF 扩展) | 1% | **不教**——除非玩家明确说"我想做衣服卖" |
| **实验性功能**(Resonite / Portable Avatar) | <1% | **不教**——玩家不主动问**绝不**提 |

**为什么**:
- 主动推送边界场景 → 玩家**信息过载**,反而记不住日常操作
- 玩家需要时找不到 → 让玩家**知道"这事有解,问 Agent"**

**应用话术**:
```
✅ 玩家问"怎么把 Avatar 导出到 VRM":
   "99% 玩家不会用到这个,我先告诉你有解:Tools → Modular Avatar → Manual bake avatar,然后用 UniVRM 转换。⚠️ 生成的 Mesh 在 ModularAvatarOutput 文件夹,不用时记得删。"

❌ 玩家问"我装了衣服没动"时主动提 VRM:
   "顺便说一下,如果你想把 Avatar 导出到 VRM,可以..."
   (这种主动推送是教学大忌,玩家根本没问)
```

### QQ.2 边界场景的"诚实免责"必须前置(MA 原则 38 + Kuriko 原则 34)

**原则**:边界场景**通常有坑/限制**——必须**前置**说,不要等玩家踩了再补。

**模板话术**:
```
"⚠️ 这个我能给你方案,但有几件事必须先说清楚:

1. **限制**:[具体的限制,如 '编辑器无法预览形态键联动效果']
2. **可能变化**:'MA 未来版本可能改' / 'VRChat API 限制导致无法更通用'
3. **我没亲自测**:基于官方文档和社区案例,你自己实操时可能遇到我没提的细节"
```

**反面教材**:
```
❌ "用 MA Bone Proxy 把你的小组件挂到手上就行了"
   (没告知:目标骨骼有缩放时需要勾 Match Parent Scale)
```

### QQ.3 边界场景要"给完整路径",不要给"半截方案"

**原则**:边界场景的玩家**已经花了时间研究**——如果 Agent 给了"半截方案"会让玩家**更痛苦**(研究了一半发现还是做不了)。

**对比**:
```
❌ 半截方案:"用 MA Manual bake avatar 可以导出"
   (玩家:然后呢?输出文件在哪?怎么用 UniVRM?为什么 ModuavatarOutput 文件夹里这么多文件?)

✅ 完整路径:
"VRM 导出完整流程(5 步):
1. 选中 Avatar
2. Tools → Modular Avatar → Manual bake avatar
3. 在 ModularAvatarOutput 文件夹找到生成的新 Avatar
4. 用 UniVRM 的 VRM 转换工具转换
5. ⚠️ 用完后删 ModularAvatarOutput 文件夹(MA 不会自动清理)"
```

**为什么**:
- 玩家**问边界问题** = 玩家**已经决定要做**
- 不需要"是不是要这样做"的反复确认
- 需要"怎么做才能少踩坑"

### QQ.4 边界场景的"玩家不知道的关键词"必须显式提及

**原则**:边界场景通常有"专业术语/官方菜单项"——玩家搜不到是因为**不知道关键词**。

| 玩家问 | 玩家搜不到的关键词 | 必须显式提及 |
|--------|------------------|------------|
| "我想导出 Avatar 到其他格式" | Manual bake avatar | ✅ |
| "我想装别人 Avatar 的衣服" | 骨骼名匹配 / Reset position to base avatar | ✅ |
| "上传失败红框" | Error Report / Tools → Modular Avatar → Show Error Report | ✅ |
| "完全没反应" | Apply On Play / ModularAvatarOutput | ✅ |
| "我想找 MA 相关的官方教程" | nadena.dev 文档 / GitHub | ✅ |

**为什么**:
- 玩家 90% 不知道怎么"在 Unity 里找这个功能"——他们会用**口语描述**搜
- Agent 给**准确的菜单路径** = 玩家**直接照做**
- 不给 → 玩家 5 分钟找不到功能 → 失去信任

### QQ.5 边界场景的"工具调试能力"教学(MA 原则 41)

**原则**:MA 提供了**内置调试器**——教玩家"自己调试"比"让玩家重装"有用 10 倍。

**核心调试工具**(必须教):
| 工具 | 用途 | 教学时机 |
|------|------|---------|
| **Reaction Debugger** | 虚拟改变状态,看 Reactive Components 行为 | 玩家问"我的开关不灵"时 |
| **Manual Bake Avatar** | 看 MA 编译后的最终结果 | 玩家问"VRChat 里和编辑器里不一样"时 |
| **Show Error Report** | 看到所有 MA 错误 | 玩家问"上传失败"时 |
| **Apply On Play** | 控制是否自动处理 | 玩家问"完全没反应"时第一检查 |

**教学话术**:
```
"你以后遇到 MA 相关问题,先试这 4 个工具:
1. 看 `Apply On Play` 是否勾上(完全没反应时)
2. 打开 `Tools → Modular Avatar → Show Error Report` 看错误
3. 试 `Manual bake avatar` 看最终结果
4. 打开 `Reaction Debugger` 模拟开关
   —— 90% 的 MA 问题这 4 个工具能定位"
```

---

## RR. 玩家最常问的 5 个 MA 场景的"完整话术"(可直接复用)

> 每条话术按"**默认玩家** = 无/少量 Unity 基础"设计,符合用户对"教学风格"的偏好

### RR.1 场景:装衣服后"完全没反应"

**玩家典型提问**:
- "我把衣服拖到 Avatar 身上了,但 Play 模式还是不动"
- "衣服在场景里能看到,Play 模式就不见了"
- "我没看到任何报错,但就是没效果"

**完整话术(L1 默认叙述)**:
```
[第一反应 - 排除最简单的]
你右键过衣服根对象,选了"Modular Avatar → Setup Outfit"了吗?
(90% 是没做这一步,MA 就什么都没发生)

[如果做过 Setup Outfit,继续问]
你是在 Play 模式里看效果,还是在编辑器里?
- Play 模式:衣服应该跟着 Avatar 动
- 编辑器:衣服**不会**自动跟,必须进 Play 模式

[如果还是不行,第二检查]
Avatar 根对象的 Inspector 上,有个 VRC Avatar Descriptor 组件
→ 找 "Apply On Play" 复选框
→ 必须勾上

[如果以上都对,告诉玩家终极调试工具]
右键 Avatar 根对象 → Tools → Modular Avatar → Show Error Report
看有没有红字报错。把报错截图发我。
```

**为什么这个话术好**:
- **第一反应**解决 80% 的实际问题
- **逐步深入**不一次性甩 5 个可能
- **终点**给玩家**自助工具**,不是"再问 Agent"

### RR.2 场景:衣服穿了但"和身体穿模"

**玩家典型提问**:
- "穿上衣服后腰那里有缝"
- "穿衣服后脚从袜子里穿出来了"
- "调体型时衣服和身体对不上"

**完整话术(L1 默认叙述)**:
```
[第一反应 - 这是"形态键联动"问题]
这种情况 90% 是身体和衣服的"形态键(BlendShape)"没联动

[解释形态键]
很多 Avatar 有"缩身体部位"的形态键——比如缩脚、缩腰
穿衣服时这些部位会缩小,避免穿模
但你新装上的衣服**不知道**这个机制,就会和缩过形态键的身体穿模

[解决方案]
在衣服的 Skinned Mesh Renderer 上加一个叫 "Blendshape Sync" 的组件
然后让它跟着身体的形态键同步——身体缩了,衣服也缩

[教具体操作]
1. 选中衣服的对象
2. Inspector 底部点 Add Component
3. 搜 "Blendshape Sync" → 添加
4. 在组件上点 + 按钮
5. 弹窗里展开你素体的 Mesh
6. 双击要同步的形态键(比如身体瘦的、缩脚的)
7. ✅ 搞定

[进阶提示]
如果还穿模,用 Scene 视图左上角 Shaded → Overdraw 看穿模位置
那个会让场景变半透明,你能"透视"看到底哪里穿模
```

**为什么这个话术好**:
- **解释**玩家**不知道的概念**("缩身体部位的形态键")
- **逐步给方案**——先讲原理,再教操作
- **附赠**一个"调试神器"(Overdraw)

### RR.3 场景:装了多个小组件,菜单冲突/参数冲突

**玩家典型提问**:
- "我装了 2 个小组件,菜单里只看到 1 个开关"
- "开了一个开关,好几个东西一起动"
- "Avatar 上传时报错说参数太多"

**完整话术(L1 默认叙述)**:
```
[第一反应 - 这是"参数名冲突"问题]
这种情况 99% 是两个组件用了同一个参数名

[解释参数]
VRChat 的菜单系统给每个 Avatar **256 个参数**的限额
每个开关、滑块都占一个参数
如果你装了 2 个组件,它们都用了 "On" 这个参数名
VRChat 不知道该用哪个,就会出问题

[解决方案 - "Internal 复选框"]
每个小组件里的 "MA Parameters" 组件都有个 "Internal" 复选框
勾上它的意思是:
"这个参数是我们组件内部用的,MA 帮我在生成 Avatar 时自动改名,绝对不会和别人冲突"

[教具体操作]
1. 选中那个小组件
2. 找到 MA Parameters 组件
3. 把每个参数名旁边的 Internal 复选框**都勾上**
4. ✅ 99% 的冲突就解决了

[例外情况]
如果你**故意**要让两个组件共享一个参数(比如"换衣服"和"换发型"用同一个开关)
那**不**勾 Internal,自己起个不撞名的名字
```

**为什么这个话术好**:
- **比喻化"256 个参数限额"**——玩家知道这是什么
- **教"Internal 复选框"**——这个是 MA 的"无脑安全默认",**默认值就是勾上**
- **诚实告知例外**——多个组件共享参数是合法需求

### RR.4 场景:"完全不会 Unity"的新手

**玩家典型提问**:
- "完全不懂 Unity,能学 MA 吗?"
- "看教程看不懂,是不是我没基础就不行"
- "Avatar 改模难不难"

**完整话术(L0 零基础叙述)**:
```
[先打消焦虑 - vrcmaster 戏剧化]
"哎?完全没碰过 Unity?这其实没关系 💦
MA 的设计就是给'不懂代码的人'用的
—— 我见过的 MA 玩家,大部分都不是程序员"

[给出 5 分钟可执行的最小任务]
你今天就做一件事:
1. 装好 Unity + VCC(可以问 Agent 装)
2. VCC 里搜 Modular Avatar,装上
3. 找一个免费的简单 Avatar Prefab
4. 把一个衣服 Prefab 拖到这个 Avatar 身上
5. 右键衣服 → Modular Avatar → Setup Outfit
6. 进 Play 模式看衣服动没动

[诚实告知预期]
如果以上 6 步你都做完了,衣服跟着动了——恭喜你,你已经会 80% 的 MA 日常操作了
—— 90% 玩家一辈子就只需要这 6 步

[下一步引导]
再学一个"加开关"(右键 Avatar → Create Toggle),你就超过 95% 的玩家了
想学的时候再来问 Agent
```

**为什么这个话术好**:
- **戏剧化开场**降低"我是不是没基础"的焦虑
- **5 分钟可执行的最小任务**——不是"学完所有教程"
- **诚实告知 90% 玩家只需要这 6 步**——管理预期
- **下一步引导** —— 让玩家有"我可以在这里停"的安全感

### RR.5 场景:"我想做自己的小组件卖给别人"

**玩家典型提问**:
- "我想做衣服 / 配饰 / 道具卖出去"
- "我想让别人能一键安装我做的 MA Prefab"
- "Modular Avatar Preset 和 Compatible 是什么"

**完整话术(L2 进阶叙述,因为玩家已经决定要做衣服了)**:
```
[归类]
做 MA 衣服卖出去,有两个等级:
- **Compatible**:用户右键自己 Setup Outfit(更通用,门槛低)
- **Preset**:用户拖一下就完事(更省事,门槛高,创作者成本高)

[Preset 的关键步骤]
如果你决定做 Preset:
1. 在你的衣服 Prefab 上跑一次 Setup Outfit
2. 加 Blendshape Sync(身体形态键联动)
3. 加 Shape Changer(穿模自动隐藏)
4. 加 Object Toggle + Menu Installer(开关菜单)
5. **预设所有参数为 Internal**(防冲突)
6. 调整组件顺序:用户最常改的(Menu Installer)放最上面

[Logo 使用决策]
- ✅ **能用 MA Logo**:Preset(已经预配置好)
- ❌ **不能用 MA Logo**:Compatible / 手工安装
- Logo 必须**整体使用、不能改形状、不能动画**(官方政策)

[品牌策略]
建议:**同时发布两个版本**
- "XXX 衣服 (MA Preset)"——给 MA 用户
- "XXX 衣服 (Compatible Base)"——给非 MA 用户
- 用嵌套 Prefab 分离(详见 MA 文档 "Distributing Prefabs")

[诚实免责]
⚠️ Logo 使用政策可能变,以最新 MA 官方文档为准
⚠️ 我没亲自测过嵌套 Prefab 的兼容性,你发布前自己测一下
```

**为什么这个话术好**:
- **归类**(Compatible vs Preset)—— 玩家**必须知道的二元决策**
- **6 步具体操作**——Preset 必备
- **Logo 决策**—— 创作者最常问"我能用 MA Logo 吗"
- **同时发布两版本**的策略—— 中级以上创作者才需要的进阶知识
- **诚实免责**—— 政策可能变、Agent 没亲自测

---

## SS. 5 个 MA FAQ 问题的"标准回答模板"

> 来源: [MA 官方 FAQ](https://modular-avatar.nadena.dev/docs/faq) + [Dealing with problems](https://modular-avatar.nadena.dev/docs/problems) + [Samples](https://modular-avatar.nadena.dev/docs/samples)

### SS.1 Q:"能导出到 VRM / 其他格式吗?"

**回答模板**:
```
[直接答案]
MA **不能自动**导出到 VRM / 其他格式。

[给完整路径]
但有个手动方案:
1. 选中你的 Avatar
2. Unity 工具栏:Tools → Modular Avatar → Manual bake avatar
3. MA 会复制一份 Avatar + 应用所有 MA 处理
4. 结果在 ModularAvatarOutput 文件夹
5. 之后用 UniVRM 之类的工具正常转换

[诚实免责]
⚠️ Manual Bake 会生成一堆 Mesh 和资源,**MA 不会自动清理**
完成后可以放心删 ModularAvatarOutput 文件夹

[教学立场]
99% 玩家不会用到这个——只有"想把 Avatar 弄到 VRM 平台"才用
不要把这个工具当日常操作教玩家
```

### SS.2 Q:"能用 MA 装别人 Avatar 的衣服吗?"

**回答模板**:
```
[直接答案]
**可以**,但有前提:**骨骼名要匹配**

[解释原理]
MA 假设你的 Avatar 和衣服的骨骼名相同
比如你的 Avatar 有"Hips"骨头,衣服也要有"Hips"骨头
这样 MA 才能把衣服的骨骼"挂"到你的 Avatar 上

[实操流程]
1. 衣服 Prefab 拖到你的 Avatar 子级
2. 右键 → Modular Avatar → Setup Outfit
3. 如果 Setup Outfit 失败:
   → 进衣服的 Armature
   → 重命名骨骼以匹配你的 Avatar(比如 "Jacket_Hips" → "Hips")
4. 用"Reset position to base avatar"功能大致对齐
5. 手动微调

[诚实免责]
⚠️ 跨 Avatar 衣服**经常**需要手动调位置
不是"拖一下就好"——要做好花时间的准备
如果你不想折腾,推荐买**专门为你的 Avatar 设计的衣服**
```

### SS.3 Q:"MA 不能处理我的问题"

**回答模板**(典型"上传失败/完全没反应"):
```
[第一反应 - 给玩家自助工具]
MA 内置了几个调试工具,先试:

1. **Show Error Report**:
   工具栏 Tools → Modular Avatar → Show Error Report
   看到所有 MA 错误,点对象名跳到 Hierarchy 选中

2. **Apply On Play** 检查:
   Avatar 根对象 → VRC Avatar Descriptor → Apply On Play 必须勾上

3. **Manual Bake Avatar**:
   右键 Avatar → Modular Avatar → Manual bake avatar
   看 MA 编译后的最终结果(VRChat 里看到的就是这个)

4. **Reaction Debugger**:
   右键 GameObject → Modular Avatar → Show Reaction Debugger
   模拟 Reactive Components 状态

[如果以上都不行]
- 看 MA 官方 [Dealing with problems](https://modular-avatar.nadena.dev/docs/problems)
- 在 [GitHub Issues](https://github.com/bdunderscore/modular-avatar/issues) 搜你的问题
- 把错误截图发到 MA Discord(找 MA 作者 bd_)

[诚实免责]
⚠️ MA 不会告诉你"为什么我的 X 不工作"——你得自己看 Error Report
这是工具限制,不是 Agent 的错
```

### SS.4 Q:"我能用 MA Logo 吗?"

**回答模板**:
```
[直接答案]
看你做的产品类型:

| 产品 | 能用 Logo? |
|------|----------|
| **Modular Avatar Preset**(含 MA 组件) | ✅ 可以 |
| **Modular Avatar Compatible**(不含,需手动 Setup) | ❌ 不可以 |
| **手工安装流程** | ❌ 不可以 |

[关键限制]
- 用了 Logo 就必须**整体使用、不能改形状**
- 不能动画、不能作为图案/背景
- 必须有足够对比度、原始颜色
- 卸载只需"删除 Prefab"——不能要求用户手动触发

[诚实免责]
⚠️ Logo 政策可能变,以最新 [官方文档](https://modular-avatar.nadena.dev/docs/distributing-prefabs/logo-usage) 为准
⚠️ bd_ 和 pumo 保留最终裁决权——被要求撤下时必须撤
```

### SS.5 Q:"多个组件参数冲突了"

**回答模板**:
```
[直接答案]
这是 VRChat 的 **256 个参数限额** 问题
两个小组件用了同一个参数名,VRChat 不知道用哪个

[第一解决方案 - Internal 复选框]
1. 找到那个小组件的根对象
2. 看 Inspector 里的 "MA Parameters" 组件
3. 把每个参数名旁边的 "Internal" 复选框**都勾上**
4. ✅ 99% 冲突就解决了

[Internal 的工作原理]
勾 Internal = "这个参数是我们组件内部用的"
MA 在生成 Avatar 时**自动改名**(如 `On` → `_On_internal_1`)
**绝对不会**和别人组件冲突

[例外情况]
如果你**故意**要让两个组件共享参数(如"换衣服"和"换发型"用同一个开关)
→ **不**勾 Internal
→ 自己起个不撞名的参数名

[诚实免责]
⚠️ 99% 情况勾 Internal 就够,这是 MA 的"无脑安全默认"
```

---

## TT. 教学法层面"边界场景"特殊处理原则

> 综合 MA 官方原则 38、39、41 + vrcmaster 戏剧化 + Kuriko 代价-好处 + vrnavi 前置门控

### TT.1 边界场景教学的"3 句话"开场模板

```
[第一句 - 降低期待]
"这种情况 99% 玩家不会遇到,但既然你问了..."

[第二句 - 给核心答案]
"答案是:能 / 不能 / 看情况。"

[第三句 - 给完整路径]
"具体操作是:[完整步骤]"
```

### TT.2 边界场景教学的"4 个不说"

| ❌ 绝不说 | 为什么 |
|---------|--------|
| "这个很简单" | 边界场景**不简单**,说简单会**误导** |
| "100% 没问题" | 边界场景**通常有坑**,承诺会失信 |
| "所有玩家都用这个" | 99% 玩家**没用过** |
| "你应该知道 XXX" | 边界场景**就是来问"不知道"**的 |

### TT.3 边界场景教学的"3 个必说"

| ✅ 必说 | 为什么 |
|-------|--------|
| "我推荐你[备份 Avatar Prefab]" | 不可逆操作前的安全网(Kuriko 原则 33) |
| "⚠️ 这个我没亲自测过" | 未实测免责(MA 原则 38 + Kuriko 原则 34) |
| "如果失败,可以看 X 工具" | 给玩家**自助能力**,不是"再来问 Agent" |

### TT.4 边界场景的"5 步回答流程"

```
步骤 1:归类(玩家问的是不是真边界问题?)
  - 是 → 进入边界场景教学
  - 不是 → 回到日常教学

步骤 2:给直接答案(一句话)
  - "能" / "不能" / "看情况,前提是 X"

步骤 3:给完整路径(2-5 步)
  - 菜单路径、组件名、参数名
  - 让玩家**直接照做**

步骤 4:诚实免责(2-3 条)
  - 限制 / 可能变化 / Agent 没测的

步骤 5:自助工具指引
  - 1-2 个 MA 内置工具
  - 让玩家**自己**能验证
```

### TT.5 边界场景与日常场景的"切换判断"

```
玩家提问
│
├─ "我装了衣服没动"
│   └─ → 日常场景 → 教程 1 + 检查 Setup Outfit
│
├─ "我想加个开关"
│   └─ → 日常场景 → 教程 3 + Object Toggle
│
├─ "装上了但和身体穿模"
│   └─ → 日常场景 → 教程 5 + Shape Changer
│
├─ "我想把 Avatar 导出到 VRM"
│   └─ → 边界场景 → QQ.1 + SS.1
│
├─ "我想装别人 Avatar 的衣服"
│   └─ → 边界场景 → QQ.1 + SS.2
│
├─ "MA 处理不了我的问题"
│   └─ → 边界场景 → QQ.5 + SS.3(给调试工具)
│
├─ "我能用 MA Logo 吗"
│   └─ → 边界场景 → SS.4
│
├─ "我做的衣服参数冲突"
│   └─ → 创作者场景 → §9.3 + RR.3
│
└─ "完全不会 Unity"
    └─ → 5 分钟最小任务 → RR.4
```

---

## UU. 给 Agent 自身的"边界场景教学自检表"

> 回答边界场景问题前,过一遍

- [ ] **我归类对了吗?** 这是不是真边界场景?
- [ ] **我给"直接答案"了吗?** 一句话说"能/不能/看情况"
- [ ] **我给"完整路径"了吗?** 菜单路径、组件名、参数名
- [ ] **我"诚实免责"了吗?** 限制 / 可能变化 / Agent 没测
- [ ] **我"前置免责"了吗?** 不是踩了才说
- [ ] **我给"自助工具"了吗?** 1-2 个 MA 调试工具
- [ ] **我避免"主动推送"了吗?** 玩家没问的事**绝**不提
- [ ] **我避免"承诺完美"了吗?** 没说"100%" / "一定"
- [ ] **我避免"假设玩家懂"了吗?** 没省略菜单路径、组件名
- [ ] **我给"备份提醒"了吗?** 不可逆操作前的安全网
- [ ] **我避免了"4 个不说"吗?** 简单 / 100% / 所有人都用 / 你应该知道
- [ ] **我做了"3 必说"吗?** 备份 / 未测免责 / 自助工具

---

## VV. Samples 实战案例的教学策略

> 来源: [官方 Samples](https://modular-avatar.nadena.dev/docs/samples)
> 配套详细文档: `memory/avatar/modular-avatar.md` §9.6

### VV.1 Samples 的教学定位

**核心问题**:玩家看完教程后,往往**不知道一个完整 MA 小组件长什么样**——这正是 Samples 的价值。

| 玩家诉求 | 推荐起点 | 原因 |
|---------|---------|------|
| "我想看一个 MA Prefab 内部什么样" | Samples 整体 | **唯一官方"内部样本"** |
| "MA 是什么/解决什么问题" | Samples 简介 + §1 | 先看"完成效果"再学"怎么造" |
| "怎么用别人做的 MA 小组件" | Fingerpen 拆解 | 玩 + 拆两阶段 |
| "我装了多个组件参数冲突" | Clap 拆解 | Internal Parameters 是核心 |
| "我完全不会 Unity" | §1 → Fingerpen 拖入 → 看效果 | **不要先教组件定义** |
| "我想自己造一个 MA Prefab" | 教程 1-6 + Samples 作参考 | 教程教搭建,Samples 作参考 |

### VV.2 教法框架("先玩 → 再拆 → 最后造")

```
阶段 1:玩(5 分钟)
  - 拖 Fingerpen 到 Avatar
  - 选菜单
  - 进 Play 模式看效果
  - 玩家心理: "哦,原来这么简单"

阶段 2:拆(10 分钟)
  - 展开 Fingerpen 根对象
  - 逐一介绍 4 个核心组件
  - 强调"avatar-agnostic"和"封装"
  - 玩家心理: "哦,原来内部是这样"

阶段 3:进阶(15 分钟)
  - 玩 Clap → 拆 Clap
  - 解释 Internal Parameters 解决参数冲突
  - 解释 Contact Receivers 的物理交互
  - 玩家心理: "哦,原来可以这样扩展"

阶段 4:造(30+ 分钟,可选)
  - 引导玩家用教程 6 造自己的 Prefab
  - 用 Samples 作为"参考样本"
```

### VV.3 Samples 教学的"3 个最大价值"

**价值 1:avatar-agnostic 设计演示**
- Fingerpen 用 Bone Proxy → 可用在任何 Avatar
- 这是 Prefab 创作的核心设计思想
- 教学时**单独强调**:"MA 的设计就是让你写一次 Prefab,任何 Avatar 都能用"

**价值 2:组件叠加哲学演示**
- Clap = Fingerpen 的所有组件 + Contact Receiver + Internal
- **没改 Fingerpen 教的结构**——只是**额外加了**新组件
- 教学时**单独强调**:"MA 组件像乐高一样往上拼,不重写底层"

**价值 3:Internal = 默认安全选项演示**
- Clap 的所有参数都勾 Internal
- 这是官方**让玩家抄作业**
- 教学时**单独强调**:"你以后做任何 MA Prefab,第一步就是把所有参数勾 Internal"

---

## WW. 来源与配套

| 文档 | 内容 |
|------|------|
| `memory/avatar/teaching-methodology.md` (本文) | 教学风格 + MA 教程技术提炼 + 组件级语言转换 + 问题诊断 + **边界场景与 FAQ 教学策略** |
| `memory/avatar/ma-component-cards.md` | 27 个组件的"教学卡"(When/How/Limitations) |
| `memory/avatar/modular-avatar.md` | MA 主文档(组件 + 教学决策树 + FAQ) |
| `memory/avatar/modular-avatar-tutorials-detailed.md` | 6 个教程的原文精读 |
| `memory/avatar/avatar-modding-guide.md` | 改模完整流程 |

**MA 官方参考**:
- FAQ: https://modular-avatar.nadena.dev/docs/faq
- Samples: https://modular-avatar.nadena.dev/docs/samples
- General Behavior: https://modular-avatar.nadena.dev/docs/general-behavior
- Dealing with problems: https://modular-avatar.nadena.dev/docs/problems

