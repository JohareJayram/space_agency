# 🛸 COSMOSX — Space Agency Information Portal

A fully responsive and interactive web portal for a fictional Space Agency, built with:
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Backend**: Python Django 4.2
- **Database**: SQLite3

---

## 🚀 Project Structure

```
space_agency_portal/
├── manage.py
├── requirements.txt
├── db.sqlite3               ← auto-created on first run
├── space_agency_portal/     ← Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── space_portal/            ← Main Django app
│   ├── models.py            ← Database models
│   ├── views.py             ← Page views
│   ├── urls.py              ← URL routing
│   ├── forms.py             ← Forms
│   ├── admin.py             ← Admin panel config
│   └── management/
│       └── commands/
│           └── seed_data.py ← Sample data seeder
├── templates/               ← HTML templates
│   ├── base.html
│   ├── space_portal/
│   │   ├── home.html
│   │   ├── missions.html
│   │   ├── mission_detail.html
│   │   ├── astronauts.html
│   │   ├── astronaut_detail.html
│   │   ├── launches.html
│   │   ├── news.html
│   │   ├── news_detail.html
│   │   ├── gallery.html
│   │   ├── contact.html
│   │   └── about.html
│   └── registration/
│       ├── login.html
│       └── register.html
└── static/
    ├── css/main.css
    └── js/main.js
```

---

## ⚙️ Setup Instructions

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)

### Step-by-Step Installation

**1. Navigate into the project folder:**
```bash
cd space_agency_portal
```

**2. Create a virtual environment:**
```bash
python -m venv venv
```

**3. Activate the virtual environment:**
```bash
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

**4. Install dependencies:**
```bash
pip install -r requirements.txt
```

**5. Run database migrations:**
```bash
python manage.py makemigrations
python manage.py migrate
```

**6. Seed the database with sample data:**
```bash
python manage.py seed_data
```

**7. Start the development server:**
```bash
python manage.py runserver
```

**8. Open your browser:**
```
http://127.0.0.1:8000/
```

---

## 🔑 Admin Access

After running `seed_data`, an admin account is created:

| Field    | Value      |
|----------|------------|
| URL      | http://127.0.0.1:8000/admin/ |
| Username | `admin`    |
| Password | `admin123` |

---

## 📄 Pages & Features

| Page | URL | Description |
|------|-----|-------------|
| Home | `/` | Hero section, stats, active missions, launches, news |
| Missions | `/missions/` | Filterable mission catalog with search |
| Mission Detail | `/missions/<slug>/` | Full mission page with crew & launches |
| Astronauts | `/astronauts/` | Crew roster with filter/search |
| Astronaut Detail | `/astronauts/<id>/` | Full profile with bio & missions |
| Launches | `/launches/` | Countdown timers for upcoming launches |
| News | `/news/` | Filterable news archive |
| News Detail | `/news/<slug>/` | Full article with related posts |
| Gallery | `/gallery/` | Spacecraft & vehicle gallery |
| About | `/about/` | Agency info, values, timeline |
| Contact | `/contact/` | Contact form (saved to DB) |
| Login | `/login/` | User authentication |
| Register | `/register/` | New user registration |
| Admin | `/admin/` | Django admin panel |

---

## 🗄️ Database Models

- **Mission** — Space missions with status, type, crew count, dates
- **Astronaut** — Crew profiles with bio, stats, mission assignments
- **Launch** — Launch events with countdown support
- **NewsArticle** — News and mission briefings
- **SpacecraftGallery** — Vehicle/spacecraft profiles
- **ContactMessage** — Messages submitted via contact form

---

## 🎨 Design Features

- **Dark space theme** with cyan accent lighting effects
- **Orbitron** display font for that sci-fi feel
- **Animated star field** background
- **Glowing orbit rings** on the hero section
- **Live countdown timers** for upcoming launches
- **Animated stat counters** on scroll
- **Scroll fade-in animations** for all elements
- **Mission Stats doughnut chart** (Chart.js)
- **Fully responsive** — mobile, tablet, desktop

---

## 🛠️ Technologies Used

| Technology | Purpose |
|-----------|---------|
| Django 4.2 | Backend framework, ORM, routing, auth |
| SQLite3 | Database (zero-config, file-based) |
| Bootstrap 5.3 | Responsive grid & UI components |
| Custom CSS | Space theme, animations, variables |
| Vanilla JS | Countdown timers, scroll animations, counters |
| Chart.js 4 | Mission statistics doughnut chart |
| Google Fonts | Orbitron + Exo 2 typography |
| Bootstrap Icons | Icon library |

---

## 📝 Notes

- The project uses SQLite — no database server needed
- All static assets load from CDN (internet required for fonts/icons)
- Media uploads are stored in `/media/` folder
- Change `SECRET_KEY` and set `DEBUG=False` for any production deployment
