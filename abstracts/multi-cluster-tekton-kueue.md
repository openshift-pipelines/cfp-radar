---
title: "From One Cluster to Many — How Tekton and Kueue Learned to Share Pipelines Across Boundaries"
tags: [multi-cluster, kueue, scheduling, scalability, tekton]
formats: [talk-35, deep-dive-45]
status: ready
target_audience: [platform-engineers, architects, sre]
difficulty: advanced
last_updated: 2026-05-12
---

## Abstract

A CI/CD platform runs on one cluster. It works — until it doesn't. One team's 200-container ML pipeline starves everyone else. A regional outage takes the entire build infrastructure offline. Compliance demands workloads stay in specific geographies. Multi-cluster is needed, but "just deploy Tekton everywhere" isn't a strategy.

PipelineRuns are Kubernetes-native — designed to live and die on a single cluster. Making them span clusters meant rethinking how pipelines are scheduled, how results are collected, and how the user experience stays coherent when TaskRuns execute on clusters nobody has directly touched.

The answer was an unlikely pairing: Tekton for pipeline execution, and Kueue — Kubernetes' batch job scheduler — for cross-cluster workload placement. A Hub-Spoke architecture where pipelines are submitted to a central Hub cluster and Kueue's MultiKueue decides which Spoke cluster runs the work — based on available capacity, resource quotas, and placement policies. A syncer service keeps pipeline state consistent across clusters, and Tekton Results aggregates logs and outcomes back to the Hub so users never chase results across clusters.

This talk demos the full journey: submit a pipeline on the Hub, watch Kueue route it to a Spoke with capacity, see it execute remotely, and view results from a single dashboard. It shares architecture decisions — why Kueue over a custom scheduler, how Hub and Spoke clusters are configured differently, and what broke along the way: secrets that didn't sync, pipelines that ran as the wrong identity, storage assumptions that fell apart across cluster boundaries.

Whether you're a platform engineer hitting single-cluster scaling limits, a team needing workload isolation across geographies, or just curious about multi-cluster pipelines in practice — this talk gives you the architecture and the lessons learned.

## Outline

- The single-cluster ceiling: when one cluster isn't enough (5 min)
- Architecture: Hub-Spoke with Tekton + Kueue MultiKueue (8 min)
- Making it work: syncer service, Results aggregation, credential management (8 min)
- War stories: secrets, identity, storage across boundaries (7 min)
- Demo: end-to-end multi-cluster pipeline execution (5 min)
- Key takeaways & Q&A (2 min)

## Key Takeaways

1. How to architect multi-cluster CI/CD with Tekton + Kueue's MultiKueue — Hub-Spoke topology and cross-cluster result aggregation
2. Real-world lessons from distributed pipeline execution: secret syncing, identity management, storage constraints, and observability across cluster boundaries
3. How Tekton became a native Kueue workload type — and what that means for CI/CD resource management

## Adaptation Notes

- **KubeCon**: Best fit for platform engineering or batch/HPC tracks
- **Multi-cluster demo**: Requires Hub + 2 Spoke clusters, ideally different regions
- **Kueue co-submission**: Consider joint submission with Kueue maintainers for credibility
- **Prerequisite**: Audience should understand Kubernetes scheduling basics and multi-cluster concepts
- Key material: tektoncd/operator (MultiCluster Scheduler, syncer-service), kubernetes-sigs/kueue (MultiKueue, composable dispatcher)
