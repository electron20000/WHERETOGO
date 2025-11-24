# WHERE TO GO

Tablica informacyjna dla działu STOW w magazynie oparta o Django 3.2.25. Główna strona (`/`) prezentuje karty lokalizacji (TRANS, P1, P2, P3, P4, STREFY) z automatycznym odświeżaniem AJAX, a panel lidera (`/leader/`) pozwala sterować zamknięciami, komunikatami oraz kolorystyką.

## Funkcje
- **Dashboard** z gradientowymi kartami, półprzezroczystą nakładką i ciemnym layoutem.
- Karty zamknięte oznaczane na czerwono z napisem „Zamknięte”; otwarte są zielone, STREFY niebieskie.
- Lista aktywnych komunikatów (puste stany pokazują „Brak aktywnych komunikatów.”). Komunikaty „Ważne” mają pulsującą ramkę.
- Odświeżanie co kilka sekund przez endpoint fragmentu HTML; treść podmieniana tylko przy zmianie znacznika czasu.
- **Panel lidera** „Sterowanie komunikatami” z przełącznikami zamknięć, formsetami komunikatów (dodawanie kolejnych pól), checkboxami aktywacji oraz przełącznikiem „Ważne”.
- **Ustawienia graficzne** z podglądem mini-dashboardu oraz edycją kolorów przez modal; zmiany zapisują się w ukrytych polach i natychmiast aktualizują podgląd (CSS variables).
- Domyślne lokalizacje i paleta kolorów tworzą się w migracji startowej.

## Wymagania
- Python 3.11+
- Django 3.2.25
- `pysqlite3-binary` (zapewnia kompatybilne SQLite także na starszych systemach)

## Instalacja i uruchomienie
1. Zainstaluj zależności:
   ```bash
   pip install -r requirements.txt
   ```
2. Wykonaj migracje i utwórz domyślne dane:
   ```bash
   python manage.py migrate
   ```
3. (Opcjonalnie) utwórz superużytkownika do panelu Django:
   ```bash
   python manage.py createsuperuser
   ```
4. Uruchom serwer deweloperski:
   ```bash
   python manage.py runserver
   ```
5. Otwórz `http://localhost:8000/` aby zobaczyć tablicę, a `http://localhost:8000/leader/` aby wejść do panelu lidera.
