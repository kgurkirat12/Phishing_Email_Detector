from flask import Flask, render_template, request
from database import init_db, save_email, get_all_emails,get_statistics

app = Flask(__name__)
init_db()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    subject = request.form["subject"]
    sender = request.form["sender"]
    body = request.form["body"]

    score = 0
    reasons = []

    suspicious_words = [
        "urgent",
        "verify",
        "click",
        "password",
        "bank",
        "account",
        "winner",
        "prize",
        "login",
        "limited",
        "security",
        "confirm",
        "payment",
        "invoice",
        "gift",
        "otp",
        "update"
    ]

    text = (subject + " " + body).lower()

    # Check suspicious words
    for word in suspicious_words:
        if word in text:
            score += 10
            reasons.append(f"Contains suspicious word: {word}")

    # Check links
    if "http://" in body or "https://" in body:
        score += 20
        reasons.append("Contains a suspicious link")

    # Free email providers
    if sender.endswith("@gmail.com") or sender.endswith("@yahoo.com") or sender.endswith("@outlook.com"):
        score += 5
        reasons.append("Uses free email provider")

    # Too many exclamation marks
    if body.count("!") >= 3:
        score += 10
        reasons.append("Too many exclamation marks")

    # Very short email
    if len(body) < 40:
        score += 5
        reasons.append("Very short email")

    # ALL CAPS subject
    if subject.isupper():
        score += 10
        reasons.append("Subject is in ALL CAPS")

    # Limit score
    if score > 100:
        score = 100

    # Risk Level
    if score >= 60:
        risk = "High"
    elif score >= 30:
        risk = "Medium"
    else:
        risk = "Low"

    # Save into database
    save_email(subject, sender, body, score, risk)

    return render_template(
        "result.html",
        score=score,
        risk=risk,
        reasons=reasons
    )


@app.route("/history")
def history():
    emails = get_all_emails()
    return render_template("history.html", emails=emails)
@app.route("/dashboard")
def dashboard():

    total, high, medium, low = get_statistics()

    return render_template(
        "dashboard.html",
        total=total,
        high=high,
        medium=medium,
        low=low
    )


if __name__ == "__main__":
    app.run(debug=True)