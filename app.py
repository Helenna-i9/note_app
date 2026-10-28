import tkinter as tk
import sys
from pathlib import Path
from tkinter import messagebox, ttk

from database import NoteDatabase


APP_DIR = Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent


class NoteApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ghi chú Local")
        self.geometry("900x560")
        self.minsize(720, 440)

        self.database = NoteDatabase(APP_DIR / "notes.db")
        self.current_note_id = None
        self.note_ids = []

        self._build_ui()
        self.refresh_notes()

    def _build_ui(self):
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        left = ttk.Frame(self, padding=12)
        left.grid(row=0, column=0, sticky="nsew")
        left.rowconfigure(2, weight=1)

        ttk.Label(left, text="Tìm ghi chú").grid(row=0, column=0, sticky="w")
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self.refresh_notes())
        ttk.Entry(left, textvariable=self.search_var, width=30).grid(
            row=1, column=0, sticky="ew", pady=(4, 10)
        )

        self.note_list = tk.Listbox(left, width=32, exportselection=False)
        self.note_list.grid(row=2, column=0, sticky="nsew")
        self.note_list.bind("<<ListboxSelect>>", self.open_selected_note)

        ttk.Button(left, text="+ Ghi chú mới", command=self.new_note).grid(
            row=3, column=0, sticky="ew", pady=(10, 0)
        )

        editor = ttk.Frame(self, padding=(0, 12, 12, 12))
        editor.grid(row=0, column=1, sticky="nsew")
        editor.columnconfigure(0, weight=1)
        editor.rowconfigure(3, weight=1)

        ttk.Label(editor, text="Tiêu đề").grid(row=0, column=0, sticky="w")
        self.title_var = tk.StringVar()
        ttk.Entry(editor, textvariable=self.title_var).grid(
            row=1, column=0, columnspan=2, sticky="ew", pady=(4, 10)
        )

        ttk.Label(editor, text="Nội dung").grid(row=2, column=0, sticky="w")
        self.content_text = tk.Text(editor, wrap="word", undo=True, padx=8, pady=8)
        self.content_text.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=(4, 10))

        ttk.Button(editor, text="Lưu", command=self.save_note).grid(
            row=4, column=0, sticky="ew", padx=(0, 5)
        )
        ttk.Button(editor, text="Xóa", command=self.delete_note).grid(
            row=4, column=1, sticky="ew", padx=(5, 0)
        )

        self.status_var = tk.StringVar(value="Sẵn sàng")
        ttk.Label(editor, textvariable=self.status_var).grid(
            row=5, column=0, columnspan=2, sticky="w", pady=(10, 0)
        )

    def refresh_notes(self, selected_id=None):
        notes = self.database.list_notes(self.search_var.get())
        self.note_list.delete(0, tk.END)
        self.note_ids = []
        selected_index = None

        for index, (note_id, title, _content, updated_at) in enumerate(notes):
            self.note_ids.append(note_id)
            display_title = title.strip() or "(Không có tiêu đề)"
            self.note_list.insert(tk.END, f"{display_title}  ·  {updated_at[:16]}")
            if note_id == selected_id:
                selected_index = index

        if selected_index is not None:
            self.note_list.selection_set(selected_index)
            self.note_list.see(selected_index)

    def open_selected_note(self, _event=None):
        selection = self.note_list.curselection()
        if not selection:
            return

        note_id = self.note_ids[selection[0]]
        notes = self.database.list_notes(self.search_var.get())
        note = next((item for item in notes if item[0] == note_id), None)
        if note is None:
            return

        self.current_note_id = note[0]
        self.title_var.set(note[1])
        self.content_text.delete("1.0", tk.END)
        self.content_text.insert("1.0", note[2])
        self.status_var.set(f"Đang mở ghi chú #{note_id}")

    def new_note(self):
        self.current_note_id = None
        self.note_list.selection_clear(0, tk.END)
        self.title_var.set("")
        self.content_text.delete("1.0", tk.END)
        self.status_var.set("Ghi chú mới — nhập nội dung rồi bấm Lưu")

    def save_note(self):
        title = self.title_var.get().strip()
        content = self.content_text.get("1.0", "end-1c").strip()
        if not title:
            messagebox.showwarning("Thiếu tiêu đề", "Bạn hãy nhập tiêu đề ghi chú.")
            return

        if self.current_note_id is None:
            self.current_note_id = self.database.create_note(title, content)
            self.status_var.set("Đã tạo ghi chú mới")
        else:
            self.database.update_note(self.current_note_id, title, content)
            self.status_var.set("Đã lưu thay đổi")

        self.search_var.set("")
        self.refresh_notes(selected_id=self.current_note_id)

    def delete_note(self):
        if self.current_note_id is None:
            messagebox.showinfo("Chưa chọn ghi chú", "Hãy chọn ghi chú cần xóa.")
            return
        if not messagebox.askyesno("Xác nhận xóa", "Bạn chắc chắn muốn xóa ghi chú này?"):
            return

        self.database.delete_note(self.current_note_id)
        self.new_note()
        self.refresh_notes()
        self.status_var.set("Đã xóa ghi chú")


if __name__ == "__main__":
    NoteApp().mainloop()
