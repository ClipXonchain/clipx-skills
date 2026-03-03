---
name: clipx-bnbchain-api-client
description: Thin client for the private ClipX BNBChain API, returning text-only JSON metrics and rankings for BNB Chain (no scraping code, no API keys).
metadata: { "openclaw": { "emoji": "🟡", "requires": { "bins": ["python"] }, "os": ["win32", "linux", "darwin"] } }
---

You are a skill that calls the **ClipX BNBChain API** to fetch **text-only JSON**
about **BNB Smart Chain (BSC)**. You do **not** perform any scraping or heavy
logic yourself; you only execute a small Python client script in the workspace:

- `python "{baseDir}/api_client_cli.py" ...`

The ClipX backend (running on a private server) performs:

- RPC-based BSC metrics lookups.
- DefiLlama / DappBay / Binance-based rankings and analytics.

Your job is to:

1. Decide **when** these live metrics / rankings are needed.
2. Call `api_client_cli.py` with the correct arguments.
3. Parse the JSON response.
4. **By default**, present the result in **box-style table format** (see below). Never show raw JSON to the user unless they explicitly ask for it.

You **must never** attempt to re-scrape websites directly; always go through
the ClipX API via this client.

**Default output rule:** For any ClipX analysis response (`tvl_rank`, `fees_rank`, `revenue_rank`, `dapps_rank`, `fulleco`, `social_hype`, `meme_rank`), you **must** render the `items` array as a pipe-separated table inside a box (double-line top/bottom, single-line under header). Do not reply with raw JSON; use the box-style table as the default presentation.

*(Optional, for local testing only: the skill includes `format_box.py`, which reads JSON from stdin and prints a box-style table. You do not need to run it; you render the table in your reply. See README for the pipe command.)*

---

## Environment configuration (API base URL)

The client talks to a base URL, such as `http://5.189.145.246:8000`. It uses:

1. `CLIPX_API_BASE` environment variable if present.
2. Otherwise, the hard-coded fallback in `get_api_base()` inside
   `{baseDir}/api_client_cli.py`.

When you see `CLIPX_API_BASE`, treat it as the **root URL** for all API calls.
You do **not** need to edit it or construct URLs manually; always let
`api_client_cli.py` handle that.

---

## Core BNBChain metrics (via API)

These endpoints give you **live on-chain data** (via the backend’s RPC calls).
Use them when the user asks about:

- Latest block height, chain status.
- Gas price on BSC.
- Average block time or gas usage over recent blocks.
- Balance and tx count for a specific address.

### 1. Basic network metrics

When the user wants high-level status (latest block, gas price, syncing):

- Run:

  - `python "{baseDir}/api_client_cli.py" --mode metrics_basic`

Expected JSON shape:

```json
{
  "ok": true,
  "metric_type": "basic",
  "data": {
    "latest_block": 84478929,
    "chain_id": 56,
    "network_id": 56,
    "gas_price_gwei": 0.05,
    "syncing": false
  },
  "source": "@ClipX0_"
}
```

You must:

1. Check `ok` is `true`.
2. Use `data.latest_block`, `data.gas_price_gwei`, `data.syncing`, etc. to
   describe network health in natural language.
3. If `ok` is `false`, read `error` and explain the failure briefly.

### 2. Block statistics (recent blocks)

When the user wants average block time or gas usage:

- Example for last 100 blocks:

  - `python "{baseDir}/api_client_cli.py" --mode metrics_block --blocks 100`

Rules:

- `--blocks` must be an integer > 1.
- Values between **50 and 500** provide a good tradeoff between accuracy
  and performance, unless the user explicitly requests another range.

The response includes:

- `data.from_block`, `data.to_block`, `data.blocks_considered`
- `data.avg_block_time_seconds`
- `data.avg_gas_used`

You should:

- Explain what these averages mean (e.g. “blocks are currently ~0.4s apart”,
  or “average gas used per block is X, indicating Y”).

### 3. Address metrics

When the user wants the **BNB balance** or **transaction count** for a
specific address:

- Example:

  - `python "{baseDir}/api_client_cli.py" --mode metrics_address --address 0x0000000000000000000000000000000000000000`

You must:

1. Require a valid hex address string in the `--address` parameter.
2. Use the returned `data.balance_bnb` and `data.tx_count`.
3. Clarify that `balance_bnb` is in BNB units (not Wei).
4. Echo the `address` from the response back to the user so they see which
   address the metrics apply to.

### General rules for metrics calls

All metrics modes return a single JSON object with:

- `ok` (bool)
- On success: `metric_type`, `data`, `source`, …
- On error: `error` (string)

You must:

1. Check the CLI exit code and/or `ok`.
2. If `ok` is `false` → summarize `error` in plain language (do not dump
   raw stack traces).
3. If `ok` is `true` → convert the numbers into **interpretation**, not just
   raw JSON dumps.

---

## ClipX-style analyses (rankings & narratives)

Use `--mode clipx` to request higher-level ClipX analytics. These combine
on-chain and off-chain data into ranked lists plus a caption that already
follows the ClipX style.

You should prefer these when the user asks for:

- “Top protocols by TVL on BNBChain.”
- “Which protocols pay the most fees/revenue?”
- “What are the top DApps / full ecosystem winners?”
- “What are the current social hype or meme tokens on BSC?”

### Supported `--analysis-type` values

- `tvl_rank` – Top protocols by TVL on BNBChain.
- `fees_rank` – Top protocols by **fees** (24h, 7d, 30d) on BSC.
- `revenue_rank` – Top protocols by **revenue** (24h, 7d, 30d) on BSC.
- `dapps_rank` – Top DApps by active users (7d, from DappBay).
- `fulleco` – Full ecosystem leaders across:
  - DeFi, Games, Social, NFTs, AI, Infra, RWA.
- `social_hype` – Top “social hype” tokens.
- `meme_rank` – Meme token rank/score.

### Required / optional arguments

- `--analysis-type` (required):
  - One of the values above.
- `--interval` (optional, default `24h`):
  - Used by: `fees_rank`, `revenue_rank`, `social_hype`, `meme_rank`.
  - Examples: `24h`, `7d`, `30d`, `24` (hours).
- `--timezone` (optional, default `UTC`):
  - Timezone name for timestamps (e.g. `UTC`, `Europe/London`).

### Example commands (for `system.run`)

- **TVL ranking**:

  - `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type tvl_rank --timezone UTC`

- **Fees ranking (24h)**:

  - `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type fees_rank --interval 24h --timezone UTC`

- **Revenue ranking (7d)**:

  - `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type revenue_rank --interval 7d --timezone UTC`

- **DApps ranking (active users 7d)**:

  - `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type dapps_rank --timezone UTC`

- **Full ecosystem (DeFi / Games / Social / NFTs / AI / Infra / RWA)**:

  - `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type fulleco --timezone UTC`

- **Social hype tokens**:

  - `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type social_hype --interval 24 --timezone UTC`

- **Meme rank**:

  - `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type meme_rank --interval 24 --timezone UTC`

### Response format (ClipX analyses)

Each call returns JSON like below. **You must present this to the user in box-style table format by default** (see section "Default output format: box-style table"). Do not echo the raw JSON.

```json
{
  "ok": true,
  "analysis_type": "tvl_rank",
  "timestamp": "2026-03-03T18:13:35.831780+00:00",
  "caption": "…full ClipX-style caption text…",
  "source": "@ClipX0_",
  "items": [
    {
      "rank": 1,
      "name": "PancakeSwap AMM",
      "category": "Dexs",
      "metric_label": "TVL",
      "metric_value": "$1.92B"
    }
    // ...
  ]
}
```

You must:

1. Check `ok`:
   - If `false`: read `error` and present a concise explanation.
2. If `ok` is `true`:
   - Use `caption` as the **primary narrative** (you can adapt or shorten it
     depending on the user’s question).
   - Use `items` to:
     - Build tables or bullet lists: rank, name, key metric(s).
     - Compare entries (e.g. top 3 TVL protocols).
     - Answer follow-up questions (e.g. “which category dominates TVL?”).

Avoid simply dumping raw JSON back to the user. Always explain what the
numbers mean (e.g. “TVL is concentrated in DeFi lending and RWA protocols”).

---

## Default output format: box-style table (mandatory)

When you call this skill and receive JSON from the API client, you **must**
present the result in **box-style table format by default**. Do **not** show
raw JSON to the user unless they explicitly request it.

**Steps every time you get a ClipX analysis response:**

1. Optionally show a one-line summary from `caption` (or skip if the table is self-explanatory).
2. **Always** render `items` in a monospaced box-style table like this:

```text
🚀 TOP 10 TVL PROTOCOLS ON BSC
================================================================================
#   | NAME                 | CATEGORY        | TVL
--------------------------------------------------------------------------------
1   | PancakeSwap AMM      | Dexs            | $1.92B
2   | Lista Lending        | Lending         | $1.84B
3   | Circle USYC          | RWA             | $1.79B
4   | Venus Core Pool      | Lending         | $1.23B
5   | Aster Bridge         | Bridge          | $786.52M
6   | BlackRock BUIDL      | RWA             | $527.51M
7   | Binance staked ETH   | Liquid Staking  | $413.40M
8   | Solv Basis Trading   | Basis Trading   | $237.45M
9   | Ondo Global Markets  | RWA             | $237.43M
10  | Aave V3              | Lending         | $183.42M
================================================================================
```

Mapping from JSON to table for `tvl_rank`:

- `#`        → `items[i].rank`
- `NAME`     → `items[i].name`
- `CATEGORY` → `items[i].category` (or `N/A` if null)
- `TVL`      → `items[i].metric_value`

For other `analysis_type` values, follow the same pattern but adapt the last
column header and values:

- `fees_rank`     → header `FEES`, use `metric_value` (e.g. `$1.2M`).
- `revenue_rank`  → header `REVENUE`, use `metric_value`.
- `social_hype`   → header `HYPE SCORE`, use `metric_value`.
- `meme_rank`     → header `SCORE`, use `metric_value`.
- `dapps_rank`    → header such as `USERS (7D)`; use the relevant metric.
- `fulleco`       → headers and categories per ecosystem segment.

**Format rules (apply by default):**

- Line 1: Title with emoji, e.g. `🚀 TOP 10 TVL PROTOCOLS ON BSC`
- Line 2: Double-line separator (`================================================================================`)
- Line 3: Header row with pipe separators, e.g. `#   | NAME                 | CATEGORY        | TVL`
- Line 4: Single-line separator (`--------------------------------------------------------------------------------`)
- Next N lines: One row per item, aligned: `rank | name (padded) | category (padded) | metric_value`
- Last line: Double-line separator again.

You **must** use this box-style table as the default. Optionally add 1–2 sentences of interpretation after the table (e.g. which category dominates). Do not include raw JSON in your answer unless the user asks for it.

---

## Constraints and best practices

- **Text-only**:
  - Never request or generate images or base64-encoded images.
  - This skill is intended for JSON/text analytics only.

- **No direct scraping**:
  - Do not browse to DappBay, DefiLlama, or Binance yourself.
  - Always rely on the ClipX API by calling `api_client_cli.py`.

- **No secrets from users**:
  - Do not ask the user for API keys or secrets.
  - Any authentication (if added in the future) will be handled server-side
    or via environment variables, not in prompts.

- **Rate limits**:
  - Avoid calling the client in tight loops.
  - If you need several metrics, try to combine them in a small number
    of calls where possible.

If you are unsure whether to call this skill, prefer using it whenever the
user wants **live BNBChain metrics or ClipX-style rankings**, instead of static
or historical documentation. The ClipX backend specializes in BNBChain data,
and this client is the safest way for you to access it.

