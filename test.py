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

hitpoints = parse_osu_file("test.osu")
lyrics = parse_lyrics_txt_file("paroles.txt")
mp3_file = "audio.mp3"
# for i in x:
#     print(i)

import asyncio
import pygame

timeprecision = 1/1000

async def afficher_paroles(mot, pas, estpremier):
    delai = pas * timeprecision
    await asyncio.sleep(delai)
    print(mot if not estpremier else f"\n{mot}", end='')

async def karaoke():
    pygame.mixer.init()
    try:
        pygame.mixer.music.load(mp3_file)
    except pygame.error as e:
        print(f"Erreur lors du chargement du fichier audio : {e}")
        return

    pygame.mixer.music.play()
    print(f"Lecture de la musique : {mp3_file}")

    tasks = []
    itemps = 0
    for verse in lyrics:
        for i, mot in enumerate(verse):
            if itemps < len(hitpoints):
                try:
                    pas = int(hitpoints[itemps])
                    estpremier = (i == 0)
                    task = asyncio.create_task(afficher_paroles(mot, pas, estpremier))
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


if __name__ == "__main__":
    asyncio.run(karaoke())

# for i in lyrics:
#     print(i)