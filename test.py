import os

def parse_osu_file(file_path):
    hitobjects = []
    with open(file_path, 'r') as f:
        file = f.read()
        flag=False
        for i in file.splitlines():
            if flag:
                line=i.split(",")
                hitobjects.append(line[2])
            if i=="[HitObjects]":
                flag=True
    return hitobjects

def parse_lyrics_txt_file(file_path):
    lyrics = []
    with open(file_path, 'r', encoding='utf-8') as f:
        file = f.read()
        flag=False
        for i in file.splitlines():
            if flag:
                line=i.split("_")
                lyrics.append(line)
            if i=="[Lyrics]":
                flag=True
    return lyrics

def find_osu_file(name):
    for root, dirs, files in os.walk("./songs"):
        for dirname in dirs:
            if dirname == name:
                for file in os.listdir(os.path.join(root, dirname)):
                    if file.endswith(".osu"):
                        return os.path.join(root, dirname, file)
    return None

def find_lyrics_txt_file(name):
    for root, dirs, files in os.walk("./songs"):
        for dirname in dirs:
            if dirname == name:
                for file in os.listdir(os.path.join(root, dirname)):
                    if file.endswith(".txt"):
                        return os.path.join(root, dirname, file)
    return None

def find_mp3_file(name):
    for root, dirs, files in os.walk("./songs"):
        for dirname in dirs:
            if dirname == name:
                for file in os.listdir(os.path.join(root, dirname)):
                    if file.endswith(".mp3"):
                        return os.path.join(root, dirname, file)
    return None

def list_songs():
    songs = []
    for root, dirs, files in os.walk("./songs"):
        for dirname in dirs:
            songs.append(dirname)
    return songs

#####################################################################################################

os.system('cls' if os.name == 'nt' else 'clear')
print("\033[?25h\033[0m")

print("Liste des chansons disponibles :")
songlist = list_songs()
for i in songlist:
    print(f"- {i}")
path = input("Quelle chanson voulez-vous choisir ?\n")
if path not in songlist:
    raise ValueError(f"La chanson '{path}' n'est pas disponible.")
print(f"Vous avez choisi la chanson : {path}")
print()

osu_file = find_osu_file(path)
lyrics_txt_file = find_lyrics_txt_file(path)
mp3_file = find_mp3_file(path)
if osu_file is None:
    raise FileNotFoundError(f"Le fichier osu n'a pas été trouvé dans le répertoire {path}")
if lyrics_txt_file is None:
    raise FileNotFoundError(f"Le fichier texte n'a pas été trouvé dans le répertoire {path}")
if mp3_file is None:
    raise FileNotFoundError(f"Le fichier mp3 n'a pas été trouvé dans le répertoire {path}")
print(f"Fichier osu trouvé : {osu_file}")
print(f"Fichier texte trouvé : {lyrics_txt_file}")
print(f"Fichier mp3 trouvé : {mp3_file}")
print()

hitpoints = parse_osu_file(osu_file)
lyrics = parse_lyrics_txt_file(lyrics_txt_file)
# print(lyrics)

# for i in x:
#     print(i)

############################### paramètres ###############################



afficher_suiv = True
cb = [255, 0, 0]
cf = [0, 255, 0]

fluide = True
maxtime = 0.5

fluide2 = 0
mintime = 0.01

##########################################################################

import asyncio
import pygame
import time



print("\033[?25l\033[0m")


timeprecision = 1/1000

async def afficher_paroles(mot, pas, estpremier, estdernier, afficher_suiv, phrasesuivante, tempssuivant, fluide=True, fluide2=0):
    delai = pas * timeprecision
    suiv = tempssuivant * timeprecision - delai
    await asyncio.sleep(delai)
    if suiv > 0.1 and fluide:
        for i in range(len(mot)):
            print(mot[i], end='' if not (estdernier and i==len(mot)-1) else '\n')
            if i < len(mot) - 1 and fluide2 == 0:
                time.sleep(suiv/len(mot) if suiv < maxtime else 0.01)
            elif i < len(mot) - 1 and fluide2 > 0 and fluide2*len(mot) < suiv:
                time.sleep(fluide2)
            elif i < len(mot) - 1 and fluide2 > 0 and fluide2*len(mot) >= suiv and mintime > 0:
                time.sleep(mintime)
    else:
        print(mot, end='' if not (estdernier) else '\n')
    
    if estdernier:
        # print("\n")
        if afficher_suiv and phrasesuivante != "":
            print(f"\033[38;2;{cb[0]};{cb[1]};{cb[2]}m{phrasesuivante}\033[38;2;{cf[0]};{cf[1]};{cf[2]}m", end='\r')
        
 
async def karaoke():
    
    pygame.mixer.init()
    try:
        pygame.mixer.music.load(mp3_file)
    except pygame.error as e:
        print(f"Erreur lors du chargement du fichier audio : {e}")
        return

    pygame.mixer.music.play()
    print(f"Lecture de la musique : {mp3_file[2:]}\nParoles : {lyrics_txt_file[2:]}\nvaleurs : {osu_file[2:]}")

    tasks = []
    itemps = 0
    print("Bonne chanson !\n")
    if afficher_suiv:
        print(f"\033[38;2;{cb[0]};{cb[1]};{cb[2]}m{''.join(lyrics[0])}\033[38;2;{cf[0]};{cf[1]};{cf[2]}m", end='\r')
    for verse in range(len(lyrics)):
        for i, mot in enumerate(lyrics[verse]):
            if itemps < len(hitpoints):
                try:
                    pas = int(hitpoints[itemps])
                    estpremier = (i == 0)
                    estdernier = (i == len(lyrics[verse]) - 1)
                    phrasesuivante = "".join(lyrics[verse + 1]) if verse + 1 < len(lyrics) else ""
                    tempssuivant = int(hitpoints[itemps + 1]) if itemps + 1 < len(hitpoints) else 0
                    # print(f"Phrase suivante : {phrasesuivante}")
                    task = asyncio.create_task(afficher_paroles(mot, pas, estpremier, estdernier, afficher_suiv, phrasesuivante, tempssuivant, fluide, fluide2))
                    tasks.append(task)
                    itemps += 1
                except ValueError:
                    print(f"Attention : la valeur '{hitpoints[itemps]}' n'est pas un nombre entier valide.")
                    itemps += 1
            else:
                break
        else:
            continue
        break
    await asyncio.gather(*tasks)
    while pygame.mixer.music.get_busy():
        time.sleep(0.5)
    pygame.mixer.music.stop()
    pygame.mixer.quit()


if __name__ == "__main__":
    asyncio.run(karaoke())
    print("\033[?25h\033[0m")

# for i in lyrics:
#     print(i)