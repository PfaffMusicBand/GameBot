import random
from collections import Counter

classes_cartes = ["commun", "atypique", "rare", "épique", "légendaire", "unique"]

cartes_commun = ["commune1", "commune2", "commune3", "commune4", "commune5", "commune6", "commune7", "commune8", "commune9", "commune10"]
cartes_atypique = ["atypique1", "atypique2", "atypique3", "atypique4", "atypique5", "atypique6", "atypique7", "atypique8", "atypique9", "atypique10"]
cartes_rare = ["rare1", "rare2", "rare3", "rare4", "rare5", "rare6", "rare7", "rare8", "rare9", "rare10"]
cartes_epique = ["epique1", "epique2", "epique3", "epique4", "epique5", "epique6", "epique7", "epique8", "epique9", "epique10"]
cartes_legendaire = ["legendaire1", "legendaire2", "legendaire3", "legendaire4", "legendaire5", "legendaire6", "legendaire7", "legendaire8", "legendaire9", "legendaire10"]
cartes_unique = ["unique1", "unique2", "unique3", "unique4", "unique5", "unique6", "unique7", "unique8", "unique9", "unique10"]

cartes_par_type = {
    "commun": cartes_commun,
    "atypique": cartes_atypique,
    "rare": cartes_rare,
    "épique": cartes_epique,
    "légendaire": cartes_legendaire,
    "unique": cartes_unique
}

probabilites_packs = {
    5000:[0.20, 0.30, 0.25, 0.15, 0.10, 0.01],
    3000: [0.20, 0.30, 0.25, 0.15, 0.10, 0.001],
    1500: [0.30, 0.30, 0.20, 0.15, 0.05, 0.001],
    1000: [0.40, 0.30, 0.20, 0.08, 0.02, 0.001],
    500: [0.45, 0.30, 0.15, 0.08, 0.02, 0.001],
    300: [0.50, 0.30, 0.15, 0.04, 0.01, 0.001],
    100: [0.60, 0.25, 0.10, 0.04, 0.01, 0.001],
    50: [0.70, 0.20, 0.07, 0.02, 0.01, 0.001],
    25: [0.80, 0.15, 0.04, 0.01, 0.005, 0.001],
    10: [0.85, 0.10, 0.04, 0.01, 0.005, 0.001],
    5: [0.90, 0.07, 0.02, 0.01, 0.005, 0.001],
}

def tirer_carte(probabilites):
    """Tire une carte selon les probabilités données."""
    type_carte = random.choices(classes_cartes, probabilites)[0]
    return type_carte

def generer_pack(cout):
    """Génère un pack de 10 cartes basé sur le coût."""
    cartes = []
    probabilites = probabilites_packs[cout]

    for _ in range(7):
        type_carte = tirer_carte(probabilites)
        cartes.append(random.choice(cartes_par_type[type_carte]))

    if cout >= 100:
        cartes.append(random.choice(cartes_par_type["rare"]))
    else:
        type_carte = tirer_carte(probabilites)
        cartes.append(random.choice(cartes_par_type[type_carte]))

    if cout >= 300:
        cartes.append(random.choice(cartes_par_type["épique"]))
    else:
        type_carte = tirer_carte(probabilites)
        cartes.append(random.choice(cartes_par_type[type_carte]))

    if cout >= 500:
        cartes.append(random.choice(cartes_par_type["légendaire"]))
    else:
        type_carte = tirer_carte(probabilites)
        cartes.append(random.choice(cartes_par_type[type_carte]))

    return cartes

def start():
    cout_pack = int(input("pack = "))
    r = int(input("range = "))
    
    total_cartes = Counter()
    type_counter = Counter()

    for _ in range(r):
        pack = generer_pack(cout_pack)
        total_cartes.update(pack)
        type_counter.update([c.split("1")[0] for c in pack])

    print(f"Total packs opened: {r}")
    print("Nombre de cartes par type:")
    for classe in classes_cartes:
        print(f"{classe}: {type_counter[classe]}")
    
    print("\nNombre d'exemplaires de chaque carte:")
    for carte, count in total_cartes.items():
        print(f"{carte}: {count}")

start()
