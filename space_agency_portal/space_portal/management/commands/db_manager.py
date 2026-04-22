"""
Space Portal DB Manager
========================
Add and delete records from the space_portal SQLite database.

Usage:
    python db_manager.py

Update DB_PATH to point to your db.sqlite3 file.
"""

import sqlite3
from datetime import datetime

DB_PATH = "db.sqlite3"  # <-- change this to your actual path


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # allows dict-style access
    return conn


# ─────────────────────────────────────────────
# MISSION
# ─────────────────────────────────────────────

def add_mission(name, slug, mission_type, status, launch_date,
                description, objectives, crew_count, agency,
                image_url="", end_date=None):
    """
    mission_type: 'lunar' | 'mars' | 'orbit' | 'deep_space'
    status:       'active' | 'completed' | 'planned'
    launch_date:  'YYYY-MM-DD'
    """
    conn = get_conn()
    conn.execute("""
        INSERT INTO space_portal_mission
            (name, slug, mission_type, status, launch_date, end_date,
             description, objectives, crew_count, agency, image_url, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, slug, mission_type, status, launch_date, end_date,
          description, objectives, crew_count, agency, image_url,
          datetime.utcnow().isoformat()))
    conn.commit()
    print(f"[+] Mission '{name}' added (id={conn.execute('SELECT last_insert_rowid()').fetchone()[0]})")
    conn.close()


def delete_mission(mission_id):
    conn = get_conn()
    conn.execute("DELETE FROM space_portal_astronaut_missions WHERE mission_id=?", (mission_id,))
    conn.execute("DELETE FROM space_portal_launch WHERE mission_id=?", (mission_id,))
    conn.execute("DELETE FROM space_portal_mission WHERE id=?", (mission_id,))
    conn.commit()
    print(f"[-] Mission id={mission_id} deleted (and related launches/astronaut links)")
    conn.close()


def list_missions():
    conn = get_conn()
    rows = conn.execute("SELECT id, name, status, mission_type, launch_date FROM space_portal_mission").fetchall()
    print("\n=== Missions ===")
    for r in rows:
        print(f"  [{r['id']}] {r['name']} | {r['mission_type']} | {r['status']} | {r['launch_date']}")
    conn.close()


# ─────────────────────────────────────────────
# ASTRONAUT
# ─────────────────────────────────────────────

def add_astronaut(name, nationality, status, bio, missions_count,
                  hours_in_space, rank, specialization,
                  birth_date=None, image_url=""):
    """
    status: 'active' | 'retired' | 'candidate'
    """
    conn = get_conn()
    conn.execute("""
        INSERT INTO space_portal_astronaut
            (name, nationality, status, bio, missions_count, hours_in_space,
             birth_date, rank, specialization, image_url, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, nationality, status, bio, missions_count, hours_in_space,
          birth_date, rank, specialization, image_url,
          datetime.utcnow().isoformat()))
    conn.commit()
    print(f"[+] Astronaut '{name}' added (id={conn.execute('SELECT last_insert_rowid()').fetchone()[0]})")
    conn.close()


def delete_astronaut(astronaut_id):
    conn = get_conn()
    conn.execute("DELETE FROM space_portal_astronaut_missions WHERE astronaut_id=?", (astronaut_id,))
    conn.execute("DELETE FROM space_portal_astronaut WHERE id=?", (astronaut_id,))
    conn.commit()
    print(f"[-] Astronaut id={astronaut_id} deleted")
    conn.close()


def assign_astronaut_to_mission(astronaut_id, mission_id):
    conn = get_conn()
    conn.execute("""
        INSERT INTO space_portal_astronaut_missions (astronaut_id, mission_id)
        VALUES (?, ?)
    """, (astronaut_id, mission_id))
    conn.commit()
    print(f"[+] Astronaut {astronaut_id} assigned to Mission {mission_id}")
    conn.close()


def list_astronauts():
    conn = get_conn()
    rows = conn.execute("SELECT id, name, nationality, status, rank FROM space_portal_astronaut").fetchall()
    print("\n=== Astronauts ===")
    for r in rows:
        print(f"  [{r['id']}] {r['name']} | {r['nationality']} | {r['status']} | {r['rank']}")
    conn.close()


# ─────────────────────────────────────────────
# LAUNCH
# ─────────────────────────────────────────────

def add_launch(rocket_name, launch_site, launch_datetime, status,
               notes, mission_id, countdown_target=None):
    """
    status:          'scheduled' | 'launched' | 'scrubbed' | 'failed'
    launch_datetime: 'YYYY-MM-DD HH:MM:SS'
    """
    conn = get_conn()
    conn.execute("""
        INSERT INTO space_portal_launch
            (rocket_name, launch_site, launch_datetime, status, notes, countdown_target, mission_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (rocket_name, launch_site, launch_datetime, status, notes, countdown_target, mission_id))
    conn.commit()
    print(f"[+] Launch '{rocket_name}' added (id={conn.execute('SELECT last_insert_rowid()').fetchone()[0]})")
    conn.close()


def delete_launch(launch_id):
    conn = get_conn()
    conn.execute("DELETE FROM space_portal_launch WHERE id=?", (launch_id,))
    conn.commit()
    print(f"[-] Launch id={launch_id} deleted")
    conn.close()


def list_launches():
    conn = get_conn()
    rows = conn.execute("SELECT id, rocket_name, launch_site, launch_datetime, status FROM space_portal_launch").fetchall()
    print("\n=== Launches ===")
    for r in rows:
        print(f"  [{r['id']}] {r['rocket_name']} | {r['launch_site']} | {r['launch_datetime']} | {r['status']}")
    conn.close()


# ─────────────────────────────────────────────
# NEWS ARTICLE
# ─────────────────────────────────────────────

def add_news_article(title, slug, category, summary, content,
                     is_featured=False, image_url="",
                     author_id=None, related_mission_id=None):
    """
    category: 'mission' | 'research' | 'technology' | 'general'
    """
    now = datetime.utcnow().isoformat()
    conn = get_conn()
    conn.execute("""
        INSERT INTO space_portal_newsarticle
            (title, slug, category, summary, content, published_at, updated_at,
             is_featured, image_url, author_id, related_mission_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (title, slug, category, summary, content, now, now,
          is_featured, image_url, author_id, related_mission_id))
    conn.commit()
    print(f"[+] News article '{title}' added (id={conn.execute('SELECT last_insert_rowid()').fetchone()[0]})")
    conn.close()


def delete_news_article(article_id):
    conn = get_conn()
    conn.execute("DELETE FROM space_portal_newsarticle WHERE id=?", (article_id,))
    conn.commit()
    print(f"[-] News article id={article_id} deleted")
    conn.close()


def list_news_articles():
    conn = get_conn()
    rows = conn.execute("SELECT id, title, category, published_at FROM space_portal_newsarticle").fetchall()
    print("\n=== News Articles ===")
    for r in rows:
        print(f"  [{r['id']}] {r['title']} | {r['category']} | {r['published_at']}")
    conn.close()


# ─────────────────────────────────────────────
# SPACECRAFT GALLERY
# ─────────────────────────────────────────────

def add_spacecraft(name, description, spacecraft_type, manufacturer,
                   first_flight=None, image_url="", mission_id=None):
    conn = get_conn()
    conn.execute("""
        INSERT INTO space_portal_spacecraftgallery
            (name, description, spacecraft_type, manufacturer, first_flight, image_url, mission_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, description, spacecraft_type, manufacturer, first_flight, image_url, mission_id))
    conn.commit()
    print(f"[+] Spacecraft '{name}' added (id={conn.execute('SELECT last_insert_rowid()').fetchone()[0]})")
    conn.close()


def delete_spacecraft(spacecraft_id):
    conn = get_conn()
    conn.execute("DELETE FROM space_portal_spacecraftgallery WHERE id=?", (spacecraft_id,))
    conn.commit()
    print(f"[-] Spacecraft id={spacecraft_id} deleted")
    conn.close()


def list_spacecraft():
    conn = get_conn()
    rows = conn.execute("SELECT id, name, spacecraft_type, manufacturer FROM space_portal_spacecraftgallery").fetchall()
    print("\n=== Spacecraft ===")
    for r in rows:
        print(f"  [{r['id']}] {r['name']} | {r['spacecraft_type']} | {r['manufacturer']}")
    conn.close()


# ─────────────────────────────────────────────
# CONTACT MESSAGE
# ─────────────────────────────────────────────

def add_contact_message(name, email, subject, message):
    conn = get_conn()
    conn.execute("""
        INSERT INTO space_portal_contactmessage
            (name, email, subject, message, submitted_at, is_read)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, email, subject, message, datetime.utcnow().isoformat(), False))
    conn.commit()
    print(f"[+] Contact message from '{name}' added")
    conn.close()


def delete_contact_message(message_id):
    conn = get_conn()
    conn.execute("DELETE FROM space_portal_contactmessage WHERE id=?", (message_id,))
    conn.commit()
    print(f"[-] Contact message id={message_id} deleted")
    conn.close()


def list_contact_messages():
    conn = get_conn()
    rows = conn.execute("SELECT id, name, email, subject, submitted_at FROM space_portal_contactmessage").fetchall()
    print("\n=== Contact Messages ===")
    for r in rows:
        print(f"  [{r['id']}] {r['name']} | {r['email']} | {r['subject']} | {r['submitted_at']}")
    conn.close()



# ─────────────────────────────────────────────
# DJANGO MANAGEMENT COMMAND
# ─────────────────────────────────────────────

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Add or delete space portal data'

    def handle(self, *args, **kwargs):

        # ── ADD a Mission ──
        add_mission(
            name="Europa Pathfinder II",
            slug="europa-pathfinder-ii",
            mission_type="deep_space",
            status="planned",
            launch_date="2028-03-10",
            description="Second mission to Europa.",
            objectives="Deploy ice probe.",
            crew_count=0,
            agency="COSMOSX Agency",
        )