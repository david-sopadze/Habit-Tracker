from habit_tracker.cli import run_cli
from habit_tracker.gui import run_gui


def main() -> None:
    mode = input("Start in GUI mode? (y/n): ").strip().lower()
    if mode in {"y", "yes"}:
        run_gui()
    else:
        run_cli()


if __name__ == "__main__":
    main()

