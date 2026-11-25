# Automated Flutter Application Generator & Productivity Suite

An automated mobile development automation engine that scaffolds, tests, and builds production-grade cross-platform Flutter applications on demand with integrated Pomodoro productivity mechanics and scheduled cron pipelines.

---

## Key Capabilities

- **Automated App Generation (`generate_apps.py`)**: Scriptable creation of responsive Flutter widgets, stateful containers, Material 3 theming, and multi-screen navigation hierarchies.
- **Productivity & Pomodoro Architecture**: Includes the `Atunafsi` productivity app template featuring interval timers, focus tracking, and local state persistence.
- **CI/CD Build Scripts**: Shell pipelines (`daily_build.sh`, `daily_job.sh`) for automated asset zipping, test execution, and deployment verification.

---

## Quickstart

```bash
# Clone the repository
git clone https://github.com/KABURAKURIA/flutter.git
cd flutter

# Generate an application batch
python generate_apps.py

# Build the Pomodoro application
python build_atunafsi_pomodoro.py
```

---

## License

MIT License. See [LICENSE](LICENSE) for details.
