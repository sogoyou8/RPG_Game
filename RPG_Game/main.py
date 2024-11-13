import os
from random import randint
from colorama import Fore, Style
from entity import Mob, Player
from objects import Object
from biome import Biome


class Game:
    def __init__(self, player):
        self.player = player
        self.biomes = {
            "plains": Biome("plains", "PLAINS", False),
            "forest": Biome("forest", "WOODS", True),
            "fields": Biome("fields", "FIELDS", False),
            "bridge": Biome("bridge", "BRIDGE", False),
            "town": Biome("town", "TOWN CENTRE", False),
            "shop": Biome("shop", "SHOP", False),
            "mayor": Biome("mayor", "MAYOR", False),
            "cave": Biome("cave", "CAVE", True),
            "mountain": Biome("mountain", "MOUNTAIN", True),
            "hills": Biome("hills", "HILLS", True)
        }
        self.map = [
            [self.biomes["plains"], self.biomes["plains"], self.biomes["plains"], self.biomes["plains"], self.biomes["forest"], self.biomes["mountain"], self.biomes["cave"]],
            [self.biomes["forest"], self.biomes["forest"], self.biomes["forest"], self.biomes["forest"], self.biomes["forest"], self.biomes["hills"], self.biomes["mountain"]],
            [self.biomes["forest"], self.biomes["fields"], self.biomes["bridge"], self.biomes["plains"], self.biomes["hills"], self.biomes["forest"], self.biomes["hills"]],
            [self.biomes["plains"], self.biomes["shop"], self.biomes["town"], self.biomes["mayor"], self.biomes["plains"], self.biomes["hills"], self.biomes["mountain"]],
            [self.biomes["plains"], self.biomes["fields"], self.biomes["fields"], self.biomes["plains"],self.biomes["hills"], self.biomes["mountain"], self.biomes["mountain"]]
        ]
        self.mob_types = {    
        "Goblin": Mob("Goblin", 1, 15, 3, 1, 8, 15),
        "Orc": Mob("Orc", 2, 35, 3, 2, 18, 30),
        "Slime": Mob("Slime", 2, 30, 4, 1, 12, 20),
        "Dragon": Mob("Dragon", 3, 50, 7, 3, 20, 200)
        }
        self.mobs = [self.mob_types["Goblin"], self.mob_types["Orc"], self.mob_types["Slime"], self.mob_types["Slime"], self.mob_types["Goblin"]]
        self.boss = self.mob_types["Dragon"]
        self.fight = False

    def heal(self, amount):
        if self.player.HP + amount < self.player.HPMAX:
            self.player.HP += amount
        else:
            self.player.HP = self.player.HPMAX
        print(f"{self.player.name}'s HP refilled to {self.player.HP}!")

    def gain_xp(self, amount):
        self.player.xp += amount
        print(f"{self.player.name} a gagné {amount} XP!")

        if self.player.xp >= self.player.xp_needed:
            self.player.level_up()

    def mayor(self):
        global speak
        speak = True  # Assurez-vous que 'speak' est initialisé

        while speak:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.draw()
            print("Hello there, " + self.player.name + "!")
            if self.player.ATK < 10:
                print(
                    "You're not strong enough to face the dragon yet! Keep practicing and come back later!")
                self.player.inventory["key"].count = 0
            else:
                print(
                    "You might want to take on the dragon now! Take this key but be careful with the beast!")
                self.player.inventory["key"].count = 1

            self.draw()
            print("1 - LEAVE")
            self.draw()

            choice = input("# ")

            if choice == "1":
                speak = False
        
    def draw(self):
        # Méthode d'affichage personnalisée
        print(f"You're in {self.map[self.player.y][self.player.x].name}.")

    def save_game(self):
        # Méthode de sauvegarde générique
        raise NotImplementedError(
            "La méthode 'save_game' doit être implémentée par les sous-classes.")

    def load_game(self):
        # Méthode de chargement générique
        raise NotImplementedError(
            "La méthode 'load_game' doit être implémentée par les sous-classes.")

    def delete_save(self):
        # Méthode de suppression générique
        raise NotImplementedError(
            "La méthode 'delete_save' doit être implémentée par les sous-classes.")

    def possible_moves(self):
        raise NotImplementedError(
            "La méthode 'possible_moves' doit être implémentée par les sous-classes.")


class RPGGame(Game):
    def save_game(self):
        list_data = [
            self.player.name,
            str(self.player.HP),
            str(self.player.ATK),
            str(self.player.DEF),
            str(self.player.level),
            str(self.player.xp),
            str(self.player.gold),
            str(self.player.x),
            str(self.player.y),
            str(self.player.inventory["potion"].count),
            str(self.player.inventory["elixir"].count),
            str(self.player.inventory["atk_boost"].count),
            str(self.player.inventory["def_boost"].count),
            str(self.player.inventory["key"].count)
        ]

        file_name = f"save_{self.player.name}.txt"
        with open(file_name, "w") as f:
            for item in list_data:
                f.write(item + "\n")
        print(f"Partie sauvegardée dans {file_name}!")

    def load_game(self):
        save_files = [f for f in os.listdir() if f.startswith(
            "save_") and f.endswith(".txt")]
        if not save_files:
            print("Aucune partie sauvegardée trouvée.")
            return False

        print("Parties sauvegardées disponibles :")
        for idx, file in enumerate(save_files):
            print(f"{idx + 1}. {file}")
        print("0. Annuler")

        choice = input(
            "Choisis un numéro de sauvegarde (ou 0 pour annuler) : ")

        if choice == "0":
            print("Annulation du chargement.")
            return False

        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(save_files):
            print("Choix invalide.")
            return False

        with open(save_files[int(choice) - 1], "r") as f:
            load_list = f.readlines()

        self.player.name = load_list[0].strip()
        self.player.HP = int(load_list[1].strip())
        self.player.ATK = int(load_list[2].strip())
        self.player.DEF = int(load_list[3].strip())
        self.player.level = int(load_list[4].strip())
        self.player.xp = int(load_list[5].strip())
        self.player.gold = int(load_list[6].strip())
        self.player.x = int(load_list[7].strip())
        self.player.y = int(load_list[8].strip())
        self.player.inventory["potion"].count = int(load_list[9].strip())
        self.player.inventory["elixir"].count = int(load_list[10].strip())
        self.player.inventory["atk_boost"].count = int(load_list[11].strip())
        self.player.inventory["def_boost"].count = int(load_list[12].strip())
        self.player.inventory["key"].count = int(load_list[13].strip())

        print(f"Partie '{self.player.name}' chargée avec succès!")
        return True

    def delete_save(self):
        save_files = [f for f in os.listdir() if f.startswith(
            "save_") and f.endswith(".txt")]
        if not save_files:
            print("Aucune sauvegarde disponible à supprimer.")
            return

        print("Sauvegardes disponibles :")
        for idx, file in enumerate(save_files):
            print(f"{idx + 1}. {file}")
        print("0. Annuler")

        choice = input(
            "Choisis un numéro pour supprimer une sauvegarde (ou 0 pour annuler) : ")

        if choice == "0":
            print("Annulation de la suppression.")
            return

        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(save_files):
            print("Choix invalide.")
            return

        file_to_delete = save_files[int(choice) - 1]
        os.remove(file_to_delete)
        print(f"Sauvegarde '{file_to_delete}' supprimée avec succès.")

    def deplacer(self, direction):
        if direction == "1" and self.player.y > 0:  # North
            self.player.y -= 1
            print("Vous allez vers le nord.")
        elif direction == "2" and self.player.x < len(self.map[0]) - 1:  # East
            self.player.x += 1
            print("Vous allez vers l'est.")
        elif direction == "3" and self.player.y < len(self.map) - 1:  # South
            self.player.y += 1
            print("Vous allez vers le sud.")
        elif direction == "4" and self.player.x > 0:  # West
            self.player.x -= 1
            print("Vous allez vers l'ouest.")
        else:
            print("Déplacement impossible dans cette direction.")
            return
        
        if self.map[self.player.y][self.player.x].ennemy & randint(0, 8) == 1:
            self.fight = True
            print("Un ennemi apparaît !")
            self.battle()

    def possible_moves(self):
        moves = []
        if self.player.y > 0:  # Nord
            moves.append("1")  # 1 correspond à Nord
        if self.player.x < len(self.map[0]) - 1:  # Est
            moves.append("2")  # 2 correspond à Est
        if self.player.y < len(self.map) - 1:  # Sud
            moves.append("3")  # 3 correspond à Sud
        if self.player.x > 0:  # Ouest
            moves.append("4")  # 4 correspond à Ouest
        return moves

    def shop(self):
        while True:
            # Nettoie le terminal
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Bienvenue au magasin !")
            print(f"OR : {self.player.gold}")
            print(f"POTIONS : {self.player.inventory['potion'].count}")
            print(f"ELIXIRS : {self.player.inventory['elixir'].count}")
            print(f"BOOST ATTAQUE : {self.player.inventory['atk_boost'].count}")
            print(f"BOOST DÉFENSE : {self.player.inventory['def_boost'].count}")
            print("=" * 30)
            print("0 - Quitter")
            print("1 - Acheter POTION (5 or)")
            print("2 - Acheter ELIXIR (8 or)")
            print("3 - Acheter BOOST ATTAQUE (10 or)")
            print("4 - Acheter BOOST DÉFENSE (10 or)")
            print("=" * 30)

            choice = input("Choisis une option : ")

            if choice == "1":
                if self.player.gold >= 5:
                    confirm = input(
                        "Confirmer l'achat de POTION pour 5 or ? (o/n) : ").lower()
                    if confirm == 'o':
                        self.player.inventory["potion"].count += 1
                        self.player.gold -= 5
                        print("Tu as acheté une potion !")
                    else:
                        print("Achat annulé.")
                else:
                    print("Pas assez d'or.")
            elif choice == "2":
                if self.player.gold >= 8:
                    confirm = input(
                        "Confirmer l'achat d'ELIXIR pour 8 or ? (o/n) : ").lower()
                    if confirm == 'o':
                        self.player.inventory["elixir"].count += 1
                        self.player.gold -= 8
                        print("Tu as acheté un élixir !")
                    else:
                        print("Achat annulé.")
                else:
                    print("Pas assez d'or.")
            elif choice == "3":
                if self.player.gold >= 10:
                    confirm = input(
                        "Confirmer l'achat de BOOST ATTAQUE pour 10 or ? (o/n) : ").lower()
                    if confirm == 'o':
                        self.player.inventory["atk_boost"].count += 1
                        self.player.gold -= 10
                        print("Tu as acheté un boost d'attaque !")
                    else:
                        print("Achat annulé.")
                else:
                    print("Pas assez d'or.")
            elif choice == "4":
                if self.player.gold >= 10:
                    confirm = input(
                        "Confirmer l'achat de BOOST DÉFENSE pour 10 or ? (o/n) : ").lower()
                    if confirm == 'o':
                        self.player.inventory["def_boost"].count += 1
                        self.player.gold -= 10
                        print("Tu as acheté un boost de défense !")
                    else:
                        print("Achat annulé.")
                else:
                    print("Pas assez d'or.")
            elif choice == "0":
                break
            else:
                print("Choix invalide.")
                
    def cave(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Une porte massive bloque le chemin.")
        if self.player.inventory["key"].count:
            print("1 - UTILISER LA CLÉ")
        print("2 - REVENIR")
        choice = input("# ")
        if choice == "1" and self.player.inventory["key"].count:
            print("La porte s'ouvre et vous entrez dans la grotte...")
            self.battle(isBoss=True)
        else:
            print("Vous sortez de la grotte.")

    def battle(self, isBoss=False):
        if len(self.mobs) == 0 and not isBoss:
            return
        self.fight = True
        # Combat avec un ennemi
        if isBoss:
            enemy = self.boss
            print(f"Vous sentez une présence menaçante...")
        else:
            id = randint(0, len(self.mobs) - 1)
            enemy = self.mobs[id]
        print(f"Un {enemy.name} apparaît !")
        while self.fight:
            print(f"{self.player.name} HP: {self.player.HP}")
            print(f"{enemy.name} HP: {enemy.HP}")
            print("1 - Attaquer")
            print("2 - Utiliser un objet")
            print("3 - Fuir")
            choice = input("# ")
            if choice == "1":
                # Attaque du joueur
                damage = self.player.ATK - enemy.DEF
                if damage < 0:
                    damage = 0
                enemy.HP -= damage
                print(f"Vous infligez {damage} points de dégâts à {enemy.name}!")
                if enemy.HP <= 0:
                    print(f"Vous avez vaincu le {enemy.name}!")
                    self.fight = False
                    self.gain_xp(enemy.XP)
                    self.player.gold += enemy.gold
                    print(f"{self.player.name} a gagné {enemy.gold} XP!")
                    if not isBoss:
                        enemy.HP = enemy.base_HP
                        self.mobs.pop(id)
                    break
                # Attaque de l'ennemi
                damage = enemy.ATK - self.player.DEF
                if damage < 0:
                    damage = 0
                self.player.HP -= damage
                print(f"{enemy.name} vous inflige {damage} points de dégâts!")
                if self.player.HP <= 0:
                    print("Vous avez été vaincu!")
                    self.fight = False
                    enemy.HP = enemy.base_HP
                    break
            elif choice == "2":
                self.utiliser_objet()
            elif choice == "3":
                print("Vous avez fui le combat!")
                self.fight = False
                enemy.HP = enemy.base_HP
                break
            else:
                print("Choix invalide.")

    def afficher_statut(self):
        os.system('cls' if os.name == 'nt' else 'clear')  # Nettoie le terminal
        print(f"{Fore.CYAN}{'=' * 30}")
        print(f"{'STATUT DU PERSONNAGE':^30}")
        print(f"{'=' * 30}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Location:{Style.RESET_ALL} {self.map[self.player.y][self.player.x].name}")
        print(f"{Fore.GREEN}Name:{Style.RESET_ALL} {self.player.name}")
        print(f"{Fore.BLUE}LVL:{Style.RESET_ALL} {self.player.level}")
        print(f"{Fore.BLUE}XP:{Style.RESET_ALL} {self.player.xp}/{self.player.xp_needed}")
        print(f"{Fore.RED}HP:{Style.RESET_ALL} {self.player.HP}/{self.player.HPMAX} ")
        print(f"{Fore.BLUE}ATK:{Style.RESET_ALL} {self.player.ATK}")
        print(f"{Fore.LIGHTBLUE_EX}DEF:{Style.RESET_ALL} {self.player.DEF}")
        print(f"{Fore.MAGENTA}Potions:{Style.RESET_ALL} {self.player.inventory['potion'].count}")
        print(f"{Fore.CYAN}Elixirs:{Style.RESET_ALL} {self.player.inventory['elixir'].count}")
        print(f"{Fore.YELLOW}Gold:{Style.RESET_ALL} {self.player.gold}")
        print(f"{Fore.WHITE}Coordonnées:{Style.RESET_ALL} {self.player.x}, {self.player.y}")

        # Afficher les mouvements possibles
        moves = self.possible_moves()
        print(f"{Fore.CYAN}Mouvements possibles: {' , '.join(moves)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 30}{Style.RESET_ALL}")

    def confirm_and_use_item(self, item_key, effect_description, effect_function):
        if self.player.inventory[item_key].count > 0:
            confirm = input(f"Confirmer l'utilisation de {effect_description} ? (oui/non) : ").lower()
            if confirm == "oui":
                self.player.inventory[item_key].count -= 1
                effect_function()  # Appelle la fonction d'effet
                print(f"Vous avez utilisé {effect_description.lower()} !")
            else:
                print("Utilisation annulée.")
        else:
            print(f"Pas de {effect_description.lower()} disponibles.")

    def utiliser_objet(self):
        while True:
            # Nettoie le terminal
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Inventaire :")
            print("=" * 30)
            print("0 - Annuler")
            print(
                f"1 - POTION ({self.player.inventory['potion'].count} disponibles) (+30 HP)")
            
            print(
                f"2 - ELIXIR ({self.player.inventory['elixir'].count} disponibles) (+50 HP)")
            print(
                f"3 - BOOST ATTAQUE ({self.player.inventory['atk_boost'].count} disponibles) (+2 ATK)")
            print(
                f"4 - BOOST DÉFENSE ({self.player.inventory['def_boost'].count} disponibles) (+2 DEF)")
            print("=" * 30)

            choice = input("Choisis un objet à utiliser : ")

            if choice == "0":
                break
            elif choice == "1":
                self.confirm_and_use_item(
                    "potion", "POTION", lambda: self.heal(30))
            elif choice == "2":
                self.confirm_and_use_item(
                    "elixir", "ELIXIR", lambda: self.heal(50))
            elif choice == "3":
                self.confirm_and_use_item(
                    "atk_boost", "BOOST ATTAQUE", lambda: self.increase_stat("ATK", 2))
            elif choice == "4":
                self.confirm_and_use_item(
                    "def_boost", "BOOST DÉFENSE", lambda: self.increase_stat("DEF", 2))
            else:
                print("Choix invalide.")

    # Fonction pour ajuster une statistique
    def increase_stat(self, stat, amount):
        setattr(self.player, stat, getattr(self.player, stat) + amount)
        print(f"{stat} augmenté de {amount}!")

    def entrer(self):
        location = self.map[self.player.y][self.player.x].name
        if location == "shop":
            self.shop()
        elif location == "mayor":
            self.mayor()
        elif location == "cave":
            self.cave()
        else:
            print("Il n'y a rien à entrer ici.")

    def peut_entrer(self):
        # Vérifie si le joueur est dans un lieu où il peut entrer
        location = self.map[self.player.y][self.player.x].name
        return location in ["shop", "mayor", "cave"]

    # def afficher_carte(self):
    #     os.system('cls' if os.name == 'nt' else 'clear')  # Nettoie le terminal
    #     print("Carte du monde :")
    #     for y in range(len(self.map)):
    #         for x in range(len(self.map[y])):
    #             if x == self.x and y == self.y:
    #                 print(Fore.RED + "P", end=" ")  # 'P' pour Player en rouge
    #             else:
    #                 print(Fore.GREEN + ".", end=" ")  # '.' pour d'autres endroits en vert
    #         print(Style.RESET_ALL)  # Réinitialise le style après chaque ligne

    def afficher_carte(self):
        print("Carte actuelle :")
        for i in range(len(self.map)):
            line = ""
            for j in range(len(self.map[i])):
                if i == self.player.y and j == self.player.x:
                    line += "[P] "  # P pour Player
                else:
                    # Première lettre de chaque biome
                    line += self.map[i][j].name[0].upper() + " "
            print(line)

    def afficher_inventaire(self):
        print(f"{Fore.CYAN}{'=' * 30}")
        print(f"{'INVENTAIRE':^30}")
        print(f"{'=' * 30}{Style.RESET_ALL}")
        for item, quantity in self.player.inventory.items():
            print(f"{Fore.YELLOW}{item.capitalize()}: {Style.RESET_ALL}{quantity}")
        print(f"{Fore.CYAN}{'=' * 30}{Style.RESET_ALL}")

    def jouer(self):
        while True:
            self.afficher_statut()
            self.afficher_carte()

            # Obtenir les mouvements possibles
            moves_possibles = self.possible_moves()
            print("0 - Quitter")
            if "1" in moves_possibles:
                print("1 - NORTH ↑")
            if "2" in moves_possibles:
                print("2 - EAST →")
            if "3" in moves_possibles:
                print("3 - SOUTH ↓")
            if "4" in moves_possibles:
                print("4 - WEST ←")
            print("5 - Utiliser un objet")

            # Afficher l'option d'entrer seulement si c'est possible
            if self.peut_entrer():
                print("6 - Entrer")

            choice = input("Choisis une option : ")

            if choice == "0":
                print("Merci d'avoir joué!")
                self.save_game()
                break
            elif choice in moves_possibles:
                self.deplacer(choice)
            elif choice == "5":
                self.utiliser_objet()
            elif choice == "6" and self.peut_entrer():
                self.entrer()
            else:
                print("Choix invalide.")

    def heal(self, amount):
        super().heal(amount)  # Appel de la méthode parente pour conserver le comportement de base
        # Comportement spécifique
        print(" Heal ")

    def gain_xp(self, amount):
        # Appel de la méthode parente pour conserver le comportement de base
        super().gain_xp(amount)
        # Comportement spécifique supplémentaire
        print("RPGGame: Gain d'XP ")


def afficher_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{Fore.GREEN}{'WELCOME IN THE GAME!':^30}{Style.RESET_ALL}")
    print(f"{'1. CREATE NEW GAME':^30}")
    print(f"{'2. LOAD SAVE GAME':^30}")
    print(f"{'3. DELETE SAVE GAME':^30}")
    print(f"{'4. ABOUT':^30}")
    print(f"{'5. EXIT':^30}")
    print(f"{'=' * 30}")


def main():
    # Créer une instance de RPGGame pour gérer les sauvegardes
    game_instance = RPGGame(player=Player("Hero"))

    while True:
        afficher_menu()
        choix = input("Veuillez faire un choix : ")

        if choix == '1':
            name = input("Entrez le nom de votre personnage : ")
            game_instance = RPGGame(player=Player(name))
            print("Démarrage d'une nouvelle partie...")
            game_instance.jouer()  # Lancer le jeu après avoir créé une nouvelle partie

        elif choix == '2':
            # Nom temporaire pour charger la sauvegarde
            game_instance = RPGGame(player=Player("Hero"))
            if game_instance.load_game():
                game_instance.jouer()  # Lancer le jeu après avoir chargé une sauvegarde

        elif choix == '3':
            # Nom temporaire pour accéder à la méthode delete_save
            game_instance = RPGGame(player=Player("Temp"))
            game_instance.delete_save()
        elif choix == '4':
            print("À propos")
            # Appeler la fonction à propos (à implémenter)
        elif choix == '5':
            print("Merci d'avoir joué ! À bientôt.")
            break
        else:
            print("Choix invalide, veuillez réessayer.")


if __name__ == "__main__":
    main()



