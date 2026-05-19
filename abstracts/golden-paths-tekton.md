---
title: "Building Golden Paths with Tekton: CI/CD as a Platform Service"
tags: [platform-engineering, golden-paths, tekton, multi-tenancy, self-service]
formats: [talk-30, deep-dive-45, workshop-90]
status: ready
target_audience: [platform-engineers, devops, architects]
difficulty: intermediate
last_updated: 2026-04-13
---

## Abstract

Platform engineering is about removing cognitive load from developers. But when it comes to CI/CD, most organizations still expect teams to write and maintain their own pipelines from scratch. The result: hundreds of snowflake pipelines, duplicated logic, inconsistent security practices, and a maintenance nightmare.

This talk presents a practical architecture for turning Tekton into a CI/CD platform service — where platform teams provide curated "golden paths" and application teams consume them with minimal configuration. We'll cover the building blocks: StepActions as reusable primitives, shared Task catalogs with versioning and governance, Tekton Results for pipeline observability, and namespace-level isolation for multi-tenant environments.

We'll walk through real patterns: a self-service pipeline provisioning model where teams get pre-configured pipelines via a simple YAML interface, a shared catalog with semantic versioning and breaking change policies, and RBAC strategies that give teams autonomy without sacrificing platform standards.

You'll see how this approach scales from 10 to 500+ pipelines while keeping the platform team's operational burden constant — and how it shifts the platform team's role from "pipeline writers" to "pipeline infrastructure providers."

## Outline

### 30-min version
- The pipeline sprawl problem: why "every team writes their own" doesn't scale (5 min)
- Architecture: golden paths with Tekton — StepActions, Tasks, Pipelines as layers (8 min)
- Shared catalogs: versioning, governance, breaking change management (7 min)
- Multi-tenancy: namespace isolation, RBAC, resource quotas (5 min)
- Demo: team self-service from onboarding to first pipeline run (5 min)

### 45-min deep dive
- Add: Tekton Results for platform-wide observability (8 min)
- Add: migration strategies from legacy CI systems (7 min)

### 90-min workshop
- Hands-on: participants build a mini golden-path platform on a shared cluster
- Pre-reqs: Kubernetes basics, kubectl access

## Key Takeaways

1. CI/CD should be a platform service, not a DIY project for every team — Tekton's layered architecture (StepActions → Tasks → Pipelines) makes this possible
2. Shared catalogs with semantic versioning let platform teams evolve infrastructure without breaking consumers
3. Multi-tenancy in Tekton requires deliberate namespace isolation, RBAC design, and resource quota strategies

## Adaptation Notes

- **PlatformCon**: lean into the IDP (Internal Developer Platform) narrative, reference Backstage/Port integration patterns
- **KubeCon**: focus on the Kubernetes-native architecture, namespace isolation, RBAC
- **cdCon**: emphasize the CDF ecosystem angle — Tekton + Tekton Chains + Tekton Results as a complete platform
- **DevOpsDays**: more conversational, focus on the cultural shift from "pipeline writers" to "platform providers"
- For the **workshop format**: needs a pre-provisioned cluster; works best at events with reliable WiFi and 15+ participants
