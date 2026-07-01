---
title: VRChat in Virtual Machine — VM + EAC 调试配置
category: world
subcategory: development

knowledge_level: applied
status: active

tags:
  - world
  - vm
  - eac
  - libvirt
  - proxmox
  - debugging

aliases:
  - VM Setup
  - Virtual Machine
  - 虚拟机
  - EAC
  - Easy Anti-Cheat
  - libvirt
  - QEMU
  - Proxmox
  - Hyper-V passthrough

related:
  - world/udon/launch-options.md
  - world/udon/using-build-test.md
  - world/udon/debugging-udon-projects.md
  - world/vvmw.md

source: docs.vrchat.com/docs/using-vrchat-in-a-virtual-machine
source_type: official
version: 1.0
last_review: 2026-06-30
confidence: High
---

# VRChat in Virtual Machine — VM + EAC 调试配置

> 来源: https://docs.vrchat.com/docs/using-vrchat-in-a-virtual-machine
> 本地化日期: 2026-06-30
> 状态: ✅ FACT (VRChat 官方 + 社区贡献)
> 关联: `world/udon/launch-options.md` (启动选项) + `world/udon/using-build-test.md` (Build & Test)

---

## ⚠️ 重要警告

> [FACT] **运行 VRChat 在虚拟机中是 **不受官方支持** 的**。
>
> VRChat 提供此文档是**基于研究**，但：
> - 这些方法**任何时候可能停止工作**
> - **官方不保证**在 VM 中能正常运行
> - 文档会尽量保持更新

> **🔴 关键事实**:
> - VRChat 的反作弊系统是 **Easy Anti-Cheat (EAC)**
> - **EAC 在 VM 环境中通常失败**
> - 通过特定配置**某些情况可绕过**

> [FACT] 经验上，**这些 workarounds 不影响性能**。

---

## 概述

> [FACT] 核心问题: **EAC 通过 CPUID 信息检测 VM**。
>
> 默认 CPUID 显示 `"Microsoft HV"`（hyper-v），**EAC 拒绝**。
>
> 通过修改 CPUID 信息（Hyper-V vendor_id），可以让 EAC 认为不在 VM 中。
>
> **技术原理**:
> - 修改 `CPUID leaf 0x40000000` 的 hyper-v vendor id
> - 默认 "Microsoft HV" → 改为其他值
> - 使用 `hv-passthrough` 模式 → "Linux KVM Hv"（EAC 接受）

> [FACT] **重要**:
> - **不需要** 隐藏 KVM 接口 (`kvm=off` 或 `<kvm><hidden state='on'/></kvm>`)
> - **不影响** 性能
> - 已有 NVIDIA code 43 修复配置的 VM 通常**开箱即用**

---

## 1. libvirt (QEMU/KVM)

> [FACT] **libvirt** 是 Linux 上管理 VM 的标准工具。

### 1.1 vendor_id 配置

> [FACT] **修改 VM 的 XML 配置**:
>
> ```bash
> virsh edit VM_NAME
> ```
>
> 在 `<features>` 块下的 `<hyperv>` 中添加:
>
> ```xml
> <vendor_id state='on' value='0123756792CD'/>
> ```
>
> 完整示例:
>
> ```xml
> <features>
>   <hyperv mode='custom'>
>     <!-- other things here -->
>     <vendor_id state='on' value='0123756792CD'/>
>   </hyperv>
>   <!-- other things here -->
> </features>
> ```

> [FACT] **推荐 vendor_id**: `0123756792CD`（或 `0123456789AB`）

### 1.2 Hyper-V Passthrough 模式（更优）

> [FACT] **更优的方案** — 使用 Hyper-V passthrough 模式:
>
> ```xml
> <hyperv mode='passthrough'>
>   <!-- whatever -->
> </hyperv>
> ```
>
> **效果**:
> - 启用**所有可用的 hyper-v enlightenments**
> - **包括 vendor id**（EAC 接受）
> - **可能改善性能**（其他 enlightenments）

> [FACT] **enlightenments** = hyper-v 的"paravirtualized extensions"
> - Linux kernel 或 QEMU 提供给 Windows 客户机
> - 在虚拟环境中增强性能/功能

### 1.3 SMBIOS 配置（2022-08-26 后必需）

> [FACT] **2022-08-26 后**，仅 vendor_id 修复**可能不够**。
>
> 需**手动设置 SMBIOS 字符串**模拟真实硬件。
>
> 理论任何有效硬件配置都可行，**推荐用真实系统的信息**。

#### 1.3.1 获取本机信息

> [FACT] 推荐命令:
>
> ```bash
> dmidecode --type bios
> dmidecode --type baseboard
> dmidecode --type system
> ```

#### 1.3.2 libvirt XML 配置

> [FACT] 添加到 domain XML（用本机信息替换）:
>
> ```xml
> <sysinfo type="smbios">
>   <bios>
>     <entry name="vendor">American Megatrends Inc.</entry>
>     <entry name="version">F31o</entry>
>     <entry name="date">12/03/2020</entry>
>   </bios>
>   <system>
>     <entry name="manufacturer">Gigabyte Technology Co., Ltd.</entry>
>     <entry name="product">X570 AORUS ULTRA</entry>
>     <entry name="version">x.x</entry>
>     <entry name="serial">BASEBOARD SERIAL HERE (or "Default string")</entry>
>     <entry name="uuid">BASEBOARD UUID HERE</entry>
>     <entry name="sku">BASEBOARD SKU HERE (or "Default string")</entry>
>     <entry name="family">X570 MB</entry>
>   </system>
> </sysinfo>
> ```
>
> **UUID 必须**与 domain XML 顶部 UUID **匹配**，否则 libvirt 报错。

#### 1.3.3 启用 SMBIOS

> [FACT] 添加到 `<os>` 组:
>
> ```xml
> <os>
>     <smbios mode="sysinfo"/>
>     <!-- whatever -->
> </os>
> ```

---

## 2. QEMU 命令行

> [FACT] 如果用 **QEMU 命令行**（不用 libvirt），加 `-cpu` flag。

### 2.1 基本配置

> [FACT] 修改 `-cpu` flag:
>
> ```bash
> -cpu 'host,migratable=off,hypervisor=on,topoext=on,hv_relaxed,hv_reset,hv_runtime,hv_stimer,hv_synic,hv_time,hv_vapic,hv_vpindex,hv-frequencies,hv-avic,hv-vendor-id=0123456789AB,host-cache-info=on,apic=on,invtsc=on'
> ```
>
> 如果已有 `-cpu` 参数，**追加** `,hv-vendor-id=0123756792CD`:
>
> ```bash
> -cpu '原有参数,hv-vendor-id=0123756792CD'
> ```

> [FACT] **推荐设置**额外启用:
> - `hv_relaxed` / `hv_reset` / `hv_runtime` / `hv_stimer` / `hv_synic` / `hv_time` / `hv_vapic` / `hv_vpindex`
> - `hv-frequencies` / `hv-avic`
> - `host-cache-info` / `apic` / `invtsc`
>
> 这些启用**高级方法**确保 CPU L2/L3 cache topology 正确传递。

### 2.2 Passthrough 模式

> [FACT] QEMU 中也支持 passthrough:
>
> ```bash
> -cpu host,migratable=off,hypervisor=on,invtsc=on,hv-time=on,hv-passthrough=on
> ```
>
> ⚠️ **`hv-passthrough` 不推荐**:
> - 激活 KVM 支持的**所有** Hyper-V entitlements
> - 不仅是硬件支持的
> - 详见: https://www.qemu.org/docs/master/system/i386/hyperv.html#supplementary-features
>
> [FACT] 使用 `hv-passthrough` 时:
> - 不需要其他 `hv-foo` 参数
> - `hv-time` **可能**是例外（源文档存疑）
> - passthrough 会处理其他

### 2.3 SMBIOS 命令行

> [FACT] QEMU 用 `-smbios` flag:
>
> ```bash
> -smbios 'type=0,version=F31o,vendor=American Megatrends International,, LLC.,uefi=on,release=5.17,date=12/03/2020'
> -smbios 'type=1,version=-CF,sku=Default string,product=X570 AORUS ULTRA,manufacturer=Gigabyte Technology Co.,, Ltd.,uuid=d30dbc2a-d9b0-11ed-afa1-0242ac120002,serial=Default string,family=X570 MB'
> -smbios 'type=2,asset=Default string,version=Default string,product=X570 AORUS ULTRA,location=Default string,manufacturer=Gigabyte Technology Co.,, Ltd.,serial=Default string'
> -smbios 'type=3,asset=Default string,version=Default string,sku=Default string,manufacturer=Default string,serial=Default string'
> -smbios 'type=4,asset=Unknown,version=AMD Ryzen 9 5950X 16-Core Processor            ,part=Zen,manufacturer=Advanced Micro Devices,, Inc.,serial=Unknown,sock_pfx=AM4'
> -smbios 'type=11,value=Default string'
> -smbios 'type=17,bank=Bank 0,asset=Not Specified,part=OV_8GR1,manufacturer=OEM_VENDOR,speed=2666,serial=OEM33161,loc_pfx=DIMM 0'
> ```

> [FACT] 推荐用**脚本**生成（避免手动填写）:
> - https://gist.github.com/kiler129/5d437a37c07ac6eb1cdf0e595e488fd2
> - 自动从真实硬件获取值
> - **确保**不与其他用户完全相同

---

## 3. Proxmox / PVE

> [FACT] **Proxmox Virtual Environment (PVE)** 设置:

### 3.1 操作系统设置

> [FACT] 在 VM Options 标签，**操作系统** 必须设为 **"Windows 7"** 或更高。

### 3.2 SMBIOS 设置

> [FACT] **步骤**:
> 1. 填写 BIOS 信息（VM → Options → SMBIOS Setting，"hoge" 占位 OK）
> 2. **网络卡 MAC 地址** 改为 **INTEL** 类型

> 参考: https://www.reddit.com/r/Proxmox/comments/1cq87xc/comment/l3q7c5k/

### 3.3 性能调优

> [FACT] **EAC 不直接相关**，但 Proxmox 上跑 VR 游戏需**一致可预测性能**。
>
> Proxmox 论坛教程: https://forum.proxmox.com/threads/hey-proxmox-community-lets-talk-about-resources-isolation.124256/

---

## 4. 技术原理（深入）

### 4.1 CPUID Hyper-V Vendor ID

> [FACT] hyper-v vendor_id 设置 CPUID `leaf 0x40000000` 的值。
>
> - **默认**: "Microsoft HV" → EAC 拒绝
> - **修改后**: "Linux KVM Hv" → EAC 接受
> - **位置**: CPU 的 hypervisor vendor identification string

### 4.2 hypervisor flag 不变

> [FACT] **不需要**修改 `hypervisor` flag。
>
> 客户机 OS kernel（Windows NT）**仍识别** VM 环境，**仍应用性能优化**。
>
> 客户机 Task Manager 仍显示 "running in a virtual machine"。
>
> **不影响** EAC 在 KVM 环境中的检测。

### 4.3 NVIDIA Code 43 类似性

> [FACT] 这个方法与著名的 **"NVIDIA code 43 fix"** 非常相似。
>
> **唯一区别**: 不需要隐藏 KVM 接口 (`kvm=off` 或 `<kvm><hidden state='on'/></kvm>`)。
>
> 如果你**已经**为 NVIDIA code 43 设置 VM（参见 https://passthroughpo.st/apply-error-43-workaround/），**VRChat + EAC 应该开箱即用**。

---

## 5. 验证 CPUID（高级）

> [FACT] 验证 CPUID 修改生效的 C++ 程序:

```cpp
#include <iostream>
#include <intrin.h>

void print_leaf(int leaf)
{
    int res[4];
    __cpuid(res, leaf);

    std::cout << "leaf: 0x" << std::hex << leaf << std::endl;

    for (size_t i = 0; i < 4; i++)
    {
        std::cout << "res" << i << ": 0x" << std::hex << res[i] << " (";
        for (size_t j = 0; j < 4; j++)
        {
            char part = (res[i] >> j * 8) & 0xff;
            std::cout << part;
        }
        std::cout << ")" << std::endl;
    }
}

int main()
{
    // 参考:
    // https://docs.microsoft.com/en-us/virtualization/hyper-v-on-windows/tlfs/feature-discovery
    // https://docs.microsoft.com/en-us/cpp/intrinsics/cpuid-cpuidex?view=msvc-170

    std::cout << "manufacturer id:" << std::endl;
    print_leaf(0); // Manufacturer ID

    std::cout << "hyper-v id:" << std::endl;
    print_leaf(0x40000000); // Hypervisor CPUID Leaf Range

    return 0;
}
```

### 5.1 预期输出（hv-passthrough 模式）

> [FACT] 预期输出示例:
>
> ```
> manufacturer id:
> leaf: 0x0
> res0: 0x10 (►   )
> res1: 0x68747541 (Auth)
> res2: 0x444d4163 (cAMD)
> res3: 0x69746e65 (enti)
> hyper-v id:
> leaf: 0x40000000
> res0: 0x40000005 (♣  @)
> res1: 0x756e694c (Linu)
> res2: 0x564b2078 (x KV)
> res3: 0x7648204d (M Hv)
> ```
>
> 注意 `hyper-v id` 显示 "Linux KVM Hv"（不是 "Microsoft HV"）— 表示 passthrough 工作。

---

## 6. 推荐流程

> [FACT] **VM 设置 VRChat 的推荐流程**:

```
1. 设置基础 VM
2. 启用 vendor_id (libvirt) 或 hv-vendor-id (QEMU)
3. 测试 EAC — 应该已工作
4. 如 EAC 仍失败（2022-08-26 后）：
   a. 获取本机 dmidecode 信息
   b. 配置 SMBIOS（libvirt sysinfo 或 QEMU -smbios）
   c. 重启 VM
5. 在 VM 中安装 VRChat
6. 测试 VRChat 启动
7. 性能调优（如果需要）
```

---

## 7. 已知问题

> [FACT] **已知问题**:

| 问题 | 原因 | 解决 |
|------|------|------|
| **EAC 仍拒绝** | vendor_id 未生效 | 检查 CPUID 输出 |
| **VM 启动失败** | SMBIOS 格式错误 | 检查 libvirt 日志 |
| **性能极差** | enlightenments 未启用 | 启用 hyper-v 完整 passthrough |
| **libvirt 报 UUID 错误** | sysinfo UUID 与 domain UUID 不匹配 | 同步 UUID |
| **NVIDIA GPU 问题** | 未做 GPU passthrough | 设置 GPU passthrough |

---

## 8. 安全提示

> [FACT] **安全考虑**:
>
> - 修改 CPUID 和 SMBIOS 是**模拟硬件** — 不影响真实安全
> - **不违反 EAC ToS**（EAC 接受模拟硬件）
> - **不违反 VRChat ToS**（VM 开发是合法的）

> **注意**: VRChat 团队**不支持** VM 运行。如果你遇到问题，**VRChat Support 可能不会帮助**。

---

## 9. 与其他文档的关系

| 文档 | 关系 |
|------|------|
| `world/udon/launch-options.md` | VM 中也可使用启动选项 |
| `world/udon/using-build-test.md` | VM 中可做 Build & Test |
| `world/udon/debugging-udon-projects.md` | VM 中调试 Udon |
| `world/vvmw.md` | VRChat 视频播放器（与 VM 无关，名称相似）|

---

## 10. Missing Information（【未确认】项）

> 以下信息需要进一步验证或在官方文档中查找:

1. ❓ **VMware Workstation** 的具体配置（user-guide 未涵盖）
2. ❓ **VirtualBox** 的具体配置
3. ❓ **macOS (Virtualization.framework)** 的支持情况
4. ❓ **Windows Hyper-V** 作为 hypervisor 跑 VM 是否可行
5. ❓ **KVM** 的精确性能影响（与裸机对比）
6. ❓ **AMD SEV** 或 **Intel TDX** 对 EAC 的影响
7. ❓ **GPU passthrough** 详细设置（VFIO、Looking Glass）
8. ❓ **2024-2026** 是否还有新的 EAC 兼容性更新

---

## 来源

- [Using VRChat in a Virtual Machine](https://docs.vrchat.com/docs/using-vrchat-in-a-virtual-machine)
- [Proxmox SMBIOS 教程](https://www.reddit.com/r/Proxmox/comments/1cq87xc/comment/l3q7c5k/)
- [NVIDIA Code 43 Fix](https://passthroughpo.st/apply-error-43-workaround/)
- [QEMU Hyper-V Documentation](https://www.qemu.org/docs/master/system/i386/hyperv.html#supplementary-features)
- [SMBIOS 脚本生成器](https://gist.github.com/kiler129/5d437a37c07ac6eb1cdf0e595e488fd2)
- 本地化版本: `参考文献/SP/user-guide/using-vrchat-in-a-virtual-machine.md`
