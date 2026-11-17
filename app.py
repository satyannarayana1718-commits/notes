
from flask import Flask, render_template_string, request, jsonify
import sqlite3

app = Flask(__name__)

# Database connection
def get_db():
    conn = sqlite3.connect("notes.db")
    conn.row_factory = sqlite3.Row
    return conn

# Create database table
with get_db() as db:
    db.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)

# Main page
@app.route("/")
def home():
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quick Notes</title>

    <style>
       
        
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: 'Segoe UI', sans-serif;
    background: #f7f6f2;
    color: #292820;
    padding: 55px 20px;
}

.container {
    max-width: 900px;
    margin: auto;
}

header {
    margin-bottom: 40px;
}

h1 {
    font-size: 36px;
    font-weight: 700;
    letter-spacing: -1.5px;
}

header p {
    color: #929087;
    margin-top: 9px;
    font-size: 15px;
}

.note-form {
    background: #fff;
    padding: 28px;
    border-radius: 18px;
    box-shadow: 0 8px 30px #00000007;
    margin-bottom: 40px;
    border: 1px solid #eeede7;
}

input, textarea {
    width: 100%;
    border: 1px solid #eeede7;
    background: #fcfcfa;
    padding: 15px;
    margin-bottom: 15px;
    border-radius: 11px;
    font-size: 15px;
    outline: none;
    font-family: inherit;
    transition: .2s;
}

input:focus, textarea:focus {
    border-color: #b8aa8b;
    background: white;
}

textarea {
    min-height: 115px;
    resize: vertical;
}

button {
    border: none;
    padding: 12px 21px;
    border-radius: 10px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 600;
    transition: .2s ease;
}

button:hover {
    transform: translateY(-2px);
}

.save-btn {
    background: #292820;
    color: white;
}

.save-btn:hover {
    background: #514d3e;
}

.notes-heading {
    margin-bottom: 22px;
    font-size: 22px;
    letter-spacing: -.5px;
}

.notes-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 20px;
}

.note-card {
    background: #fff;
    padding: 23px;
    border-radius: 16px;
    border: 1px solid #eeede7;
    min-height: 165px;
    box-shadow: 0 5px 20px #00000005;
    transition: .25s ease;
}

.note-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 28px #0000000d;
}

.note-card h3 {
    margin-bottom: 12px;
    font-size: 18px;
}

.note-card p {
    color: #77766f;
    white-space: pre-wrap;
    overflow-wrap: anywhere;
    line-height: 1.7;
    margin-bottom: 20px;
}

.actions {
    display: flex;
    gap: 10px;
}

.edit-btn {
    background: #f0eee6;
    color: #514d3e;
}

.delete-btn {
    background: #fff0ed;
    color: #c35c50;
}

body {
    background: #F5F6FA;
    font-family: Arial, sans-serif;
    color: #263238;
}

h1 {
    color: #263B5E;
}

form {
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 3px 12px #00000010;
}

input, textarea {
    background: #FAFBFF;
    border: 1px solid #DCE3EF;
    border-radius: 8px;
    padding: 12px;
}

button {
    background: #4A90E2;
    color: white;
    border: none;
    padding: 10px 16px;
    border-radius: 8px;
    cursor: pointer;
}

button:hover {
    opacity: 0.85;
}
.empty {
    color: #069AF3;
    text-align: center;
    padding: 35px;
    background: white;
    border-radius: 14px;
}

@media(max-width: 500px) {
    body {
        padding: 30px 15px;
    }

    h1 {
        font-size: 29px;
    }

    .note-form {
        padding: 20px;
    }
}
body {
    background-color: #F0F4F8;
    color: #263238;
    font-family: Arial, sans-serif;
}

h1 {
    color: #3563A9;
}

input, textarea {
    background-color: #FFFFFF;
    border: 1px solid #B8CCE4;
    border-radius: 8px;
    padding: 10px;
}

button {
    background-color: #4A90E2;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 18px;
    cursor: pointer;
}

button:hover {
    background-color: #286BB5;
}

    </style>
</head>

<body>
    <div class="container">

        <header>
            <div>
                <h1>Quick Notes.</h1>
                <p>Your thoughts, organized simply.</p>
            </div>
        </header>

        <section class="note-form">
            <input id="title" placeholder="Note title">
            <textarea id="content" placeholder="Write something..."></textarea>
            <button class="save-btn" onclick="saveNote()">
                + Save Note
            </button>
        </section>

        <h2 class="notes-heading">Your Notes</h2>

        <div class="notes-grid" id="notes"></div>

    </div>

    <script>
        let editingId = null;

        async function loadNotes() {
            const response = await fetch("/api/notes");
            const notes = await response.json();

            const container = document.getElementById("notes");
            container.innerHTML = "";

            if (notes.length === 0) {
                container.innerHTML =
                    '<div class="empty">No notes yet. Create your first note!</div>';
                return;
            }

            notes.forEach(note => {
                const card = document.createElement("div");
                card.className = "note-card";

                const heading = document.createElement("h3");
                heading.textContent = note.title;

                const paragraph = document.createElement("p");
                paragraph.textContent = note.content;

                const actions = document.createElement("div");
                actions.className = "actions";

                const edit = document.createElement("button");
                edit.className = "edit-btn";
                edit.textContent = "Edit";
                edit.onclick = () => editNote(note);

                const remove = document.createElement("button");
                remove.className = "delete-btn";
                remove.textContent = "Delete";
                remove.onclick = () => deleteNote(note.id);

                actions.append(edit, remove);
                card.append(heading, paragraph, actions);
                container.appendChild(card);
            });
        }

        async function saveNote() {
            const title = document.getElementById("title").value.trim();
            const content = document.getElementById("content").value.trim();

            if (!title || !content) {
                alert("Please enter both title and content.");
                return;
            }

            const url = editingId
                ? `/api/notes/${editingId}`
                : "/api/notes";

            const method = editingId ? "PUT" : "POST";

            const response = await fetch(url, {
                method: method,
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({title, content})
            });

            if (response.ok) {
                document.getElementById("title").value = "";
                document.getElementById("content").value = "";
                editingId = null;
                document.querySelector(".save-btn").textContent = "+ Save Note";
                loadNotes();
            }
        }

        function editNote(note) {
            document.getElementById("title").value = note.title;
            document.getElementById("content").value = note.content;
            editingId = note.id;
            document.querySelector(".save-btn").textContent = "Update Note";
            window.scrollTo({top: 0, behavior: "smooth"});
        }

        async function deleteNote(id) {
            if (!confirm("Are you sure you want to delete this note?")) return;

            await fetch(`/api/notes/${id}`, {method: "DELETE"});
            loadNotes();
        }

        loadNotes();
    </script>
</body>
</html>
    """)

# Get all notes
@app.route("/api/notes", methods=["GET"])
def get_notes():
    with get_db() as db:
        notes = db.execute("SELECT * FROM notes ORDER BY id DESC").fetchall()
    return jsonify([dict(note) for note in notes])

# Add a note
@app.route("/api/notes", methods=["POST"])
def add_note():
    data = request.get_json()
    with get_db() as db:
        db.execute(
            "INSERT INTO notes (title, content) VALUES (?, ?)",
            (data["title"], data["content"])
        )
    return jsonify({"message": "Note saved"}), 201

# Edit a note
@app.route("/api/notes/<int:note_id>", methods=["PUT"])
def update_note(note_id):
    data = request.get_json()
    with get_db() as db:
        db.execute(
            "UPDATE notes SET title=?, content=? WHERE id=?",
            (data["title"], data["content"], note_id)
        )
    return jsonify({"message": "Note updated"})

# Delete a note
@app.route("/api/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    with get_db() as db:
        db.execute("DELETE FROM notes WHERE id=?", (note_id,))
    return jsonify({"message": "Note deleted"})

if __name__ == "__main__":
    app.run(debug=True)
conn = sqlite3.connect("notes.db")
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE notes ADD COLUMN favourite INTEGER DEFAULT 0")
except sqlite3.OperationalError:
    pass

try:
    cursor.execute("ALTER TABLE notes ADD COLUMN color TEXT DEFAULT '#FFFFFF'")
except sqlite3.OperationalError:
    pass

conn.commit()
conn.close()