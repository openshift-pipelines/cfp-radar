---
title: "From SLSA Level 2 to Level 3: The Hard Parts Nobody Talks About"
tags: [supply-chain, security, slsa, tekton-chains, sigstore]
formats: [talk-30, deep-dive-45]
status: ready
target_audience: [security-engineers, platform-engineers, devops]
difficulty: intermediate
last_updated: 2026-04-13
---

## Abstract

Every CNCF project blog post makes SLSA compliance sound straightforward: add Tekton Chains, configure signing, done. But the journey from Level 2 to Level 3 is where the real engineering challenges live — and nobody is talking about them.

This talk takes you through the battle-tested lessons from building and operating SLSA-compliant CI/CD pipelines with Tekton Chains in production. We'll cover the unglamorous but critical topics: key management strategies that don't become a single point of failure, policy-as-code for attestation verification at scale, handling the transitive dependency problem when your SBOM has SBOMs, and the operational cost of hermetic builds on Kubernetes.

We'll walk through real-world patterns for integrating Tekton Chains with Sigstore for keyless signing, configuring OCI registries as attestation stores, and building verification gates that don't slow down developer velocity. You'll see what breaks when you move from "demo-ready" to "production-ready" supply chain security — and how to fix it.

Whether you're starting your SLSA journey or stuck at Level 2, this talk gives you the practical playbook to close the gap, with honest assessments of the trade-offs involved.

## Outline

- The SLSA promise vs. reality: what Level 2 gives you and what it doesn't (5 min)
- Key management: Sigstore keyless vs. KMS-backed keys, rotation, and emergency procedures (8 min)
- Attestation at scale: OCI storage, verification policies, handling transitive deps (8 min)
- Hermetic builds on Kubernetes: network policies, caching strategies, build performance (5 min)
- Demo: end-to-end signed pipeline with verification gate (5 min)
- Takeaways and roadmap (4 min)

## Key Takeaways

1. SLSA Level 3 requires solving key management, hermetic builds, and attestation verification — each is a project in itself
2. Sigstore keyless signing with Tekton Chains eliminates key management pain but introduces identity provider dependencies
3. Supply chain security must be invisible to developers — if it slows them down, they'll work around it

## Adaptation Notes

- For **security-focused events** (SupplyChainSecurityCon, OpenSSF Day): lean into the threat model, compliance angles (EU CRA, DORA), and policy-as-code depth
- For **developer events** (DevOpsDays, Devoxx): emphasize the developer experience angle — how to make security invisible
- For a **15-min lightning talk**: cut to "3 things that break when you try SLSA Level 3" format
- Demo options: pre-recorded is safer for conference WiFi; live works well at meetups
- Pairs well with: `supply-chain-security-invisible` abstract for a 2-talk series
