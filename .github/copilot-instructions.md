# GitHub Copilot instructions for this repository ✅

## TL;DR
- Small Python Tkinter GUI project. Current entrypoint: `main.py` (contents: `import tkinter as Tk`). There are no tests, requirements, or docs yet. Focus on building a clear GUI MVC structure, add persistence (JSON), and add tests for non-GUI logic.

---

## Project snapshot (discoverable facts) 🔎
- Language: **Python**
- Entry point: `main.py` (currently only: `import tkinter as Tk`).
- No `requirements.txt`, no `README.md`, no test suite found.
- Repo folder name (Portuguese): "Cronograma Transição Hormonal" → implies a schedule/plan GUI for hormone transition.

---

## Immediate goals for an AI coding agent (practical, ordered) 🛠️
1. Create a minimal runnable GUI scaffold.
   - Implement `gui.py` with `create_main_window()` that returns a `Tk` root and a `MainFrame` class.
   - Update `main.py` to launch the scaffold when run as `__main__`.
   - Example: `root = Tk.Tk(); root.title("Cronograma Transição Hormonal"); root.mainloop()`
2. Add a stable data model and persistence layer.
   - Add `model.py` (data classes representing scheduled items) and `storage.py` (JSON read/write helpers).
   - Keep I/O synchronous and filesystem-based for simplicity: e.g., `data/schedule.json`.
3. Add unit tests for model and storage.
   - Use `pytest`; place tests under `tests/` (e.g., `tests/test_model.py`, `tests/test_storage.py`).
   - Make tests independent of GUI; mock filesystem when needed (use `tmp_path`).
4. Add developer docs & environment files.
   - `requirements.txt`, a short `README.md` (run & build notes), and this `.github/copilot-instructions.md`.
5. Add packaging note (optional): use `PyInstaller` or `brief instructions` for building a Windows executable.

---

## Conventions & patterns to follow (repository-specific) 📚
- Keep GUI code separated from pure logic: `gui/` or `gui.py` for all Tkinter widgets, `model.py` for domain objects, `storage.py` for persistence.
- Mimic the existing import style if referencing `main.py`: the repo currently uses `import tkinter as Tk` (capital `T`). New modules may follow standard lowercase imports, but keep consistent if working inside an existing file.
- Tests must not rely on a display. Abstract GUI interactions behind testable interfaces.

---

## How to run, debug, and test (concrete commands) ▶️
- Create and activate virtual env (Windows PowerShell):
  - `python -m venv .venv`
  - `.\.venv\Scripts\Activate.ps1`
- Install dev dependencies:
  - `pip install -r requirements.txt` (create if missing; include `pytest` and `pyinstaller` as needed)
- Run the app (from workspace root):
  - `python main.py`
- Run tests:
  - `python -m pytest -q`

---

## Useful examples for the agent (copyable snippets) ✂️
- Minimal `main.py` pattern:
```py
from gui import create_main_window

if __name__ == "__main__":
    root = create_main_window()
    root.mainloop()
```
- Storage helper (JSON):
```py
import json
from pathlib import Path

def load_schedule(path: Path):
    if not path.exists():
        return []
    return json.loads(path.read_text())
```

---

## Files to inspect when expanding features 🔧
- `main.py` (entry point, currently minimal)
- Newly created: `gui.py`, `model.py`, `storage.py`, `tests/`

---

## When to ask the repo owner for clarifications ❓
- Confirm expected data fields for schedule items (dates, medication, dosage, notes).
- Confirm whether persistence should be local JSON, SQLite, or cloud-backed.
- Confirm Windows packaging requirements and target Python versions.

---

If anything in this file looks off or you'd like me to emphasize different conventions (language, packaging, or test style), tell me which area to iterate on and I will update this doc. 👋
