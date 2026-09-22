"""The built-in delivery transports (goal:g7.32.4): append to the file, or
nudge the pane. Moved verbatim out of send.py and admitted by discovery, not
by an import in send.py; the pane helpers arrive through ``helpers`` so this
module never imports send.
"""
from __future__ import annotations


def register(register_delivery, helpers) -> None:
    def deliver(root, kind, path, payload, **kw) -> bool:
        if kind == "file":
            with open(path, "a") as f:
                f.write(payload)
            return True
        if kind == "nudge":
            ok = helpers["nudge_window"](root, path,
                                         sender=kw.get("sender"), body=payload)
            helpers["announce_nudge"](kw.get("croot", root), path, ok)
            return True
        return False

    register_delivery("default", deliver)