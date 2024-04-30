from django.core.management.base import BaseCommand
from faker import Faker
from django.contrib.auth.hashers import make_password
from myapp.models import User, Event, EventsJoined
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Create random users, events and joined events'

    def handle(self, *args, **kwargs):
        fake = Faker('es_ES')  # Configura Faker para usar español

        sports = ['Futbol', 'Baloncesto', 'Tenis Mesa', 'Padel', 'Tenis', 'Gimnasio']

        def create_fake_user():
            for _ in range(100):  # Cambia el rango a la cantidad de usuarios que quieres crear
                User.objects.create(
                    username=fake.unique.user_name(),
                    email=fake.unique.email(),
                    password=make_password('P@ssw0rd'),  # Usa una contraseña predeterminada
                    city=fake.city(),
                    birthdate=fake.date_of_birth(minimum_age=18, maximum_age=90),  # Edades entre 18 y 90
                    description=fake.text(),
                    instagram=fake.user_name(),
                    twitter=fake.user_name(),
                )

        def create_fake_event():
            users = User.objects.all()
            for _ in range(100):  # Cambia el rango a la cantidad de eventos que quieres crear
                Event.objects.create(
                    title=fake.sentence(nb_words=6),
                    sport=random.choice(sports),
                    date=fake.date_between(start_date='-1y', end_date='+1y'),
                    time=fake.time(),
                    location=fake.address(),
                    description=fake.text(),
                    user=random.choice(users),
                    image_path=fake.file_path(),
                )

        def create_fake_events_joined():
            users = User.objects.all()
            events = Event.objects.all()
            for _ in range(100):  # Cambia el rango a la cantidad de eventos unidos que quieres crear
                EventsJoined.objects.create(
                    user_id=random.choice(users),
                    username=fake.user_name(),
                    event=random.choice(events),
                    join_date=fake.date_time_this_year(),
                )

        create_fake_user()
        create_fake_event()
        create_fake_events_joined()

        self.stdout.write(self.style.SUCCESS('Successfully created fake data'))