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


        locations = [
             {
            "nombre de ubicacion": "C/ Miquel Roncali, Av. del Baix Llobregat, Cornellà de Llobregat",
            "ubicacion": {
                "latitude": 41.353403,
                "longitude": 2.064821
            },
            "actividad": ["Futbol", "Baloncesto", "Tenis Mesa", "Barras"],
            "imagen": "./img/Places/CampDeLesAigues.jpg"

        },
        {
            "nombre de ubicacion": "C/ Maria Aurèlia Capmany, 14. Parc del Canal de la Infanta",
            "ubicacion": {
                "latitude": 41.3592698,
                "longitude": 2.0638505
            },
            "actividad": ["Baloncesto", "Tenis Mesa"],
            "imagen": "./img/Places/ParcDeLaInfanta.png"
        },

        {
            "nombre de ubicacion": "Sampa, San Joan Despí",
            "ubicacion": {
                "latitude": 41.365101,
                "longitude": 2.0624128
            },
            "actividad": ["Futbol", "Baloncesto"],
            "imagen": "./img/Places/Sampa.png"

        },

        {
            "nombre de ubicacion": "La Jaula, Plaça de la Sardana, Cornellà de Llobregat",
            "ubicacion": {
                "latitude": 41.3512363,
                "longitude": 2.072168
            },
            "actividad": ["Futbol", "Baloncesto"],
            "imagen": "./img/Places/LaJaula.jpg"
        },

        {
            "nombre de ubicacion": "C/ Tirso de Molina, 40, Cornella de Llobregat",
            "ubicacion": {
                "latitude": 41.351872,
                "longitude": 2.086180    
            },
            "actividad": ["Futbol"],
            "imagen": "./img/Places/EspaiEsportiuAlmeda.jpg"
        },


        {
            "nombre de ubicacion": "C/ Verge de Montserrat, 48, Padel Delfos, Cornellà de Llobregat",
            "ubicacion": {
                "latitude": 41.3484288,
                "longitude": 2.0688359
            },
            "actividad": ["Padel"],
            "imagen": "./img/Places/PadelDelfos.jpg"
        },

        {
            "nombre de ubicacion": "C/ Verge de Montserrat, Centre Internacional de Tennis, Cornellà de Llobregat",
            "ubicacion": {
                "latitude": 41.3490142,
                "longitude": 2.0684062
            },
            "actividad": ["Tenis"],
            "imagen": "./img/Places/FederacioCatalanaTenis.jpeg"
        },

        {
            "nombre de ubicacion": "C/ Verge de Montserrat, 51, Parc de calistènia Cornellà",
            "ubicacion": {
                "latitude": 41.348588,
                "longitude": 2.0687571
            },
            "actividad": ["Barras"],
            "imagen": "./img/Places/Calistenia.jpg"
        },

        {
            "nombre de ubicacion": " Pg. dels Ferrocarrils Catalans, 177, Pista esportiva, Cornellà de Llobregat",
            "ubicacion": {
                "latitude": 41.3531689,
                "longitude": 2.0842169
            },
            "actividad": ["Futbol", "Baloncesto"],
            "imagen": "./img/Places/EspaiEsportiuPasseigAlmeda.jpg"
        }, 
        
        {
            "nombre de ubicacion": " C/ Bonavista, 70, Cornellà de Llobregat",
            "ubicacion": {
                "latitude": 41.3559335,
                "longitude": 2.0747592
            },
            "actividad": ["Futbol", "Baloncesto"],
            "imagen": "./img/Places/Futbol_Predef.jpg"
        }, 
        
        {
            "nombre de ubicacion": "Plaça de Josep Tarradellas, Cornellà de Llobregat ",
            "ubicacion": {
                "latitude": 41.3623421,
                "longitude": 2.0714046
            },
            "actividad": ["Tenis Mesa"],
            "imagen": "./img/Places/TenisMesa_Predef.jpg"
        }, 
        
        {
            "nombre de ubicacion": " Plaça de Pau Casals",
            "ubicacion": {
                "latitude": 41.3632773,
                "longitude": 2.0721183
            },
            "actividad": ["Baloncesto"],
            "imagen": "./img/Places/PISTA_PAUCASALS.JPG"
        }, 
        
        {
            "nombre de ubicacion": "Av. de Salvador Allende, 4, Pista esportiva, Cornellà de Llobregat ",
            "ubicacion": {
                "latitude": 41.3571756,
                "longitude": 2.078195
            },
            "actividad": ["Baloncesto"],
            "imagen": "./img/Places/Baloncesto_Predef.jpeg"
        },  
        
        {
            "nombre de ubicacion": "C/ Marfull, 6, Cornellà de Llobregat",
            "ubicacion": {
                "latitude": 41.359108,
                "longitude": 2.081566
            },  
            "actividad": ["Futbol", "Baloncesto"],
            "imagen": "./www/img/Places/Futbol_Predef.jpg"
        }, 
        
        {
            "nombre de ubicacion": "Parque Can Mercader, Cornellà de Llobregat",
            "ubicacion": {
                "latitude": 41.358706,
                "longitude": 2.0853477
            },
            "actividad": ["Barras"],
            "imagen": "./img/Places/Barras_Predef.jpeg"
        }, 
        
        {
            "nombre de ubicacion": "Passatge dels Alps, Aurial Padel Cornellà by Marta Marrero, Cornellà de Llobregat ",
            "ubicacion": {
                "latitude": 41.356264,
                "longitude": 2.081358
            }, 
            "actividad": ["Padel"],
            "imagen":"./img/Places/Aurial_Padel.jpeg"
        }, 
        
        {
            "nombre de ubicacion": "Av. del Baix Llobregat, 11",
            "ubicacion": {
                "latitude":41.353857,
                "longitude": 2.064640
            }, 
            "actividad": ["Tenis Mesa"],
            "imagen": "./img/Places/TenisMesa_Predef.jpg"
        }, 
        
        {
            "nombre de ubicacion": "C/ La Fontsanta, 48, Soccer and Basketball Court, Sant Joan Despí",
            "ubicacion": {
                "latitude":41.371874,
                "longitude": 2.074016
            }, 
            "actividad": ["Futbol", "Baloncesto"],
            "imagen": "./img/Places/Futbol_Predef.jpg"
        }, 
        
        {
            "nombre de ubicacion": "Plaça l'Estatut, 5, Sant Joan Despí",
            "ubicacion": {
                "latitude":41.372854,
                "longitude": 2.069475
            }, 
            "actividad": ["Tenis Mesa", "Baloncesto"],
            "imagen": "./img/Places/Baloncesto_Predef.jpeg"
        }, 
        
        {
            "nombre de ubicacion": "Parque de Calistenia, Sant Joan Despí",
            "ubicacion": {
                "latitude":41.367568,
                "longitude": 2.050804
            }, 
            "actividad": ["Barras"],
            "imagen":"./img/Places/Barras_Predef.jpeg"
        }, 
        
        {
            "nombre de ubicacion": "Parc Pou d’en Fèlix, Esplugues de Llobregat, Barcelona",
            "ubicacion": {
                "latitude":41.3764435,
                "longitude": 2.0821609
            }, 
            "actividad": ["Futbol"],
            "imagen": "./img/Places/Futbol_Predef.jpg"
        }, 
        
        {
            "nombre de ubicacion": "C/ Josep Bastús i Planes, 1, Sant Joan Despí, Barcelona",
            "ubicacion": {
                "latitude":41.3706173,
                "longitude": 2.0525969
            }, 
            "actividad": ["Tenis", "Padel"],
            "imagen": "./img/Places/elmoli.jpeg"
        }, 
        
        {
            "nombre de ubicacion": "C/ Sant Martí de l'Erm, 30, Sant Joan Despí, Barcelona",
            "ubicacion": {
                "latitude":41.371445,
                "longitude": 2.069749
            }, 
            "actividad": ["Tenis", "Padel"],
            "imagen": "./img/Places/tennis-sant-joan-despi.jpg"
        }, 
        
        {
            "nombre de ubicacion": "C/ de Maria Montessori, 4, Sant Just Desvern, Barcelona",
            "ubicacion": {
                "latitude":41.389112,
                "longitude": 2.060393
            }, 
            "actividad": ["Padel"],
            "imagen": "./img/Places/santjust.jpeg"
        }, 
        
        {
            "nombre de ubicacion": "C/ Laureà Miró, 63, Esplugues de Llobregat, Barcelona",
            "ubicacion": {
                "latitude":41.376118,
                "longitude": 2.097020
            }, 
            "actividad": ["Futbol"],
            "imagen":"./img/Places/cruyff.jpeg"
        }, 
        
        {
            "nombre de ubicacion": "Riera de la Salut, 41, Sant Feliu de Llobregat, Barcelona",
            "ubicacion": {
                "latitude":41.388237,
                "longitude": 2.047785
            }, 
            "actividad": ["Futbol"],
            "imagen":"./img/Places/Riera.png"
        }, 
        
        {
            "nombre de ubicacion": "C/ Trepaderas, 3, L'Hospitalet de Llobregat, Barcelona",
            "ubicacion": {
                "latitude":41.368098,
                "longitude": 2.115184
            }, 
            "actividad": ["Futbol"],
            "imagen":"./img/Places/cruyff_hospitalet.jpg"
        }, 
        
        {
            "nombre de ubicacion": "Camí Pau Redó, L'Hospitalet de Llobregat, Barcelona",
            "ubicacion": {
                "latitude":41.344797,
                "longitude": 2.113111
            }, 
            "actividad": ["Futbol"],
            "imagen":"./img/Places/PauRedo.jpeg"
        }, 
        
        {
            "nombre de ubicacion": "Camí Pau Redó, 10, 08908 L'Hospitalet de Llobregat, Barcelona",
            "ubicacion": {
                "latitude":41.3442731,
                "longitude": 2.1115648
            }, 
            "actividad": ["Tenis","Padel"],
            "imagen":"./img/Places/tenis_redo.jpeg"
        }, 

        {
            "nombre de ubicacion": "C/ del Crom, 100, L'Hospitalet de Llobregat, Barcelona",
            "ubicacion": {
                "latitude":41.3499183,
                "longitude": 2.0984353
            }, 
            "actividad": ["Futbol"],
            "imagen":"./img/Places/golagol.jpeg"
        }, 
        
        {
            "nombre de ubicacion": "Parc del Llobregat, San Felíu de Llobregat, Barcelona",
            "ubicacion": {
                "latitude":41.383279,
                "longitude": 2.037862
            }, 
            "actividad": ["Baloncesto", "Futbol"],
            "imagen": "./img/Places/Baloncesto_Predef.jpeg"
        }, 
        
        {
            "nombre de ubicacion": "Plaça Dicià, Sant Feliu de Llobregat, Barcelona",
            "ubicacion": {
                "latitude":41.385299,
                "longitude": 2.054068
            }, 
            "actividad": ["Baloncesto"],
            "imagen":"./img/Places/dicia.png"

        }, 
        
        {
            "nombre de ubicacion": "Parc de Iulia Quieta, Sant Just Desvern, Barcelona",
            "ubicacion": {
                "latitude":41.386210,
                "longitude": 2.058667
            }, 
            "actividad": ["Futbol", "Baloncesto"],
            "imagen":"./img/Places/Futbol_Predef.jpg"
        }, 
        
        {
            "nombre de ubicacion": "C/ Tenerife, Horta-Guinardó, 08024 Barcelona",
            "ubicacion": {
                "latitude":41.385989,
                "longitude": 2.101456
            }, 
            "actividad": ["Futbol", "Baloncesto"],
            "imagen":"./img/Places/Futbol_Predef.jpg"
        },
        {
            "nombre de ubicacion": "Horta-Guinardó, 08024 Barcelona",
            "ubicacion": {
                "latitude":41.4165692,
                "longitude": 2.1644985
            }, 
            "actividad": ["Tenis Mesa"],
            "imagen":"./img/Places/Tenerife.png"
        }
      
    ]

        def create_fake_user():
            
            catalonia_cities = ['Barcelona', 'Girona', 'Badalona', 'Mataró', 'Santa Coloma de Gramenet', 'Sant Joan Despí', 'Esplugues de Llobregat', 'Sant Feliu de Llobregat', 'Cornellà de Llobregat', 'Gavà', 'Pallejà', 'Sant Boi de Llobregat', 'el Prat de Llobregat', 'Sant Just Desvern', 'Hospitales de Llobregat','Barcelona']  

            for _ in range(100):  
                User.objects.create(
                    username=fake.unique.user_name(),
                    email=fake.unique.email(),
                    password=make_password('P@ssw0rd'),  
                    city=random.choice(catalonia_cities),  
                    birthdate=fake.date_of_birth(minimum_age=12, maximum_age=90),  
                    description=fake.sentence(nb_words=10),  # Generar una frase en español de 10 palabras
                    instagram=fake.user_name(),
                    twitter=fake.user_name(),
                )

        def create_fake_event():
            users = User.objects.all()
            for _ in range(100):  # Cambia el rango a la cantidad de eventos que quieres crear
                location = random.choice(locations)  # Selecciona una ubicación aleatoria
                Event.objects.create(
                    title=fake.sentence(nb_words=6),
                    sport=random.choice(location['actividad']),  # Selecciona una actividad de la ubicación
                    date=fake.date_between(start_date='today', end_date='+1y'),  # Solo fechas futuras
                    time=fake.time(),
                    location=location['nombre de ubicacion'],  # Usa el nombre de la ubicación seleccionada
                    description=fake.text(),
                    user=random.choice(users),
                    image_path=location['imagen'],  # Usa la ruta de la imagen de la ubicación seleccionada
                )

        def create_fake_events_joined():
            users = User.objects.all()
            events = Event.objects.filter(date__gte=datetime.now())  # Solo eventos futuros
            for _ in range(100):  # Cambia el rango a la cantidad de eventos unidos que quieres crear
                user = random.choice(users)
                EventsJoined.objects.create(
                    user_id=user,
                    username=user.username,
                    event=random.choice(events),
                    join_date=fake.date_time_between(start_date='now', end_date='+1y'),  # Solo fechas futuras
                )

        create_fake_user()
        create_fake_event()
        create_fake_events_joined()

        self.stdout.write(self.style.SUCCESS('Successfully created fake data'))