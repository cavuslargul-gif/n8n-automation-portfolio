"""Fail if any workflow export or README in the repo still contains real identifiers.

Run from anywhere:  python scripts/check-sanitized.py
Exit code 0 = clean, 1 = findings (printed with file and line).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FAKE_MAIL_DOMAINS = {"example.com", "beispielbetrieb.de", "test.de"}

MAIL = re.compile(r"[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Za-z]{2,})")
KEYS = re.compile(
    r"gsk_[A-Za-z0-9]{10,}|sk-[A-Za-z0-9_-]{16,}|AIza[0-9A-Za-z_-]{20,}|xox[bp]-[A-Za-z0-9-]+"
    r"|ghp_[A-Za-z0-9]{20,}|secret_[A-Za-z0-9]{10,}|Bearer\s+[A-Za-z0-9._-]{20,}"
)
SECRET_FIELD = re.compile(r'"(apiKey|api_key|token|accessToken|refreshToken|password|clientSecret)"\s*:\s*"[^"]{6,}"', re.I)
INSTANCE = re.compile(r'"instanceId"')
HOST = re.compile(r"hstgr\.cloud|\.app\.n8n\.cloud")
SHEET_URL = re.compile(r"docs\.google\.com/spreadsheets/d/(?!your-)[A-Za-z0-9_-]{20,}")


def line_of(text, pos):
    return text.count("\n", 0, pos) + 1


def check_text(path, text, findings):
    for m in MAIL.finditer(text):
        if m.group(1).lower() not in FAKE_MAIL_DOMAINS:
            findings.append((path, line_of(text, m.start()), f"real-looking email: {m.group(0)}"))
    for rx, label in ((KEYS, "key/token pattern"), (SECRET_FIELD, "secret field with value"),
                      (INSTANCE, "instanceId"), (HOST, "instance hostname"), (SHEET_URL, "sheet URL with real id")):
        for m in rx.finditer(text):
            findings.append((path, line_of(text, m.start()), f"{label}: {m.group(0)[:40]}"))


def walk(obj, path, findings, text):
    """Structural checks on parsed workflow JSON."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "credentials" and isinstance(v, dict):
                for ctype, c in v.items():
                    cid = c.get("id", "") if isinstance(c, dict) else ""
                    if not str(cid).startswith("your-"):
                        findings.append((path, 0, f"credential id not a placeholder ({ctype}): {cid}"))
            elif k == "webhookId" and v != "your-webhook-id":
                findings.append((path, 0, f"webhookId not a placeholder: {v}"))
            elif k in ("documentId", "spreadsheetId") and isinstance(v, dict) and str(v.get("value", "")) not in ("", ) and not str(v.get("value")).startswith("your-"):
                findings.append((path, 0, f"{k} not a placeholder: {v.get('value')}"))
            else:
                walk(v, path, findings, text)
    elif isinstance(obj, list):
        for i in obj:
            walk(i, path, findings, text)


def main():
    findings = []
    files = [p for p in ROOT.rglob("*") if p.suffix in (".json", ".md") and ".git" not in p.parts]
    for p in files:
        rel = p.relative_to(ROOT).as_posix()
        text = p.read_text(encoding="utf-8")
        check_text(rel, text, findings)
        if p.suffix == ".json":
            try:
                data = json.loads(text)
            except json.JSONDecodeError as e:
                findings.append((rel, e.lineno, f"invalid JSON: {e.msg}"))
                continue
            walk(data, rel, findings, text)
            if isinstance(data, dict):
                if data.get("id") not in (None, "your-workflow-id"):
                    findings.append((rel, 0, f"workflow id not a placeholder: {data.get('id')}"))
                if data.get("versionId") not in (None, "placeholder"):
                    findings.append((rel, 0, f"versionId not a placeholder: {data.get('versionId')}"))
    for path, line, msg in findings:
        print(f"{path}:{line or '-'}  {msg}")
    print(f"\n{len(files)} files checked, {len(findings)} finding(s)")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
