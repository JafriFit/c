from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any
import json

from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__, static_folder="static", static_url_path="")

MESSAGES_FILE = Path("data/messages.json")
MESSAGES_FILE.parent.mkdir(parents=True, exist_ok=True)


def _load_messages() -> list[dict[str, Any]]:
    if not MESSAGES_FILE.exists():
        return []
    try:
        return json.loads(MESSAGES_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []


def _save_messages(entries: list[dict[str, Any]]) -> None:
    MESSAGES_FILE.write_text(
        json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8"
    )


@app.route("/")
def index() -> Any:
    return send_from_directory(app.static_folder, "index.html")


@app.post("/api/contact")
def contact() -> Any:
    payload = request.get_json(force=True, silent=True) or {}
    name = (payload.get("name") or "").strip()
    email = (payload.get("email") or "").strip()
    message = (payload.get("message") or "").strip()

    if not name or not email or not message:
        return jsonify({"error": "Please provide name, email, and message."}), 400

    new_entry = {
        "name": name,
        "email": email,
        "message": message,
        "received_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
    }

    existing = _load_messages()
    existing.append(new_entry)
    _save_messages(existing)

    return jsonify({"status": "ok", "received": new_entry}), 201


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
