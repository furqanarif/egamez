import database
from datetime import datetime, timedelta

def add_sample_tournaments():
    sample_tournaments = [
        {
            "name": "Valorant Champions Tour 2025",
            "game": "Valorant",
            "start_date": datetime(2025, 7, 1, 10, 0, 0),
            "end_date": datetime(2025, 7, 15, 18, 0, 0),
            "max_participants": 32,
            "entry_fee": 0.0,
            "prize_pool": 1000000.0,
            "status": "upcoming",
            "description": "The premier Valorant tournament of the year, featuring top teams from around the globe.",
            "rules": "Standard VCT ruleset. Best of 3 matches, Grand Finals Best of 5.",
            "format": "Double Elimination",
            "platform": "PC",
            "match_schedule": [
                {"time": "2025-07-01T10:00:00Z", "team1": "Team Liquid", "team2": "Fnatic", "stream_link": "https://twitch.tv/valorant"},
                {"time": "2025-07-01T13:00:00Z", "team1": "Sentinels", "team2": "LOUD", "stream_link": "https://twitch.tv/valorant"}
            ],
            "results": []
        },
        {
            "name": "FIFA eWorld Cup 2025",
            "game": "FIFA",
            "start_date": datetime(2025, 8, 1, 9, 0, 0),
            "end_date": datetime(2025, 8, 7, 17, 0, 0),
            "max_participants": 64,
            "entry_fee": 50.0,
            "prize_pool": 500000.0,
            "status": "upcoming",
            "description": "The official FIFA esports tournament, bringing together the best virtual footballers.",
            "rules": "Official FIFA esports rules. Group stage followed by knockout bracket.",
            "format": "Group Stage + Single Elimination",
            "platform": "PlayStation 5",
            "match_schedule": [
                {"time": "2025-08-01T09:00:00Z", "player1": "MsDossary", "player2": "Tekkz", "stream_link": "https://youtube.com/fifaesports"}
            ],
            "results": []
        },
        {
            "name": "Tekken World Tour Finals 2025",
            "game": "Tekken",
            "start_date": datetime(2025, 9, 10, 11, 0, 0),
            "end_date": datetime(2025, 9, 12, 19, 0, 0),
            "max_participants": 16,
            "entry_fee": 0.0,
            "prize_pool": 250000.0,
            "status": "upcoming",
            "description": "The culmination of the Tekken World Tour, where the best players battle for supremacy.",
            "rules": "Standard Tekken competitive rules. Double elimination bracket.",
            "format": "Double Elimination",
            "platform": "PC",
            "match_schedule": [
                {"time": "2025-09-10T11:00:00Z", "player1": "Arslan Ash", "player2": "Knee", "stream_link": "https://twitch.tv/tekken"}
            ],
            "results": []
        },
        {
            "name": "League of Legends World Championship 2025",
            "game": "League of Legends",
            "start_date": datetime(2025, 10, 1, 12, 0, 0),
            "end_date": datetime(2025, 11, 5, 20, 0, 0),
            "max_participants": 24,
            "entry_fee": 0.0,
            "prize_pool": 2225000.0,
            "status": "upcoming",
            "description": "The pinnacle of League of Legends esports, where champions are crowned.",
            "rules": "Official LoL esports rules. Group stage, knockout stage, and grand finals.",
            "format": "Group Stage + Knockout",
            "platform": "PC",
            "match_schedule": [
                {"time": "2025-10-01T12:00:00Z", "team1": "T1", "team2": "Gen.G", "stream_link": "https://youtube.com/lolesports"}
            ],
            "results": []
        },
        {
            "name": "Dota 2 The International 2025",
            "game": "Dota 2",
            "start_date": datetime(2025, 8, 20, 10, 0, 0),
            "end_date": datetime(2025, 8, 25, 18, 0, 0),
            "max_participants": 18,
            "entry_fee": 0.0,
            "prize_pool": 30000000.0,
            "status": "upcoming",
            "description": "The largest Dota 2 tournament with the biggest prize pool in esports.",
            "rules": "Standard Dota 2 competitive rules. Group stage and double elimination playoffs.",
            "format": "Group Stage + Double Elimination",
            "platform": "PC",
            "match_schedule": [
                {"time": "2025-08-20T10:00:00Z", "team1": "Team Spirit", "team2": "Gaimin Gladiators", "stream_link": "https://twitch.tv/dota2"}
            ],
            "results": []
        },
        {
            "name": "CS2 Major Stockholm 2025",
            "game": "Counter-Strike 2",
            "start_date": datetime(2025, 11, 1, 10, 0, 0),
            "end_date": datetime(2025, 11, 10, 18, 0, 0),
            "max_participants": 24,
            "entry_fee": 0.0,
            "prize_pool": 1250000.0,
            "status": "upcoming",
            "description": "The next Counter-Strike 2 Major, hosted in Stockholm.",
            "rules": "Official CS2 Major rules. Swiss system group stage, single elimination playoffs.",
            "format": "Swiss + Single Elimination",
            "platform": "PC",
            "match_schedule": [
                {"time": "2025-11-01T10:00:00Z", "team1": "FaZe Clan", "team2": "Team Vitality", "stream_link": "https://twitch.tv/csgo"}
            ],
            "results": []
        },
        {
            "name": "Overwatch League Grand Finals 2025",
            "game": "Overwatch 2",
            "start_date": datetime(2025, 9, 20, 14, 0, 0),
            "end_date": datetime(2025, 9, 22, 20, 0, 0),
            "max_participants": 8,
            "entry_fee": 0.0,
            "prize_pool": 1500000.0,
            "status": "upcoming",
            "description": "The final showdown of the Overwatch League season.",
            "rules": "Official OWL rules. Double elimination bracket.",
            "format": "Double Elimination",
            "platform": "PC",
            "match_schedule": [
                {"time": "2025-09-20T14:00:00Z", "team1": "Seoul Dynasty", "team2": "San Francisco Shock", "stream_link": "https://youtube.com/overwatchleague"}
            ],
            "results": []
        },
        {
            "name": "Rocket League Championship Series 2025",
            "game": "Rocket League",
            "start_date": datetime(2025, 7, 25, 10, 0, 0),
            "end_date": datetime(2025, 7, 28, 18, 0, 0),
            "max_participants": 16,
            "entry_fee": 0.0,
            "prize_pool": 600000.0,
            "status": "upcoming",
            "description": "The biggest Rocket League tournament, featuring the best car soccer teams.",
            "rules": "Standard RLCS rules. Double elimination bracket.",
            "format": "Double Elimination",
            "platform": "PC",
            "match_schedule": [
                {"time": "2025-07-25T10:00:00Z", "team1": "Gen.G Mobil1 Racing", "team2": "Team BDS", "stream_link": "https://twitch.tv/rocketleague"}
            ],
            "results": []
        },
        {
            "name": "Apex Legends Global Series Championship 2025",
            "game": "Apex Legends",
            "start_date": datetime(2025, 9, 1, 13, 0, 0),
            "end_date": datetime(2025, 9, 5, 19, 0, 0),
            "max_participants": 40,
            "entry_fee": 0.0,
            "prize_pool": 2000000.0,
            "status": "upcoming",
            "description": "The ultimate Apex Legends competition, where teams fight for global supremacy.",
            "rules": "Official ALGS rules. Group stage and bracket stage.",
            "format": "Group Stage + Bracket",
            "platform": "PC",
            "match_schedule": [
                {"time": "2025-09-01T13:00:00Z", "team1": "TSM", "team2": "DarkZero Esports", "stream_link": "https://twitch.tv/playapex"}
            ],
            "results": []
        },
        {
            "name": "Street Fighter 6 Capcom Cup XI",
            "game": "Street Fighter 6",
            "start_date": datetime(2025, 12, 1, 10, 0, 0),
            "end_date": datetime(2025, 12, 3, 18, 0, 0),
            "max_participants": 48,
            "entry_fee": 0.0,
            "prize_pool": 1000000.0,
            "status": "upcoming",
            "description": "The biggest fighting game tournament of the year, featuring the best Street Fighter players.",
            "rules": "Standard FGC rules. Double elimination bracket.",
            "format": "Double Elimination",
            "platform": "PC",
            "match_schedule": [
                {"time": "2025-12-01T10:00:00Z", "player1": "MenaRD", "player2": "Tokido", "stream_link": "https://twitch.tv/capcomfighters"}
            ],
            "results": []
        },
        {
            "name": "Call of Duty League Championship 2025",
            "game": "Call of Duty",
            "start_date": datetime(2025, 6, 20, 15, 0, 0),
            "end_date": datetime(2025, 6, 23, 21, 0, 0),
            "max_participants": 12,
            "entry_fee": 0.0,
            "prize_pool": 2000000.0,
            "status": "completed",
            "description": "The ultimate Call of Duty esports event, crowning the season's champion.",
            "rules": "Official CDL rules. Double elimination bracket.",
            "format": "Double Elimination",
            "platform": "PlayStation 5",
            "match_schedule": [
                {"time": "2025-06-20T15:00:00Z", "team1": "Atlanta FaZe", "team2": "OpTic Texas", "stream_link": "https://youtube.com/codleague"}
            ],
            "results": [
                {"match": "Grand Finals", "winner": "Atlanta FaZe"}
            ]
        },
        {
            "name": "PUBG Global Championship 2025",
            "game": "PUBG: Battlegrounds",
            "start_date": datetime(2025, 11, 15, 12, 0, 0),
            "end_date": datetime(2025, 11, 20, 18, 0, 0),
            "max_participants": 32,
            "entry_fee": 0.0,
            "prize_pool": 2000000.0,
            "status": "upcoming",
            "description": "The biggest PUBG tournament, where teams battle for chicken dinners.",
            "rules": "Official PGC rules. Group stage and grand finals.",
            "format": "Group Stage + Grand Finals",
            "platform": "PC",
            "match_schedule": [
                {"time": "2025-11-15T12:00:00Z", "team1": "Gen.G", "team2": "FaZe Clan", "stream_link": "https://twitch.tv/pubg"}
            ],
            "results": []
        },
        {
            "name": "Free Fire World Series 2025",
            "game": "Free Fire",
            "start_date": datetime(2025, 10, 20, 14, 0, 0),
            "end_date": datetime(2025, 10, 25, 19, 0, 0),
            "max_participants": 18,
            "entry_fee": 0.0,
            "prize_pool": 1000000.0,
            "status": "upcoming",
            "description": "The global championship for Free Fire, mobile battle royale.",
            "rules": "Official FFWS rules. Group stage and grand finals.",
            "format": "Group Stage + Grand Finals",
            "platform": "Mobile",
            "match_schedule": [
                {"time": "2025-10-20T14:00:00Z", "team1": "EVOS Esports", "team2": "Team Flash", "stream_link": "https://youtube.com/freefireesports"}
            ],
            "results": []
        },
        {
            "name": "Mobile Legends: Bang Bang World Championship 2025",
            "game": "Mobile Legends: Bang Bang",
            "start_date": datetime(2025, 12, 10, 10, 0, 0),
            "end_date": datetime(2025, 12, 15, 18, 0, 0),
            "max_participants": 16,
            "entry_fee": 0.0,
            "prize_pool": 800000.0,
            "status": "upcoming",
            "description": "The M-Series World Championship for Mobile Legends: Bang Bang.",
            "rules": "Official MLBB rules. Group stage and double elimination playoffs.",
            "format": "Group Stage + Double Elimination",
            "platform": "Mobile",
            "match_schedule": [
                {"time": "2025-12-10T10:00:00Z", "team1": "Blacklist International", "team2": "ECHO", "stream_link": "https://youtube.com/mobilelegendsbangbang"}
            ],
            "results": []
        },
        {
            "name": "Clash Royale League World Finals 2025",
            "game": "Clash Royale",
            "start_date": datetime(2025, 9, 5, 11, 0, 0),
            "end_date": datetime(2025, 9, 7, 17, 0, 0),
            "max_participants": 8,
            "entry_fee": 0.0,
            "prize_pool": 500000.0,
            "status": "upcoming",
            "description": "The global championship for Clash Royale.",
            "rules": "Official CRL rules. Double elimination bracket.",
            "format": "Double Elimination",
            "platform": "Mobile",
            "match_schedule": [
                {"time": "2025-09-05T11:00:00Z", "player1": "Mohamed Light", "player2": "Mortar", "stream_link": "https://youtube.com/clashroyale"}
            ],
            "results": []
        },
        {
            "name": "Brawl Stars World Finals 2025",
            "game": "Brawl Stars",
            "start_date": datetime(2025, 11, 25, 13, 0, 0),
            "end_date": datetime(2025, 11, 28, 19, 0, 0),
            "max_participants": 16,
            "entry_fee": 0.0,
            "prize_pool": 1000000.0,
            "status": "upcoming",
            "description": "The global championship for Brawl Stars.",
            "rules": "Official Brawl Stars rules. Group stage and knockout bracket.",
            "format": "Group Stage + Knockout",
            "platform": "Mobile",
            "match_schedule": [
                {"time": "2025-11-25T13:00:00Z", "team1": "SK Gaming", "team2": "Tribe Gaming", "stream_link": "https://youtube.com/brawlstars"}
            ],
            "results": []
        },
        {
            "name": "Wild Rift Global Championship 2025",
            "game": "League of Legends: Wild Rift",
            "start_date": datetime(2025, 10, 5, 10, 0, 0),
            "end_date": datetime(2025, 10, 10, 18, 0, 0),
            "max_participants": 12,
            "entry_fee": 0.0,
            "prize_pool": 700000.0,
            "status": "upcoming",
            "description": "The global championship for League of Legends: Wild Rift.",
            "rules": "Official Wild Rift rules. Group stage and knockout bracket.",
            "format": "Group Stage + Knockout",
            "platform": "Mobile",
            "match_schedule": [
                {"time": "2025-10-05T10:00:00Z", "team1": "FunPlus Phoenix", "team2": "Team Secret", "stream_link": "https://youtube.com/wildriftesports"}
            ],
            "results": []
        },
        {
            "name": "Honor of Kings International Championship 2025",
            "game": "Honor of Kings",
            "start_date": datetime(2025, 12, 20, 12, 0, 0),
            "end_date": datetime(2025, 12, 25, 20, 0, 0),
            "max_participants": 16,
            "entry_fee": 0.0,
            "prize_pool": 10000000.0,
            "status": "upcoming",
            "description": "The biggest Honor of Kings tournament, featuring top teams from around the world.",
            "rules": "Official HOK rules. Group stage and knockout bracket.",
            "format": "Group Stage + Knockout",
            "platform": "Mobile",
            "match_schedule": [
                {"time": "2025-12-20T12:00:00Z", "team1": "eStar Pro", "team2": "Wolves Esports", "stream_link": "https://youtube.com/honorofkings"}
            ],
            "results": []
        },
        {
            "name": "Garena Premier League 2025",
            "game": "League of Legends",
            "start_date": datetime(2025, 7, 1, 10, 0, 0),
            "end_date": datetime(2025, 7, 30, 18, 0, 0),
            "max_participants": 8,
            "entry_fee": 0.0,
            "prize_pool": 100000.0,
            "status": "active",
            "description": "Regional League of Legends tournament for Southeast Asia.",
            "rules": "Standard LoL competitive rules.",
            "format": "Round Robin + Playoffs",
            "platform": "PC",
            "match_schedule": [
                {"time": "2025-07-01T10:00:00Z", "team1": "Team Flash", "team2": "Saigon Buffalo", "stream_link": "https://twitch.tv/garena"}
            ],
            "results": []
        },
        {
            "name": "ESL One Cologne 2025",
            "game": "Counter-Strike 2",
            "start_date": datetime(2025, 8, 15, 10, 0, 0),
            "end_date": datetime(2025, 8, 20, 18, 0, 0),
            "max_participants": 16,
            "entry_fee": 0.0,
            "prize_pool": 400000.0,
            "status": "upcoming",
            "description": "One of the most prestigious CS2 tournaments of the year.",
            "rules": "Standard ESL rules. Group stage and single elimination playoffs.",
            "format": "Group Stage + Single Elimination",
            "platform": "PC",
            "match_schedule": [
                {"time": "2025-08-15T10:00:00Z", "team1": "G2 Esports", "team2": "Natus Vincere", "stream_link": "https://twitch.tv/esl_csgo"}
            ],
            "results": []
        },
        {
            "name": "DreamHack Masters Dallas 2025",
            "game": "Counter-Strike 2",
            "start_date": datetime(2025, 6, 1, 10, 0, 0),
            "end_date": datetime(2025, 6, 5, 18, 0, 0),
            "max_participants": 16,
            "entry_fee": 0.0,
            "prize_pool": 250000.0,
            "status": "completed",
            "description": "A major CS2 tournament part of the DreamHack Masters series.",
            "rules": "Standard DreamHack rules.",
            "format": "Group Stage + Single Elimination",
            "platform": "PC",
            "match_schedule": [
                {"time": "2025-06-01T10:00:00Z", "team1": "Cloud9", "team2": "FURIA Esports", "stream_link": "https://twitch.tv/dreamhackcs"}
            ],
            "results": [
                {"match": "Grand Finals", "winner": "Cloud9"}
            ]
        }
    ]

    for tournament_data in sample_tournaments:
        try:
            database.create_tournament(**tournament_data)
            print(f"Added tournament: {tournament_data['name']}")
        except Exception as e:
            print(f"Error adding tournament {tournament_data['name']}: {e}")

if __name__ == "__main__":
    add_sample_tournaments()
