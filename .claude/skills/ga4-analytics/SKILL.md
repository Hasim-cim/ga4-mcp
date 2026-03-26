---
name: ga4-analytics
user-invocable: true
description: >
  Queries Google Analytics 4 data for CIM (cim.io): realtime visitors,
  top pages, traffic sources, demographics, and custom reports.
  Triggers for "analytics", "GA4", "website traffic", "page views",
  "who is on the site", "visitor stats", or "CIM website".
---

# GA4 Analytics — CIM Website

Query Google Analytics 4 for the CIM website (cim.io, property 274384629).

## Prerequisites

Dependencies are handled by `uv sync`. Auth uses the service account key in this project:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="credentials.json"
```

## Usage

Always run from the project root with `uv run`:

```bash
# Who is on the site right now?
uv run python ga4.py realtime

# Realtime by country
uv run python ga4.py realtime --dimensions country

# Top pages (last 7 days)
uv run python ga4.py top-pages

# Top pages for a specific period
uv run python ga4.py top-pages --start 2026-03-01 --end 2026-03-25 --limit 10

# Traffic sources
uv run python ga4.py traffic-sources

# Demographics (country + device)
uv run python ga4.py demographics

# Property metadata
uv run python ga4.py property

# Custom report — any metrics and dimensions
uv run python ga4.py custom --metrics sessions activeUsers bounceRate --dimensions date --start 7daysAgo --end yesterday --limit 7
```

## Available Presets

| Preset | Metrics | Dimensions | Description |
|--------|---------|------------|-------------|
| `realtime` | activeUsers | (optional via --dimensions) | Live visitors right now |
| `top-pages` | pageViews, activeUsers, avgSessionDuration | pagePath, pageTitle | Most visited pages |
| `traffic-sources` | sessions, activeUsers, bounceRate | source, medium | Where visitors come from |
| `demographics` | activeUsers, sessions | country, deviceCategory | Visitor geography + device |
| `property` | — | — | GA4 property metadata |
| `custom` | (--metrics) | (--dimensions) | Any metrics/dimensions combo |

## Common GA4 Metrics

`activeUsers`, `sessions`, `screenPageViews`, `bounceRate`, `averageSessionDuration`,
`newUsers`, `totalUsers`, `conversions`, `engagedSessions`, `engagementRate`,
`eventCount`, `eventsPerSession`, `userEngagementDuration`

## Common GA4 Dimensions

`date`, `country`, `city`, `deviceCategory`, `browser`, `operatingSystem`,
`pagePath`, `pageTitle`, `sessionSource`, `sessionMedium`, `sessionCampaignName`,
`unifiedScreenName`, `landingPage`, `firstUserSource`, `firstUserMedium`

## Interpreting Results

- Output is JSON with `row_count` and `rows` array
- `bounceRate` is a decimal (0.45 = 45%)
- `averageSessionDuration` is in seconds
- Realtime data covers the last 30 minutes
- Standard reports have a 24-48 hour processing delay for the most recent day
