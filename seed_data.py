"""
Esegui con: python3 seed_data.py
Popola il database con dati di esempio per tutte le entità.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'animetracker.settings')
django.setup()

from anime.models import Anime, Genre, Studio, Episode

# --- Generi ---
genre_data = [
    ("Azione", "Combattimenti, avventura e ritmo serrato."),
    ("Fantasy", "Mondi immaginari, magia e creature mitologiche."),
    ("Sci-Fi", "Fantascienza, tecnologia avanzata e spazio."),
    ("Thriller", "Tensione, misteri e colpi di scena."),
    ("Slice of Life", "Storie quotidiane realistiche."),
    ("Storico", "Ambientazioni in epoche passate."),
]
genres = {}
for name, desc in genre_data:
    g, _ = Genre.objects.get_or_create(name=name, defaults={'description': desc})
    genres[name] = g
print(f"Generi: {Genre.objects.count()}")

# --- Studi ---
studio_data = [
    ("Wit Studio", "Giappone", 2012),
    ("Madhouse", "Giappone", 1972),
    ("ufotable", "Giappone", 2000),
    ("Bones", "Giappone", 1998),
    ("J.C.Staff", "Giappone", 1986),
    ("Sunrise", "Giappone", 1972),
    ("Pierrot", "Giappone", 1979),
]
studios = {}
for name, country, year in studio_data:
    s, _ = Studio.objects.get_or_create(name=name, defaults={'country': country, 'founded_year': year})
    studios[name] = s
print(f"Studi: {Studio.objects.count()}")

# --- Anime ---
anime_data = [
    ("Attack on Titan", "L'umanità sopravvive dietro enormi mura per proteggersi dai Titani.", 87, 2013, "Wit Studio", ["Azione", "Fantasy"]),
    ("Death Note", "Uno studente trova un quaderno che uccide chiunque il cui nome venga scritto.", 37, 2006, "Madhouse", ["Thriller"]),
    ("Fullmetal Alchemist: Brotherhood", "Due fratelli cercano la Pietra Filosofale per recuperare i loro corpi.", 64, 2009, "Bones", ["Azione", "Fantasy"]),
    ("Demon Slayer", "Un ragazzo diventa un cacciatore di demoni per salvare sua sorella.", 26, 2019, "ufotable", ["Azione", "Fantasy"]),
    ("One Punch Man", "Un supereroe che sconfigge tutti i nemici con un solo pugno.", 12, 2015, "Madhouse", ["Azione"]),
    ("Sword Art Online", "I giocatori rimangono intrappolati in un MMORPG virtuale.", 25, 2012, "J.C.Staff", ["Azione", "Sci-Fi", "Fantasy"]),
    ("My Hero Academia", "In un mondo di supereroi, un ragazzo senza poteri sogna di diventare il più grande.", 113, 2016, "Bones", ["Azione"]),
    ("Naruto", "Un ragazzo emarginato diventa un ninja e sogna di diventare Hokage.", 220, 2002, "Pierrot", ["Azione"]),
    ("Dragon Ball Z", "Goku e i suoi amici difendono la Terra da minacce sempre più potenti.", 291, 1989, "Toei Animation", ["Azione"]),
    ("Cowboy Bebop", "Un gruppo di cacciatori di taglie viaggia per il sistema solare nel 2071.", 26, 1998, "Sunrise", ["Sci-Fi", "Azione"]),
    ("Steins;Gate", "Uno scienziato scopre accidentalmente come inviare messaggi nel passato.", 24, 2011, "J.C.Staff", ["Sci-Fi", "Thriller"]),
    ("Vinland Saga", "Un giovane vichingo cerca vendetta per la morte del padre.", 24, 2019, "Wit Studio", ["Storico", "Azione"]),
]

created = 0
for title, description, episodes, year, studio_name, genre_names in anime_data:
    studio_obj = studios.get(studio_name)
    if not studio_obj:
        studio_obj, _ = Studio.objects.get_or_create(name=studio_name, defaults={'country': 'Giappone'})
    anime_obj, was_created = Anime.objects.get_or_create(
        title=title,
        defaults={
            'description': description,
            'episodes': episodes,
            'year': year,
            'studio': studio_obj,
        }
    )
    if not was_created:
        anime_obj.studio = studio_obj
        anime_obj.year = year
        anime_obj.save()
    for g_name in genre_names:
        if g_name in genres:
            anime_obj.genres.add(genres[g_name])
    if was_created:
        created += 1

print(f"Anime creati: {created}. Totale: {Anime.objects.count()}")

# --- Episodi campione (primi 3 ep per i primi 3 anime) ---
ep_samples = [
    ("Attack on Titan", [
        (1, "Per te, duemila anni dopo", 24),
        (2, "Quel giorno", 24),
        (3, "Notte del giuramento — Per far arretrare l'umanità", 24),
    ]),
    ("Death Note", [
        (1, "Rinascita", 23),
        (2, "Confronto", 23),
        (3, "Decadimento", 23),
    ]),
    ("Steins;Gate", [
        (1, "Apertura: Divergenza epocale", 24),
        (2, "Variabile temporale di prolasso", 24),
        (3, "Proof Divergence", 24),
    ]),
]
ep_created = 0
for anime_title, episodes in ep_samples:
    try:
        anime_obj = Anime.objects.get(title=anime_title)
        for num, title, duration in episodes:
            _, was_created = Episode.objects.get_or_create(
                anime=anime_obj,
                number=num,
                defaults={'title': title, 'duration_minutes': duration}
            )
            if was_created:
                ep_created += 1
    except Anime.DoesNotExist:
        pass

print(f"Episodi creati: {ep_created}. Totale: {Episode.objects.count()}")
