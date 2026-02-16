from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models
from octofit_tracker import settings
from django.conf import settings as django_settings

from pymongo import MongoClient

# Sample data
USERS = [
    {"name": "Clark Kent", "email": "superman@dc.com", "team": "Team DC"},
    {"name": "Bruce Wayne", "email": "batman@dc.com", "team": "Team DC"},
    {"name": "Diana Prince", "email": "wonderwoman@dc.com", "team": "Team DC"},
    {"name": "Tony Stark", "email": "ironman@marvel.com", "team": "Team Marvel"},
    {"name": "Steve Rogers", "email": "captainamerica@marvel.com", "team": "Team Marvel"},
    {"name": "Natasha Romanoff", "email": "blackwidow@marvel.com", "team": "Team Marvel"},
]

TEAMS = [
    {"name": "Team DC", "members": ["superman@dc.com", "batman@dc.com", "wonderwoman@dc.com"]},
    {"name": "Team Marvel", "members": ["ironman@marvel.com", "captainamerica@marvel.com", "blackwidow@marvel.com"]},
]

ACTIVITIES = [
    {"user_email": "superman@dc.com", "activity": "Flight", "duration": 60},
    {"user_email": "batman@dc.com", "activity": "Martial Arts", "duration": 45},
    {"user_email": "ironman@marvel.com", "activity": "Suit Training", "duration": 50},
]

LEADERBOARD = [
    {"team": "Team DC", "points": 300},
    {"team": "Team Marvel", "points": 350},
]

WORKOUTS = [
    {"name": "Super Strength", "suggested_for": "Team DC"},
    {"name": "Tech Endurance", "suggested_for": "Team Marvel"},
]

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        client = MongoClient(django_settings.DATABASES['default']['CLIENT']['host'])
        db = client['octofit_db']

        # Drop collections if they exist
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Insert test data
        db.users.insert_many(USERS)
        db.teams.insert_many(TEAMS)
        db.activities.insert_many(ACTIVITIES)
        db.leaderboard.insert_many(LEADERBOARD)
        db.workouts.insert_many(WORKOUTS)

        # Create unique index on email for users
        db.users.create_index([('email', 1)], unique=True)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
