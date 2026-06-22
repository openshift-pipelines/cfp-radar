# CFP Radar

AI-powered webpage generator to discover and track tech events (CI/CD, DevOps, Platform Engineering, Cloud Native) with CFP opportunities.

<img width="3826" height="2000" alt="image" src="https://github.com/user-attachments/assets/fee98e12-853e-4385-825f-e020f2294c9d" />

See it live on: https://openshift-pipelines.github.io/cfp-radar/

## Setup

Install uv on your Fedora or macOS via brew or via curl:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```bash
# Install dependencies
uv sync

# Set required environment variables for Claude on Vertex AI
export GOOGLE_CLOUD_PROJECT="your-project"
# Or: export ANTHROPIC_VERTEX_PROJECT_ID="your-project"
export GOOGLE_CLOUD_LOCATION="global"
export AI_MODEL="claude-sonnet-4-6"
gcloud auth application-default login
```

You need the `roles/aiplatform.user` role on the GCP project. Claude web search also requires the `constraints/vertexai.allowedPartnerModelFeatures` org policy to allow web search. Collection works without GCP credentials when using `--no-ai`.

See [Claude on Vertex AI](https://docs.anthropic.com/en/api/claude-on-vertex-ai) and [Vertex AI pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing) for details.

Set `export SLACK_WEBHOOK_URL="your-webhook-url"` if you plan to use Slack notifications.

## Configuration

Cities to track are configured in `config.yaml` in the project root:

```yaml
cities:
  - city: Paris
    country: France
  - city: Bangalore
    country: India
  - city: Pune
    country: India
  - city: Tel Aviv
    country: Israel
  - city: Raleigh
    country: USA
  - city: Brno
    country: Czech Republic
```

You can override the default config file using the `--config` argument:

```bash
uv run cfp-radar collect --config my-cities.yaml
uv run cfp-radar list --config my-cities.yaml
```

If `config.yaml` is not found, the tool falls back to built-in defaults.

## Usage

```bash
# Collect events and generate HTML (default: data/index.html)
uv run cfp-radar collect

# Collect events to custom output file
uv run cfp-radar collect ./output/events.html

# Collect without AI-powered search (faster)
uv run cfp-radar collect --no-ai

# List collected events
uv run cfp-radar list

# List events filtered by city
uv run cfp-radar list --city Paris

# List only events with open CFP
uv run cfp-radar list --cfp

# Send Slack notifications for upcoming CFP deadlines
uv run cfp-radar notify
```

## Output

The `collect` command generates a static HTML file at `data/index.html` by default. Open this file in a browser to view events.

## Abstract Bank

The `abstracts/` directory contains a shared bank of speaker-neutral, reusable talk proposals. Anyone on the team can pick one up, adapt it to a specific event, and submit.

Each abstract includes:

- YAML frontmatter (tags, formats, difficulty, target audience)
- A 200-300 word abstract text
- Talk outline with timing for multiple formats (lightning, talk, deep-dive, workshop)
- Key takeaways
- Adaptation notes — hints on how to tailor per event type

### Adding a new abstract

Copy `abstracts/_template.md`, fill it in, open a PR.

### Current abstracts

| Title | Tags | Formats | Status |
|-------|------|---------|--------|
| From SLSA Level 2 to Level 3: The Hard Parts | supply-chain, slsa, tekton-chains | talk, deep-dive | ready |
| Signing Everything: Making Supply Chain Security Invisible | supply-chain, DX, sigstore | talk, lightning | ready |
| Building Golden Paths with Tekton: CI/CD as a Platform Service | platform-engineering, multi-tenancy | talk, deep-dive, workshop | ready |
| CI/CD for AI: When Your Artifact Is a Model, Not a Binary | ai, mlops, eu-ai-act | talk, deep-dive | ready |
| AI-Assisted CI/CD: Using LLMs to Debug and Generate Pipelines | ai, llm, developer-experience | talk, lightning | draft |
| Death by a Thousand Reconciles — Performance at Scale | performance, kubernetes-operators, observability | talk, deep-dive | ready |
| 12 CVEs and Counting — CNCF Project Security Lifecycle | security, cve, vulnerability-management | talk, deep-dive | ready |
| Your Pipeline Has the Keys — A Live Security Walkthrough | security, supply-chain, slsa, demo | talk | ready |
| Eating Our Own Dogfood — A Workflow Engine's Automation Story | open-source, ci-cd, dogfooding | talk | ready |
| The PVC Must Die — Rethinking Data Sharing with Trusted Artifacts | architecture, kubernetes, storage, supply-chain | talk | ready |
| From One Cluster to Many — Tekton + Kueue Multi-Cluster Pipelines | multi-cluster, kueue, scheduling | talk, deep-dive | ready |
| Beyond Pipeline Runs — A Supply Chain Ledger with ORAS | supply-chain, slsa, oras, oci | talk, deep-dive | ready |

## Copyright

[Apache-2.0](./LICENSE)

## Authors

### Chmouel Boudjnah

- Fediverse - <[@chmouel@chmouel.com](https://fosstodon.org/@chmouel)>
- Twitter - <[@chmouel](https://twitter.com/chmouel)>
- Blog  - <[https://blog.chmouel.com](https://blog.chmouel.com)>
