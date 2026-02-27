from __future__ import annotations

import tkinter as tk
from tkinter import messagebox
from typing import Optional

from habit_tracker.analytics import (
    longest_streak_for_habit,
    longest_streak_overall_with_habit,
)
from habit_tracker.fixtures import build_predefined_habits_with_4_weeks_data
from habit_tracker.storage_json import JsonStorage
from habit_tracker.tracker import HabitTracker


class HabitTrackerGUI(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Habit Tracker")
        self.geometry("900x520")

        self.tracker = HabitTracker(storage=JsonStorage(file_path="data.json"))
        self.tracker.load()

        # ---------- Layout containers ----------
        left = tk.Frame(self, padx=10, pady=10)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        right = tk.Frame(self, padx=10, pady=10)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # ---------- Habits list ----------
        tk.Label(left, text="Habits", font=("Segoe UI", 14, "bold")).pack(anchor="w")

        self.habit_list = tk.Listbox(left, height=16, width=60)
        self.habit_list.pack(fill=tk.BOTH, expand=True, pady=(6, 8))
        self.habit_list.bind("<<ListboxSelect>>", lambda e: self.refresh_stats())

        habit_buttons = tk.Frame(left)
        habit_buttons.pack(fill=tk.X, pady=(0, 10))

        tk.Button(habit_buttons, text="Refresh", command=self.refresh_all).pack(side=tk.LEFT)
        tk.Button(habit_buttons, text="Load Demo Data", command=self.load_demo).pack(side=tk.LEFT, padx=6)
        tk.Button(habit_buttons, text="Check-off Selected", command=self.check_off_selected).pack(side=tk.LEFT, padx=6)
        tk.Button(habit_buttons, text="Delete Selected", command=self.delete_selected_habit).pack(side=tk.LEFT, padx=6)

        # ---------- Create habit ----------
        create_box = tk.LabelFrame(left, text="Create Habit", padx=10, pady=10)
        create_box.pack(fill=tk.X)

        tk.Label(create_box, text="Name").grid(row=0, column=0, sticky="w")
        self.h_name = tk.Entry(create_box, width=30)
        self.h_name.grid(row=0, column=1, sticky="w", padx=6)

        tk.Label(create_box, text="Periodicity").grid(row=1, column=0, sticky="w", pady=(6, 0))
        self.h_period = tk.StringVar(value="daily")
        tk.OptionMenu(create_box, self.h_period, "daily", "weekly").grid(row=1, column=1, sticky="w", padx=6, pady=(6, 0))

        tk.Label(create_box, text="Description").grid(row=2, column=0, sticky="w", pady=(6, 0))
        self.h_desc = tk.Entry(create_box, width=45)
        self.h_desc.grid(row=2, column=1, sticky="w", padx=6, pady=(6, 0))

        tk.Button(create_box, text="Create Habit", command=self.create_habit).grid(row=3, column=1, sticky="w", padx=6, pady=(10, 0))

        # ---------- Stats ----------
        tk.Label(right, text="Stats", font=("Segoe UI", 14, "bold")).pack(anchor="w")
        self.stats_text = tk.Text(right, height=10, width=45)
        self.stats_text.pack(fill=tk.X, pady=(6, 12))
        self.stats_text.configure(state="disabled")

        tk.Button(right, text="Show Longest Overall", command=self.show_longest_overall).pack(anchor="w")

        # ---------- Tasks  ----------
        tasks_box = tk.LabelFrame(right, text="Eisenhower Tasks", padx=10, pady=10)
        tasks_box.pack(fill=tk.BOTH, expand=True, pady=(12, 0))

        self.task_list = tk.Listbox(tasks_box, height=10)
        self.task_list.pack(fill=tk.BOTH, expand=True, pady=(0, 8))

        t_form = tk.Frame(tasks_box)
        t_form.pack(fill=tk.X)

        tk.Label(t_form, text="Title").grid(row=0, column=0, sticky="w")
        self.t_title = tk.Entry(t_form, width=26)
        self.t_title.grid(row=0, column=1, sticky="w", padx=6)

        self.t_urgent = tk.BooleanVar(value=False)
        self.t_important = tk.BooleanVar(value=False)
        tk.Checkbutton(t_form, text="Urgent", variable=self.t_urgent).grid(row=1, column=0, sticky="w", pady=(6, 0))
        tk.Checkbutton(t_form, text="Important", variable=self.t_important).grid(row=1, column=1, sticky="w", padx=6, pady=(6, 0))

        tk.Label(t_form, text="Due (optional)").grid(row=2, column=0, sticky="w", pady=(6, 0))
        self.t_due = tk.Entry(t_form, width=26)
        self.t_due.grid(row=2, column=1, sticky="w", padx=6, pady=(6, 0))

        btns = tk.Frame(tasks_box)
        btns.pack(fill=tk.X)

        tk.Button(btns, text="Add Task", command=self.add_task).pack(side=tk.LEFT)
        tk.Button(btns, text="Refresh Tasks", command=self.refresh_tasks).pack(side=tk.LEFT, padx=6)
        tk.Button(btns, text="Mark Task Done", command=self.mark_task_done).pack(side=tk.LEFT, padx=6)
        tk.Button(btns, text="Delete Task", command=self.delete_task).pack(side=tk.LEFT, padx=6)

        # initial fill
        self.refresh_all()

    # ----------------- Helpers -----------------

    def refresh_all(self) -> None:
        self.refresh_habits()
        self.refresh_tasks()
        self.refresh_stats()

    def refresh_habits(self) -> None:
        self.habit_list.delete(0, tk.END)
        for h in self.tracker.list_habits():
            self.habit_list.insert(tk.END, f"{h.name} [{h.periodicity}]  (completions: {len(h.completions)})")

    def refresh_tasks(self) -> None:
        self.task_list.delete(0, tk.END)
        tasks = self.tracker.list_tasks()
        for i, t in enumerate(tasks, start=1):
            status = "DONE" if t.completed else "TODO"
            quad = (
                "Q1" if (t.urgent and t.important)
                else "Q2" if ((not t.urgent) and t.important)
                else "Q3" if (t.urgent and (not t.important))
                else "Q4"
            )
            due = f" | due: {t.due_datetime}" if t.due_datetime else ""
            self.task_list.insert(tk.END, f"{i}) [{status}] [{quad}] {t.title}{due}")

    def selected_habit_name(self) -> Optional[str]:
        sel = self.habit_list.curselection()
        if not sel:
            return None
        idx = sel[0]
        habits = self.tracker.list_habits()
        if idx < 0 or idx >= len(habits):
            return None
        return habits[idx].name

    def refresh_stats(self) -> None:
        name = self.selected_habit_name()
        overall = longest_streak_overall_with_habit(self.tracker.list_habits())

        lines = []
        if overall is None:
            lines.append("Longest overall: (no habits)")
        else:
            hname, streak = overall
            lines.append(f"Longest overall: {streak}  (Habit: {hname})")

        if name is None:
            lines.append("Selected habit: (none)")
        else:
            habit = self.tracker.get_habit_by_name(name)
            if habit:
                lines.append(f"Selected habit: {habit.name}")
                lines.append(f"Streak for selected: {longest_streak_for_habit(habit)}")
                lines.append(f"Total completions: {len(habit.completions)}")

        self.stats_text.configure(state="normal")
        self.stats_text.delete("1.0", tk.END)
        self.stats_text.insert(tk.END, "\n".join(lines))
        self.stats_text.configure(state="disabled")

    # ----------------- Habit actions -----------------

    def create_habit(self) -> None:
        try:
            name = self.h_name.get().strip()
            period = self.h_period.get().strip()
            desc = self.h_desc.get().strip()
            self.tracker.create_habit(name=name, periodicity=period, description=desc)
            self.h_name.delete(0, tk.END)
            self.h_desc.delete(0, tk.END)
            self.refresh_all()
            messagebox.showinfo("Success", "Habit created & saved.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def check_off_selected(self) -> None:
        name = self.selected_habit_name()
        if not name:
            messagebox.showwarning("No selection", "Select a habit first.")
            return
        try:
            self.tracker.check_off(name)
            self.refresh_all()
            messagebox.showinfo("Success", f"Checked-off: {name}")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def delete_selected_habit(self) -> None:
        name = self.selected_habit_name()
        if not name:
            messagebox.showwarning("No selection", "Select a habit first.")
            return
        if not messagebox.askyesno("Confirm", f"Delete habit '{name}'?"):
            return
        try:
            self.tracker.delete_habit(name)
            self.refresh_all()
            messagebox.showinfo("Deleted", f"Deleted: {name}")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def load_demo(self) -> None:
        if not messagebox.askyesno("Confirm", "Replace all habits with demo data?"):
            return
        self.tracker.replace_all_habits(build_predefined_habits_with_4_weeks_data())
        self.refresh_all()
        messagebox.showinfo("Loaded", "Demo habits loaded & saved.")

    def show_longest_overall(self) -> None:
        overall = longest_streak_overall_with_habit(self.tracker.list_habits())
        if overall is None:
            messagebox.showinfo("Longest overall", "No habits available.")
        else:
            name, streak = overall
            messagebox.showinfo("Longest overall", f"{streak} (Habit: {name})")

    # ----------------- Task actions -----------------

    def add_task(self) -> None:
        try:
            title = self.t_title.get().strip()
            urgent = bool(self.t_urgent.get())
            important = bool(self.t_important.get())
            due = self.t_due.get().strip() or None

            self.tracker.create_task(
                title=title,
                urgent=urgent,
                important=important,
                due_datetime=due,
            )
            self.t_title.delete(0, tk.END)
            self.t_due.delete(0, tk.END)
            self.t_urgent.set(False)
            self.t_important.set(False)
            self.refresh_tasks()
            messagebox.showinfo("Success", "Task created & saved.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def mark_task_done(self) -> None:
        sel = self.task_list.curselection()
        if not sel:
            messagebox.showwarning("No selection", "Select a task first.")
            return
        idx = sel[0] + 1  # 1-based for tracker
        try:
            self.tracker.mark_task_completed(idx)
            self.refresh_tasks()
            messagebox.showinfo("Success", "Task marked DONE.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def delete_task(self) -> None:
        sel = self.task_list.curselection()
        if not sel:
            messagebox.showwarning("No selection", "Select a task first.")
            return
        idx = sel[0] + 1
        if not messagebox.askyesno("Confirm", "Delete selected task?"):
            return
        try:
            self.tracker.delete_task(idx)
            self.refresh_tasks()
            messagebox.showinfo("Deleted", "Task deleted.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))


def run_gui() -> None:
    app = HabitTrackerGUI()
    app.mainloop()
