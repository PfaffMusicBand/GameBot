import os
import argparse

def main():
    try:
        parser = argparse.ArgumentParser(description='Scripte Launcher.')
        parser.add_argument('--bot', type=str, default="Bot", help='Nom du bot à lancer')
        parser.add_argument('--version', type=float, default=1.4, help='Version du scripte de bot actuel.')
        parser.add_argument('--restart', type=str, default="n", help='Redémarage du bot y/n.')
        parser.add_argument('--pasword', type=str, default="pasword", help="Mot de passe")
        args = parser.parse_args()
        if args.restart.lower() == "y":
            launch_bot(args.bot, args.version, args.pasword)
        else:
            start()

    except SystemExit as e:
        print(f"Erreur lors de l'analyse des arguments : {e}")
        raise

os.system("cls||clear")

liste = ["","BetaBelouga","Belouga","GameHub"]

LICENCE = open("LICENCE").read()
print(LICENCE)

def start():
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
    print(f"""
Bot: {liste[int(bot)]}
    """)
    version = input(f"""
=========================================================
|    Selectionnez une version:                          |
|    _________________                                  |
|   |[versions]|[code]|                                 |
|   |   1.4    |  1.4 |                                 |
|   '''''''''''''''''''                                 |
=========================================================

Version=>   """)
    pasword = input("Pasword =>")

    try:
        launch_bot(bot_name = liste[int(bot)], bot_version=float(version), pasword=pasword)
    except Exception as errors:
        print(f"Une erreur est survenue:{errors}")
        start()
    pass

def launch_bot(bot_name, bot_version, pasword):
    try:
        os.system(f"python BOT_V{bot_version}.py {bot_name} --pasword {pasword}")
    except Exception as errors:
        print(f"Une erreur est survenue : {errors}")
        start()
        
if __name__ == '__main__':
    main()