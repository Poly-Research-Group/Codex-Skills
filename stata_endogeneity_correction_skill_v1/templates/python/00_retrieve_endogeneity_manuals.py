"""
Retrieve or audit Stata manual/help sources for endogeneity-related commands.

This script does not redistribute manuals. It maps commands to official Stata Press/Stata manual URLs
and optionally checks URL availability if internet access is available.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "templates" / "metadata" / "stata_endogeneity_command_registry.csv"
OUTDIR = ROOT / "output" / "endogeneity"
OUTDIR.mkdir(parents=True, exist_ok=True)
OUTFILE = OUTDIR / "manual_retrieval_log.csv"

# Optional command plan path can be provided as first argument.
COMMAND_PLAN = Path(sys.argv[1]) if len(sys.argv) > 1 else None

# Minimal URL hints for official command PDFs. These should be verified against Stata Press TOC pages.
URL_HINTS = {
    "regress": "https://www.stata.com/manuals/rregress.pdf",
    "xtreg, fe": "https://www.stata.com/manuals/xtxtreg.pdf",
    "xtreg": "https://www.stata.com/manuals/xtxtreg.pdf",
    "areg": "https://www.stata.com/manuals/rareg.pdf",
    "ivregress 2sls": "https://www.stata.com/manuals/rivregress.pdf",
    "ivregress": "https://www.stata.com/manuals/rivregress.pdf",
    "ivregress postestimation": "https://www.stata.com/manuals/rivregresspostestimation.pdf",
    "xtivreg": "https://www.stata.com/manuals/xtxtivreg.pdf",
    "cfregress": "https://www.stata.com/manuals/rcfregress.pdf",
    "cfprobit": "https://www.stata.com/manuals/rcfprobit.pdf",
    "etregress": "https://www.stata.com/manuals/causaletregress.pdf",
    "didregress": "https://www.stata.com/manuals/causaldidregress.pdf",
    "xtdidregress": "https://www.stata.com/manuals/causaldidregress.pdf",
    "didregress postestimation": "https://www.stata.com/manuals/causaldidregresspostestimation.pdf",
    "teffects psmatch": "https://www.stata.com/manuals/causalteffectspsmatch.pdf",
    "teffects ipw": "https://www.stata.com/manuals/causalteffectsipw.pdf",
    "teffects ipwra": "https://www.stata.com/manuals/causalteffectsipwra.pdf",
    "teffects aipw": "https://www.stata.com/manuals/causalteffectsaipw.pdf",
    "tebalance": "https://www.stata.com/manuals/causaltebalance.pdf",
    "xtabond": "https://www.stata.com/manuals/xtxtabond.pdf",
    "xtabond postestimation": "https://www.stata.com/manuals/xtxtabondpostestimation.pdf",
    "xtdpdsys": "https://www.stata.com/manuals/xtxtdpdsys.pdf",
    "xtdpdsys postestimation": "https://www.stata.com/manuals/xtxtdpdsyspostestimation.pdf",
    "heckman": "https://www.stata.com/manuals/rheckman.pdf",
    "eivreg": "https://www.stata.com/manuals/reivreg.pdf",
    "margins": "https://www.stata.com/manuals/rmargins.pdf",
    "etable": "https://www.stata.com/manuals/retable.pdf",
}


def normalize(cmd: str) -> str:
    cmd = (cmd or "").strip().lower()
    return cmd


def url_status(url: str) -> str:
    if not url or not url.startswith("http"):
        return "not_checked"
    try:
        req = Request(url, method="HEAD", headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=10) as resp:
            return f"ok_{resp.status}"
    except HTTPError as exc:
        return f"http_{exc.code}"
    except URLError as exc:
        return f"url_error_{exc.reason}"
    except Exception as exc:  # pragma: no cover
        return f"error_{type(exc).__name__}"


def read_registry():
    rows = []
    with REGISTRY.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows.append(row)
    return rows


def read_commands_from_plan(path: Path):
    if not path or not path.exists():
        return []
    cmds = []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cmd = row.get("command_or_package") or row.get("command") or row.get("stata_command") or ""
            if cmd.strip():
                cmds.append(cmd.strip())
    return cmds

registry = read_registry()
registry_by_command = {normalize(r["command"]): r for r in registry}
commands = read_commands_from_plan(COMMAND_PLAN) if COMMAND_PLAN else [r["command"] for r in registry]

out_rows = []
for cmd in commands:
    ncmd = normalize(cmd)
    matched = registry_by_command.get(ncmd)
    # allow prefix matching for commands with options
    if matched is None:
        for key, row in registry_by_command.items():
            if ncmd.startswith(key) or key.startswith(ncmd):
                matched = row
                break
    official = matched.get("official_or_community") if matched else "unknown"
    source = matched.get("manual_or_help_source") if matched else "not_in_registry"
    url = URL_HINTS.get(ncmd, "")
    if not url:
        for key, val in URL_HINTS.items():
            if ncmd.startswith(key) or key.startswith(ncmd):
                url = val
                break
    status = url_status(url) if url else "manual_url_not_mapped"
    out_rows.append({
        "command": cmd,
        "official_or_community": official,
        "manual_or_help_source": source,
        "url_hint": url,
        "url_status": status,
        "action_required": "verify installed help for community command" if official == "community" else "verify against Stata version",
    })

with OUTFILE.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()) if out_rows else ["command"])
    writer.writeheader()
    writer.writerows(out_rows)

print(f"Wrote {OUTFILE}")
