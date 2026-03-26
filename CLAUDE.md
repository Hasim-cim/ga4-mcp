# GA4 Analytics — CIM Website

Google Analytics 4 data for the CIM website (cim.io), property **274384629**.

## Setup

```bash
uv sync
```

Auth uses the service account key bundled in this project. Set the env var:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/ga4-mcp/credentials.json"
```

## Usage

```bash
uv run python ga4.py realtime --dimensions country
uv run python ga4.py top-pages
uv run python ga4.py traffic-sources
uv run python ga4.py demographics
uv run python ga4.py property
uv run python ga4.py custom --metrics sessions activeUsers --dimensions date --limit 7
```

Or use the `/ga4-analytics` skill in Claude Code — it handles everything.

## GCP Details

- **Project:** cim-analytics-mcp
- **Service Account:** id-ga4-mcp-connector@cim-analytics-mcp.iam.gserviceaccount.com
- **APIs:** Analytics Data API, Analytics Admin API
