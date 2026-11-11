"""Local planning and verification tools; publishing is performed by Codex's browser tools."""
import argparse
import json
import sys
from pathlib import Path
from urllib.parse import urlparse


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def plan(config, state):
    books = config["books"]
    for book in books:
        total, size = book["total_chapters"], book["chapters_per_post"]
        if type(total) is not int or type(size) is not int or total < 1 or size < 1:
            raise ValueError("Chapter totals and batch sizes must be positive integers")
        completed = state.get("completed", {}).get(book["id"], [])
        if any(type(n) is not int or n < 1 or n > total for n in completed):
            raise ValueError("Completed chapter is outside the book")
        for start in range(1, total + 1, size):
            batch = list(range(start, min(start + size, total + 1)))
            present = set(batch).intersection(completed)
            if present and len(present) != len(batch):
                raise ValueError("Partially completed batch: reconcile actual posts first")
            if not present:
                return {"book_id": book["id"], "title": book["title"],
                        "source": str(Path(config["source_root"]) / book["source"]),
                        "chapters": batch, "blog_url": config["blog_url"],
                        "category": config["category"]}
    return None


def verify(config, manifest, base):
    """Check local publication evidence. These assertions do not query Naver."""
    errors = []
    actual, expected = urlparse(manifest.get("published_url", "")), urlparse(config["blog_url"])
    if (actual.scheme != "https" or actual.netloc != expected.netloc
            or actual.query or actual.fragment or actual.username
            or actual.path.rsplit("/", 1)[0].rstrip("/") != expected.path.rstrip("/")
            or not actual.path.rsplit("/", 1)[-1].isdigit()):
        errors.append("Published URL must identify a post in the configured blog")
    if manifest.get("category") != config["category"]:
        errors.append("Category differs from configuration")
    images = manifest.get("images", [])
    if len(images) not in (5, 6) or len(images) != len(set(images)):
        errors.append("Expected 5 or 6 distinct images, thumbnail first")
    if manifest.get("thumbnail") != (images[0] if images else None):
        errors.append("Thumbnail must be first")
    for name in images + [manifest.get("screenshot", "")]:
        target = (base / name).resolve()
        if not name or not target.is_relative_to(base.resolve()) or not target.is_file():
            errors.append("Missing evidence or path outside bundle: " + name)
    checks = ("source_read", "range_verified", "duplicate_checked", "text_checked",
              "image_text_checked", "thumbnail_dimensions_checked", "heading_styles_checked",
              "divider_alignment_checked", "closing_font_checked", "citation_font_checked",
              "public_post_opened", "published_images_checked")
    for key in checks:
        if manifest.get("checks", {}).get(key) is not True:
            errors.append("Unverified: " + key)
    return errors


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["plan", "prompt", "verify"])
    parser.add_argument("--config", default="config.local.json")
    parser.add_argument("--state", default="state.local.json")
    parser.add_argument("--manifest", help="Publication evidence JSON (verify only)")
    args = parser.parse_args()
    config = read_json(args.config)
    if args.command == "verify":
        if not args.manifest:
            parser.error("--manifest is required")
        errors = verify(config, read_json(args.manifest), Path(args.manifest).resolve().parent)
        print(json.dumps({"ok": not errors, "errors": errors}, ensure_ascii=False, indent=2))
        return 1 if errors else 0
    target = plan(config, read_json(args.state))
    if args.command == "plan" or target is None:
        print(json.dumps(target, ensure_ascii=False, indent=2))
    else:
        print(Path(__file__).with_name("prompts").joinpath("publish.md").read_text(encoding="utf-8"))
        print("\n오늘 대상:\n" + json.dumps(target, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
