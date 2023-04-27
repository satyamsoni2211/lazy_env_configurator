# ChangeLog

---

## VERSION 0.3.0-alpha

- Changed `BaseConfig` by Default to be self contained.
- Included `Pydantic` Validations with `Env` variables.
- Default type fallback to `Optional[str]` for Env variables.
- `BaseConfig` now accepts `validations` as dictionary with values as `ValidationOptions` which are accepted by `FieldInfo`.
- `Env` has a granular validator included which takes length validators, value validators etc.
- Optimised metaclass creation and validations.

## VERSION 0.2.0

---

- Self Contained Classes
- Validator for `envs` attribute if not iterable.
- Validator for `dot-env-path` attribute if invalid.
- Slotted Env to reduce memory footprint.
- Added tests
- Raises Warning when no `.env` file found with `contained` set to `True`.

## VERSION 0.1.0

---

- Dynamic Environment Configuration
- Auto Load .env file
- Load Env Lazily
