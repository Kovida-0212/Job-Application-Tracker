from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import date

app = Flask(__name__)
app.secret_key = "job-tracker-secret-key"
DATABASE = "job_tracker.db"

STATUSES = ["Applied", "Assessment", "Interview", "Selected", "Rejected"]

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            role TEXT NOT NULL,
            application_date TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Applied',
            interview_date TEXT,
            resume_version TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def dashboard():
    conn = get_db()
    total = conn.execute("SELECT COUNT(*) FROM applications").fetchone()[0]
    counts = {
        status: conn.execute(
            "SELECT COUNT(*) FROM applications WHERE status = ?", (status,)
        ).fetchone()[0]
        for status in STATUSES
    }
    recent = conn.execute(
        "SELECT * FROM applications ORDER BY application_date DESC, id DESC LIMIT 5"
    ).fetchall()
    conn.close()

    return render_template(
        "dashboard.html",
        total=total,
        counts=counts,
        recent=recent,
        statuses=STATUSES
    )

@app.route("/applications")
def applications():
    search = request.args.get("search", "").strip()
    status = request.args.get("status", "").strip()

    query = "SELECT * FROM applications WHERE 1=1"
    params = []

    if search:
        query += " AND (company LIKE ? OR role LIKE ? OR notes LIKE ?)"
        like = f"%{search}%"
        params.extend([like, like, like])

    if status in STATUSES:
        query += " AND status = ?"
        params.append(status)

    query += " ORDER BY application_date DESC, id DESC"

    conn = get_db()
    rows = conn.execute(query, params).fetchall()
    conn.close()

    return render_template(
        "applications.html",
        applications=rows,
        search=search,
        selected_status=status,
        statuses=STATUSES
    )

@app.route("/add", methods=["GET", "POST"])
def add_application():
    if request.method == "POST":
        company = request.form.get("company", "").strip()
        role = request.form.get("role", "").strip()
        application_date = request.form.get("application_date", "").strip()
        status = request.form.get("status", "Applied")
        interview_date = request.form.get("interview_date", "").strip()
        resume_version = request.form.get("resume_version", "").strip()
        notes = request.form.get("notes", "").strip()

        if not company or not role or not application_date:
            flash("Company, job role, and application date are required.", "danger")
            return render_template("add_application.html", statuses=STATUSES)

        if status not in STATUSES:
            status = "Applied"

        conn = get_db()
        conn.execute("""
            INSERT INTO applications
            (company, role, application_date, status, interview_date, resume_version, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (company, role, application_date, status, interview_date or None,
              resume_version, notes))
        conn.commit()
        conn.close()

        flash("Application added successfully!", "success")
        return redirect(url_for("applications"))

    return render_template(
        "add_application.html",
        statuses=STATUSES,
        today=date.today().isoformat()
    )

@app.route("/view/<int:application_id>")
def view_application(application_id):
    conn = get_db()
    application = conn.execute(
        "SELECT * FROM applications WHERE id = ?", (application_id,)
    ).fetchone()
    conn.close()

    if not application:
        flash("Application not found.", "danger")
        return redirect(url_for("applications"))

    return render_template("view_application.html", application=application)

@app.route("/edit/<int:application_id>", methods=["GET", "POST"])
def edit_application(application_id):
    conn = get_db()
    application = conn.execute(
        "SELECT * FROM applications WHERE id = ?", (application_id,)
    ).fetchone()

    if not application:
        conn.close()
        flash("Application not found.", "danger")
        return redirect(url_for("applications"))

    if request.method == "POST":
        company = request.form.get("company", "").strip()
        role = request.form.get("role", "").strip()
        application_date = request.form.get("application_date", "").strip()
        status = request.form.get("status", "Applied")
        interview_date = request.form.get("interview_date", "").strip()
        resume_version = request.form.get("resume_version", "").strip()
        notes = request.form.get("notes", "").strip()

        if not company or not role or not application_date:
            flash("Company, job role, and application date are required.", "danger")
            conn.close()
            return render_template(
                "edit_application.html",
                application=application,
                statuses=STATUSES
            )

        conn.execute("""
            UPDATE applications
            SET company=?, role=?, application_date=?, status=?,
                interview_date=?, resume_version=?, notes=?
            WHERE id=?
        """, (company, role, application_date, status,
              interview_date or None, resume_version, notes, application_id))
        conn.commit()
        conn.close()

        flash("Application updated successfully!", "success")
        return redirect(url_for("view_application", application_id=application_id))

    conn.close()
    return render_template(
        "edit_application.html",
        application=application,
        statuses=STATUSES
    )

@app.route("/delete/<int:application_id>", methods=["POST"])
def delete_application(application_id):
    conn = get_db()
    conn.execute("DELETE FROM applications WHERE id = ?", (application_id,))
    conn.commit()
    conn.close()

    flash("Application deleted.", "success")
    return redirect(url_for("applications"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
