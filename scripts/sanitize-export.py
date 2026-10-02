"""Replace real identifiers in an exported n8n workflow JSON with placeholders.

Usage:
    python scripts/sanitize-export.py path/to/export.json [more.json ...]
    python scripts/sanitize-export.py --dry-run path/to/export.json
    python scripts/sanitize-export.py --no-check path/to/export.json

Rewrites each file in place, then runs scripts/check-sanitized.py over the whole
repo and exits with its code (0 = clean). The patterns are shared with the
checker, so the two cannot drift apart. Values that already start with "your-"
are left alone, so running it twice changes nothing.

Placeholders: your-<type>-credential-id, your-webhook-id, your-workflow-id,
your-spreadsheet-id, your-email@example.com, versionId "placeholder",
meta.instanceId removed.

Output is formatted like n8n's own export (2-space indent, expanded arrays). A
file that was written in another style (compact arrays) is reformatted once;
the content stays identical.

Not handled, review by hand: pinData (printed as a warning), real names or
addresses inside free text, and anything a regex cannot recognise.
"""
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("check_sanitized", HERE / "check-sanitized.py")
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)

SECRET_KEYS = {"apikey", "api_key", "token", "accesstoken", "refreshtoken", "password", "clientsecret"}
PLACEHOLDER_MAIL = "your-email@example.com"
PLACEHOLDER_HOST = "your-n8n-instance.example.com"
PLACEHOLDER_SECRET = "your-secret-removed"
PLACEHOLDER_SHEET_URL = "docs.google.com/spreadsheets/d/your-spreadsheet-id"


def slug(credential_type):
    """googleSheetsOAuth2Api -> google-sheets, gmailOAuth2 -> gmail-o-auth2."""
    s = re.sub(r"(OAuth2Api|Api)$", "", credential_type)
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", s)
    s = re.sub(r"([A-Z])([A-Z][a-z])", r"\1-\2", s)
    return s.lower()


class Counter(dict):
    def hit(self, label):
        self[label] = self.get(label, 0) + 1


def clean_string(s, stats):
    def mail(m):
        if m.group(1).lower() in check.FAKE_MAIL_DOMAINS:
            return m.group(0)
        stats.hit("email")
        return PLACEHOLDER_MAIL

    s = check.MAIL.sub(mail, s)
    s, n = check.SHEET_URL.subn(PLACEHOLDER_SHEET_URL, s)
    stats["sheet url"] = stats.get("sheet url", 0) + n
    s, n = check.HOST.subn(PLACEHOLDER_HOST, s)
    stats["hostname"] = stats.get("hostname", 0) + n
    s, n = check.KEYS.subn(PLACEHOLDER_SECRET, s)
    stats["KEY/TOKEN"] = stats.get("KEY/TOKEN", 0) + n
    return s


def clean(obj, stats):
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if k == "credentials" and isinstance(v, dict):
                out[k] = {}
                for ctype, c in v.items():
                    if isinstance(c, dict) and not str(c.get("id", "")).startswith("your-"):
                        c = {**c, "id": f"your-{slug(ctype)}-credential-id"}
                        stats.hit("credential id")
                    out[k][ctype] = c
            elif k == "webhookId" and v != "your-webhook-id":
                out[k] = "your-webhook-id"
                stats.hit("webhook id")
            elif k in ("documentId", "spreadsheetId") and isinstance(v, dict):
                v = clean(v, stats)
                if str(v.get("value", "")) and not str(v["value"]).startswith("your-"):
                    v = {**v, "value": "your-spreadsheet-id"}
                    stats.hit("spreadsheet id")
                out[k] = v
            elif isinstance(v, str) and k.lower() in SECRET_KEYS and len(v) >= 6 and not v.startswith("your-"):
                out[k] = PLACEHOLDER_SECRET
                stats.hit("KEY/TOKEN")
            else:
                out[k] = clean(v, stats)
        return out
    if isinstance(obj, list):
        return [clean(i, stats) for i in obj]
    if isinstance(obj, str):
        return clean_string(obj, stats)
    return obj


def sanitize(data, stats):
    data = clean(data, stats)
    if isinstance(data, dict):
        if data.get("id") not in (None, "your-workflow-id"):
            data["id"] = "your-workflow-id"
            stats.hit("workflow id")
        for key in ("versionId", "activeVersionId"):
            if data.get(key) not in (None, "placeholder"):
                data[key] = "placeholder"
                stats.hit(key)
        meta = data.get("meta")
        if isinstance(meta, dict) and "instanceId" in meta:
            del meta["instanceId"]
            stats.hit("instanceId")
        if data.get("pinData"):
            print("  WARNING: pinData is not empty, review it by hand")
    return data


def main(argv):
    dry = "--dry-run" in argv
    skip_check = "--no-check" in argv
    files = [a for a in argv if not a.startswith("--")]
    if not files:
        print(__doc__)
        return 2
    for name in files:
        path = Path(name)
        raw = path.read_text(encoding="utf-8")
        stats = Counter()
        data = sanitize(json.loads(raw), stats)
        changed = {k: v for k, v in stats.items() if v}
        print(f"{path}: {changed if changed else 'nothing to replace'}")
        if "KEY/TOKEN" in changed:
            print("  WARNING: a key or token was present in this export, rotate it")
        if dry:
            continue
        indent = "\t" if "\n\t" in raw[:200] else 2
        path.write_text(json.dumps(data, indent=indent, ensure_ascii=False) + "\n", encoding="utf-8")
    if dry or skip_check:
        return 0
    return subprocess.call([sys.executable, str(HERE / "check-sanitized.py")])


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
