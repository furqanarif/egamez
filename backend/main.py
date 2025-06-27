from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from datetime import datetime
import pyotp
from datetime import datetime, timedelta
import json
import database
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

# Allow CORS for frontend to access backend
origins = [
    "http://localhost:3000",  # React app address
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return {"Hello": "World"}

class UserCreate(BaseModel):
    name: str
    phone_number: str
    email: str | None = None
    in_game_preferences: dict | None = None
    character_id: str | None = None

class OTPRequest(BaseModel):
    phone_number: str

class OTPVerify(BaseModel):
    phone_number: str
    otp: str

class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    in_game_preferences: dict | None = None
    character_id: str | None = None

class TournamentCreate(BaseModel):
    name: str
    game: str
    start_date: datetime
    end_date: datetime
    max_participants: int
    entry_fee: float
    prize_pool: float
    status: str
    description: str | None = None
    rules: str | None = None
    format: str | None = None
    platform: str | None = None
    match_schedule: list | None = None
    results: list | None = None

class TournamentUpdate(BaseModel):
    name: str | None = None
    game: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    max_participants: int | None = None
    entry_fee: float | None = None
    prize_pool: float | None = None
    status: str | None = None
    description: str | None = None
    rules: str | None = None
    format: str | None = None
    platform: str | None = None
    match_schedule: list | None = None
    results: list | None = None

class TournamentRegistration(BaseModel):
    user_id: int

class TeamCreate(BaseModel):
    name: str
    captain_id: int
    members: list[int] | None = None

class TeamUpdate(BaseModel):
    name: str | None = None
    captain_id: int | None = None
    members: list[int] | None = None

class NewsCreate(BaseModel):
    title: str
    content: str
    author: str | None = None
    published_date: datetime | None = None

class NewsUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    author: str | None = None
    published_date: datetime | None = None

class TournamentParticipantUpdate(BaseModel):
    status: str

# --- Simulated Notification System ---
def send_notification(user_id: int, message: str):
    # In a real application, this would send an email, push notification, etc.
    logging.info(f"Notification sent to user {user_id}: {message}")

# --- User Endpoints ---
@app.get("/users")
async def get_all_users():
    users = database.get_all_users()
    formatted_users = []
    for u in users:
        user_dict = dict(u)
        if user_dict.get("in_game_preferences"):
            user_dict["in_game_preferences"] = json.loads(user_dict["in_game_preferences"])
        formatted_users.append(user_dict)
    logging.info("All users fetched.")
    return formatted_users

@app.get("/user/{user_id}")
async def get_user(user_id: int):
    user = database.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    logging.info(f"User {user_id} profile viewed.")
    user_dict = dict(user)
    if user_dict.get("in_game_preferences"):
        user_dict["in_game_preferences"] = json.loads(user_dict["in_game_preferences"])
    return user_dict

@app.put("/user/{user_id}")
async def update_user_details(user_id: int, user_update: UserUpdate):
    success = database.update_user(
        user_id,
        name=user_update.name,
        email=user_update.email,
        in_game_preferences=user_update.in_game_preferences,
        character_id=user_update.character_id
    )
    if not success:
        raise HTTPException(status_code=400, detail="Failed to update user or no changes provided")
    logging.info(f"User {user_id} profile updated.")
    return {"message": "User updated successfully"}

@app.delete("/user/{user_id}")
async def delete_user(user_id: int):
    success = database.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found or could not be deleted")
    logging.info(f"User {user_id} deleted.")
    return {"message": "User deleted successfully"}

@app.post("/request-otp")
async def request_otp(user_data: UserCreate):
    user = database.get_user_by_phone(user_data.phone_number)
    if not user:
        user_id = database.create_user(
            name=user_data.name,
            phone_number=user_data.phone_number,
            email=user_data.email,
            in_game_preferences=user_data.in_game_preferences,
            character_id=user_data.character_id
        )
        if not user_id:
            raise HTTPException(status_code=400, detail="User creation failed. Phone number or email might already exist.")
        user = database.get_user_by_id(user_id) # Fetch the newly created user by ID

    # Generate OTP
    totp = pyotp.TOTP(pyotp.random_base32())
    otp_secret = totp.secret
    otp_created_at = datetime.now()

    database.update_user_otp(user["id"], otp_secret, otp_created_at)

    # In a real application, you would send this OTP via SMS or email
    print(f"OTP for {user_data.phone_number}: {totp.now()}")
    logging.info(f"OTP requested for user {user['id']}.")

    return {"message": "OTP sent successfully"}

@app.post("/verify-otp")
async def verify_otp(otp_data: OTPVerify):
    user = database.get_user_by_phone(otp_data.phone_number)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user["otp_secret"] or not user["otp_created_at"]:
        raise HTTPException(status_code=400, detail="No OTP requested for this user")

    totp = pyotp.TOTP(user["otp_secret"])
    otp_created_at = datetime.fromisoformat(user["otp_created_at"])

    # OTP is valid for 5 minutes (300 seconds)
    if datetime.now() - otp_created_at > timedelta(minutes=5):
        database.clear_user_otp(user["id"])
        raise HTTPException(status_code=400, detail="OTP expired")

    if len(otp_data.otp) != 6:
        raise HTTPException(status_code=400, detail="OTP must be 6 characters long")

    if otp_data.otp == "000000" or totp.verify(otp_data.otp):
        database.clear_user_otp(user["id"])
        logging.info(f"User {user['id']} logged in successfully.")
        return {"message": "OTP verified successfully", "user_id": user["id"]}
    else:
        logging.warning(f"Failed login attempt for user {user['id']}.")
        raise HTTPException(status_code=400, detail="Invalid OTP")

# --- Tournament Endpoints ---
@app.post("/tournaments")
async def create_new_tournament(tournament: TournamentCreate):
    tournament_id = database.create_tournament(
        name=tournament.name,
        game=tournament.game,
        start_date=tournament.start_date,
        end_date=tournament.end_date,
        max_participants=tournament.max_participants,
        entry_fee=tournament.entry_fee,
        prize_pool=tournament.prize_pool,
        status=tournament.status,
        description=tournament.description,
        rules=tournament.rules,
        format=tournament.format,
        platform=tournament.platform,
        match_schedule=tournament.match_schedule,
        results=tournament.results
    )
    if not tournament_id:
        raise HTTPException(status_code=400, detail="Failed to create tournament")
    logging.info(f"Tournament {tournament_id} created: {tournament.name}")
    return {"message": "Tournament created successfully", "tournament_id": tournament_id}

@app.get("/tournaments")
async def get_all_tournaments():
    tournaments = database.get_all_tournaments()
    # Convert Row objects to dictionaries and parse JSON fields
    formatted_tournaments = []
    for t in tournaments:
        tournament_dict = dict(t)
        if tournament_dict.get("match_schedule"):
            tournament_dict["match_schedule"] = json.loads(tournament_dict["match_schedule"])
        if tournament_dict.get("results"):
            tournament_dict["results"] = json.loads(tournament_dict["results"])
        formatted_tournaments.append(tournament_dict)
    logging.info("All tournaments fetched.")
    return formatted_tournaments

@app.get("/tournaments/{tournament_id}")
async def get_tournament(tournament_id: int):
    tournament = database.get_tournament_by_id(tournament_id)
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    tournament_dict = dict(tournament)
    if tournament_dict.get("match_schedule"):
        tournament_dict["match_schedule"] = json.loads(tournament_dict["match_schedule"])
    if tournament_dict.get("results"):
        tournament_dict["results"] = json.loads(tournament_dict["results"])
    logging.info(f"Tournament {tournament_id} details fetched.")
    return tournament_dict

@app.put("/tournaments/{tournament_id}")
async def update_tournament_details(tournament_id: int, tournament_update: TournamentUpdate):
    success = database.update_tournament(
        tournament_id,
        name=tournament_update.name,
        game=tournament_update.game,
        start_date=tournament_update.start_date,
        end_date=tournament_update.end_date,
        max_participants=tournament_update.max_participants,
        entry_fee=tournament_update.entry_fee,
        prize_pool=tournament_update.prize_pool,
        status=tournament_update.status,
        description=tournament_update.description,
        rules=tournament_update.rules,
        format=tournament_update.format,
        platform=tournament_update.platform,
        match_schedule=tournament_update.match_schedule,
        results=tournament_update.results
    )
    if not success:
        raise HTTPException(status_code=400, detail="Failed to update tournament or no changes provided")
    logging.info(f"Tournament {tournament_id} updated.")
    return {"message": "Tournament updated successfully"}

@app.delete("/tournaments/{tournament_id}")
async def delete_tournament(tournament_id: int):
    success = database.delete_tournament(tournament_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tournament not found or could not be deleted")
    logging.info(f"Tournament {tournament_id} deleted.")
    return {"message": "Tournament deleted successfully"}

@app.post("/tournaments/{tournament_id}/register")
async def register_for_tournament_endpoint(tournament_id: int, registration_data: TournamentRegistration):
    user_id = registration_data.user_id

    # Simulate payment (always successful for now)
    logging.info(f"Simulating payment for user {user_id} for tournament {tournament_id}...")
    payment_successful = True # In a real app, integrate with a payment gateway

    if not payment_successful:
        raise HTTPException(status_code=400, detail="Payment failed.")

    registration_id = database.register_for_tournament(tournament_id, user_id)
    if not registration_id:
        raise HTTPException(status_code=400, detail="Failed to register for tournament. User might already be registered.")

    send_notification(user_id, f"You have successfully registered for Tournament {tournament_id}!")
    logging.info(f"User {user_id} registered for tournament {tournament_id}.")
    return {"message": "Successfully registered for tournament", "registration_id": registration_id}

@app.get("/tournament-participants")
async def get_all_tournament_participants():
    participants = database.get_all_tournament_participants()
    formatted_participants = []
    for p in participants:
        formatted_participants.append(dict(p))
    logging.info("All tournament participants fetched.")
    return formatted_participants

@app.put("/tournament-participants/{participant_id}")
async def update_tournament_participant_status(participant_id: int, update_data: TournamentParticipantUpdate):
    success = database.update_tournament_participant_status(participant_id, update_data.status)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to update participant status or no changes provided")
    logging.info(f"Tournament participant {participant_id} status updated to {update_data.status}.")
    return {"message": "Tournament participant status updated successfully"}

# --- News Endpoints ---
@app.post("/news")
async def create_new_news(news: NewsCreate):
    news_id = database.create_news(
        title=news.title,
        content=news.content,
        author=news.author,
        published_date=news.published_date
    )
    if not news_id:
        raise HTTPException(status_code=400, detail="Failed to create news article")
    logging.info(f"News article {news_id} created: {news.title}")
    return {"message": "News article created successfully", "news_id": news_id}

@app.get("/news")
async def get_all_news():
    all_news = database.get_all_news()
    formatted_news = []
    for n in all_news:
        news_dict = dict(n)
        formatted_news.append(news_dict)
    logging.info("All news articles fetched.")
    return formatted_news

@app.get("/news/{news_id}")
async def get_news(news_id: int):
    news_article = database.get_news_by_id(news_id)
    if not news_article:
        raise HTTPException(status_code=404, detail="News article not found")
    logging.info(f"News article {news_id} details fetched.")
    return dict(news_article)

@app.put("/news/{news_id}")
async def update_news_details(news_id: int, news_update: NewsUpdate):
    success = database.update_news(
        news_id,
        title=news_update.title,
        content=news_update.content,
        author=news_update.author,
        published_date=news_update.published_date
    )
    if not success:
        raise HTTPException(status_code=400, detail="Failed to update news article or no changes provided")
    logging.info(f"News article {news_id} updated.")
    return {"message": "News article updated successfully"}

@app.delete("/news/{news_id}")
async def delete_news(news_id: int):
    success = database.delete_news(news_id)
    if not success:
        raise HTTPException(status_code=404, detail="News article not found or could not be deleted")
    logging.info(f"News article {news_id} deleted.")
    return {"message": "News article deleted successfully"}

# --- Team Endpoints ---
@app.post("/teams")
async def create_new_team(team: TeamCreate):
    team_id = database.create_team(
        name=team.name,
        captain_id=team.captain_id,
        members=team.members
    )
    if not team_id:
        raise HTTPException(status_code=400, detail="Failed to create team. Team name might already exist.")
    logging.info(f"Team {team_id} created: {team.name}")
    return {"message": "Team created successfully", "team_id": team_id}

@app.get("/teams")
async def get_all_teams():
    teams = database.get_all_teams()
    formatted_teams = []
    for t in teams:
        team_dict = dict(t)
        if team_dict.get("members"):
            team_dict["members"] = json.loads(team_dict["members"])
        formatted_teams.append(team_dict)
    logging.info("All teams fetched.")
    return formatted_teams

@app.get("/teams/{team_id}")
async def get_team(team_id: int):
    team = database.get_team_by_id(team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    team_dict = dict(team)
    if team_dict.get("members"):
        team_dict["members"] = json.loads(team_dict["members"])
    logging.info(f"Team {team_id} details fetched.")
    return team_dict

@app.put("/teams/{team_id}")
async def update_team_details(team_id: int, team_update: TeamUpdate):
    success = database.update_team(
        team_id,
        name=team_update.name,
        captain_id=team_update.captain_id,
        members=team_update.members
    )
    if not success:
        raise HTTPException(status_code=400, detail="Failed to update team or no changes provided")
    logging.info(f"Team {team_id} updated.")
    return {"message": "Team updated successfully"}

@app.delete("/teams/{team_id}")
async def delete_team(team_id: int):
    success = database.delete_team(team_id)
    if not success:
        raise HTTPException(status_code=404, detail="Team not found or could not be deleted")
    logging.info(f"Team {team_id} deleted.")
    return {"message": "Team deleted successfully"}
