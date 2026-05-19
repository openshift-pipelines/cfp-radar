---
title: "Death by a Thousand Reconciles — Performance Lessons from a Kubernetes Workflow Engine at Scale"
tags: [performance, kubernetes-operators, observability, tekton]
formats: [talk-35, deep-dive-45]
status: ready
target_audience: [platform-engineers, kubernetes-developers, operator-authors]
difficulty: intermediate
last_updated: 2026-05-12
---

## Abstract

When Tekton Pipelines worked fine on test clusters, the team declared victory. Then users ran 14,000 PipelineRuns with dashboard retention, and the reconciler ground to a halt. A single Prometheus metric label created 1.2 million time series. A per-task API call that was invisible at 5 tasks became a wall at 50.

This talk shares the performance lessons learned scaling a Kubernetes-native workflow engine. It covers the naive decisions that bit hard (reflect.DeepEqual for map comparison, really?), the observability gaps that hid problems for years, and the benchmarking framework built to stop guessing.

Attendees will leave with concrete patterns for building performant Kubernetes operators: bounded metric cardinality, short-circuiting completed resource reconciliation, cache strategies that don't pressure the GC, and how to add distributed tracing to catch the next bottleneck before users do.

These lessons apply to anyone building controllers and operators — not just workflow engines.

## Outline

- The "it works on my cluster" trap: what changes at 10,000+ resources (5 min)
- Reconcile churn: why completed resources keep triggering work (8 min)
- Metric cardinality explosion: 1.2M series and Prometheus scrape timeouts (7 min)
- Cache strategies: LRU, bigcache, and GC pressure trade-offs (5 min)
- Building a benchmarking practice into an open source project (5 min)
- Key takeaways & Q&A (5 min)

## Key Takeaways

1. How to identify and fix reconcile churn at scale
2. Metric design patterns that don't explode Prometheus
3. Building a benchmarking practice into an open source project

## Adaptation Notes

- **Maintainer Track**: Best fit — this is a war story from active maintainers with concrete before/after numbers
- **General audience**: Emphasize the patterns are universal to any Kubernetes operator, not Tekton-specific
- **Deep-dive variant**: Add live profiling demo showing reconcile hot paths
- **Related abstracts**: Pairs well with dogfooding talk (same project, different angle)
- Key material: PRs #9706 (reconcile churn), #9530 (metric cardinality), #9778 (maps.Equal), #9601 (O(N)→O(1) API calls), #6914 (cache rework), #9043 (OpenTelemetry migration)
- Blog: https://developers.redhat.com/articles/2026/04/30/how-statefulset-deployments-tripled-openshift-pipelines-throughput
