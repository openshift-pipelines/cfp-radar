---
title: "Beyond Pipeline Runs — How a Persistence Layer Became a Supply Chain Ledger"
tags: [supply-chain, slsa, oras, oci, tekton-results, observability]
formats: [talk-35, deep-dive-45]
status: ready
target_audience: [security-engineers, platform-engineers, architects]
difficulty: advanced
last_updated: 2026-05-12
---

## Abstract

A CI/CD pipeline generates more than container images. Every build produces a trail of evidence: SLSA attestations, SBOMs, vulnerability scans, test results, and signed provenance. But can you answer the question: "Show me every artifact produced by this pipeline run — and prove they haven't been tampered with"?

Tekton Results started as a persistence layer: store archived PipelineRuns in PostgreSQL and logs in external storage so they survive Kubernetes garbage collection. It worked. But then users asked harder questions. "Where's the SBOM for this build?" "Can I see the vulnerability scan results?" "Prove this attestation came from a trusted build system, not a developer's laptop." It wasn't just pipeline storage anymore — it needed to track the entire supply chain.

This talk shows how Tekton Results evolved into a supply chain ledger that indexes all build artifacts while keeping its existing architecture intact. Results still stores pipeline resources in PostgreSQL and logs in external storage — that foundation doesn't change. What's new is the ledger capability: pipelines generate rich metadata for every artifact they produce (SBOM, attestation, scan result, test report), and that metadata gets stored in OCI registries via ORAS. Results becomes the index that ties everything together — pipeline executions, their outputs, and cryptographic proof of what happened.

The architecture leverages what registries do best: content-addressable storage, immutability, cryptographic verification, and global distribution. When a PipelineRun produces an SBOM, the pipeline generates metadata and pushes it to the registry using ORAS. Results tracks the relationship: "PipelineRun abc-123 produced SBOM xyz-456 at this registry location with this content hash." When an auditor asks "prove this image's provenance," Results provides the full graph — pipeline execution from PostgreSQL, logs from storage, and verifiable artifact metadata from the registry, all linked by cryptographic hashes.

This enables SLSA Build L3 compliance: the ledger proves what was built, when, by what pipeline, with non-falsifiable evidence. The talk demos the full lifecycle: a PipelineRun executes, generates artifact metadata, stores it via ORAS, and Results indexes it all. A developer then inspects the complete artifact graph from the UI — pipeline history, logs, SBOMs, attestations, all in one place.

## Outline

- The persistence problem: why GC kills your audit trail (5 min)
- From storage to ledger: the questions users actually ask (5 min)
- Architecture: PostgreSQL + logs + OCI registries via ORAS (8 min)
- SLSA Build L3: non-falsifiable evidence with cryptographic linking (7 min)
- Demo: full artifact graph from pipeline to UI (7 min)
- Key takeaways & Q&A (3 min)

## Key Takeaways

1. How to extend a pipeline persistence system into a supply chain ledger by indexing artifact metadata stored in OCI registries via ORAS
2. Achieving SLSA Build L3 compliance through verifiable artifact tracking — pipelines generate metadata, registries provide immutable storage, Results provides the index
3. Architectural patterns for supply chain traceability: keeping existing storage while adding an artifact metadata layer in OCI registries

## Adaptation Notes

- **Security/compliance conferences**: Lead with the audit/compliance angle and SLSA requirements
- **Architecture conferences**: Emphasize the ledger pattern and separation of concerns (index vs. storage)
- **Demo**: Requires Results instance with ORAS-enabled OCI registry and UI
- **Related abstracts**: Builds on the SLSA hard-parts talk; complements the pipeline security walkthrough
- Key material: tekton-experiments prototype, ORAS integration PoC, Tekton Chains for attestation generation
