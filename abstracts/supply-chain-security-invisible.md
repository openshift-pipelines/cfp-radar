---
title: "Signing Everything: Making Supply Chain Security Invisible to Developers"
tags: [supply-chain, security, tekton-chains, developer-experience, sigstore]
formats: [talk-30, lightning-15]
status: ready
target_audience: [developers, platform-engineers, devops]
difficulty: beginner
last_updated: 2026-04-13
---

## Abstract

The best security is security developers never think about. Yet most supply chain security implementations add friction: new CLI tools to learn, signing steps to remember, attestation metadata to manage. No wonder adoption stalls.

This talk shows how Tekton Chains takes a radically different approach: supply chain security that happens automatically, transparently, and without any developer intervention. Every pipeline run is automatically signed, every artifact gets provenance metadata, and every image is attested — all without changing a single line in your pipeline definitions.

We'll demonstrate the complete developer experience: from pushing code to having a fully signed, attested, SLSA-compliant artifact in your registry, with zero additional steps. Then we'll look under the hood at how Tekton Chains observes TaskRun completions, generates in-toto attestations, signs with Sigstore, and stores provenance in OCI registries — all as a Kubernetes controller that runs alongside your existing Tekton installation.

You'll leave with a clear understanding of how to add supply chain security to your existing CI/CD pipelines without asking developers to change anything about how they work.

## Outline

### 30-min version
- The developer experience problem with supply chain security (5 min)
- Demo: push code → signed artifact, zero extra steps (5 min)
- How Tekton Chains works under the hood (10 min)
- Setting it up: from install to first signed artifact in 10 minutes (5 min)
- Integration points: Sigstore, OCI registries, policy engines (5 min)

### 15-min lightning version
- The problem: security vs. developer velocity (3 min)
- Live demo: automatic signing with Tekton Chains (5 min)
- How it works in 3 slides (4 min)
- Getting started (3 min)

## Key Takeaways

1. Supply chain security doesn't have to mean more work for developers — Tekton Chains proves it can be completely transparent
2. Automatic signing and attestation at the CI/CD layer is more reliable than asking developers to sign manually
3. You can go from zero to SLSA Level 2 compliance in under 30 minutes with Tekton Chains

## Adaptation Notes

- This is the **introductory companion** to `slsa-hard-parts` — good for events where the audience is newer to supply chain security
- Works especially well at **developer-focused events** (Devoxx, DevOpsDays) where the audience cares more about DX than security depth
- The live demo is very visual and impactful — show the signing happening in real-time via `cosign verify`
- For **French events** (Devoxx France, Cloud Native Days France): consider presenting in French, the DX angle resonates strongly
