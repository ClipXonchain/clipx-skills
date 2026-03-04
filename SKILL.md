---
name: clipx-bnbchain-api-client
description: Thin client for the private ClipX BNBChain API, returning text-only JSON metrics and rankings for BNB Chain (no scraping code, no API keys).
metadata: { "openclaw": { "emoji": "🟡", "requires": { "bins": ["python"] }, "os": ["win32", "linux", "darwin"] } }
---

## Response rules (read first)

**Rule 1 — Menu format:** Always use numbered lines (1. 2. 3. …). See "Interactive menu" section.

**Rule 2 — Table format:** Always wrap the table output in `<pre>` and `</pre>` tags. This is required so the table displays in monospace with aligned columns. Without `<pre>` tags the columns will be misaligned and unreadable.

**Rule 3 — Response ends with the table.** After the closing `</pre>`, your message is complete. Write nothing else.

---

## What this skill does

Calls the ClipX BNBChain API via `python "{baseDir}/api_client_cli.py"` to fetch text-only BNB Chain metrics and rankings. The backend handles all scraping.

---

## Interactive menu

When the user says "clipx", "bnbchain", "bnbchain analysis", or asks for BNB Chain reports without specifying which one, output this menu exactly:

🟡 ClipX / BNBChain Analysis — Choose one:

1. TVL Rank — Top 10 protocols by Total Value Locked
2. Fees Rank — Top 10 protocols by fees paid (24h/7d/30d)
3. Revenue Rank — Top 10 protocols by revenue (24h/7d/30d)
4. DApps Rank — Top 10 DApps by users (7d)
5. Full Ecosystem — DeFi, Games, Social, NFTs, AI, Infra, RWA leaders
6. Social Hype — Top 10 social hype tokens
7. Meme Rank — Top 10 meme tokens by score
8. Network metrics — Latest block, gas price, sync state

Reply with a number (1–8).

---

## Commands (number → command)

| # | Command |
|---|---------|
| 1 | `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type tvl_rank --timezone UTC` |
| 2 | `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type fees_rank --interval 24h --timezone UTC` |
| 3 | `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type revenue_rank --interval 24h --timezone UTC` |
| 4 | `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type dapps_rank --timezone UTC` |
| 5 | `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type fulleco --timezone UTC` |
| 6 | `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type social_hype --interval 24 --timezone UTC` |
| 7 | `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type meme_rank --interval 24 --timezone UTC` |
| 8 | `python "{baseDir}/api_client_cli.py" --mode metrics_basic` |

For 2 (fees) and 3 (revenue), default to 24h. If the user specifies 7d or 30d, use `--interval 7d` or `--interval 30d`.

---

## Displaying results

The client prints a pre-formatted table. Your job:

1. Run the command.
2. Take the stdout output (the formatted table).
3. Wrap the entire output between `<pre>` and `</pre>` tags.
4. Send it. Done. Your response is complete.

Your response must look exactly like this:

<pre>
================================================================================
🚀 TOP 10 MEME TOKENS BY SCORE
================================================================================
--------------------------------------------------------------------------------
#   | NAME                 | —               | SCORE
--------------------------------------------------------------------------------
1   | TokenA               | —               | 4.76
2   | TokenB               | —               | 4.61
...
================================================================================
Source: @ClipX0_
</pre>

---

## Network metrics (option 8)

Returns JSON with `latest_block`, `gas_price_gwei`, `syncing`. Summarize in plain language.

---

## Other modes

- `--mode metrics_block --blocks 100` — average block time and gas over recent blocks.
- `--mode metrics_address --address 0x...` — BNB balance and tx count for an address.

---

## Environment

The API base URL defaults to `http://5.189.145.246:8000`. Override with `CLIPX_API_BASE` env var.
