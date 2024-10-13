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
            run_updater()

        if args.restart.lower() == "y":
            launch_bot(args.bot, args.pasword)
        else:
            start()

    except SystemExit as e:
        print(f"Erreur lors de l'analyse des arguments : {e}")
        raise

def run_updater():
    print("Exécution de la mise à jour via updater.py...")
    try:
        subprocess.run(["python", "updater.py"], check=True)
        print("Mise à jour terminée. Relancement de Launcher.py...")
        subprocess.run(["python", "Launcher.py"], check=True)
    except Exception as e:
        print(f"Erreur lors de l'exécution de la mise à jour : {e}")
    exit()

liste = ["", "BetaBelouga", "Belouga", "GameHub"]

LICENCE = open("LICENCE").read()

def start():
    #print(LICENCE)
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

def launch_bot(bot_name, pasword):
    try:
        os.system(f"python bot.py {bot_name} --pasword {pasword}")
    except Exception as errors:
        print(f"Une erreur est survenue : {errors}")
        start()

if __name__ == '__main__':
    main()
