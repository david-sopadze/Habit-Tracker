\# Habit Tracker (OOP Python Project)



This project is a habit tracking application developed as part of an Object-Oriented Programming portfolio assignment.



\## Overview



The application allows users to create and manage habits with different periodicities and track their progress over time.



\## Technologies Used



\- Python

\- Pytest

\- JSON for data persistence

\- Tkinter (GUI)



\## Features



\- Create, edit, and delete habits

\- Support for daily and weekly habit periodicities

\- Streak tracking that respects habit periodicity

\- Analytics functions:

  - List all habits

  - List habits by periodicity

  - Determine the longest streak overall

  - Determine the longest streak per habit

\- Command-line interface (CLI)

\- Graphical user interface (GUI) using Tkinter

\- JSON-based data persistence

\- Unit tests using pytest



\## Project Structure



\- `habit\_tracker/` - Application source code (models, persistence, analytics, CLI/GUI)

\- `tests/` - Unit test suite (pytest)

\- `data.json` - Predefined fixture data used for testing and demonstration

## Running the Application

The application starts in command-line mode and allows the user to optionally launch the graphical interface (GUI).

From the project root directory, run:

```bash
py main.py

