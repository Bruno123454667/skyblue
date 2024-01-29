import pandas as pd
import os

# Hämta vart den ska leta efter filerna 
dir_path = os.getcwd()

# Filnamn för kartan och rum-informationen
map_file = "Map.xlsx"
room_information_file = "Enchanted Forest.xlsx"

# Skapa vägarna till Excel-filerna
map_file_path = os.path.join(dir_path, map_file)
room_information_path = os.path.join(dir_path, room_information_file)

# Kontrollera om båda filerna finns i mappen
if os.path.isfile(map_file_path) and os.path.isfile(room_information_path):
    # Ladda in data från Excel-filerna till dataframes
    map_data = pd.read_excel(map_file_path)
    room_information_df = pd.read_excel(room_information_path)
else:
    print("Error, en eller båda kalkylarken hittas inte.")


def visa_rum(rum_data, aktuellt_rum):
    # Skriv ut de tillgängliga rummen
    print("Available rooms:", rum_data['Room'].unique())
    # Hämta information om det aktuella rummet
    matchande_rum = rum_data.loc[rum_data['Room'] == aktuellt_rum]

    if not matchande_rum.empty:
        # Om rummet finns, skriv ut beskrivning och tillgängliga handlingar
        beskrivning = matchande_rum['Description'].values[0]
        print(f'Du är i rummet: {aktuellt_rum}')
        print(f'Beskrivning: {beskrivning}')
        handlingar = matchande_rum['Actions'].values[0]
        print(f'Möjliga handlingar: {handlingar}')
        return beskrivning, handlingar
    else:
        # Om rummet inte finns, skriv ut ett felmeddelande
        print(f"Rummet {aktuellt_rum} finns inte i kalkylbladet.")
        return None, None


# Hitta nytt Rum
def hitta_nytt_rum(map_data, aktuellt_rum, riktning):
    # Hitta det nya rummet baserat på riktningen
    return map_data.loc[map_data['Room'] == aktuellt_rum, riktning].values[0]

def spela():
    # Fråga användaren vilket rum de vill börja i
    aktuellt_rum = input("Vilket rum vill du börja i? ")

    while True:
        # Kontrollera om det givna rummet finns i rum-informationen
        if aktuellt_rum not in room_information_df['Room'].values:
            print(f"Rummet {aktuellt_rum} finns inte i kalkylbladet för rum.")
            break

        # Visa information om det aktuella rummet
        beskrivning, handlingar = visa_rum(room_information_df, aktuellt_rum)
        # Fråga användaren vad de vill göra sen
        kommando = input("Vad vill du göra? ")

        if kommando.lower() == "quit":
            break

        # Hämta riktningen från användarens kommando
        riktning = kommando.lower().split()[-1]

        # Kontrollera om riktningen är giltig
        if riktning in ['north', 'south', 'east', 'west']:
            # Hitta det nya rummet baserat på riktningen
            nytt_rum = hitta_nytt_rum(map_data, aktuellt_rum, riktning)
        else:
            print("Ogiltig riktning. Försök igen.")
            continue

        if not pd.isnull(nytt_rum):
            # Uppdatera det aktuella rummet till det nya rummet
            aktuellt_rum = nytt_rum
        else:
            print("Ogiltig riktning. Försök igen.")

# Starta spelet
spela()
