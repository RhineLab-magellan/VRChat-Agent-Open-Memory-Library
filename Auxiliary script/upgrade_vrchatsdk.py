#!/usr/bin/env python3
"""
升级 vrchatsdk/01_首页.md 的 frontmatter
"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

fp = Path(r'C:\CherryStudio\Agent\UdonSharpAgent\memory\vrchatsdk\01_首页.md')
content = fp.read_text(encoding='utf-8')

# 找到 body 起始(line 6 = "# VRChat.community")
lines = content.split('\n')
body_start = None
for i, line in enumerate(lines):
    if line.startswith('# VRChat'):
        body_start = i
        break

if body_start is None:
    print('ERROR: body not found')
    sys.exit(1)

body = '\n'.join(lines[body_start:])

new_frontmatter = """---
title: VRChatSDK 首页
category: vrchatsdk

knowledge_level: core
status: active

tags:
  - vrchatsdk
  - api
  - http
  - websocket
  - sdk

aliases:
  - VRChatSDK
  - VRChat SDK
  - HTTP API
  - SDK 首页

related:
  - vrchatsdk/02_TypeScript_SDK.md
  - vrchatsdk/03_Websocket_API.md
  - vrchatsdk/04_Instances.md
  - hybrid/osc-protocol.md

source: VRChat 官方文档
source_type: official
version: 1.0
last_review: 2026-06-20
confidence: High
---
"""

new_content = new_frontmatter + body
fp.write_text(new_content, encoding='utf-8')

print(f'Upgraded: {fp}')
print(f'New size: {len(new_content)} bytes')
print(f'New lines: {len(new_content.split(chr(10)))}')
