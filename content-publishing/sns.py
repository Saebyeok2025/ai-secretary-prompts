"""Offline SNS planning. No publishing, scheduling, authentication or state writes."""
import argparse
import json
import sys
from pathlib import Path

from agent import plan, read_json


def build_plan(config, state):
    count = config.get("card_count", 8)
    if type(count) is not int or not 6 <= count <= 10:
        raise ValueError("card_count must be an integer from 6 to 10")
    for key in ("instagram_handle", "threads_handle", "facebook_profile"):
        if not isinstance(config.get(key), str) or not config[key].strip():
            raise ValueError("Missing account setting: " + key)
    if config.get("publication_route") != "instagram_connected_share":
        raise ValueError("Only the approved Instagram connected-share route is supported")
    # Only the book selection algorithm is reused; state is supplied separately.
    selection = plan({**config, "blog_url": "", "category": ""}, state)
    if selection is None:
        return None
    for key in ("blog_url", "category"):
        selection.pop(key)
    return {
        **selection,
        "channel": "sns",
        "accounts": {key: config[key] for key in
                     ("instagram_handle", "threads_handle", "facebook_profile")},
        "timezone": "Asia/Seoul", "prepare_time": "18:30", "public_time_target": "20:00",
        "publication_route": config["publication_route"],
        "card_count": count, "dimensions": [1080, 1350], "caption_max_chars": 500,
        "cards": [f"{i:02d}.png" for i in range(1, count + 1)],
        "requires_actual_account_and_post_verification": True,
    }


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("plan", "prompt"))
    parser.add_argument("--config", default="sns.config.local.json")
    parser.add_argument("--state", default="sns.state.local.json")
    args = parser.parse_args()
    target = build_plan(read_json(args.config), read_json(args.state))
    if args.command == "prompt" and target is not None:
        print(Path(__file__).with_name("prompts").joinpath("instagram.md").read_text(encoding="utf-8"))
        print("\n실행 대상:")
    print(json.dumps(target, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
