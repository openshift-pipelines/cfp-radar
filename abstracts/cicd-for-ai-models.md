---
title: "CI/CD for AI: What Changes When Your Artifact Is a Model, Not a Binary"
tags: [ai, mlops, supply-chain, tekton, model-provenance, eu-ai-act]
formats: [talk-30, deep-dive-45]
status: ready
target_audience: [ml-engineers, platform-engineers, devops, security-engineers]
difficulty: intermediate
last_updated: 2026-04-13
---

## Abstract

Your CI/CD pipeline knows how to build, test, sign, and deploy a container image. But what happens when your artifact is a machine learning model? Suddenly, the rules change: your "source code" includes training data, your "build" is a GPU-intensive training run, your "tests" are statistical evaluations, and your "binary" is a set of weights that might behave unpredictably in production.

This talk explores what CI/CD must look like when AI models are first-class artifacts. We'll examine how concepts like SLSA provenance, SBOM generation, and artifact signing apply (or don't) to ML models. How do you attest the training data? How do you verify that a model was trained on approved datasets? What does "hermetic build" even mean when your build takes 8 hours on 4 GPUs?

With the EU AI Act requiring traceability for high-risk AI systems and organizations scrambling to prove their models are trustworthy, the CI/CD layer becomes the natural enforcement point. We'll show how Tekton pipelines can orchestrate the full model lifecycle — from data validation through training, evaluation, signing, and deployment — with provenance and attestation at every step.

You'll leave with practical patterns for building ML pipelines that are auditable, reproducible, and compliant — using the same supply chain security principles you already apply to your software.

## Outline

- Software CI/CD vs. ML CI/CD: what's different and what's the same (5 min)
- Model provenance: applying SLSA and in-toto to training pipelines (8 min)
- Training data attestation: the hardest unsolved problem (7 min)
- Demo: Tekton pipeline for model training with full provenance chain (5 min)
- Compliance angle: EU AI Act, audit trails, and the CI/CD enforcement point (5 min)

## Key Takeaways

1. ML models need supply chain security too — training data provenance and model attestation are the new frontier
2. Tekton's Kubernetes-native architecture makes it uniquely suited for GPU-intensive ML training workflows with full auditability
3. The EU AI Act makes model traceability a legal requirement — your CI/CD pipeline is the natural place to enforce it

## Adaptation Notes

- For **AI/ML events**: go deeper on the ML specifics — Kubeflow integration, distributed training, model registries
- For **security events**: emphasize the compliance and attestation angles, EU AI Act requirements
- For **KubeCon/cdCon**: focus on the Tekton architecture and Kubernetes scheduling for GPU workloads
- This abstract **bridges supply chain and AI** — good for events that have both tracks
- The EU AI Act angle makes this very timely for **European events** (Devoxx France, Cloud Native Days France)
- Consider co-presenting with someone from the ML/data science side for credibility across both domains
