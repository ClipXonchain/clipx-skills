"""
Read ClipX JSON from stdin and print box-style table to stdout.
Run locally to test formatted output, e.g.:
  python api_client_cli.py --mode clipx --analysis-type tvl_rank --timezone UTC | python format_box.py
"""
import json
import sys

def main():
    # Use utf-8-sig to strip BOM when piping on Windows
    raw = sys.stdin.buffer.read().decode("utf-8-sig").strip()
    if not raw:
        print("No input (pipe JSON from api_client_cli.py)", file=sys.stderr)
        sys.exit(1)
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)

    if not data.get("ok"):
        print("Error:", data.get("error", "unknown"), file=sys.stderr)
        sys.exit(1)

    analysis_type = data.get("analysis_type", "")
    items = data.get("items", [])
    if not items:
        print(data.get("caption", ""))
        return

    # Title and column header from analysis_type
    titles = {
        "tvl_rank": ("TOP 10 TVL PROTOCOLS ON BSC", "#", "NAME", "CATEGORY", "TVL"),
        "fees_rank": ("TOP 10 FEES PROTOCOLS ON BSC", "#", "NAME", "CATEGORY", "FEES"),
        "revenue_rank": ("TOP 10 REVENUE PROTOCOLS ON BSC", "#", "NAME", "CATEGORY", "REVENUE"),
        "dapps_rank": ("TOP 10 DAPPS BY USERS (7D)", "#", "NAME", "CATEGORY", "USERS"),
        "fulleco": ("FULL ECOSYSTEM LEADERS", "#", "NAME", "CATEGORY", "METRIC"),
        "social_hype": ("TOP 10 SOCIAL HYPE TOKENS", "#", "NAME", "SENTIMENT", "HYPE SCORE"),
        "meme_rank": ("TOP 10 MEME TOKENS BY SCORE", "#", "NAME", "—", "SCORE"),
    }
    title_line, col1, col2, col3, col4 = titles.get(
        analysis_type, ("RANKING", "#", "NAME", "CATEGORY", "VALUE")
    )

    w2, w3, w4 = 22, 16, 12
    sep_double = "=" * 80
    sep_single = "-" * 80

    print()
    print(f"🚀 {title_line}")
    print(sep_double)
    print(f"{col1:<3} | {col2:<{w2}} | {col3:<{w3}} | {col4}")
    print(sep_single)
    for it in items:
        rank = it.get("rank", "")
        name = (it.get("name") or "")[:w2]
        cat = (it.get("category") or "—")[:w3]
        val = it.get("metric_value", "")
        print(f"{rank:<3} | {name:<{w2}} | {cat:<{w3}} | {val}")
    print(sep_double)
    if data.get("source"):
        print(f"Source: {data['source']}")
    print()

if __name__ == "__main__":
    main()
