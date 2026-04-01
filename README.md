# GA4 Analytics for CIM

A lightweight Google Analytics 4 connector that lets your team query CIM website
(cim.io) analytics directly from the command line or through Claude Code as a
skill. Built on the GA4 Data API, it provides instant access to realtime
visitors, top pages, traffic sources, demographics, and fully custom reports -
no need to open the GA4 dashboard.

When used as a Claude Code skill, you can ask natural-language questions like
"who is on the site right now?" or "what were our top pages last week?" and get
structured answers without leaving your terminal.

## How to Share with Your Team

This project is designed to be used as a local Claude Code skill. Your teammates
do not need a hosted MCP server. They clone the repo, install dependencies, add
their local credential file, and invoke `/ga4-analytics` from Claude Code.

### 1. Clone the repo

```bash
git clone https://github.com/Hasim-cim/ga4-mcp.git
cd ga4-mcp
```

### 2. Install dependencies

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

### 3. Set up credentials

The project uses a GCP service account
(`id-ga4-mcp-connector@cim-analytics-mcp.iam.gserviceaccount.com`). Ask your
team lead for the `credentials.json` file, then point
`GOOGLE_APPLICATION_CREDENTIALS` at its absolute path.

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/ga4-mcp/credentials.json"
```

macOS/Linux Terminal from the repo root:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="$(pwd)/credentials.json"
```

PowerShell:

```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS = (Resolve-Path .\credentials.json)
```

The credentials file is git-ignored and must be shared separately. Never commit
it, publish it on a website, or put it in the repo.

### 4. Teammate quick setup

For a teammate using Claude Code/Desktop:

1. Clone this repo locally.
2. Receive `credentials.json` through a private channel such as 1Password,
   Bitwarden, Google Drive with restricted access, or direct handoff.
3. Place `credentials.json` in the repo root.
4. Run `uv sync`.
5. In macOS/Linux Terminal, run:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="$(pwd)/credentials.json"
```

6. In PowerShell, run:

```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS = (Resolve-Path .\credentials.json)
```

7. Open the repo in Claude Code/Desktop.
8. Ask Claude to use `/ga4-analytics` or ask natural questions like:

- "How many visitors are on cim.io right now?"
- "Show me the top pages this month"
- "Where is our traffic coming from?"

### 5. Use as a Claude Code skill (recommended)

Once cloned, add the project as a Claude Code workspace or open it alongside
your main project. The `/ga4-analytics` skill is automatically discovered by
Claude Code from the `.claude/skills/` directory.

Then just ask Claude things like:

- "How many visitors are on cim.io right now?"
- "Show me the top pages this month"
- "Where is our traffic coming from?"

### 6. Use from the command line

```bash
uv run python ga4.py realtime
uv run python ga4.py top-pages
uv run python ga4.py traffic-sources
uv run python ga4.py demographics
uv run python ga4.py property
uv run python ga4.py custom --metrics sessions activeUsers --dimensions date --start 7daysAgo --end yesterday
```

## Example Use Cases

### "Who is visiting our site right now?"

```bash
uv run python ga4.py realtime --dimensions country
```

See a live count of active users broken down by country - useful before or
during a product launch to gauge immediate traction.

### "What are our most popular pages this quarter?"

```bash
uv run python ga4.py top-pages --start 2026-01-01 --end 2026-03-27 --limit 20
```

Identify which content drives the most engagement so marketing can double down
on what works.

### "Where is our traffic coming from?"

```bash
uv run python ga4.py traffic-sources --start 30daysAgo --end yesterday
```

Break down sessions by source and medium (Google organic, LinkedIn, direct,
etc.) to evaluate campaign performance.

### "Generate a visitor map"

```bash
uv run python map_visitors.py
```

Produces an interactive world-map choropleth (`reports/cim-visitors-map-7d.html`)
showing active users by country. The script also attempts to save
`reports/cim-visitors-map-7d.png`.

### "Custom deep-dive: daily sessions trend"

```bash
uv run python ga4.py custom --metrics sessions activeUsers bounceRate --dimensions date --start 14daysAgo --end yesterday --limit 14
```

Pull any combination of GA4 metrics and dimensions for ad-hoc analysis without
touching the GA4 UI.

### "Ask Claude in natural language"

With the skill loaded in Claude Code, just type conversationally:

- *"Compare this week's traffic to last week"*
- *"What devices do our visitors use?"*
- *"Show me bounce rate by landing page for the last 30 days"*

Claude will pick the right preset or build a custom query, run it, and
summarize the results.
