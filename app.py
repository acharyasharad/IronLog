from flask import Flask, jsonify, request, render_template
import sqlite3
from datetime import date

app = Flask(__name__)
DB = "workouts.db"

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.executescript("""
            CREATE TABLE IF NOT EXISTS workouts (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                name       TEXT NOT NULL,
                date       DATE DEFAULT CURRENT_DATE,
                notes      TEXT DEFAULT ''
            );
            CREATE TABLE IF NOT EXISTS exercises (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                workout_id INTEGER NOT NULL,
                name       TEXT NOT NULL,
                sets       INTEGER NOT NULL,
                reps       INTEGER NOT NULL,
                weight     REAL DEFAULT 0,
                unit       TEXT DEFAULT 'kg',
                FOREIGN KEY (workout_id) REFERENCES workouts(id)
            );
        """)

init_db()

@app.route("/")
def index():
    return render_template("index.html")

# ── Workouts ──────────────────────────────────────────────────────────────────
@app.route("/api/workouts", methods=["GET"])
def get_workouts():
    db = get_db()
    workouts = db.execute("SELECT * FROM workouts ORDER BY date DESC, id DESC").fetchall()
    result = []
    for w in workouts:
        exercises = db.execute(
            "SELECT * FROM exercises WHERE workout_id=?", (w["id"],)
        ).fetchall()
        result.append({
            "id": w["id"], "name": w["name"],
            "date": w["date"], "notes": w["notes"],
            "exercises": [dict(e) for e in exercises],
        })
    return jsonify(result)

@app.route("/api/workouts", methods=["POST"])
def create_workout():
    data = request.json
    if not data.get("name"):
        return jsonify({"error": "Workout name required"}), 400
    db = get_db()
    cur = db.execute(
        "INSERT INTO workouts (name, date, notes) VALUES (?,?,?)",
        (data["name"], data.get("date", date.today().isoformat()), data.get("notes", ""))
    )
    db.commit()
    return jsonify({"id": cur.lastrowid}), 201

@app.route("/api/workouts/<int:wid>", methods=["DELETE"])
def delete_workout(wid):
    db = get_db()
    db.execute("DELETE FROM exercises WHERE workout_id=?", (wid,))
    db.execute("DELETE FROM workouts WHERE id=?", (wid,))
    db.commit()
    return jsonify({"deleted": True})

# ── Exercises ─────────────────────────────────────────────────────────────────
@app.route("/api/workouts/<int:wid>/exercises", methods=["POST"])
def add_exercise(wid):
    data = request.json
    if not all([data.get("name"), data.get("sets"), data.get("reps")]):
        return jsonify({"error": "Name, sets and reps required"}), 400
    db = get_db()
    cur = db.execute(
        "INSERT INTO exercises (workout_id, name, sets, reps, weight, unit) VALUES (?,?,?,?,?,?)",
        (wid, data["name"], data["sets"], data["reps"],
         data.get("weight", 0), data.get("unit", "kg"))
    )
    db.commit()
    return jsonify({"id": cur.lastrowid}), 201

@app.route("/api/exercises/<int:eid>", methods=["DELETE"])
def delete_exercise(eid):
    db = get_db()
    db.execute("DELETE FROM exercises WHERE id=?", (eid,))
    db.commit()
    return jsonify({"deleted": True})

# ── Personal bests ────────────────────────────────────────────────────────────
@app.route("/api/pbs")
def personal_bests():
    db = get_db()
    rows = db.execute("""
        SELECT e.name, MAX(e.weight) as max_weight, e.unit,
               MAX(e.sets * e.reps) as max_volume
        FROM exercises e
        GROUP BY LOWER(e.name)
        ORDER BY max_weight DESC
    """).fetchall()
    return jsonify([dict(r) for r in rows])

# ── Stats ─────────────────────────────────────────────────────────────────────
@app.route("/api/stats")
def stats():
    db = get_db()
    total_workouts = db.execute("SELECT COUNT(*) as c FROM workouts").fetchone()["c"]
    total_sets = db.execute("SELECT SUM(sets) as c FROM exercises").fetchone()["c"] or 0
    total_reps = db.execute("SELECT SUM(sets * reps) as c FROM exercises").fetchone()["c"] or 0
    total_weight = db.execute("SELECT SUM(sets * reps * weight) as c FROM exercises").fetchone()["c"] or 0
    return jsonify({
        "total_workouts": total_workouts,
        "total_sets":     int(total_sets),
        "total_reps":     int(total_reps),
        "total_weight_kg": round(total_weight, 1),
    })

if __name__ == "__main__":
    app.run(debug=True, port=8083)
