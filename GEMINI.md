# Project Overview
This is a full-stack web application for e-sports, likely serving as a tournament management or news platform, now named eGamez.

## Technology Stack
- **Backend:** Python with FastAPI
- **Frontend:** React (JavaScript)

## Key Directories
- `backend/`: Contains the Python FastAPI application.
- `frontend/`: Contains the React web application.

## How to Run/Develop
### Backend
1. Navigate to the `backend/` directory.
2. Install dependencies: `pip install -r requirements.txt` (preferably in a virtual environment).
3. Run the application: `uvicorn main:app --reload`

### Frontend
1. Navigate to the `frontend/` directory.
2. Install dependencies: `npm install`
3. Run the application: `npm start`

## Recent Changes
- **Site Name:** Changed from 'eGameUnity'/'eGameValhalla' to 'eGamez' site-wide.
- **Backend Features:** Implemented OTP-based login/registration and user profile management with SQLite database.
- **Frontend Enhancements:**
    - Footer updated with more content, quick links, and social media placeholders.
    - Mobile navigation toggle now changes icon on click.
    - Hover (bright pink) and active (bright yellow) effects added to all header items and Call-to-Action (CTA) buttons.

## Expectations for Gemini CLI
- Adhere to existing code conventions and style.
- Prioritize safe and verified changes.
- Use project-specific tools for testing, linting, and building.
- When making changes, ensure both frontend and backend remain functional and compatible.