import os
import argparse
import subprocess

def main():
    try:
        parser = argparse.ArgumentParser(description='Scripte Launcher.')
        parser.add_argument('--bot', type=str, default="Bot", help='Nom du bot à lancer')
        parser.add_argument('--restart', type=str, default="n", help='Redémarage du bot y/n.')
        parser.add_argument('--pasword', type=str, default="pasword", help="Mot de passe")
        parser.add_argument('--update', action='store_true', help="Vérifie la mise à jour avant de lancer")
        args = parser.parse_args()

        if args.update:
            if args.restart.lower() == "y":
                with open("temp_args", "w") as temp_file:
                    temp_file.write(f"{args.bot},{args.pasword}")
            run_updater()

        if args.restart.lower() == "y":
            launch_bot(args.bot, args.pasword)

        else:
            try:
                with open("temp_args", "r") as temp_file:
                    ligne = temp_file.readline()
                if ligne != "":
                    bot, pasword = ligne.split(",")
                    os.remove("temp_args")
                    launch_bot(bot, pasword)
            except:
                start()

    except SystemExit as e:
        print(f"Erreur lors de l'analyse des arguments : {e}")
        raise

LICENCE = open("LICENCE").read()

def force_run_updater():
    print(LICENCE)
    print("Exécution de la mise à jour via updater.py...")
    try:
        subprocess.run(["python", "updater.py", "--force"], check=True)
        print("Mise à jour terminée. Relancement de Launcher.py...")
        subprocess.run(["python", "Launcher.py"], check=True)
    except Exception as e:
        print(f"Erreur lors de l'exécution de la mise à jour : {e}")
    exit()

def run_updater():
    print(LICENCE)
    print("Exécution de la mise à jour via updater.py...")
    try:
        subprocess.run(["python", "updater.py"], check=True)
        print("Mise à jour terminée. Relancement de Launcher.py...")
        subprocess.run(["python", "Launcher.py"], check=True)
    except Exception as e:
        print(f"Erreur lors de l'exécution de la mise à jour : {e}")
    exit()

liste = ["", "BetaBelouga", "Belouga", "GameHub"]

def start():
    choice = input("""
Sélectionner une option:
[1]Choix du Bot
[2]Terminal
[3]Licence
[4]Mise à jour 
""")
    if not choice.isdigit():
        print("Veuillez entrer un entier valide.")
        start()
    if choice == "4":
        option = input("""
[1]Check&Update
[2]Force Update
""")
        if not option.isdigit():
            print("Veuillez entrer un entier valide.")
            start()
        if option == "1":
            run_updater()
        if option == "2":
            force_run_updater()
        else: start()
    if choice == "3":
        print(LICENCE)
        start()
    if choice == "2":
        commande = input("launcher:")
        try:
            os.system(commande)
        except Exception as e:
            print(e)
        start()
    if choice == "1":
        bot = input(f"""
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@    _________________________________________________________________________________________________________________    @
@                                                                                                                         @
@    #####  ###### #      ###### #    # ######      #      #          #     #    # #    # ###### #    # ###### #####      @
@    #    # #      #      #    # #    # #    #     # #     #         # #    #    # # #  # #      #    # #      #    #     @
@    #####  ####   #      #    # #    # #         #   #    #        #   #   #    # #  # # #      ###### ####   #####      @
@    #    # #      #      #    # #    # #   ###  #######   #       #######  #    # #   ## #      #    # #      #    #     @
@    #####  #####  ###### ###### ###### ######  #       #  ###### #       # ###### #    # ###### #    # ###### #     #    @
@    _________________________________________________________________________________________________________________    @
@                                                                                             By Smaugue#9833             @
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
=========================================================
|    Bienvenu dans le BelougaLuncher.                   |
|    Quel bot désirez vous lancer?                      |
|    _____________________________                      |
|   |[versions]|[___Bot___]|[code]|                     |
|   |     x    |BetaBelouga|   1  |                     |
|   |     x    |  Belouga  |   2  |                     |
|   |     x    |  GameHub  |   3  |                     |
|   '''''''''''''''''''''''''''''''                     |
=========================================================

Bot=>   """)
        if not bot.isdigit():
            print("Veuillez entrer un entier valide.")
            start()

        pasword = input("Pasword =>")

        try:
            launch_bot(bot_name = liste[int(bot)], pasword=pasword)
        except Exception as errors:
            print(f"Une erreur est survenue : {errors}")
            start()
    else: start()

def launch_bot(bot_name, pasword):
    try:
        os.system(f"python bot.py {bot_name} --pasword {pasword}")
    except Exception as errors:
        print(f"Une erreur est survenue : {errors}")
        start()

if __name__ == '__main__':
    main()
