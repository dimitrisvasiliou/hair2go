# app.py
from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

app = Flask(__name__)
app.secret_key = "hair2go_secret_key"  # change in production
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Hard‑coded users (Sonia & Pavlos)
USERS = {
    "sonia@example.com": {
        "name": "Sonia",
        "password": "sonia123",
        "role": "staff"
    },
    "pavlos@example.com": {
        "name": "Pavlos",
        "password": "pavlos123",
        "role": "staff"
    }
}


@app.route("/")
def index():
    if "user_email" not in session:
        return redirect(url_for("login"))
    return render_template("calendar.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = USERS.get(email)
        if user and user["password"] == password:
            session["user_email"] = email
            session["user_name"] = user["name"]
            session["user_role"] = user["role"]
            return redirect(url_for("index"))
        return "Invalid email or password", 401

    return """
    <h1>HAIR2GO — Login</h1>
    <form method="POST">
      <label>Email:</label><br/>
      <input type="email" name="email" required><br/>
      <label>Password:</label><br/>
      <input type="password" name="password" required><br/>
      <button type="submit">Login</button>
    </form>
    """


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/api/appointments", methods=["GET"])
def get_appointments():
    if "user_email" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    date = request.args.get("date")
    if not date:
        return jsonify({"error": "Missing date (YYYY-MM-DD)"}), 400

    res = supabase.table("hair2go_appointments").select("*").eq("date", date).execute()
    appointments = res.data or []

    return jsonify({"appointments": appointments})


@app.route("/api/appointments", methods=["POST"])
def add_appointment():
    if "user_email" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    required = ["date", "time_from", "time_to", "client_name"]
    for key in required:
        if not data.get(key):
            return jsonify({"error": f"Missing {key}"}), 400

    barber = session["user_name"]
    if barber not in ["Sonia", "Pavlos"]:
        return jsonify({"error": "Invalid user"}), 400

    new_row = {
        "date": data["date"],
        "time_from": data["time_from"],
        "time_to": data["time_to"],
        "client_name": data["client_name"],
        "barber": barber,
    }

    res = supabase.table("hair2go_appointments").insert(new_row).execute()
    if not res.data:
        return jsonify({"error": "Insert failed"}), 500

    return jsonify({"success": True, "id": res.data[0]["id"]})


@app.route("/api/appointments/<uuid:id>", methods=["PATCH"])
def update_appointment(id):
    if "user_email" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    if "time_from" in data and "time_to" in data:
        res = supabase.table("hair2go_appointments").update({
            "time_from": data["time_from"],
            "time_to": data["time_to"],
        }).eq("id", id).execute()
        if not res.data:
            return jsonify({"error": "Update failed"}), 500

    return jsonify({"success": True})