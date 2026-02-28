# Habit Tracker (OOP Python Project)

This project is a habit tracking application developed as part of an Object-Oriented Programming (OOP) portfolio assignment.

The goal of the project is to design and implement a modular, testable habit tracking system that supports different habit periodicities and provides analytical insights into user progress.

---

## Overview

The application allows users to create and manage habits with daily or weekly periodicities, track completion streaks, and analyze habit performance over time.  
It provides both a command-line interface (CLI) and an optional graphical user interface (GUI).

---

## Technologies Used

- Python
- Pytest (unit testing)
- JSON (data persistence)
- Tkinter (GUI)

---

## Features

- Create, edit, and delete habits
- Support for daily and weekly habit periodicities
- Streak tracking that respects habit periodicity
- Analytics functions:
  - List all habits
  - List habits by periodicity
  - Determine the longest streak overall
  - Determine the longest streak per habit
- Command-line interface (CLI)
- Optional graphical user interface (GUI) using Tkinter
- JSON-based data persistence
- Comprehensive unit test suite using pytest

---

## Project Structure

- `habit_tracker/` – Application source code (models, persistence, analytics, CLI/GUI)
- `tests/` – Unit test suite (pytest)
- `data.json` – Predefined fixture data used for testing and demonstration
- `docs/screenshots/` – Evidence screenshots (tests, CLI, GUI)

---

## Installation

1. Ensure Python 3.13 (or a compatible version) is installed.
2. Download or clone this repository from GitHub.
3. Open a terminal (PowerShell on Windows).
4. Navigate to the project root directory.

If `python` is not available on your system, you can use the Python launcher:

```bash
py --version