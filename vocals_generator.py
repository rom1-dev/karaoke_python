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

def find_lyrics_txt_file(name):
    for root, dirs, files in os.walk("./songs"):
        for dirname in dirs:
            if dirname == name:
                for file in os.listdir(os.path.join(root, dirname)):
                    if file.endswith(".txt"):
                        return os.path.join(root, dirname, file)
    return None

def to_list(list_of_lists):
    """Convertit une liste de listes en une liste plate."""
    return [item for sublist in list_of_lists for item in sublist]


import pyttsx3
import os















son = "avf" # Nom de la chanson à traiter
















# Nom du sous-dossier où enregistrer les syllabes
sous_dossier = f"songs/{son}/syllabes"

def enregistrer_syllabe(syllabe, nom_fichier):
    """Enregistre la synthèse vocale d'une syllabe dans un fichier audio."""
    engine = pyttsx3.init()
    engine.setProperty('rate', 150000)  # Vitesse de la voix
    chemin_fichier = os.path.join(sous_dossier, nom_fichier)

    # Vérifier si l'enregistrement au format MP3 est supporté
    try:
        engine.save_to_file(syllabe, chemin_fichier)
        engine.runAndWait()
        print(f"La syllabe '{syllabe}' a été enregistrée dans '{chemin_fichier}'")
        return True
    except Exception as e:
        print(f"Erreur lors de l'enregistrement de '{syllabe}': {e}")
        print("Le format MP3 n'est peut-être pas directement supporté.")
        print("Essayez un autre format comme '.wav' si le moteur le permet.")
        return False

if __name__ == "__main__":
    syllabes = parse_lyrics_txt_file(find_lyrics_txt_file(son))
    syllabes_a_enregistrer = to_list(syllabes)
    noms_fichiers = [f"syllabe_{"0"*(len(str(len(syllabes_a_enregistrer)))-len(str(i)))}{i}.mp3" for i in range(len(syllabes_a_enregistrer))]

    # Créer le sous-dossier s'il n'existe pas déjà
    if not os.path.exists(sous_dossier):
        os.makedirs(sous_dossier)
        print(f"Le sous-dossier '{sous_dossier}' a été créé.")

    for syllabe, nom_fichier in zip(syllabes_a_enregistrer, noms_fichiers):
        enregistrer_syllabe(syllabe, nom_fichier)

    print("L'enregistrement de toutes les syllabes est terminé dans le sous-dossier.")