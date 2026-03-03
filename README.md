## ClipX BNBChain API Client Skill (Public)

This folder is the **public skill** you can upload to **ClawHub**. It contains
only a thin client that calls your **private ClipX BNBChain API** and returns
text-only JSON for:

- Core BNB Smart Chain metrics (basic, block stats, address).
- ClipX-style rankings (TVL, fees, revenue, DApps, full ecosystem, social hype, meme rank).

The actual scraping and analytics logic (Playwright, DefiLlama, DappBay,
Binance page structure, etc.) lives **behind your API** and is **not**
included here.

---

### Files in This Public Skill

- `SKILL.md`  
  OpenClaw skill metadata and instructions on how to use the client via
  `system.run`.

- `api_client_cli.py`  
  Tiny Python CLI that calls your hosted API and prints the JSON response.
  This is what the agent will execute.

- `format_box.py`  
  Optional helper: reads JSON from stdin and prints a box-style table. Use
  for local testing only (see below); the agent renders tables in its reply
  per `SKILL.md`.

- `requirements.txt`  
  Only `requests` is required on the client side.

Place this folder (with these files) under your workspace `skills`
directory when testing locally, or publish it to ClawHub.

---

### Client Requirements

- **Python**: 3.10–3.12 recommended.
- **Dependencies**:

  ```bash
  pip install -r requirements.txt
  ```

  Installs:

  - `requests`

No Playwright, FastAPI, or other heavy dependencies are needed here.

---

### Configuring the API Base URL

By default, `api_client_cli.py` uses this logic:

1. If the environment variable `CLIPX_API_BASE` is set, it uses that
   (e.g. `https://api.clipx.app`).
2. Otherwise, it falls back to the hard-coded base URL inside
   `get_api_base()` (you should edit this before publishing).

To configure via environment:

```bash
export CLIPX_API_BASE="https://your-clipx-api.com"
```

On Windows PowerShell:

```powershell
$env:CLIPX_API_BASE = "https://your-clipx-api.com"
```

---

### How Agents Should Call the Client

The model instructions in `SKILL.md` tell the agent to use the `system.run`
tool to execute:

- **Core metrics**:

  ```bash
  python "{baseDir}/api_client_cli.py" --mode metrics_basic
  python "{baseDir}/api_client_cli.py" --mode metrics_block --blocks 100
  python "{baseDir}/api_client_cli.py" --mode metrics_address --address 0x...
  ```

- **ClipX analyses** (formatted table is default; use `--no-formatted` for raw JSON):

  ```bash
  python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type tvl_rank --timezone UTC
  python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type fees_rank --interval 24h --timezone UTC
  python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type revenue_rank --interval 7d --timezone UTC
  python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type dapps_rank --timezone UTC
  python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type fulleco --timezone UTC
  python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type social_hype --interval 24 --timezone UTC
  python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type meme_rank --interval 24 --timezone UTC
  ```

**Formatted table is the default** for clipx mode; the CLI prints the server-formatted table (identical to VPS output). The agent displays it in a code block or `<pre>`. Use `--no-formatted` to get raw JSON instead.

---

### Local testing: box-style table

Use `format_box.py` to print a box-style table. You can either fetch and format in one command, or pipe from the CLI.

**One command (fetch + format):**

```bash
python format_box.py --analysis-type tvl_rank
python format_box.py --analysis-type meme_rank --interval 24 --timezone UTC
python format_box.py --analysis-type fees_rank --interval 7d
```

Optional: `--interval` (default `24h`), `--timezone` (default `UTC`). Supported `--analysis-type`: `tvl_rank`, `fees_rank`, `revenue_rank`, `dapps_rank`, `fulleco`, `social_hype`, `meme_rank`.

**Or pipe from the client:**

```bash
python api_client_cli.py --mode clipx --analysis-type tvl_rank --timezone UTC | python format_box.py
```

`format_box.py` reads JSON from stdin (UTF-8 or UTF-8 BOM) when no `--analysis-type` is given.

---

### Telegram: monospace and one-click copy

For the ClipX table to appear in **Telegram** in monospace (aligned columns, copy-friendly block like the reference), the message must be sent with **parse_mode=HTML**. The agent is instructed to wrap the table in `<pre>...</pre>`. Your bot or OpenClaw→Telegram bridge should send the agent’s reply with **parse_mode=HTML** so Telegram renders the `<pre>` block in monospace. Do not strip the `<pre>` tags when forwarding to Telegram.

---

### Private API (Server Side)

This folder assumes you have a **separate private repo or directory** that
hosts your actual API service, for example:

- `clipx_api/main.py` (FastAPI app).
- `clipx_api/requirements.txt` (FastAPI, uvicorn, Playwright, pytz, etc.).

The API should expose endpoints like:

- `GET /api/bnb/metrics/basic`
- `GET /api/bnb/metrics/block-stats?blocks=100`
- `GET /api/bnb/metrics/address?address=0x...`
- `GET /api/clipx/analysis?t=tvl_rank&interval=24h&tz=UTC`

Each endpoint should return JSON shaped like:

```json
{
  "ok": true,
  "analysis_type": "tvl_rank",
  "timestamp": "2026-03-03T17:03:08.394Z",
  "caption": "…",
  "source": "@ClipX0_",
  "items": [ { "rank": 1, "name": "…", "metric_label": "TVL", "metric_value": "$1.92B" } ],
  "meta": { "interval": "24h" }
}
```

On error:

```json
{ "ok": false, "error": "Human-readable error" }
```

This server-side code should **not** be included in the ClawHub skill
bundle if you want to keep it private.

---

### Publishing to ClawHub

From the `ClipX_Skills` folder:

```bash
clawhub publish . \
  --slug clipx-bnbchain-api-client \
  --name "ClipX BNBChain Metrics & Rankings (API Client)" \
  --version 1.0.0 \
  --tags latest,bnbchain,metrics,clipx
```

This publishes only the thin client and `SKILL.md`, keeping your real logic
behind your API.

## BNB Chain / ClipX Metrics Skill (Text-Only, No API Keys)

### Overview

This skill bundle provides two related text-only capabilities that agents
can call safely without any API keys:

- **Core BNB Smart Chain metrics** via **public RPC**.
- **ClipX-style BNBChain rankings/analytics** (TVL, fees, revenue, DApps,
  full ecosystem, social hype, meme rank) based on your existing scripts.

Everything is returned as **pure JSON/text**. No images or binary data are
produced by the CLIs; image generation in your original scripts remains
unused by this skill.

---

### Files in This Skill Package

- **`bnbchain_metrics_skill.py`**  
  Core implementation of the text-only BNB Chain metrics skill (public JSON-RPC;
  no `web3` dependency).

- **`bnbchain_metrics_cli.py`**  
  CLI wrapper around `bnbchain_metrics_skill.py` for OpenClaw’s `system.run`.

- **`bnbchain_metrics_tool.json`**  
  JSON schema definition for registering core metrics as a tool (for non‑OpenClaw
  frameworks).

- **`clipx_text_skill.py`**  
  Text-only aggregator around your existing ClipX scripts:
  - `tvl_ranking_template_fill.py`
  - `fees_ranking_template_fill.py`
  - `revenue_ranking_template_fill.py`
  - `dapps_ranking_template_fill.py`
  - `fulleco_template_fill.py`
  - `social_hype_template_fill.py`
  - `meme_rank_template_fill.py`

- **`clipx_text_cli.py`**  
  CLI wrapper that exposes all ClipX-style analyses as JSON (caption + ranked
  items, with `source: "@ClipX0_"`).

- **`example_agent_integration.py`**  
  Minimal example showing how to call the core metrics skill from a Python agent/tool handler.

- **`SKILL.md`**  
  OpenClaw skill definition and agent instructions for both CLIs.

- **`requirements.txt`**  
  Python dependencies needed to run everything.

Place all of these files together in your project (for example, in `f:\skill`).

---

### Requirements and Installation

#### Supported Python

- Recommended: **Python 3.11 or 3.12**
  - The code is tested on **3.12.0** on Windows.

#### 1. Create and activate a virtual environment (optional but recommended)

```bash
python -m venv .venv
```

On **Windows PowerShell**:

```bash
.\.venv\Scripts\Activate.ps1
```

On **Windows cmd**:

```bash
.\.venv\Scripts\activate.bat
```

On **Linux/macOS**:

```bash
source .venv/bin/activate
```

#### 2. Install dependencies

From the folder that contains `requirements.txt`:

```bash
pip install -r requirements.txt
```

This installs:

- **`requests`**: HTTP client (used for JSON-RPC and logos).
- **`python-dotenv`**: loads `.env` (optional, used by your original scripts).
- **`playwright`**: headless browser used by your template scripts to scrape pages.
- **`pytz`**: timezone handling (optional but recommended).

> Note: `tweepy` is *not* required for this skill. Your social/meme scripts
> only import it optionally, and the text-only wrappers avoid posting to Twitter.

#### 3. Install Playwright browsers (required for scraping)

Playwright must download a Chromium build:

```bash
playwright install chromium
```

Run this once inside the same virtual environment.

---

### Public RPC Endpoint (No API Key) – Core Metrics

By default, the skill connects to:

- `https://bsc-dataseed1.bnbchain.org`

This is a **public BNB Smart Chain RPC endpoint** that does **not** require any
authentication or API key. You may replace it with a different public BSC RPC
URL if needed (for example, another BNB Chain public node or a self-hosted node).

You can customize the RPC URL:

- In Python by passing the `rpc_url` argument.
- From agents via the `rpc_url` parameter in the tool schema.

---

### Core Metrics: Python Usage (Direct)

Basic usage from Python:

```python
from bnbchain_metrics_skill import (
    BnbChainMetricsSkill,
    run_bnbchain_metrics_skill,
)

# One-shot helpers
basic = run_bnbchain_metrics_skill("basic")
print(basic)

block_stats = run_bnbchain_metrics_skill("block_stats", blocks=200)
print(block_stats)

address_stats = run_bnbchain_metrics_skill(
    "address",
    address="0x0000000000000000000000000000000000000000",
)
print(address_stats)

# Reusing a single instance (more efficient if you call it many times)
skill = BnbChainMetricsSkill()
print(skill.handle_request(metric_type="basic"))
print(skill.handle_request(metric_type="block_stats", blocks=100))
print(
    skill.handle_request(
        metric_type="address",
        address="0x0000000000000000000000000000000000000000",
    )
)
```

Example output (shape only, numbers will differ on live chain):

```json
{
  "metric_type": "basic",
  "data": {
    "latest_block": 41500000,
    "chain_id": 56,
    "network_id": 56,
    "gas_price_gwei": 3.25,
    "syncing": false
  },
  "source": "@ClipX0_"
}
```

All responses are **JSON-safe Python dicts** and contain only text/number/boolean
fields, so they can be serialized to JSON and displayed as text by agents.

---

### Core Metrics: Agent / Tool Integration

You can register this skill as a tool named `bnbchain_metrics`.

#### Tool schema

The file `bnbchain_metrics_tool.json` contains a ready-to-use JSON schema:

- **`name`**: `bnbchain_metrics`
- **`description`**: Explains that it fetches BNB Chain metrics using public RPC.
- **`parameters`**:
  - **`metric_type`** (string, required): one of:
    - `basic`
    - `block_stats`
    - `address`
  - **`blocks`** (integer, optional): used when `metric_type = "block_stats"`.
  - **`address`** (string, optional): used when `metric_type = "address"`.
  - **`rpc_url`** (string, optional): custom public RPC if you do not want to use the default.

This schema works well for:

- OpenAI / OpenRouter tools (function calling).
- OpenClaw-style tool systems.
- Most JSON-schema-based agent frameworks.

#### Tool handler function

Use `example_agent_integration.py` as a template. The core handler looks like:

```python
from typing import Any, Dict
from bnbchain_metrics_skill import run_bnbchain_metrics_skill

def bnbchain_metrics_tool_handler(args: Dict[str, Any]) -> Dict[str, Any]:
    return run_bnbchain_metrics_skill(
        metric_type=args["metric_type"],
        blocks=args.get("blocks"),
        address=args.get("address"),
        rpc_url=args.get("rpc_url") or None,
    )
```

Register `bnbchain_metrics_tool_handler` as the implementation for the
`bnbchain_metrics` tool name in your agent runtime.

---

### Supported Metrics in Detail

#### 1. `basic`

- **Purpose**: Get high-level BNB Chain network status.
- **Input**:

```json
{ "metric_type": "basic" }
```

- **Output** (`data` fields):
  - `latest_block` (int): latest block number.
  - `chain_id` (int): chain ID (56 for mainnet).
  - `network_id` (int): network ID.
  - `gas_price_gwei` (float): current gas price in Gwei.
  - `syncing` (bool): whether the node is still catching up.

#### 2. `block_stats`

- **Purpose**: Analyze recent blocks for timing and gas usage trends.
- **Input**:

```json
{ "metric_type": "block_stats", "blocks": 200 }
```

- **Output** (`data` fields):
  - `from_block` (int): first block in the sampled range.
  - `to_block` (int): last (latest) block in the sampled range.
  - `blocks_considered` (int): number of blocks actually processed.
  - `avg_block_time_seconds` (float): average time between blocks in seconds.
  - `avg_gas_used` (float): average `gasUsed` across the sampled blocks.

> Larger `blocks` values smooth the averages but generate more RPC calls.

#### 3. `address`

- **Purpose**: Inspect a specific address on BNB Chain.
- **Input**:

```json
{
  "metric_type": "address",
  "address": "0x0000000000000000000000000000000000000000"
}
```

- **Output** (`data` fields):
  - `address` (string): checksum-normalized BSC address.
  - `balance_bnb` (float): balance in BNB (not Wei).
  - `tx_count` (int): number of transactions sent by this address.

---

### ClipX Text Analyses (All Template Scripts)

The file `clipx_text_skill.py` exposes your existing scripts as a **single
text-only interface** via:

```python
from clipx_text_skill import run_clipx_text_skill

result = run_clipx_text_skill(
    analysis_type="tvl_rank",  # see list below
    interval="24h",            # only used for some types
    timezone="UTC",
)
```

Supported `analysis_type` values:

- `tvl_rank` – Top BNBChain protocols by TVL (from DefiLlama).
- `fees_rank` – Top protocols by fees (24h, 7d, 30d) on BSC.
- `revenue_rank` – Top protocols by protocol revenue (24h, 7d, 30d) on BSC.
- `dapps_rank` – Top DApps by active users (7d) from DappBay.
- `fulleco` – Full ecosystem leaders (DeFi, Games, Social, NFTs, AI, Infra, RWA).
- `social_hype` – Social hype tokens (Binance “social hype” page).
- `meme_rank` – Meme token rank/score (Binance trenches).

Each call returns JSON with:

- `analysis_type`
- `interval` (where applicable)
- `timestamp`
- `caption` – your existing ClipX caption text.
- `source` – always `@ClipX0_`.
- `items` – list of:
  - `rank` (int)
  - `name` (str)
  - `category` (str or null)
  - `metric_label` (str)
  - `metric_value` (str)

#### ClipX text CLI (for OpenClaw / system.run)

To use this from an agent or terminal:

```bash
python clipx_text_cli.py --analysis-type tvl_rank --timezone UTC
```

More examples:

- TVL ranking:

  ```bash
  python clipx_text_cli.py --analysis-type tvl_rank --timezone UTC
  ```

- Fees ranking (24h):

  ```bash
  python clipx_text_cli.py --analysis-type fees_rank --interval 24h --timezone UTC
  ```

- Revenue ranking (7d):

  ```bash
  python clipx_text_cli.py --analysis-type revenue_rank --interval 7d --timezone UTC
  ```

- DApps ranking:

  ```bash
  python clipx_text_cli.py --analysis-type dapps_rank --timezone UTC
  ```

- Full ecosystem:

  ```bash
  python clipx_text_cli.py --analysis-type fulleco --timezone UTC
  ```

- Social hype tokens:

  ```bash
  python clipx_text_cli.py --analysis-type social_hype --interval 24 --timezone UTC
  ```

- Meme rank:

  ```bash
  python clipx_text_cli.py --analysis-type meme_rank --interval 24 --timezone UTC
  ```

The CLI prints a single JSON object on stdout with the shape described above.

---

### Text-Only Guarantee

- The skill **never** produces images or binary data.
- All endpoints return **Python dicts** that are JSON-serializable.
- Agents should display these results as plain text, JSON, or formatted text.

This makes the skill safe and efficient for text-only agent environments.

---

### Error Handling

The skill uses Python exceptions for clear, predictable failure modes:

- **Invalid metric type**:
  - Raises `ValueError` with a message listing supported types.
- **Missing required parameters**:
  - `block_stats` without valid `blocks` (or `blocks <= 1`) → `ValueError`.
  - `address` without `address` value → `ValueError`.
- **RPC connectivity issues**:
  - On initialization, if the RPC is unreachable → `RuntimeError`.
  - When fetching specific blocks (e.g. from a pruned node) → `RuntimeError`.

At the agent level, you should:

- Catch these exceptions.
- Return a user-friendly error string (still text-only) back to the user.

---

### Security and Privacy

- Uses only **public on-chain data** from BNB Smart Chain.
- Does **not** handle private keys or sensitive data.
- Safe to expose as a public tool, subject only to the rate limits and policies
  of the chosen public RPC endpoint.

---

### Quick Start Checklist (for Agents)

1. **Copy files** (`bnbchain_metrics_skill.py`, `bnbchain_metrics_cli.py`,
   `clipx_text_skill.py`, `clipx_text_cli.py`, all `*_template_fill.py` files,
   `SKILL.md`, `requirements.txt`) into your project/skill folder.
2. **Create and activate a virtual environment** (Python 3.11–3.12 recommended).
3. **Install dependencies** with `pip install -r requirements.txt`.
4. **Install Playwright Chromium** with `playwright install chromium`.
5. For **OpenClaw**:
   - Ensure `SKILL.md` is present (this file describes how to call both CLIs).
   - Let the agent use `system.run` to call:
     - `python "{baseDir}/bnbchain_metrics_cli.py" ...` for raw BSC metrics.
     - `python "{baseDir}/clipx_text_cli.py" ...` for ClipX-style rankings.
6. For other frameworks:
   - Optionally use `bnbchain_metrics_tool.json` + `example_agent_integration.py`
     for core metrics.
   - Directly shell out to `clipx_text_cli.py` for ClipX analyses and parse
     the returned JSON.



