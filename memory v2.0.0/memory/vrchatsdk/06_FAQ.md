---
title: Frequently asked questions
category: vrchatsdk

knowledge_level: applied
status: active

tags:
  - vrchatsdk
  - performance
  - udonsharp

aliases:
  - "Frequently asked questions"

source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
---
---
source: https://vrchat.community/faq
date: 2026-06-10
---

# Frequently asked questions

Common questions and answers about the VRChat API, including authentication, rate limits, unofficial status, and best practices for developers building VRChat integrations.

## What should I do if I think I've found a bug in any of the libraries?

If the issue pertains to an endpoint that has been changed in any way, such as incorrect types or a missing endpoint, please create an issue on the specification repository.

For language-specific issues, kindly create an issue on the relevant SDK repository. However, it's worth noting that libraries are generated from the specification, and therefore most issues need to be resolved in the specification itself.

## I found an exploit or vulnerability!

If the exploit is in VRChat's scope, and not handled by us, please adhere to their responsible disclosure policy and do not discuss it in public channels or forums.

Report it on VRChat's disclosure form page. If the exploit pertains to SDKs, or libraries built by the community, you can report it in the VRChat Community Discord.

It's also recommended to include additional details such as a proof-of-concept, documentation, background, attack scenarios, and potential mitigations.

**Note:** Bans are not issued for exploit reports and research, assuming that:
- the exploit has not been used by you in a harmful manner
- all research was helpful and conducted in good faith
- you are respecting our Terms of Service

## I'm getting rate limited, what does this mean? 429 Too many requests

Rate limiting happens when you're making requests too quickly to VRChat's API. The `429 Too Many Requests` response is VRChat's way of telling you to slow down and give their servers a breather.

Rate limits can happen at any time and must not be treated as consistent or predictable. You should always be prepared to receive a 429 response, regardless of how many requests you think you've made.

**The golden rule: Do not submit repeated, un-metered requests.**

Here's how to handle this properly:

- **Always implement exponential backoff** - Start with a small delay (like 1 second), then double it with each retry (2s, 4s, 8s, etc.)
- **Cache aggressively** - Save data that rarely changes (user profiles, world details, etc.) and reuse it rather than making the same API calls over and over
- **Respect HTTP status codes** - When you get a 429, back off immediately
- **Expect the unexpected** - Design your application to gracefully handle rate limits as a normal part of operation, not an error condition

Remember, rate limits exist to keep the API stable for everyone. Working with them, not against them, will give you better performance in the long run.

## Disclaimer

VRChat's API is not officially supported or documented by VRChat. This documentation project is maintained on a best-effort basis by the community and attempts to smooth over API breakage by quickly updating when endpoints change. Use responsibly and be aware that endpoints may still break without notice.

Abuse of the API may result in account termination. For their official stance, refer to VRChat's Creator Guidelines.