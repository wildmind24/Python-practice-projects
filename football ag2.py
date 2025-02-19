import random

# Create classes for all involved in the game: Agent, Player, Club.

# Agent Class
class Agent:
    def __init__(self, name):
        self.name = name
        self.reputation = 0
        self.earnings = 0
        self.players = []
        self.skill_level = 1

    def sign_player(self, player):
        self.players.append(player)
        print(f"{player.name} has been signed to your agency!")

    def negotiate_contract(self, player, club):
        print(f"\nNegotiating {player.name}'s transfer to {club.name}...")
        offer = club.make_offer(player)
        print(f"{club.name} offers {offer:.2f} Naira for {player.name}.")

        negotiation_chance = random.uniform(0.8, 1.5) + (self.skill_level * 0.1)
        decision = input("Do you accept the offer? (yes/no): ").lower()

        if decision == "yes":
            if negotiation_chance > 1 and offer <= club.budget:
                club.budget -= offer
                self.earnings += offer * 0.10
                player.current_club = club.name
                self.reputation += 1
                self.skill_level += 0.1
                print(f"Transfer successful! You earned {offer * 0.10:.2f} Naira. Skill level increased!")
            elif offer > club.budget:
                print("The club does not have enough budget.")
            else:
                print("Negotiation failed. Skill level remains the same.")
        elif decision == "no":
            print("Negotiation declined.")
        else:
            print("Invalid response.")

# Player Class
class Player:
    def __init__(self, name, position, rating):
        self.name = name
        self.position = position
        self.rating = rating
        self.market_value = rating * 1000
        self.current_club = None
        self.morale = 100
        self.fitness = 100

    def update_rating(self, new_rating):
        self.rating = new_rating
        self.market_value = new_rating * 1000
        print(f"{self.name}'s rating has been updated to {new_rating}.")

    def update_morale(self, morale_change):
        self.morale = max(0, min(100, self.morale + morale_change))
        print(f"{self.name}'s morale is now {self.morale}.")

    def update_fitness(self, fitness_change):
        self.fitness = max(0, min(100, self.fitness + fitness_change))
        print(f"{self.name}'s fitness is now {self.fitness}.")

# Club Class
class Club:
    def __init__(self, name, budget, required_positions):
        self.name = name
        self.budget = budget
        self.required_positions = required_positions

    def make_offer(self, player):
        return player.market_value * random.uniform(0.8, 1.2)

# GameManager Class
class GameManager:
    def __init__(self):
        self.agent = None
        self.available_players = []
        self.clubs = []
        self.current_month = 1

    def start_game(self):
        print("Welcome to My Football Agent Management Game")
        agent_name = input("Enter your agent name: ")
        self.agent = Agent(agent_name)
        print(f"Agent {agent_name} profile created\n")

        self.generate_players()
        self.generate_clubs()
        self.game_loop()

    def generate_players(self):
        positions = ["Forward", "Midfielder", "Defender", "Goalkeeper"]
        names = ["Philip", "Goodluck", "Musa", "BAT", "Peter", "Eze", "Rugger"]

        selected_names = random.sample(names, 5)  # Randomly choose 5 unique names
        for name in selected_names:
            position = random.choice(positions)
            rating = random.randint(60, 90)
            player = Player(name, position, rating)
            self.available_players.append(player)
        print("Players generated!\n")

    def generate_clubs(self):
        club_names = ["Remo Stars", "Intersport FC", "United Legends", "Lasgidi City Strikers"]
        for name in club_names:
            budget = random.randint(70000, 200000000)
            required_positions = ["Forward", "Midfielder", "Defender"]
            club = Club(name, budget, required_positions)
            self.clubs.append(club)
        print("Clubs generated!\n")

    def game_loop(self):
        while True:
            print(f"\n--- Month: {self.current_month} ---")
            print("1. View Available Players")
            print("2. Sign a Player")
            print("3. Negotiate Player Transfer")
            print("4. View Agent Profile")
            print("5. Advance Time (Next Month)")
            print("6. Quit Game")

            choice = input("Choose an option: ")
            if choice == "1":
                self.show_available_players()
            elif choice == "2":
                self.sign_player()
            elif choice == "3":
                self.negotiate_transfer()
            elif choice == "4":
                self.view_agent_profile()
            elif choice == "5":
                self.advance_time()
            elif choice == "6":
                print("Thank you for playing bye bye")
                break
            else:
                print("Invalid option. Please try again.")

    def show_available_players(self):
        print("\n--- Available Players ---")
        for i, player in enumerate(self.available_players):
            print(f"{i+1}. {player.name} - {player.position}, Rating: {player.rating}, Value: {player.market_value:.2f} Naira")

    def sign_player(self):
        self.show_available_players()
        try:
            choice = int(input("Enter the number of the player to sign: ")) - 1
            if 0 <= choice < len(self.available_players):
                player = self.available_players.pop(choice)
                self.agent.sign_player(player)
            else:
                print("Invalid choice.")
        except (ValueError, IndexError):
            print("Invalid input. Please enter a valid number.")

    def negotiate_transfer(self):
        if not self.agent.players:
            print("You have no players to negotiate transfers for.")
            return

        print("\n--- Your Players ---")
        for i, player in enumerate(self.agent.players):
            print(f"{i+1}. {player.name} - {player.position}, Rating: {player.rating}, Club: {player.current_club or 'Free Agent'}")

        try:
            player_choice = int(input("Choose a player: ")) - 1
            if 0 <= player_choice < len(self.agent.players):
                player = self.agent.players[player_choice]
                club = random.choice(self.clubs)
                self.agent.negotiate_contract(player, club)
            else:
                print("Invalid choice.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    def view_agent_profile(self):
        print("\n--- Agent Profile ---")
        print(f"Name: {self.agent.name}")
        print(f"Reputation: {self.agent.reputation}")
        print(f"Earnings: {self.agent.earnings:.2f} Naira")
        print(f"Skill Level: {self.agent.skill_level:.1f}")
        print("Players Managed:")
        for player in self.agent.players:
            print(f"  - {player.name} ({player.position}, Rating: {player.rating})")

    def advance_time(self):
        self.current_month += 1
        print(f"Time advanced to Month {self.current_month}.")
        for player in self.agent.players:
            morale_change = random.randint(-10, 10)
            fitness_change = random.randint(-10, 5)
            player.update_morale(morale_change)
            player.update_fitness(fitness_change)

game_manager = GameManager()
game_manager.start_game()