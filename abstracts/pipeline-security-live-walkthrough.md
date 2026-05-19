---
title: "Your Pipeline Has the Keys — A Live Security Walkthrough"
tags: [security, supply-chain, tekton-chains, trusted-resources, slsa, demo]
formats: [talk-25, talk-30]
status: ready
target_audience: [developers, devops, security-engineers]
difficulty: beginner
last_updated: 2026-05-12
---

## Abstract

A CI/CD pipeline has the keys to production. But what happens when someone swaps a trusted Task for a backdoored one — and there's no way to prove what actually ran?

In this demo-driven talk, two real attack scenarios are shown against a Tekton pipeline. First, a Task in the cluster is replaced with a tampered version that injects a backdoor into the build. The pipeline succeeds, the image ships, nobody notices. Second, even if the tampering were caught, without provenance attestations there's no evidence trail — no record of what ran, what source was used, or who triggered the build.

Then both attacks are fixed, live. Tekton's Trusted Resources and VerificationPolicies ensure only cryptographically signed Tasks execute in the cluster. Tekton Chains automatically generates SLSA provenance attestations for every build — capturing the full chain of inputs, steps, and outputs. Everything is verified with cosign, showing what a secured supply chain actually looks like.

Attendees will leave knowing exactly how to go from "anyone can tamper with my pipeline" to a verifiable, attestation-backed supply chain.

## Outline

- Your pipeline is a trust boundary — and you're not guarding it (3 min)
- Attack 1: Task tampering — injecting a backdoor undetected (7 min, live demo)
- Attack 2: No provenance — you can't prove what ran (5 min, live demo)
- Fix: Trusted Resources + VerificationPolicies (5 min, live demo)
- Fix: Tekton Chains + SLSA provenance + cosign verification (5 min, live demo)
- Key takeaways & Q&A (5 min)

## Key Takeaways

1. How pipeline task tampering works and why it's hard to detect without provenance
2. Hands-on with Tekton Trusted Resources and VerificationPolicies
3. Automated SLSA provenance with Tekton Chains — from zero to verifiable builds

## Adaptation Notes

- **Demo-heavy**: 80% live demo, minimal slides — best for conferences that value practical demonstrations
- **Solo presenter**: Designed for a single speaker running live demos
- **Prerequisite**: Audience should know basic Kubernetes and CI/CD concepts
- **Fallback**: Prepare recorded demo backups in case of live demo issues
- **Related abstracts**: Complements the SLSA hard-parts talk (this is user-facing, that is implementation-facing) and the CVE lifecycle talk (this is about prevention, that is about response)
