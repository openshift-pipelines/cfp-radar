---
event: Open Source Summit + ELC Europe 2026
deadline: 2026-06-24
source_abstract: trusted-artifacts-pvc-must-die.md
status: ready-to-submit
---

# OSS EU 2026: Submission 2

## Title
The PVC Must Die: How a Workflow Engine Rethought Data Sharing with Trusted Artifacts

## Session Format
Session Presentation (40 min, incl. Q&A)

## Track
Packages, Images & Containers (sub-topic: Build, Test, Release Pipelines / Supply Chain Security; alt: Cloud & Orchestration)

## Audience Experience Level
Intermediate

## Abstract (public)
When a CI/CD pipeline runs each step as a separate Kubernetes Pod, those Pods need a way to pass data to one another. Tekton chose the obvious Kubernetes-native answer: a shared persistent volume. Clone code in step one, build it in step two, both read from the same disk. Simple.

It wasn't. Shared volumes meant pinning Pods to the same node, which broke autoscaling. Users hit storage limits, leaked volumes after failures, and spent more time debugging infrastructure than building pipelines. Each fix created new edge cases.

Then a different question: what if steps didn't share a disk at all? What if each step uploaded what it produced, and the next downloaded and verified it, with cryptographic hashes at every handoff? That's Trusted Artifacts. The shared volume disappears, and in its place you get a verifiable chain of trust: every handoff is hashed, signed, and traceable. A storage problem became a security feature.

This talk traces that journey: the design that seemed right, the years of workarounds, and the moment the team stopped fixing the plumbing and rethought the architecture. It's for anyone who's wondered whether to keep patching a leaky abstraction or tear it out.

## Benefits to the Ecosystem (reviewers)
A concrete, transferable case study in platform architecture decision-making: when to keep patching an abstraction vs. when to replace it. Attendees leave with a design framework and a real example of how rethinking data sharing simultaneously improved reliability and supply-chain security, relevant to anyone building Kubernetes-native platforms.

## Speaker Bio
<!-- FILL: short bio emphasizing Tekton maintainership + platform architecture -->

## Notes
- Key material: TEP-0139 (Trusted Artifacts), TEP-0147 (Artifacts Phase 1), issues #4699, #8015, #6985, #3440.
