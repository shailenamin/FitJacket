# FitJacket 🧥💪

FitJacket is a fitness-focused web application that allows users to track workouts, challenge friends, and stay motivated on their fitness journey. Built as a group project with a full-stack architecture.

🔗 **Live Demo:** [https://shailenamin.github.io/fitjacket](https://shailenamin.github.io/fitjacket)  
🛠️ **Tech Stack:** Django · React Native (Expo) · PostgreSQL · TailwindCSS · Bootstrap · OpenAI API · Strava API

## Features
- AI Fitness Coach with GPT-4 integration  
- Dynamic Events page with filterable, animated Bootstrap cards  
- Strava OAuth for syncing and displaying workout data  
- User authentication and profile tracking  
- Create and accept fitness challenges from friends  
- Responsive and unified site design  

## My Contributions
- **Events Page:** Built a dynamic, filterable Events page using animated Bootstrap cards, with modals for detailed views and a polished “Create Event” workflow that redirects on success.  
- **Frontend Design:** Unified the site’s look and feel by refactoring the base template and CSS, implementing responsive navigation, consistent typography, and smooth hover/animation effects.  
- **AI Fitness Coach:** Developed a GPT-4 powered fitness coach using Django forms, environment-secured OpenAI integration, Markdown-to-HTML rendering, session history, and interactive feedback/favorites toggles.  
- **Strava Integration:** Integrated Strava OAuth and activity import so users can sync and view workouts directly on the platform.  
- **Backend Architecture:** Structured the codebase into modular Django apps with clear models, forms, and views. Managed environment variables with `.env`, and ensured seamless team development by syncing migrations.  

## Installation (Local Setup)
```bash
# Clone the repo
git clone https://github.com/shailenamin/fitjacket.git

# Backend setup
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# Frontend setup
cd frontend
npm install
expo start

