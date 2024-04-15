import os
import argparse

def main():
    try:
        parser = argparse.ArgumentParser(description='Scripte Launcher.')
        parser.add_argument('--bot', type=str, default="Bot", help='Nom du bot à lancer')
        parser.add_argument('--version', type=float, default=1.2, help='Version du scripte de bot actuel.')
        parser.add_argument('--restart', type=str, default="n", help='Redémarage du bot y/n.')
        args = parser.parse_args()

        if args.restart.lower() == "y":
            launch_bot(args.bot, args.version)
        else:
            start()

    except SystemExit as e:
        print(f"Erreur lors de l'analyse des arguments : {e}")
        raise

os.system("cls||clear")

liste = ["SettoOwner","BetaBelouga","Belouga","GameHub"]

LICENCE = open("LICENCE").read()
print(LICENCE)

def start():
    bot = input(f"""
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@    _________________________________________________________________________________________________________________    @
@                                                                                                                         @
@    #####  ###### #      ###### #    # ######      #      #      #    #     #     ##   # ###### #    # ###### #####      @
@    #    # #      #      #    # #    # #    #     # #     #      #    #    # #    # #  # #      #    # #      #    #     @
@    #####  ####   #      #    # #    # #         #   #    #      #    #   #   #   #  # # #      ###### ####   #####      @
@    #    # #      #      #    # #    # #   ###  #######   #      #    #  #######  #   ## #      #    # #      #    #     @
@    #####  #####  ###### ###### ###### ######  #       #  ###### ###### #       # #    # ###### #    # ###### #     #    @
@    _________________________________________________________________________________________________________________    @
@                                                                                             By Smaugue#9833             @
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
=========================================================
|    Bienvenu dans le BelougaLuncher.                   |
|    Quel bot désirez vous lancer?                      |
|    _____________________________                      |
|   |[versions]|[___Bot___]|[code]|                     |
|   |   <1.2   |BetaBelouga|   1  |                     |
|   |   <1.2   |  Belouga  |   2  |                     |
|   |   <1.2   |  GameHub  |   3  |                     |
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
|   |  GH(1.1) |  1.1 |                                 |
|   |  BB(1.2) |  1.2 |                                 |
|   |BB/GH(1.3)|  1.3 |                                 |
|   '''''''''''''''''''                                 |
=========================================================

Version=>   """)
    try:
        launch_bot(bot_name = liste[int(bot)], bot_version=float(version))
    except Exception as errors:
        print(f"Une erreur est survenue:{errors}")
        start()
    pass

def launch_bot(bot_name, bot_version):
    try:
        os.system(f"python BOT_V{bot_version}.py {bot_name}")
    except Exception as errors:
        print(f"Une erreur est survenue : {errors}")
        start()
        
if __name__ == '__main__':
    main()