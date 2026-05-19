---
title: "12 CVEs and Counting — What Maintaining a CNCF Project Taught Us About Security"
tags: [security, cve, vulnerability-management, open-source, supply-chain]
formats: [talk-35, deep-dive-45]
status: ready
target_audience: [open-source-maintainers, security-engineers, platform-engineers]
difficulty: intermediate
last_updated: 2026-05-12
---

## Abstract

In March 2026, a security researcher reported a critical path traversal in Tekton's git resolver — an attacker with basic Kubernetes access could read arbitrary files from the controller pod. Two weeks later, the team was coordinating patches across five LTS branches, managing embargo timelines, and realizing that the vulnerability management process needed as much engineering as the code.

This talk is an honest look at how maintainers handle the full lifecycle of security vulnerabilities in a CNCF project. It walks through real advisories — from a DoS via a truncation bug no one noticed for four years, to SSRF attacks that exfiltrated cloud credentials via IMDS, to a compromised GitHub Action in the project's own CI pipeline. The triage workflow is laid bare: GitHub Private Vulnerability Reporting, coordinated disclosure with embargoes, and cherry-picking fixes to multiple release branches under time pressure.

The talk also tackles the dependency CVE firehose: why Dependabot's "update everything" approach creates noise that hides real threats, how govulncheck's reachability analysis focuses effort on what actually matters, and why verifying checksums on release artifacts is now non-negotiable. Whether you're an open source maintainer drowning in security reports or a consumer trying to assess real risk, you'll leave with a practical playbook.

## Outline

- A critical CVE lands: the first 48 hours (5 min)
- The coordinated disclosure workflow: triage → embargo → patch → release → advisory (8 min)
- Real advisories: path traversal, SSRF, RCE, DoS — patterns and root causes (8 min)
- Dependency CVE noise: govulncheck vs Dependabot and reachability analysis (7 min)
- Hardening your own CI/CD against supply chain attacks (5 min)
- Key takeaways & Q&A (2 min)

## Key Takeaways

1. A coordinated vulnerability disclosure workflow for open source maintainers (triage → embargo → patch → release → advisory)
2. govulncheck vs Dependabot: cutting through dependency CVE noise with reachability analysis
3. Hardening your project's own CI/CD against supply chain attacks

## Adaptation Notes

- **Maintainer Track**: Ideal — speaks directly to other CNCF/OSS maintainers
- **Security conferences**: Emphasize the SSRF/path traversal war stories and attack patterns
- **General audience**: Focus on "how to assess CVE risk as a consumer" angle
- **Sensitive content**: All advisories referenced are already public (GHSA links available)
- Key material: GHSA-j5q5 (path traversal, CVSS 9.6), GHSA-cv4x (DoS), GHSA-wjxp (token leak), GHSA-94jr (RCE), GHSA-vxcg (SSRF), Issue #9712 (compromised CI action)
