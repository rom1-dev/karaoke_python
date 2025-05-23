import difflib

def find_nearest(chaine_entree, liste_de_chaines):
    """
    Trouve la chaîne de caractères la plus proche dans une liste donnée.

    Args:
        chaine_entree (str): La chaîne de caractères à rechercher.
        liste_de_chaines (list): La liste de chaînes dans laquelle chercher.

    Returns:
        tuple: Un tuple contenant (chaine_la_plus_proche, ratio_de_similitude).
               Retourne (None, 0.0) si la liste est vide.
    """
    if not liste_de_chaines:
        return None, 0.0

    meilleure_correspondance = None
    meilleur_ratio = 0.0

    for chaine_cible in liste_de_chaines:
        # Calcule le ratio de similitude entre la chaîne d'entrée et la chaîne cible
        ratio = difflib.SequenceMatcher(None, chaine_entree.lower(), chaine_cible.lower()).ratio()

        if ratio > meilleur_ratio:
            meilleur_ratio = ratio
            meilleure_correspondance = chaine_cible

    return meilleure_correspondance, meilleur_ratio

# --- Exemple d'utilisation ---
if __name__ == "__main__":
    liste_de_chaines = ["apple", "banana", "orange", "grape"]
    chaine_entree = "appl"
    
    correspondance, ratio = find_nearest(chaine_entree, liste_de_chaines)
    print(f"Chaîne la plus proche : {correspondance}, Ratio de similitude : {ratio:.2f}")