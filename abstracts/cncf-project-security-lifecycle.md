---
title: "When the LLMs Come Knocking — AI-Powered Vulnerability Research Meets Open Source Maintainers"
tags: [security, cve, vulnerability-management, open-source, supply-chain, ai, llm]
formats: [talk-35, deep-dive-45]
status: ready
target_audience: [open-source-maintainers, security-engineers, platform-engineers]
difficulty: intermediate
last_updated: 2026-06-04
---

## Abstract

In early 2026, our vulnerability inbox went from a trickle to a flood. Tekton — the Kubernetes-native CI/CD framework we maintain — received more security reports in four months than in the previous four years combined. The reports were detailed, well-structured, came with working reproducers and CVSS scores, and many of them were genuinely valid. They were also, overwhelmingly, AI-generated.

LLM-powered security research has changed the game for open source maintainers. Researchers are using AI to audit codebases systematically, finding real vulnerabilities that humans missed for years — a path traversal reading arbitrary files from the controller pod, an SSRF exfiltrating cloud credentials via IMDS, a JSON injection enabling RCE through Kubernetes webhook endpoints. These aren't hallucinated bugs. They're real, and they're arriving faster than a small maintainer team can patch, coordinate disclosure, and ship fixes across multiple release branches.

But the flood also carries noise. Pattern-matched variants of already-fixed CVEs. Reports that technically describe a bug but misunderstand the threat model. Duplicate findings from multiple researchers scanning the same codebase with similar tools. The maintainer challenge has shifted: it's no longer "find vulnerabilities" — it's "triage an AI-accelerated firehose while keeping your coordinated disclosure process from collapsing."

This talk walks through how we're trying to adapt: what our triage workflow looks like under pressure, how we attempt to distinguish signal from noise in AI-generated reports, what we got right (govulncheck over Dependabot, GitHub Private Vulnerability Reporting), and what we got wrong. This isn't a talk about whether AI security research is good or bad — it's clearly both. It's an honest, in-progress survival guide from maintainers living through this transition right now.

## Outline

- The inbox before and after: what changed in 2026 (5 min)
- Real AI-found vulnerabilities: path traversal, SSRF, RCE — the ones that were right (8 min)
- The noise: pattern-matched variants, threat model mismatches, duplicates (7 min)
- Triage under pressure: coordinated disclosure when reports arrive faster than patches (7 min)
- What we got right, what we got wrong, and what we'd tell other maintainers (5 min)
- Q&A (3 min)

## Key Takeaways

1. AI-powered security research is finding real vulnerabilities in open source projects at unprecedented scale — this is not theoretical
2. The maintainer bottleneck has shifted from "finding bugs" to "triaging an AI-accelerated firehose" while maintaining coordinated disclosure quality
3. Practical triage patterns for distinguishing signal from noise in AI-generated security reports

## Adaptation Notes

- **Digital Trust / Security conferences**: Emphasize the vulnerability details and coordinated disclosure workflow
- **AI conferences**: Focus on the LLM-as-security-researcher angle and quality assessment
- **Maintainer/community conferences**: Emphasize the human cost and process adaptation
- **European events**: The Digital Trust track at OSS EU is a natural fit
- **Sensitive content**: All advisories referenced are already public (GHSA links available) or will be by event date
- Key material: GHSA-j5q5 (path traversal, CVSS 9.6), GHSA-cv4x (DoS), GHSA-wjxp (token leak), GHSA-94jr (RCE), GHSA-vxcg (SSRF), Triggers JSON injection reports, Issue #9712 (compromised CI action)
- This talk supersedes the earlier "12 CVEs and Counting" version — same core material, reframed around the AI-accelerated reporting phenomenon
