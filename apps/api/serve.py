"""Single entrypoint: migrate, then serve.

Why this module exists
----------------------
Render's free tier has no ``preDeployCommand``, so migrations have to run
either in the build step or the start step. Both of those have already failed
here, in two different ways:

1. The build step was left as Render's default, ``pip install -r
   requirements.txt``. That succeeds, so the deploy reports success, and then
   the application dies at startup on ``relation "clearance_records" does not
   exist`` -- a table that migration 0003 creates.
2. Putting ``alembic upgrade head && uvicorn ...`` in the start step does not
   work either, because Render hands the entire field to a single process.
   Alembic receives ``&& uvicorn app.main:app`` as literal arguments and exits
   2.

The failure mode in both cases is the same and it is the bad one: a deploy that
*looks* successful and is not. So the decision is taken out of the dashboard
entirely. This module runs the migrations and then serves, in one process, so:

* the Start Command is a single argument-free command, with no ``&&``;
* a database that has not been migrated cannot start, so it fails at deploy
  time with a short message instead of a 200-frame SQLAlchemy traceback during
  the demo;
* the build step needs no changes, because it is now only ``pip install``.

Run locally the same way:  ``python serve.py``
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def migrate() -> None:
    """Bring the database to head, or exit with an explanation.

    A migration failure is not recoverable at runtime and must not be
    swallowed. The database is the system of record; serving reads against a
    schema that does not match the code produces wrong answers rather than an
    error, which is the failure this project exists to avoid.
    """
    from alembic.config import Config

    from alembic import command

    config = Config(str(ROOT / "alembic.ini"))
    # Set explicitly rather than relying on the working directory, so this works
    # whichever directory the process is started from.
    config.set_main_option("script_location", str(ROOT / "alembic"))
    command.upgrade(config, "head")


def main() -> int:
    try:
        migrate()
    except Exception as exc:  # noqa: BLE001 - the message is the deliverable
        print(
            "\n"
            "=========================================================\n"
            " MIGRATION FAILED - the database schema is not current.\n"
            "=========================================================\n"
            f" {type(exc).__name__}: {exc}\n"
            "\n"
            " Check, in order:\n"
            "  1. DATABASE_URL is set and points at a reachable database.\n"
            "  2. The credentials are correct and the IP allowlist permits this host.\n"
            "  3. The build step ran 'pip install -r requirements.txt' successfully.\n"
            "\n"
            " The application will not start against an unmigrated database,\n"
            " because serving reads against a schema that does not match the\n"
            " code produces wrong answers rather than an error.\n",
            file=sys.stderr,
        )
        return 1

    import uvicorn

    port = int(os.getenv("PORT", "8000"))
    # PORT is injected per service by the platform. A hardcoded port binds the
    # wrong socket and the health check never passes, so the variable is
    # required rather than defaulted in a way that can be missed.
    print(f"Database is at head. Serving app.main:app on 0.0.0.0:{port}")
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, log_level="info")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
