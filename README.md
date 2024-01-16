
---

# Chess Tournament Management Program

## Description
This Python application is designed for managing chess tournaments. It allows users to create tournaments, register players, enter match results, and generate tournament reports, all in an offline environment. The application is compatible with Windows and MacOS operating systems.

## Installation

### Prerequisites
- Python 3.x
- pip (Python package manager)

### Setup
1. Clone the repository to your local machine:
   ```
   git clone https://github.com/Ryu-134/P3-Application-Developer-Skills-Bootcamp.git
   ```
2. Navigate to the cloned directory:
   ```
   cd P3-Application-Developer-Skills-Bootcamp
   ```

## Running the Program
To start the program, run the following command in your terminal (Command Prompt on Windows, or Terminal on MacOS):
```
python manage_clubs.py
```

## Using the Program
- **Main Menu**: Navigate through options to view/manage tournaments, or create a new tournament.
- **Tournament Management**: 
  - Register players for a tournament.
  - Enter results for current round matches.
  - Advance to the next round.
  - Generate a tournament report.
- **Exiting**: Follow on-screen instructions to navigate back to the main menu or exit the program.

## Generating Flake8 Report
Ensure `flake8` and `flake8-html` are installed:
```
pip install flake8 flake8-html
```
Run `flake8` to generate a report:
```
flake8 --format=html --htmldir=flake8_report
```
The report will be saved in the `flake8_report` directory.

---

