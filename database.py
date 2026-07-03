import sqlite3


def init_db():
    conn = sqlite3.connect("emails.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS emails(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT,
        sender TEXT,
        body TEXT,
        score INTEGER,
        risk TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_email(subject, sender, body, score, risk):
    conn = sqlite3.connect("emails.db")
    c = conn.cursor()

    c.execute("""
    INSERT INTO emails(subject, sender, body, score, risk)
    VALUES (?, ?, ?, ?, ?)
    """, (subject, sender, body, score, risk))

    conn.commit()
    conn.close()


def get_all_emails():
    conn = sqlite3.connect("emails.db")
    c = conn.cursor()

    c.execute("SELECT * FROM emails ORDER BY id DESC")

    emails = c.fetchall()

    conn.close()

    return emails


def get_statistics():
    conn = sqlite3.connect("emails.db")
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM emails")
    total = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM emails WHERE risk='High'")
    high = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM emails WHERE risk='Medium'")
    medium = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM emails WHERE risk='Low'")
    low = c.fetchone()[0]

    conn.close()

    return total, high, medium, low