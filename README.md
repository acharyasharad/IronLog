# 🏋️ IronLog — Workout Logger

A clean workout tracking web app. Log exercises, track sets/reps/weight, and automatically surface your personal bests. Built with Python Flask + SQLite.

---

## ✨ Features

- 🏋️ Log workouts with multiple exercises per session
- 📊 Track sets, reps, and weight per exercise
- 🏆 Auto-calculated personal bests per exercise
- 📈 Lifetime stats — total workouts, sets, reps, kg lifted
- 📅 Date-based workout history
- 🗑️ Delete workouts or individual exercises

---

## 🛠 Tech Stack

| Layer    | Technology           |
|----------|----------------------|
| Backend  | Python, Flask        |
| Database | SQLite               |
| Frontend | HTML, CSS, Vanilla JS|

---

## 🚀 Getting Started

```bash
pip install -r requirements.txt
python app.py
```

Open **http://127.0.0.1:8083**

---

## 📁 Project Structure

```
workoutlogger/
├── app.py              # Flask backend — workouts, exercises, PB logic
├── templates/
│   └── index.html      # Frontend — log form, history, personal bests
├── requirements.txt
└── README.md
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/workouts` | All workouts with exercises |
| POST | `/api/workouts` | Create a workout |
| DELETE | `/api/workouts/:id` | Delete a workout |
| POST | `/api/workouts/:id/exercises` | Add exercise to workout |
| DELETE | `/api/exercises/:id` | Delete an exercise |
| GET | `/api/pbs` | Personal bests per exercise |
| GET | `/api/stats` | Lifetime stats |

---

## 💡 How to Extend

- Add **charts** showing weight progression over time per exercise
- Add **workout templates** (save a routine and reuse it)
- Add **body weight tracking**
- Add **export to CSV**
