# AnimeTracker

Web app per tracciare anime, scrivere recensioni e gestire la propria lista personale.

Progetto Django con SQLite.

---

## Stack

- **Backend:** Python / Django
- **Database:** SQLite
- **Frontend:** Django Templates (HTML/CSS)
- **Lingua interfaccia:** Italiano

---

## Funzionalità

- Catalogo anime con ricerca per titolo e filtro per genere
- Pagina dettaglio: episodi, studio, rating medio, recensioni
- Lista personale per utente (Da vedere / In visione / Completato)
- Valutazione da 1 a 10 per ogni anime
- Recensioni con titolo, testo e voto
- Navigazione per generi e studi di produzione
- Registrazione e autenticazione utenti

---

## Modelli

| Modello | Descrizione |
|---------|-------------|
| `Anime` | Titolo, descrizione, episodi, anno, studio, generi |
| `Genre` | Genere con descrizione |
| `Studio` | Studio di produzione con paese e anno fondazione |
| `Episode` | Episodi collegati all'anime |
| `UserAnime` | Lista personale utente con status e voto |
| `Review` | Recensione utente su un anime |

---

## Avvio

```bash
# Installa dipendenze
pip install -r requirements.txt

# Applica migrazioni
python manage.py migrate

# (Opzionale) Popola il database con dati di esempio
python seed_data.py

# Avvia il server
python manage.py runserver
```

App disponibile su `http://127.0.0.1:8000`

---

## Struttura

```
animetracker/
├── anime/                  # App principale
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   ├── migrations/
│   └── templates/anime/
├── animetracker/           # Configurazione Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── db.sqlite3
├── manage.py
└── seed_data.py
```
