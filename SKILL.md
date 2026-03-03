---
name: clipx-bnbchain-api-client
description: Thin client for the private ClipX BNBChain API, returning text-only JSON metrics and rankings for BNB Chain (no scraping code, no API keys).
metadata: { "openclaw": { "emoji": "🟡", "requires": { "bins": ["python"] }, "os": ["win32", "linux", "darwin"] } }
---

**MENU RULE:** When user asks for clipx/BNBChain reports without specifying which one: show a **numbered** list (1., 2., 3., …). Never bullets (•). Never "tvl 24h" or "fees 7d". Say: "Reply with a number (1–8) to run that analysis."

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
2. **When the user says "clipx" or "bnbchain analysis"** (without specifying which analysis), show the numbered menu (see "Interactive menu" below) and wait for them to reply with 1–8.
3. Call `api_client_cli.py` with the correct arguments.
4. Parse the JSON response.
5. **By default**, present the result in **box-style table format** (see below). Never show raw JSON to the user unless they explicitly ask for it.

You **must never** attempt to re-scrape websites directly; always go through
the ClipX API via this client.

**Preferred: server-formatted output is the default.** For ClipX analyses, call the client (formatted output is on by default). The API returns the exact VPS-style table; the client prints it. You then display that output in a single code block (or `<pre>...</pre>` for Telegram) so the format matches the server and stays monospace. Example: `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type tvl_rank --timezone UTC`. If formatted output fails, fall back to parsing JSON and rendering the box-style table yourself as described below.

**Never offer follow-up options.** After displaying the table, do **not** add any of these:
- "If you want machine-readable output (pipe-separated lines or JSON), I can..."
- "re-run with --no-formatted" or "parse into pipe-separated lines"
- "Which would you like?" / "Want pipe, save, or post?"
- "24h pipe?", "7d pipe?", "save to file?", "post to Moltbook/Telegram?"

Show **only** the box-style table. Stop. Do not suggest alternatives unless the user explicitly asks.

*(Optional, for local testing only: the skill includes `format_box.py`, which reads JSON from stdin and prints a box-style table. You do not need to run it; you render the table in your reply. See README for the pipe command.)*

---

## Interactive menu: "clipx" or "bnbchain analysis"

When the user says **"clipx"**, **"bnbchain analysis"**, **"metrics for BNB Chain"**, **"show clipx options"**, or similar (asking for ClipX/BNBChain analytics without specifying which one), you **must** show this **numbered** menu (1., 2., 3., … — never bullets):

```
🟡 ClipX / BNBChain Analysis — Choose one:

1. TVL Rank — Top 10 protocols by Total Value Locked
2. Fees Rank — Top 10 protocols by fees paid (24h/7d/30d)
3. Revenue Rank — Top 10 protocols by revenue (24h/7d/30d)
4. DApps Rank — Top 10 DApps by users (7d)
5. Full Ecosystem — DeFi, Games, Social, NFTs, AI, Infra, RWA leaders
6. Social Hype — Top 10 social hype tokens
7. Meme Rank — Top 10 meme tokens by score
8. Network metrics — Latest block, gas price, sync state

Reply with a number (1–8) to run that analysis.
```

**Do not** use bullet points (•) or ask for command names like "tvl 24h", "fees 7d", "meme 24h". **Always** use numbered items and instruct the user to reply with a number only.

**When the user replies with a number (1–8):** Run the corresponding command:

| # | analysis_type | Command |
|---|---------------|---------|
| 1 | tvl_rank | `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type tvl_rank --timezone UTC` |
| 2 | fees_rank | `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type fees_rank --interval 24h --timezone UTC` |
| 3 | revenue_rank | `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type revenue_rank --interval 24h --timezone UTC` |
| 4 | dapps_rank | `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type dapps_rank --timezone UTC` |
| 5 | fulleco | `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type fulleco --timezone UTC` |
| 6 | social_hype | `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type social_hype --interval 24 --timezone UTC` |
| 7 | meme_rank | `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type meme_rank --interval 24 --timezone UTC` |
| 8 | metrics_basic | `python "{baseDir}/api_client_cli.py" --mode metrics_basic` |

For **2** (fees) and **3** (revenue), you may ask "24h, 7d, or 30d?" if the user wants a different interval, or default to 24h. Display the result in a code block (or `<pre>` for Telegram) as usual.

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

**Critical — monospace so columns don't break:**  
You **must** wrap the entire table in a **single** block so it renders in monospace and supports one-click copy. Use **one** of these formats:

- **For Telegram (preferred when the reply is shown in a Telegram bot chat):** Wrap the table in **HTML pre** so Telegram displays it in monospace with a copy-friendly block. Output the table inside `<pre>...</pre>`. Escape any `&`, `<`, `>` in the table as `&amp;`, `&lt;`, `&gt;`. The integration must send the message with **parse_mode=HTML** so Telegram renders the `<pre>` block in monospace (like the reference: aligned columns and one-click copy).
- **Otherwise:** Use a single **markdown code block** (triple backticks, e.g. ` ```text ` … ` ``` `). Do not split the table across multiple blocks or mix non-code text inside the block.

**Steps every time you get a ClipX analysis response:**

1. Call the client (formatted output is **default** for clipx mode) so the API returns the server’s pre-formatted table and the client prints it. The command output is then the exact VPS-style table — display it **as-is** in a single code block (or `<pre>...</pre>` for Telegram). No need to rebuild the table from JSON.
2. If formatted output failed or you used `--no-formatted`, parse the JSON and render `items` in a monospaced box-style table **inside a fenced code block** (triple backticks). Use this **exact layout** so columns stay aligned (same as the VPS/server and `format_box.py` output):

- Line 1: double-line separator (`========...`)
- Line 2: title with emoji, e.g. `🚀 TOP 10 TVL PROTOCOLS ON BSC` (for fees/revenue append interval like ` (7D)` when present)
- Line 3: double-line separator again
- Line 4: single-line separator (`--------...`)
- Line 5: header row: `#   | NAME                 | CATEGORY        | TVL` (or FEES, REVENUE, etc.)
- Line 6: single-line separator again
- Next N lines: one row per item, same column widths so pipes align
- Then: double-line separator, then `Source: @ClipX0_`, then close the code block

Example (inside a code block):

```text
================================================================================
🚀 TOP 10 FEES PAID PROTOCOLS ON BSC (7D)
================================================================================
--------------------------------------------------------------------------------
#   | NAME                 | CATEGORY        | FEES
--------------------------------------------------------------------------------
1   | BSC                  | Chain           | $2.04M
2   | PancakeSwap AMM V3   | Dexs            | $1.87M
3   | GMGN                 | Telegram Bot    | $994.0K
...
================================================================================
Source: @ClipX0_
```

**Telegram: monospace and one-click copy (reference format)**  
For the table to appear in Telegram like the reference (monospace, aligned columns, copy button), the message must be sent with **parse_mode=HTML**. Output the table inside HTML pre tags:

`<pre>`
`================================================================================`
`🚀 TOP 10 FEES PAID PROTOCOLS ON BSC (7D)`
`================================================================================`
… (all table lines) …
`Source: @ClipX0_`
`</pre>`

If the table contains `&`, `<`, or `>`, escape them as `&amp;`, `&lt;`, `&gt;`. The bot or integration that sends the agent reply to Telegram must use **parse_mode=HTML** so the `<pre>` block is rendered in monospace. Prefer this format when the user is in a Telegram chat or when they expect Telegram-style output.

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

**Format rules (apply by default) — match this order so client output matches the server/VPS:**

- **Wrap the whole table in a single code block:** Start with ` ```text ` or ` ``` `, then the table lines below, then close with ` ``` `. One block only — this keeps the table in monospace and lets the chat UI show a one-click copy button for the whole table.
- Line 1: Double-line separator (`================================================================================`)
- Line 2: Title with emoji, e.g. `🚀 TOP 10 TVL PROTOCOLS ON BSC` or `🚀 TOP 10 FEES PAID PROTOCOLS ON BSC (7D)` (add interval in parens for fees_rank/revenue_rank when present)
- Line 3: Double-line separator again
- Line 4: Single-line separator (`--------------------------------------------------------------------------------`)
- Line 5: Header row with pipe separators, e.g. `#   | NAME                 | CATEGORY        | TVL` (use fixed column widths: rank 3, name 22, category 16 so pipes align)
- Line 6: Single-line separator again
- Next N lines: One row per item, same widths: `rank | name (padded to 22) | category (padded to 16) | metric_value`
- Then: Double-line separator; then `Source: @ClipX0_`; then close the code block with ` ``` `.

You **must** use this box-style table as the default, **always inside a code block**. Optionally add 1–2 sentences of interpretation after the code block (e.g. which category dominates). Do not include raw JSON in your answer unless the user asks for it.

**Do not recommend or show pipe-separated format:** Do **not** offer or suggest "export as pipe lines", "pipe-separated output", or "pipe-separated format". Do **not** display a separate "Pipe-separated output:" section or raw pipe-delimited lines (e.g. `1|Name|Category|Value`). Present **only** the box-style table (or `<pre>` for Telegram). If you add a follow-up, keep it generic (e.g. "Want a different interval or another metric?") and do not mention pipe-separated export, save to file, or post/share unless the user explicitly asks.

**Forbidden follow-up options — never offer these:** You must **never** add suggestions after the table. Forbidden: "If you want machine-readable output...", "re-run with --no-formatted", "parse into pipe-separated lines", "24h pipe", "7d pipe", "save to file", "post to Moltbook/Telegram", "Which would you like?". Simply show the box-style table and **stop**. Do not offer any alternatives.

---

## Constraints and best practices

- **Text-only**:
  - Never request or generate images or base64-encoded images.
  - This skill is intended for JSON/text analytics only.

- **No follow-up suggestions after the table**:
  - Do not offer machine-readable output, --no-formatted, pipe-separated lines, save, post, or "Which would you like?". Show the table and stop. No alternatives.

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

