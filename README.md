# ILearn - Podcast Platform

A full-stack web application for discovering, creating, and managing podcasts. Users can browse podcasts by category, follow their favorites, upload episodes, and engage through comments.

## Features

- **Browse & Discover**: Explore podcasts across categories (Cucina, Scienza, Sport, Tecnologia, Altro)
- **User Authentication**: Sign up, log in, and manage your profile
- **Podcast Management**: Create, edit, and delete podcasts with cover images
- **Episode Management**: Upload audio episodes (MP3/WAV) with descriptions
- **Follow System**: Follow/unfollow podcasts and view them in your profile
- **Comments**: Leave and manage comments on episodes
- **Responsive Design**: Works on desktop and mobile devices

## Tech Stack

- **Backend**: Python 3.11, Flask
- **Authentication**: Flask-Login, Werkzeug (password hashing)
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Deploy**: Render (Gunicorn WSGI server)

## Local Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/scale-up-agency/ilearn-podcast.git
   cd ilearn-podcast
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python app.py
   ```

5. Open your browser at [http://localhost:3000](http://localhost:3000)

### Test Credentials

- **Email**: `alessandro@gmail.com`
- **Password**: `passwordsito`

## Project Structure

```
ilearn-podcast/
├── app.py                 # Main Flask application
├── db_interaction.py      # Database queries and operations
├── models.py              # User model (Flask-Login)
├── requirements.txt       # Python dependencies
├── Procfile               # Gunicorn config for Render
├── runtime.txt            # Python version for Render
├── db/                    # SQLite database
├── static/                # CSS, JS, images, audio files
└── templates/             # Jinja2 HTML templates
```

## Live Demo

[https://ilearn-podcast.onrender.com](https://ilearn-podcast.onrender.com)

---

Built by **Scale UP Agency**
