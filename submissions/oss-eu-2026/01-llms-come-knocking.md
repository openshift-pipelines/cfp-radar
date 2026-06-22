---
event: Open Source Summit + ELC Europe 2026
deadline: 2026-06-24
source_abstract: cncf-project-security-lifecycle.md
status: ready-to-submit
---

# OSS EU 2026: Submission 1

## Title
When the LLMs Come Knocking: Surviving AI-Powered Vulnerability Reports

## Session Format
Session Presentation (40 min, incl. Q&A)

## Track
Security (sub-topic: Security and Vulnerability Management; alt: Digital Trust)

## Audience Experience Level
Intermediate

## Abstract (public)
In early 2026 our vulnerability inbox suddenly exploded. Tekton, the Kubernetes-native CI/CD framework we maintain, received more security reports in four months than in all the previous years combined: detailed, with working reproducers and CVSS scores. Many were genuinely valid. They were also, overwhelmingly, AI-generated.

LLM-powered research has changed the game. Tools now audit codebases systematically and surface real bugs humans missed for years: a path traversal reading arbitrary files from the controller pod, an SSRF exfiltrating cloud credentials, a JSON injection enabling RCE. These aren't hallucinations, and they arrive faster than a small team can patch, disclose, and backport.

But the flood carries noise too: variants of fixed CVEs, reports that misunderstand the threat model, duplicates. The challenge has shifted from "find vulnerabilities" to "triage an AI-accelerated firehose without your disclosure process collapsing."

This is an honest, in-progress survival guide from maintainers living through it: how triage holds up under pressure, how we separate signal from noise, what we got right, and what we got wrong.

## Benefits to the Ecosystem (reviewers)
Every CNCF and open source project is about to face (or is already facing) this exact wave of AI-generated security reports. This talk gives maintainers and security teams concrete, battle-tested triage patterns and disclosure-process adaptations they can apply immediately, plus a realistic picture of what's coming. All advisories referenced are public (GHSA links) or will be by the event date.

## Speaker Bio
<!-- FILL: short bio emphasizing Tekton maintainership + security work -->

## Notes
- Key material: GHSA-j5q5 (path traversal, CVSS 9.6), GHSA-cv4x (DoS), GHSA-wjxp (token leak), GHSA-94jr (RCE), GHSA-vxcg (SSRF), Triggers JSON injection, Issue #9712 (compromised CI action).
