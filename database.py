import sqlite3
from contextlib import closing
from pathlib import Path


class NoteDatabase:
    """Lớp duy nhất chịu trách nhiệm đọc/ghi dữ liệu ghi chú."""

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._create_table()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _create_table(self):
        with closing(self._connect()) as connection:
            with connection:
                connection.execute(
                    """
                    CREATE TABLE IF NOT EXISTS notes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        content TEXT NOT NULL DEFAULT '',
                        updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                    )
                    """
                )

    def list_notes(self, keyword=""):
        pattern = f"%{keyword.strip()}%"
        with closing(self._connect()) as connection:
            return connection.execute(
                """
                SELECT id, title, content, updated_at
                FROM notes
                WHERE title LIKE ? OR content LIKE ?
                ORDER BY updated_at DESC, id DESC
                """,
                (pattern, pattern),
            ).fetchall()

    def create_note(self, title, content):
        with closing(self._connect()) as connection:
            with connection:
                cursor = connection.execute(
                    "INSERT INTO notes (title, content) VALUES (?, ?)",
                    (title, content),
                )
                return cursor.lastrowid

    def update_note(self, note_id, title, content):
        with closing(self._connect()) as connection:
            with connection:
                connection.execute(
                    """
                    UPDATE notes
                    SET title = ?, content = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                    """,
                    (title, content, note_id),
                )

    def delete_note(self, note_id):
        with closing(self._connect()) as connection:
            with connection:
                connection.execute("DELETE FROM notes WHERE id = ?", (note_id,))
