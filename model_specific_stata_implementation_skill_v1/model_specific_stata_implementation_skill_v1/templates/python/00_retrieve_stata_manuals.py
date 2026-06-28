"""
Read stata_command_plan.csv, map requested commands to official Stata manual sources
or community-package help retrieval steps, and export a manual retrieval log.

This script is designed for Codex-generated projects. It may download PDFs when
internet access is available. Do not redistribute downloaded manuals; cache them
only inside the project for local research use.
"""
from __future__ import annotations

import csv
import datetime as dt
import re
import sys
from pathlib import Path
from urllib.request import urlopen, Request

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PLAN = ROOT / "examples" / "stata_command_plan_example.csv"
REGISTRY = ROOT / "templates" / "metadata" / "manual_source_registry.csv"
OUT_DIR = ROOT / "output" / "manuals"
CACHE_DIR = ROOT / "manuals" / "cache"


def normalize_command(cmd: str) -> str:
    cmd = (cmd or "").strip().strip('"').lower()
    cmd = re.sub(r"\s+", " ", cmd)
    return cmd


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing CSV: {path}")
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def safe_download(url: str, cache_path: Path, timeout: int = 30) -> str:
    if not url:
        return "no_url"
    try:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=timeout) as resp:
            data = resp.read()
        if len(data) < 500:
            return "download_failed_too_small"
        cache_path.write_bytes(data)
        return "downloaded"
    except Exception as exc:  # noqa: BLE001
        return f"download_failed: {type(exc).__name__}: {exc}"


def main(plan_path: str | None = None, download: bool = False) -> None:
    plan = Path(plan_path) if plan_path else DEFAULT_PLAN
    command_rows = read_csv(plan)
    registry_rows = read_csv(REGISTRY)
    registry = {normalize_command(r["command_or_package"]): r for r in registry_rows}

    out_rows: list[dict[str, str]] = []
    community_commands: list[str] = []
    timestamp = dt.datetime.now(dt.timezone.utc).isoformat()

    for row in command_rows:
        raw_cmd = row.get("command_or_package", "")
        key = normalize_command(raw_cmd)
        # Normalize common variants
        lookup_keys = [key]
        if key.startswith("xtreg"):
            lookup_keys.append("xtreg")
        if key.startswith("estout") or key.startswith("esttab"):
            lookup_keys.append("estout/esttab")
        if key.startswith("reghdfe"):
            lookup_keys.append("reghdfe")
        if key.startswith("ppmlhdfe"):
            lookup_keys.append("ppmlhdfe")

        reg = None
        for lk in lookup_keys:
            if lk in registry:
                reg = registry[lk]
                break

        if reg is None:
            official = row.get("official_or_community", "unknown")
            reg = {
                "official_or_community": official,
                "manual_volume": "unknown",
                "manual_volume_url": "",
                "command_pdf_url": "",
                "manual_title": "unknown",
                "implementation_note": "No registry match; search official Stata Press manual pages and installed help.",
            }

        official_or_community = reg.get("official_or_community", row.get("official_or_community", ""))
        pdf_url = reg.get("command_pdf_url", "")
        local_path = ""
        retrieval_status = "not_downloaded"
        if official_or_community == "community":
            retrieval_status = "community_help_required"
            community_commands.append(raw_cmd)
        elif download and pdf_url:
            filename = pdf_url.rstrip('/').split('/')[-1]
            cache_path = CACHE_DIR / filename
            retrieval_status = safe_download(pdf_url, cache_path)
            local_path = str(cache_path) if cache_path.exists() else ""
        elif pdf_url:
            retrieval_status = "url_mapped"

        out_rows.append({
            "command_or_package": raw_cmd,
            "official_or_community": official_or_community,
            "requested_status": row.get("status", ""),
            "retrieval_status": retrieval_status,
            "manual_volume_url": reg.get("manual_volume_url", ""),
            "command_pdf_url": pdf_url,
            "local_cached_path": local_path,
            "installed_help_status": "pending_stata_check",
            "key_syntax_notes": reg.get("manual_title", ""),
            "postestimation_notes": "review command postestimation manual/help",
            "version_notes": row.get("installation_or_version_note", ""),
            "timestamp": timestamp,
            "reviewed_by_user": "no",
        })

    fieldnames = [
        "command_or_package", "official_or_community", "requested_status", "retrieval_status",
        "manual_volume_url", "command_pdf_url", "local_cached_path", "installed_help_status",
        "key_syntax_notes", "postestimation_notes", "version_notes", "timestamp", "reviewed_by_user"
    ]
    write_csv(OUT_DIR / "manual_retrieval_log.csv", out_rows, fieldnames)

    digest_lines = ["# Stata Manual Digest", "", f"Generated: {timestamp}", "", "## Commands"]
    for r in out_rows:
        digest_lines.append(f"- `{r['command_or_package']}`: {r['retrieval_status']}; source={r['command_pdf_url'] or r['manual_volume_url'] or 'community/installed help'}")
    if community_commands:
        digest_lines.extend(["", "## Community-command help retrieval needed", ""])
        digest_lines.extend([f"- `{cmd}`" for cmd in community_commands])
        digest_lines.append("\nRun the generated Stata script `01_environment_and_manual_checks.do` to check `which`, `help`, and package installation status.")
    (OUT_DIR / "manual_digest.md").write_text("\n".join(digest_lines), encoding="utf-8")
    print(f"Wrote {OUT_DIR / 'manual_retrieval_log.csv'}")


if __name__ == "__main__":
    # Usage: python 00_retrieve_stata_manuals.py [path/to/stata_command_plan.csv] [--download]
    args = sys.argv[1:]
    do_download = "--download" in args
    args = [a for a in args if a != "--download"]
    main(args[0] if args else None, download=do_download)
