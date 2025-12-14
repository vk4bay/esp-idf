# ESP-IDF Copilot Guide

## Project Overview
- ESP-IDF is the firmware SDK for Espressif SoCs; `README.md` documents release cadence and new-target guidance.
- `components/README.md` defines two core layers: G0 (hal/arch/esp_rom/esp_common/soc) and G1 (esp_hw_support/esp_system/freertos/log/heap/newlib/esp_mm); keep dependencies flowing upward.
- Application code lives in standalone IDF projects under `examples/*` and target validation suites under `tools/test_apps/*`; copy them out-of-tree before modifying.
- Docs in `docs/en/**` feed https://docs.espressif.com; update the matching `.rst` when APIs or behavior change.

## Build Workflow
- Bootstrap toolchains with `install.ps1` (Windows) or `install.sh` plus `--enable-pytest`/`--enable-pytest-specific` when tests need host deps (`docs/en/contribute/esp-idf-tests-with-pytest.rst`).
- Every new shell must run `export.ps1`/`export.sh` to populate `IDF_PATH`, PATH, and Python venv before calling `idf.py`.
- Use `idf.py set-target <chip>` to switch SoCs; `idf.py --list-targets [--preview]` shows supported devices (per `README.md`).
- `idf.py build`, `idf.py flash`, `idf.py monitor`, and `idf.py flash monitor` wrap CMake+Ninja; prefer `idf.py app`/`app-flash` for quick iterations once bootloader is stable.
- Feature flags originate from `Kconfig`; run `idf.py menuconfig` and check in reproducible defaults via `sdkconfig.defaults` or numbered variants like `sdkconfig.ci`.

## Component Patterns
- Components register sources via `idf_component_register(...)` inside `components/*/CMakeLists.txt`; gate optional files with `if(CONFIG_...)` as shown in `components/esp_system/CMakeLists.txt`.
- Public headers sit in `components/<name>/include`; internal APIs go under `private_include` or subfolders and are wired through `INCLUDE_DIRS`/`PRIV_INCLUDE_DIRS` arguments to `idf_component_register`.
- Add new configuration knobs to the component's `Kconfig` and include it from the nearest parent `Kconfig` so `menuconfig` picks them up.
- Preserve the G0/G1 layering: hardware primitives (`hal`, `soc`, `esp_rom`) must not call into system-level services (`esp_system`, `freertos`, etc.).

## Testing & CI
- Pytest discovery is restricted to `pytest_*.py` per root `pytest.ini`; keep scripts beside the test app that they drive.
- Default options in `pytest.ini` enable `--embedded-services esp,idf`, strict markers, and CI log routing; reuse them when invoking `pytest` locally.
- Target and environment markers (`@pytest.mark.esp32`, `@pytest.mark.generic`, etc.) are defined in `tools/ci/idf_pytest/constants.py`; annotate cases so CI selects the right hardware.
- Use fixtures from `conftest.py` (`dut`, `config`, `case_tester`, multi-DUT utilities) instead of reimplementing serial flows; they encapsulate app download, log dirs, and Unity integration.
- Follow `docs/en/contribute/esp-idf-tests-with-pytest.rst` for multi-DUT parameterization (`count`, `target`, `app_path`) and Unity helpers like `dut.run_all_single_board_cases()`.

## Tooling Notes
- Adhere to `docs/en/contribute/style-guide.rst`: 4-space indent, `s_` prefix for static globals, no tabs or trailing whitespace.
- Optional git hooks in `docs/en/contribute/install-pre-commit-hook.rst` help enforce formatting and lint checks; install them before large refactors.
- Non-GitHub mirrors must run `tools/set-submodules-to-github.sh` so `git submodule update --init --recursive` succeeds (see `README.md`).

## Key Paths
- `components/` core libraries, sorted by discipline; read `components/README.md` before touching unfamiliar subsystems.
- `examples/` official reference projects; they double as regression baselines and sample `sdkconfig.ci` files.
- `tools/ci/` houses `idf_pytest`, embedded test DSLs, and build metadata consumed by `conftest.py`.
