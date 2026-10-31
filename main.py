import fastapi
import uvicorn
import sqlite3
import json
from pathlib import Path

print("FastAPI version:", fastapi.__version__)
print("Uvicorn is ready!")

from fastapi import FastAPI

app = FastAPI(title="BrandGuard API")

@app.get("/api/health")
def health_check():
    return {
        "status": "success",
        "message": "BrandGuard backend is working!"
    }

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uvicorn
import threading
import re

app = FastAPI(title="BrandGuard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
# Persistent SQLite database setup
BASE_DIR = Path(__file__).resolve().parent
DB_FILE = BASE_DIR / "brandguard.db"

def init_database():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS app_state (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                data TEXT NOT NULL
            )
        """)
        conn.commit()

init_database()

# Initial data
DB = {
    "products": [
        {
            "id": 1,
            "name": "AquaPure X1 Water Purifier",
            "price": 12999,
            "features": "7-stage RO+UV; 8 L tank; 1-year warranty"
        }
    ],
    "claims": [
        {
            "id": 1,
            "pid": 1,
            "text": "Removes up to 99% of dissolved impurities",
            "proof": "Lab test LT-2025-14"
        },
        {
            "id": 2,
            "pid": 1,
            "text": "1-year warranty on all parts",
            "proof": "Warranty policy v3"
        }
    ],
    "rules": [
        {"id": 1, "kind": "banned", "term": "cheap",
         "rep": "affordable", "note": "Brand voice guide p.4"},
        {"id": 2, "kind": "banned", "term": "best",
         "rep": "", "note": "Claims policy 2.1"},
        {"id": 3, "kind": "banned", "term": "miracle",
         "rep": "", "note": "Claims policy 2.1"},
        {"id": 4, "kind": "preferred", "term": "purifier machine",
         "rep": "water purifier", "note": "Terminology sheet"},
        {"id": 5, "kind": "preferred", "term": "buy",
         "rep": "get", "note": "Brand voice guide p.3"},
    ],
    "subs": [],
    "audit": []
}

COUNTERS = {"products": 2, "claims": 3, "rules": 6, "subs": 1}

# Save application state permanently in SQLite
def save_state():
    state = {
        "DB": DB,
        "COUNTERS": COUNTERS
    }

    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(
            """
            INSERT INTO app_state (id, data)
            VALUES (1, ?)
            ON CONFLICT(id) DO UPDATE SET data = excluded.data
            """,
            (json.dumps(state),)
        )


# Load saved state when the backend starts
def load_state():
    with sqlite3.connect(DB_FILE) as conn:
        row = conn.execute(
            "SELECT data FROM app_state WHERE id = 1"
        ).fetchone()

    if row:
        saved_state = json.loads(row[0])
        DB.update(saved_state["DB"])
        COUNTERS.update(saved_state["COUNTERS"])


load_state()

def log_action(user, action, detail):
    DB["audit"].insert(0, {
        "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "u": user,
        "a": action,
        "d": detail
    })
    save_state()


@app.get("/")
def home():
    return {"message": "BrandGuard API is running"}


@app.get("/api/health")
def health():
    return {"status": "success", "message": "BrandGuard backend is working!"}


@app.get("/api/state")
def get_state():
    return {
        "products": DB["products"],
        "claims": DB["claims"],
        "rules": DB["rules"],
        "subs": DB["subs"],
        "audit": DB["audit"]
    }


class ReviewRequest(BaseModel):
    text: str
    pid: Optional[int] = 1
    fg: Optional[str] = "#222222"
    bg: Optional[str] = "#ffffff"
    img: Optional[bool] = False
    alt: Optional[str] = ""


@app.post("/api/review")
def review(data: ReviewRequest):
    text = data.text
    findings = []

    def add(category, issue, why, source, severity, confidence, suggestion, span=None, origin="Rule"):
        findings.append({
            "c": category,
            "i": issue,
            "w": why,
            "s": source,
            "sv": severity,
            "cf": confidence,
            "sg": suggestion,
            "r": span,
            "o": origin
        })

    for rule in DB["rules"]:
        term = rule["term"].strip()
        if not term:
            continue

        for match in re.finditer(re.escape(term), text, re.IGNORECASE):
            if rule["kind"] == "banned":
                add(
                    "Tone rule",
                    f"Potentially banned term: {match.group()}",
                    "This term may not follow the approved brand voice.",
                    rule.get("note", "Brand rules"),
                    "medium",
                    0.95,
                    f"Consider using '{rule['rep']}' instead." if rule.get("rep")
                    else "Remove or rewrite this term.",
                    [match.start(), match.end()]
                )
            elif rule["kind"] == "preferred":
                add(
                    "Terminology",
                    f"Use preferred wording: {match.group()}",
                    "The brand guide recommends consistent terminology.",
                    rule.get("note", "Brand rules"),
                    "low",
                    0.95,
                    f"Use '{rule['rep']}' instead.",
                    [match.start(), match.end()]
                )

    # Flag claims that are not present in the approved knowledge base.
    approved_claims = [
        c["text"].lower()
        for c in DB["claims"]
        if c["pid"] == data.pid
    ]

    if re.search(r"\b100%\s*guaranteed\b|\bguaranteed pure\b", text, re.I):
        add(
            "Claim",
            "Potential unsupported guarantee",
            "This guarantee needs evidence from an approved source.",
            "Approved claims in Knowledge Base",
            "high",
            0.90,
            "Remove the guarantee unless it can be verified."
        )

    if data.img and not data.alt.strip():
        add(
            "Accessibility",
            "Image has no alt text",
            "Screen-reader users may not understand the image.",
            "Accessibility guideline",
            "medium",
            0.99,
            "Add a short description of the image."
        )

    findings.sort(key=lambda x: {"high": 0, "medium": 1, "low": 2}[x["sv"]])
    return findings


class SubmissionRequest(BaseModel):
    title: Optional[str] = "Untitled"
    pid: int = 1
    text: str
    fg: Optional[str] = "#222222"
    bg: Optional[str] = "#ffffff"
    img: Optional[bool] = False
    alt: Optional[str] = ""
    dec: Optional[dict] = {}
    rev: Optional[int] = None


@app.post("/api/submissions")
def create_submission(data: SubmissionRequest, x_role: str = "Employee", x_user: str = "Asha"):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if data.rev:
        existing = next((s for s in DB["subs"] if s["id"] == data.rev), None)
        if existing is None:
            raise HTTPException(status_code=404, detail="Submission not found")

        version_number = len(existing["v"]) + 1
        existing["v"].append({
            "n": version_number,
            "text": data.text,
            "ts": now,
            "dec": data.dec or {}
        })
        existing["status"] = "Pending"
        existing["comment"] = ""
        submission = existing
    else:
        submission_id = COUNTERS["subs"]
        COUNTERS["subs"] += 1

        submission = {
            "id": submission_id,
            "title": data.title or "Untitled",
            "pid": data.pid,
            "status": "Pending",
            "creator": x_user,
            "role": x_role,
            "created": now,
            "comment": "",
            "v": [{
                "n": 1,
                "text": data.text,
                "ts": now,
                "dec": data.dec or {}
            }]
        }
        DB["subs"].insert(0, submission)

    log_action(x_user, "Submission created/updated", submission["title"])
    return {"status": "success", "submission": submission}


class DecisionRequest(BaseModel):
    status: str
    comment: Optional[str] = ""


@app.post("/api/submissions/{submission_id}/decision")
def decide_submission(
    submission_id: int,
    data: DecisionRequest,
    x_role: str = "Manager",
    x_user: str = "Tarun"
):
    submission = next(
        (s for s in DB["subs"] if s["id"] == submission_id),
        None
    )

    if submission is None:
        raise HTTPException(status_code=404, detail="Submission not found")

    if data.status not in ["Approved", "Changes", "Rejected"]:
        raise HTTPException(status_code=400, detail="Invalid decision")

    submission["status"] = data.status
    submission["comment"] = data.comment or ""

    log_action(x_user, data.status, submission["title"])
    save_state()
    
    return {"status": "success", "submission": submission}


# Knowledge Base: products, claims and rules
class ProductRequest(BaseModel):
    name: str
    price: float = 0
    features: str = ""


class ClaimRequest(BaseModel):
    pid: int = 1
    text: str
    proof: str = ""


class RuleRequest(BaseModel):
    kind: str
    term: str
    rep: str = ""
    note: str = ""


@app.post("/api/products")
def add_product(data: ProductRequest, x_user: str = "Tarun"):
    item = {"id": COUNTERS["products"], **data.model_dump()}
    COUNTERS["products"] += 1
    DB["products"].append(item)
    log_action(x_user, "Product added", item["name"])
    save_state()
    return item


@app.post("/api/claims")
def add_claim(data: ClaimRequest, x_user: str = "Tarun"):
    item = {"id": COUNTERS["claims"], **data.model_dump()}
    COUNTERS["claims"] += 1
    DB["claims"].append(item)
    log_action(x_user, "Claim added", item["text"])
    save_state()
    return item


@app.post("/api/rules")
def add_rule(data: RuleRequest, x_user: str = "Tarun"):
    if data.kind not in ["banned", "preferred"]:
        raise HTTPException(status_code=400, detail="Invalid rule kind")

    item = {"id": COUNTERS["rules"], **data.model_dump()}
    COUNTERS["rules"] += 1
    DB["rules"].append(item)
    log_action(x_user, "Rule added", item["term"])
    save_state()
    return item


@app.delete("/api/{kind}/{item_id}")
def delete_item(kind: str, item_id: int, x_user: str = "Tarun"):
    if kind not in ["products", "claims", "rules"]:
        raise HTTPException(status_code=400, detail="Invalid item type")

    item = next((x for x in DB[kind] if x["id"] == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    DB[kind].remove(item)
    log_action(x_user, f"{kind[:-1].title()} deleted", str(item_id))
    save_state()
    return {"status": "success", "deleted_id": item_id}
