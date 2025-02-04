# version 0.2.31
import xbmc
import xbmcgui
import xbmcvfs
import datetime
import os

# Percorso assoluto della directory dell'addon
ADDON_PATH = xbmcvfs.translatePath("special://home/addons/script.french.revolutionary.calendar/")
IMAGE_PATH = os.path.join(ADDON_PATH, "resources", "image")

# Giorni della settimana nel calendario rivoluzionario
DAYS_OF_WEEK = ["Primidì", "Duodì", "Tridì", "Quartidì", "Quintidì", "Sestidì", "Settidì", "Ottidì", "Nonidì", "Decadì"]

# Mesi del calendario rivoluzionario
MONTHS = ["Vendemmiaio", "Brumaio", "Frimaio", "Nevoso", "Piovoso", "Ventoso", "Germinale", "Floreale", "Pratile", "Messidoro", "Termidoro", "Fruttidoro", "Sanculottidi"]

# Date dell'equinozio d'autunno per gli anni recenti
EQUINOX_DATES = {
    2024: datetime.date(2024, 9, 22),
    2025: datetime.date(2025, 9, 22),
    2026: datetime.date(2026, 9, 23),
    2027: datetime.date(2027, 9, 23),
    2028: datetime.date(2028, 9, 22),
    2029: datetime.date(2029, 9, 22),
    2030: datetime.date(2030, 9, 22)
}

def get_latest_equinox(year):
    """Restituisce la data dell'equinozio d'autunno per l'anno corrente."""
    return EQUINOX_DATES.get(year, datetime.date(year, 9, 22))  # Default 22 settembre se non presente

def calculate_revolutionary_date(today):
    """Calcola la data nel calendario rivoluzionario."""
    equinox = get_latest_equinox(today.year)
    delta_days = (today - equinox).days
    
    if delta_days < 0:
        equinox = get_latest_equinox(today.year - 1)
        delta_days = (today - equinox).days
    
    month = (delta_days // 30) + 1
    day = (delta_days % 30) + 1
    week_day = DAYS_OF_WEEK[(day - 1) % 10]
    month_name = MONTHS[month - 1] if month <= 12 else "Sanculottidi"
    
    print(f"DEBUG: Data odierna: {today}")
    print(f"DEBUG: Equinozio di riferimento: {equinox}")
    print(f"DEBUG: Giorni trascorsi dall'equinozio: {delta_days}")
    print(f"DEBUG: Giorno rivoluzionario: {day}, Mese: {month} ({month_name}), Giorno della settimana: {week_day}")
    
    return day, month, week_day, month_name

def get_image_path(day, month):
    """Restituisce il percorso dell'immagine corrispondente al giorno e mese forniti."""
    month_str = f"M{month:02d}"
    day_str = f"D{day:02d}"
    image_filename = f"{month_str}{day_str}.png"
    image_filepath = os.path.join(IMAGE_PATH, image_filename)
    
    print(f"DEBUG: Controllo esistenza immagine: {image_filepath}")  # Log di debug
    
    if os.path.exists(image_filepath):
        print("DEBUG: Immagine trovata!")
        return image_filepath
    else:
        print("DEBUG: Immagine NON trovata!")
        return None

def show_image_and_text(image_path, week_day, day, month_name):
    """Mostra un'immagine centrata con il nome del giorno rivoluzionario sotto di essa."""
    window = xbmcgui.Window()
    
    screen_width = 1280
    screen_height = 720
    image_width = 600
    image_height = 400
    text_width = 600
    text_height = 50
    
    image_x = (screen_width - image_width) // 2
    image_y = (screen_height - image_height) // 3
    text_x = (screen_width - text_width) // 2
    text_y = image_y + image_height + 20
    
    if image_path:
        image_control = xbmcgui.ControlImage(image_x, image_y, image_width, image_height, image_path)
        window.addControl(image_control)
    
    text_label = f"{week_day}, {day} {month_name}"
    text_control = xbmcgui.ControlLabel(text_x, text_y, text_width, text_height, text_label, textColor='white', alignment=2)
    window.addControl(text_control)
    
    window.show()
    xbmc.sleep(5000)  # Mostra per 5 secondi
    window.close()

def main():
    """Funzione principale per calcolare e mostrare il giorno rivoluzionario."""
    today = datetime.date.today()
    day, month, week_day, month_name = calculate_revolutionary_date(today)
    image_path = get_image_path(day, month)
    
    print(f"DEBUG: Visualizzazione dati: {week_day}, {day} {month_name}")
    show_image_and_text(image_path, week_day, day, month_name)

main()
