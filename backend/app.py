from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

DB = "database.db"

def connect_db():
    return sqlite3.connect(DB)


@app.route("/tasks", methods=["GET"])
def get_tasks():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    conn.close()

    tasks = []
    for row in rows:
        tasks.append({
    "id": row[0],
    "name": row[1],
    "description": row[2],
    "done": bool(row[3]),
    "priority": row[4]
})
    return jsonify(tasks)


@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.json

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
    "INSERT INTO tasks (name, description, done, priority) VALUES (?, ?, ?, ?)",
    (data["name"], data["description"], 0, data["priority"])
)

    conn.commit()
    conn.close()

    return jsonify({"message": "Task added"})


@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return jsonify({"message": "Deleted"})


if __name__ == "__main__":
    app.run(debug=True)