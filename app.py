from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "mysecretkey"

USERS_FILE = "users.json"

# Ensure JSON file exists
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump([], f)

# Load users
def load_users():
    with open(USERS_FILE, "r") as f:
        return json.load(f)

# Save users
def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

# Home page (redirect to login if not logged in)
@app.route("/")
def home():
    if "user" in session:
        return f"Hello, {session['user']['name']}! <a href='/logout'>Logout</a>"
    return redirect(url_for("login"))

# Signup
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        users = load_users()
        if any(u["email"] == email for u in users):
            return "Email already registered! <a href='/signup'>Try again</a>"

        hashed_pw = generate_password_hash(password)
        users.append({"name": name, "email": email, "password": hashed_pw})
        save_users(users)
        return redirect(url_for("login"))

    return render_template("signup.html")

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        users = load_users()
        user = next((u for u in users if u["email"] == email), None)
        if user and check_password_hash(user["password"], password):
            session["user"] = {"name": user["name"], "email": user["email"]}
            return redirect(url_for("home"))
        return "Invalid email or password! <a href='/login'>Try again</a>"

    return render_template("login.html")

# Logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
