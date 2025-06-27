import sqlite3
from datetime import datetime, timedelta
import json

DATABASE_URL = "database.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            phone_number TEXT UNIQUE NOT NULL,
            in_game_preferences TEXT, -- Stored as JSON string
            character_id TEXT,
            otp_secret TEXT,
            otp_created_at DATETIME
        )
    ''')

    # Tournaments Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tournaments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            game TEXT NOT NULL,
            start_date DATETIME NOT NULL,
            end_date DATETIME NOT NULL,
            max_participants INTEGER,
            entry_fee REAL,
            prize_pool REAL,
            status TEXT NOT NULL, -- e.g., 'upcoming', 'active', 'completed'
            description TEXT,
            rules TEXT,
            format TEXT,
            platform TEXT,
            match_schedule TEXT, -- Stored as JSON string
            results TEXT -- Stored as JSON string
        )
    ''')

    # Add new columns if they don't exist (for existing databases)
    try:
        cursor.execute("ALTER TABLE tournaments ADD COLUMN description TEXT")
    except sqlite3.OperationalError:
        pass # Column already exists
    try:
        cursor.execute("ALTER TABLE tournaments ADD COLUMN rules TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE tournaments ADD COLUMN format TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE tournaments ADD COLUMN platform TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE tournaments ADD COLUMN match_schedule TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE tournaments ADD COLUMN results TEXT")
    except sqlite3.OperationalError:
        pass

    # Tournament Participants Table (Many-to-Many relationship)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tournament_participants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tournament_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            registration_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            status TEXT NOT NULL, -- e.g., 'registered', 'checked-in', 'eliminated'
            FOREIGN KEY (tournament_id) REFERENCES tournaments (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # Teams Table (New)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            captain_id INTEGER NOT NULL,
            members TEXT, -- Stored as JSON string of user IDs
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (captain_id) REFERENCES users (id)
        )
    ''')

    # News Table (New)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            author TEXT,
            published_date DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Add new columns to teams table if they don't exist
    try:
        cursor.execute("ALTER TABLE teams ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP")
    except sqlite3.OperationalError:
        pass

    conn.commit()
    conn.close()

def create_user(name: str, phone_number: str, email: str = None, in_game_preferences: dict = None, character_id: str = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (name, email, phone_number, in_game_preferences, character_id) VALUES (?, ?, ?, ?, ?)",
            (name, email, phone_number, json.dumps(in_game_preferences) if in_game_preferences else None, character_id)
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None # User with this phone_number or email already exists
    finally:
        conn.close()

def get_user_by_phone(phone_number: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE phone_number = ?", (phone_number,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_user_by_id(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_all_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

def delete_user(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

def update_user(user_id: int, name: str = None, email: str = None, in_game_preferences: dict = None, character_id: str = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    updates = []
    params = []
    if name is not None:
        updates.append("name = ?")
        params.append(name)
    if email is not None:
        updates.append("email = ?")
        params.append(email)
    if in_game_preferences is not None:
        updates.append("in_game_preferences = ?")
        params.append(json.dumps(in_game_preferences))
    if character_id is not None:
        updates.append("character_id = ?")
        params.append(character_id)

    if not updates:
        return False # No updates to perform

    query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
    params.append(user_id)

    cursor.execute(query, tuple(params))
    conn.commit()
    conn.close()
    return True

def update_user_otp(user_id: int, otp_secret: str, otp_created_at: datetime):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET otp_secret = ?, otp_created_at = ? WHERE id = ?",
        (otp_secret, otp_created_at, user_id)
    )
    conn.commit()
    conn.close()

def clear_user_otp(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET otp_secret = NULL, otp_created_at = NULL WHERE id = ?",
        (user_id,)
    )
    conn.commit()
    conn.close()

def create_tournament(name: str, game: str, start_date: datetime, end_date: datetime, max_participants: int, entry_fee: float, prize_pool: float, status: str, description: str = None, rules: str = None, format: str = None, platform: str = None, match_schedule: list = None, results: list = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tournaments (name, game, start_date, end_date, max_participants, entry_fee, prize_pool, status, description, rules, format, platform, match_schedule, results) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (name, game, start_date, end_date, max_participants, entry_fee, prize_pool, status, description, rules, format, platform, json.dumps(match_schedule) if match_schedule else None, json.dumps(results) if results else None)
    )
    conn.commit()
    conn.close()
    return cursor.lastrowid

def get_tournament_by_id(tournament_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tournaments WHERE id = ?", (tournament_id,))
    tournament = cursor.fetchone()
    conn.close()
    return tournament

def get_all_tournaments():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tournaments")
    tournaments = cursor.fetchall()
    conn.close()
    return tournaments

def update_tournament(tournament_id: int, name: str = None, game: str = None, start_date: datetime = None, end_date: datetime = None, max_participants: int = None, entry_fee: float = None, prize_pool: float = None, status: str = None, description: str = None, rules: str = None, format: str = None, platform: str = None, match_schedule: list = None, results: list = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    updates = []
    params = []
    if name is not None:
        updates.append("name = ?")
        params.append(name)
    if game is not None:
        updates.append("game = ?")
        params.append(game)
    if start_date is not None:
        updates.append("start_date = ?")
        params.append(start_date)
    if end_date is not None:
        updates.append("end_date = ?")
        params.append(end_date)
    if max_participants is not None:
        updates.append("max_participants = ?")
        params.append(max_participants)
    if entry_fee is not None:
        updates.append("entry_fee = ?")
        params.append(entry_fee)
    if prize_pool is not None:
        updates.append("prize_pool = ?")
        params.append(prize_pool)
    if status is not None:
        updates.append("status = ?")
        params.append(status)
    if description is not None:
        updates.append("description = ?")
        params.append(description)
    if rules is not None:
        updates.append("rules = ?")
        params.append(rules)
    if format is not None:
        updates.append("format = ?")
        params.append(format)
    if platform is not None:
        updates.append("platform = ?")
        params.append(platform)
    if match_schedule is not None:
        updates.append("match_schedule = ?")
        params.append(json.dumps(match_schedule))
    if results is not None:
        updates.append("results = ?")
        params.append(json.dumps(results))

    if not updates:
        return False

    query = f"UPDATE tournaments SET {', '.join(updates)} WHERE id = ?"
    params.append(tournament_id)

    cursor.execute(query, tuple(params))
    conn.commit()
    conn.close()
    return True

def delete_tournament(tournament_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tournaments WHERE id = ?", (tournament_id,))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

def register_for_tournament(tournament_id: int, user_id: int, status: str = "registered"):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO tournament_participants (tournament_id, user_id, status) VALUES (?, ?, ?)",
            (tournament_id, user_id, status)
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None # User already registered for this tournament
    finally:
        conn.close()

def get_all_tournament_participants():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tournament_participants")
    participants = cursor.fetchall()
    conn.close()
    return participants

def update_tournament_participant_status(participant_id: int, status: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tournament_participants SET status = ? WHERE id = ?",
        (status, participant_id)
    )
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

def create_team(name: str, captain_id: int, members: list = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO teams (name, captain_id, members) VALUES (?, ?, ?)",
            (name, captain_id, json.dumps(members) if members else None)
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None # Team with this name already exists
    finally:
        conn.close()

def get_team_by_id(team_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM teams WHERE id = ?", (team_id,))
    team = cursor.fetchone()
    conn.close()
    return team

def get_all_teams():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM teams")
    teams = cursor.fetchall()
    conn.close()
    return teams

def update_team(team_id: int, name: str = None, captain_id: int = None, members: list = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    updates = []
    params = []
    if name is not None:
        updates.append("name = ?")
        params.append(name)
    if captain_id is not None:
        updates.append("captain_id = ?")
        params.append(captain_id)
    if members is not None:
        updates.append("members = ?")
        params.append(json.dumps(members))

    if not updates:
        return False

    query = f"UPDATE teams SET {', '.join(updates)} WHERE id = ?"
    params.append(team_id)

    cursor.execute(query, tuple(params))
    conn.commit()
    conn.close()
    return True

def delete_team(team_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM teams WHERE id = ?", (team_id,))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

def create_news(title: str, content: str, author: str = None, published_date: datetime = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO news (title, content, author, published_date) VALUES (?, ?, ?, ?)",
        (title, content, author, published_date)
    )
    conn.commit()
    conn.close()
    return cursor.lastrowid

def get_news_by_id(news_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM news WHERE id = ?", (news_id,))
    news_article = cursor.fetchone()
    conn.close()
    return news_article

def get_all_news():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM news")
    all_news = cursor.fetchall()
    conn.close()
    return all_news

def update_news(news_id: int, title: str = None, content: str = None, author: str = None, published_date: datetime = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    updates = []
    params = []
    if title is not None:
        updates.append("title = ?")
        params.append(title)
    if content is not None:
        updates.append("content = ?")
        params.append(content)
    if author is not None:
        updates.append("author = ?")
        params.append(author)
    if published_date is not None:
        updates.append("published_date = ?")
        params.append(published_date)

    if not updates:
        return False

    query = f"UPDATE news SET {', '.join(updates)} WHERE id = ?"
    params.append(news_id)

    cursor.execute(query, tuple(params))
    conn.commit()
    conn.close()
    return True

def delete_news(news_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM news WHERE id = ?", (news_id,))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

# Initialize the database when this module is imported
init_db()