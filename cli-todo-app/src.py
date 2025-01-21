# CLI TODO app using Typer, Rich, and SQLite

import typer
import sqlite3
from rich.console import Console
from rich.table import Table

app = typer.Typer()
c = Console()


# Setup sqlite3 database
def setup_database():
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'pending'
        )
    """)
    conn.commit()
    conn.close()


# Add a task to the database
@app.command()
def add(title: str, description: str = typer.Option("", help="Task description")):
    """Add a new task."""
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, description) VALUES (?, ?)", (title, description)
    )
    conn.commit()
    conn.close()
    c.print(f"[green]Task '{title}' added![/green]")


# List all tasks
@app.command()
def list():
    """List all tasks."""
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()

    table = Table(title="Tasks")
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Title", style="magenta")
    table.add_column("Description", style="green")
    table.add_column("Status", style="yellow")

    for task in tasks:
        table.add_row(str(task[0]), task[1], task[2], task[3])

    c.print(table)


# Update a task
@app.command()
def update(
    task_id: int, title: str = None, description: str = None, status: str = None
):
    """Update task details."""
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()

    if title:
        cursor.execute("UPDATE tasks SET title = ? WHERE id = ?", (title, task_id))
    if description:
        cursor.execute(
            "UPDATE tasks SET description = ? WHERE id = ?", (description, task_id)
        )
    if status:
        cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, task_id))

    conn.commit()
    conn.close()
    c.print(f"[blue]Task {task_id} updated![/blue]")


# Delete a task
@app.command()
def delete(task_id: int):
    """Delete a task."""
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    c.print(f"[red]Task {task_id} deleted![/red]")


if __name__ == "__main__":
    setup_database()
    app()
