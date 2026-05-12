---
title: "Eating Our Own Dogfood (and Sometimes Choking) — A Workflow Engine's Automation Story"
tags: [open-source, ci-cd, dogfooding, automation, tekton]
formats: [talk-25, talk-30]
status: ready
target_audience: [open-source-maintainers, devops, platform-engineers]
difficulty: beginner
last_updated: 2026-05-12
---

## Abstract

Tekton is a workflow engine. So naturally, its CI runs on... GitHub Actions. Stay with us — there's a good reason.

The Tekton project has lived through three automation eras. It started with Prow — Kubernetes' own CI system — which gave powerful merge automation but cost thousands of dollars a month in cloud infrastructure and demanded constant operational attention. When the cloud credits dried up and the operational toil became unsustainable, the project migrated to GitHub Actions: free compute, zero infrastructure to manage, and a rich ecosystem of reusable actions. It worked. But it meant a workflow engine project wasn't using its own workflow engine.

Now in era three: bringing automation back home. Custom slash commands — `/cherry-pick`, `/rebase`, `/retest` — are being migrated from GitHub Actions to a Tekton-powered cluster. Releases already run on Tekton Pipelines. Some features like Trusted Resources and Tekton Chains exist partly because the project needed them itself. And the talk is honest about what's still broken: flaky nightly tests, gaps in monitoring, and the constant tension between dogfooding purity and getting things done.

This is the story of three migrations, the trade-offs made at each step — including the ones driven by budget, not technology — and what was learned about building automation for an open source community. If you maintain a project and wrestle with "build vs. buy" for your own infrastructure, enough mistakes have been made to fill a talk.

## Outline

- Era 1: Prow — powerful but expensive (5 min)
- Era 2: GitHub Actions — free but not dogfooding (5 min)
- Era 3: Coming home — migrating to Tekton (7 min)
- What's still broken and why that's okay (3 min)
- Key takeaways & Q&A (5 min)

## Key Takeaways

1. Lessons from migrating CI infrastructure across three platforms (Prow → GitHub Actions → Tekton dogfooding)
2. Reusable automation patterns for open source: slash commands, cherry-pick bots, release pipelines
3. The real cost of dogfooding — and why it's worth it anyway

## Adaptation Notes

- **Accessible talk**: No deep technical knowledge required — this is a story about decisions and trade-offs
- **Open source conferences**: Emphasize the community and budget aspects
- **Platform engineering conferences**: Focus on the automation patterns (slash commands, release pipelines)
- **Related abstracts**: Pairs well with the performance talk (same project, different angle)
- Key material: tektoncd/plumbing repo, Prow decommission (#3182-#3183), slash command migration (#3121-#3127), GitHub Merge Queue (#3177)
