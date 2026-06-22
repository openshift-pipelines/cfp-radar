---
event: Open Source Summit + ELC Europe 2026
deadline: 2026-06-24
source_abstract: tekton-dogfooding-story.md
status: ready-to-submit
---

# OSS EU 2026: Submission 3

## Title
Eating Our Own Dogfood (and Sometimes Choking): A Workflow Engine's Automation Story

## Session Format
Session Presentation (40 min, incl. Q&A)

## Track
OSS Enabling & Management (sub-topic: Project Leadership > Growing, Managing & Sustaining Open Source Projects; alt: Packages, Images & Containers)

## Audience Experience Level
Beginner

## Abstract (public)
Tekton is a workflow engine. So naturally, its CI runs on… GitHub Actions. Stay with us, there's a good reason.

The project has lived through three automation eras. It started with Prow, Kubernetes' own CI system: powerful merge automation, but thousands of dollars a month and constant operational toil. When the cloud credits dried up, the project migrated to GitHub Actions: free compute, no infrastructure to manage, a rich ecosystem of actions. It worked, but a workflow engine project wasn't using its own workflow engine.

Now era three: bringing automation back home. Slash commands (`/cherry-pick`, `/rebase`, `/retest`) are migrating to a Tekton-powered cluster. Releases already run on Tekton Pipelines. Some features exist partly because the project needed them itself. And we're honest about what's still broken: flaky nightly tests, monitoring gaps, and the tension between dogfooding purity and getting things done.

This is the story of three migrations, the trade-offs at each step (including the ones driven by budget, not technology) and what we learned building automation for an open source community.

## Benefits to the Ecosystem (reviewers)
An accessible, honest look at the real economics and trade-offs of running CI/CD for an open source project: budget pressures, operational toil, and the value (and cost) of dogfooding. Attendees get reusable automation patterns (slash commands, cherry-pick bots, release pipelines) and a candid build-vs-buy decision narrative they can apply to their own projects.

## Speaker Bio
<!-- FILL: short bio emphasizing Tekton maintainership + community/infra work -->

## Notes
- Key material: tektoncd/plumbing repo, Prow decommission (#3182-#3183), slash command migration (#3121-#3127), GitHub Merge Queue (#3177).
