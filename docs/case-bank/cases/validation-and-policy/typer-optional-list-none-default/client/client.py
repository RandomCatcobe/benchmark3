from __future__ import annotations

import json
from typing import List, Optional

import typer
from typer.testing import CliRunner


app = typer.Typer()
observed_items = []


@app.command()
def main(items: Optional[List[str]] = None) -> None:
    observed_items.append(items)


def _type_name(value: object) -> str:
    return type(value).__name__


if __name__ == "__main__":
    result = CliRunner().invoke(app, [])
    callback_value = observed_items[0] if observed_items else None
    print(
        json.dumps(
            {
                "library_version": typer.__version__,
                "cli_exit_code": result.exit_code,
                "callback_items": callback_value,
                "callback_items_type": _type_name(callback_value),
                "exception_type": _type_name(result.exception) if result.exception else None,
            },
            sort_keys=True,
        )
    )
