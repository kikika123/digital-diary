# Digital Diary 📝

A simple desktop **Digital Diary** built with **Python (Tkinter)** and **MySQL**.  
Users can register (with email OTP), log in, and create/open/save diary entries.

![GitHub repo size](https://img.shields.io/github/repo-size/kikika123/digital-diary)
![GitHub stars](https://img.shields.io/github/stars/kikika123/digital-diary?style=social)

---

## ✨ Features
- Account creation with **OTP email verification**
- **Login** and profile store (MySQL)
- Create / open / save diary entries
- Simple **Tkinter GUI**
- File persistence (pickle)

---

## 📦 Tech Stack
- Python 3.x, Tkinter
- MySQL (tables provided in `setup.sql`)
- SMTP (Outlook) for OTP
- `.env` + python-dotenv for credentials

---

## 🚀 Quick Start
```bash
git clone https://github.com/kikika123/digital-diary.git
cd digital-diary
python -m venv .venv
# Windows
.\.venv\Scripts\activate
pip install -r requirements.txt
