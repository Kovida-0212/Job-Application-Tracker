# Job Application Tracker

A modern Flask + SQLite application for tracking job applications.

## Features

- Add job applications
- Track company and job role
- Application date
- Status: Applied / Assessment / Interview / Selected / Rejected
- Interview date
- Resume version
- Notes
- Search applications
- Filter by status
- Edit and delete applications
- Dashboard statistics
- Responsive Bootstrap UI
- No API keys required
- SQLite database

## 1. Open the project

Open this folder in VS Code.

## 2. Create a virtual environment (recommended)

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

If PowerShell blocks activation, you can simply use:

```bash
venv\Scripts\python.exe -m pip install -r requirements.txt
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Run the app

```bash
python app.py
```

You should see Flask start locally.

Open the browser at:

http://127.0.0.1:5000

## Database

SQLite is built into Python. The `job_tracker.db` file is automatically created the first time you run the application.

## Stop the server

Press:

```text
CTRL + C
```

## Project structure

```text
Job-Application-Tracker/
├── app.py
├── requirements.txt
├── README.md
├── job_tracker.db
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── applications.html
│   ├── add_application.html
│   ├── edit_application.html
│   └── view_application.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── script.js
```
