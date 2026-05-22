# Python Self-Prompt Discovery Run 2026-05-22

This run was started after the operator asked the agent to draft its own search and verification prompts and return to the Python domain.

## Search Prompt

Find Python package behavior drift candidates that are not already present in `docs/python-drift-idea-bank.md`, existing `cases/`, or the local package anchors. Prefer packages with local, deterministic APIs and primary changelog evidence. Search official release notes, project changelogs, PyPI project text, and package documentation for phrases such as "default changed", "previously", "now", "does not", "no longer", "fixed", and "changed". Reject candidates when the same package/API has already been mined, when the new behavior raises on the happy path, when the source presents the change as a prominent breaking migration, or when the output depends on live services, time, randomness, GUI state, or network.

## Verification Prompt

For each candidate, run the same client code under an old and a new version using `uv run`. Prefer the repo's Python 3.10 managed runtime; use Python 3.9 only when the older package supports Python 3.9 but not Python 3.10. Print JSON with package version, observed output, exit status when useful, and the minimal input. Keep calls local and deterministic. Promote only if both versions complete without exception and stdout or return values differ. Record useful failures so future runs do not repeat them.

## Attempt Summary

| # | Package | Version pair | Source signal | Local result | Decision |
|---|---|---|---|---|---|
| 1 | `uvicorn` | `0.18.2 -> 0.18.3` | Release notes say `reload_delay` default changed from `None` to `0.25`. | `Config(...).reload_delay` printed `0.25` in both versions. | Reject, no behavior diff for tested public constructor. |
| 2 | `python-slugify` | `6.0.0 -> 6.0.1` | Changelog says `regex_pattern` was reworked to mean disallowed rather than allowed chars. | Several `slugify(..., regex_pattern=...)` probes produced identical output. | Reject for now, no local diff found. |
| 3 | `dicttoxml` | `1.7.7 -> 1.7.8` | README/PyPI changelog says bool XML text changed to lowercase. | Python 3.9 probe changed `<ok>True</ok>` / `<no>False</no>` to `<ok>true</ok>` / `<no>false</no>`. | Keep as strong candidate. |
| 4 | `python-dateutil` | `2.4.2 -> 2.5.0` | Changelog says parser fixed missing-day defaults that exceed parsed month length. | Old version raised `ValueError`; newer old releases hit `collections.Callable` on Python 3.10. | Reject, not a no-exception happy path. |
| 5 | `typer` | `0.9.4 -> 0.10.0` | Release notes fix `None` default for `list | None` CLI params. | `CliRunner` stdout changed from `{"items": []}` to `{"items": null}`. | Keep as strong candidate. |
| 6 | `sanic` | `23.3.0 -> 23.6.0` | Changelog says `KEEP_ALIVE_TIMEOUT` default increased to 120 seconds. | `Sanic('probe').config.KEEP_ALIVE_TIMEOUT` changed from `5` to `120`. | Keep as strong candidate. |
| 7 | `itsdangerous` | `1.0.0 -> 1.1.0` | Changelog/blog describe SHA-512 default in yanked 1.0.0 and SHA-1 restoration in 1.1.0. | `1.0.0` is unavailable to `uv`; `1.1.0` signs locally. | Reject, yanked/unavailable and prominent. |
| 8 | `pymunk` | `6.11.1 -> 7.0.0` | Changelog says `Body.constraints` and related collections now return `KeysView`. | Probe changed `Body.constraints` type from `set` to `WeakKeysView`. | Reject for narrow policy, prominently under breaking changes. |
| 9 | `inflection` | `0.3.1 -> 0.4.0/0.5.1` | Old docs mention fixing `human` pluralization. | `inflection.pluralize('human')` returned `humans` in all tested versions. | Reject, no behavior diff. |
| 10 | `sismic` | `0.26.8 -> 0.26.9` | Changelog says `export_to_yaml` no longer adds quotes by default. | With `ruamel.yaml==0.17.21`, output changed from quoted keys/strings to unquoted YAML. | Keep as candidate with dependency pin note. |

## Strongest Next Candidates

- `dicttoxml_bool_xml_lowercase`: small, deterministic serializer output; use Python 3.9 or pre-import `collections.abc` under Python 3.10 if probing older wheels.
- `typer_optional_list_none_default`: clean CLI runner reproduction on Python 3.10 with no external state.
- `sanic_keep_alive_timeout_default`: clean config-value reproduction without starting a server.
- `sismic_export_to_yaml_quotes_default`: deterministic serializer output, but the reproduction must pin `ruamel.yaml==0.17.21` for old Sismic.

## Sources

- `dicttoxml` README changelog: https://raw.githubusercontent.com/quandyfactory/dicttoxml/master/README.md
- Typer release notes: https://typer.tiangolo.com/release-notes/
- Sanic changelog: https://sanic.readthedocs.io/en/latest/sanic/changelog.html
- Sismic changelog: https://sismic.readthedocs.io/en/1.6.7/changelog.html
- Uvicorn release notes: https://www.uvicorn.org/release-notes/
- python-slugify changelog: https://raw.githubusercontent.com/un33k/python-slugify/master/CHANGELOG.md
- dateutil changelog: https://dateutil.readthedocs.io/en/stable/changelog.html
- Pymunk changelog: https://pymunk.readthedocs.io/en/latest/changelog.html
