---
title: "The PVC Must Die — How a Workflow Engine Rethought Data Sharing with Trusted Artifacts"
tags: [architecture, kubernetes, storage, supply-chain, tekton]
formats: [talk-25, talk-30]
status: ready
target_audience: [platform-engineers, kubernetes-developers, architects]
difficulty: intermediate
last_updated: 2026-05-12
---

## Abstract

When a CI/CD pipeline runs each step as a separate Kubernetes Pod, those Pods need a way to pass data to each other. Tekton chose the obvious Kubernetes-native answer: a shared persistent volume. Clone code in step one, build it in step two, both read from the same disk. Simple.

It wasn't simple. Shared volumes meant pinning Pods to the same node — which broke autoscaling. Users hit storage limitations, leaked volumes after failures, and spent more time debugging infrastructure than building pipelines. Fix after fix shipped, each one creating new edge cases. The abstraction was leaking faster than anyone could patch it.

Then a different question was asked: what if steps didn't share a disk at all? What if each step uploaded what it produced and the next step downloaded and verified it — with cryptographic hashes at every handoff? That's Trusted Artifacts. The shared volume disappears, and in its place you get something better: a verifiable chain of trust where every piece of data passed between steps is hashed, signed, and traceable. What started as a storage problem became a security feature.

This talk traces that journey — the original design that seemed right, the years of workarounds, and the moment the team stopped fixing the plumbing and rethought the architecture. It's a story for anyone who's ever wondered whether to keep patching a leaky abstraction or tear it out entirely.

## Outline

- The obvious answer: shared PVCs for step-to-step data (5 min)
- Death by a thousand edge cases: node affinity, leaked volumes, autoscaler conflicts (7 min)
- The rethink: what if steps don't share storage at all? (5 min)
- Trusted Artifacts: cryptographic verification at every handoff (5 min)
- Key takeaways & Q&A (3 min)

## Key Takeaways

1. Why "the obvious Kubernetes-native answer" isn't always the right one
2. How replacing shared storage with verifiable artifact passing improved both reliability and security
3. Design lessons for platform builders: when to stop patching and start rethinking

## Adaptation Notes

- **Architecture conferences**: Emphasize the design decision framework (patch vs. rethink)
- **Security conferences**: Focus on the supply chain trust angle — every handoff is verified
- **Kubernetes conferences**: Deep-dive into PVC/node affinity/autoscaler technical details
- **Related abstracts**: Natural companion to the pipeline security walkthrough (Trusted Artifacts are part of the defense)
- Key material: TEP-0139 (Trusted Artifacts), TEP-0147 (Artifacts Phase 1), issues #4699, #8015, #6985, #3440
