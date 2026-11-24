"""The Funniest Toaster Error Message (make.fun).

Writes a single line -- the funniest error message a kitchen toaster
would show its owner -- to $MAKEFUN_OUTPUT_DIR/entry.txt
(or /output/entry.txt when that variable is unset).
"""

import os
from pathlib import Path

# One line, 63 characters: the toaster remembers the fork its owner
# dismissed as "probably fine".
ENTRY = "ERROR 04: Fork in slot 2. You said 'probably fine.' I remember."


def main() -> None:
    # The gate refuses anything outside 1-120 characters, so fail loudly
    # here rather than shipping an invalid entry.
    assert 1 <= len(ENTRY) <= 120, f"entry is {len(ENTRY)} chars"
    assert "\n" not in ENTRY, "entry must be a single line"
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "entry.txt").write_text(ENTRY + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
