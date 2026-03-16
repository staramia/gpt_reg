import subprocess
from pathlib import Path
import shutil
from typing import List, Optional


def _run(cmd: List[str], *, stdin_data: Optional[str] = None) -> int:
    print(f"\n>>> {' '.join(cmd)}", flush=True)
    completed = subprocess.run(cmd, input=stdin_data, text=True)
    return completed.returncode


def _clear_output_dir(output_dir: Path) -> None:
    if not output_dir.exists():
        print(f"\n>>> output directory not found: {output_dir}", flush=True)
        return

    if not output_dir.is_dir():
        raise RuntimeError(f"output path is not a directory: {output_dir}")

    removed = 0
    for child in output_dir.iterdir():
        if child.is_dir() and not child.is_symlink():
            shutil.rmtree(child)
            removed += 1
        else:
            child.unlink(missing_ok=True)
            removed += 1

    print(f"\n>>> cleared output/: removed {removed} item(s)", flush=True)


def main() -> int:
    repo_root = Path(__file__).resolve().parent

    # Provide enough newlines to satisfy all input() prompts and accept defaults.
    default_enters = "\n" * 200

    rc = _run(["uv", "run", "main.py"], stdin_data=default_enters)
    if rc != 0:
        return rc

    upload_rc = _run(["uv", "run", "upload.py"])
    _clear_output_dir(repo_root / "output")
    return upload_rc


if __name__ == "__main__":
    raise SystemExit(main())
