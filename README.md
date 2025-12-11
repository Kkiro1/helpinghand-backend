# HelpingHand – Backend (Django + REST API)

This repository contains the **backend API** for the HelpingHand donation platform.  
The main goal of this project is to **practice real software engineering workflow**:

- Git branches, commits, and pull requests  
- GitHub Issues & Project board  
- GitHub Actions CI (running automated tests)  
- Clean and simple Django REST API

The frontend team can use these endpoints to build the UI.

---

## Tech Stack

- **Language:** Python 3.11
- **Framework:** Django + Django REST Framework
- **Auth:** JSON Web Tokens (SimpleJWT)
- **Database:** SQLite (for development and CI)
- **CI:** GitHub Actions (run Django tests on every push / PR)

---

## How to Run the Backend Locally

1. **Clone the repo**

```bash
git clone https://github.com/Kkiro1/helpinghand-backend.git
cd helpinghand-backend
