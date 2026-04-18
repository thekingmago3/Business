"""CLI entrypoint.

Commands:
  python -m content_agent run               # start the daily scheduler
  python -m content_agent generate          # run every slot once (catch-up / one-shot)
  python -m content_agent generate --platform tiktok --time 09:00
  python -m content_agent analytics         # refresh metrics for shipped posts
"""

from __future__ import annotations

import argparse
import logging
import sys

from .agent import ContentAgent
from .analytics import refresh_metrics
from .config import load_settings
from .scheduler import run_scheduler
from .storage import Storage


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="content_agent")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("run", help="start the daily scheduler (blocking)")

    g = sub.add_parser("generate", help="generate pieces once (for all slots, or a specific one)")
    g.add_argument("--platform", choices=("tiktok", "instagram", "youtube"))
    g.add_argument("--time", help="specific slot time from schedule.yaml, e.g. 09:00")

    sub.add_parser("analytics", help="refresh metrics for shipped posts")

    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    settings = load_settings()

    if args.cmd == "run":
        run_scheduler(settings)
        return 0

    if args.cmd == "generate":
        agent = ContentAgent(settings)
        if args.platform and args.time:
            slots = [s for s in settings.schedule.slots_for(args.platform) if s.time == args.time]
            if not slots:
                print(f"no slot at {args.time} for {args.platform}", file=sys.stderr)
                return 2
            r = agent.run_slot(args.platform, slots[0])
            print(f"✓ {r.platform} @ {r.slot_time} — piece_id={r.piece_id} "
                  f"{'[dry-run]' if r.dry_run else 'published'}"
                  + (f" err={r.error}" if r.error else ""))
            return 0
        results = agent.run_day()
        for r in results:
            status = "dry-run" if r.dry_run else ("error" if r.error else "posted")
            print(f"  {r.platform:10s} {r.slot_time}  piece={r.piece_id}  {status}")
        return 0

    if args.cmd == "analytics":
        storage = Storage(settings.db_path)
        n = refresh_metrics(settings, storage)
        print(f"refreshed metrics for {n} post(s)")
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
