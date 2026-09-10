import json
import random
from collections import deque
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
STATS_FILE = BASE_DIR / "player_stats.json"

SUITS = ("Spades", "Hearts", "Diamonds", "Clubs")
RANKS = {
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
    7: "7",
    8: "8",
    9: "9",
    10: "10",
    11: "Jack",
    12: "Queen",
    13: "King",
    14: "Ace",
}

RULES = {
    "classic": {
        "name": "Classic War",
        "face_down": 3,
    },
    "quick": {
        "name": "Quick War",
        "face_down": 1,
    },
}


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return f"{RANKS[self.rank]} of {self.suit}"


class Deck:
    def __init__(self):
        self.cards = [
            Card(rank, suit)
            for rank in RANKS
            for suit in SUITS
        ]
        random.shuffle(self.cards)

    def deal(self):
        midpoint = len(self.cards) // 2

        return (
            deque(self.cards[:midpoint]),
            deque(self.cards[midpoint:]),
        )


class Player:
    def __init__(self, name, cards=None, is_computer=False):
        self.name = name
        self.cards = cards if cards is not None else deque()
        self.is_computer = is_computer

    def draw_card(self):
        if not self.cards:
            return None

        return self.cards.popleft()

    def collect_cards(self, cards):
        cards = list(cards)
        random.shuffle(cards)
        self.cards.extend(cards)

    def card_count(self):
        return len(self.cards)


def load_stats():
    try:
        with STATS_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, dict):
            return data

    except (FileNotFoundError, json.JSONDecodeError):
        pass

    return {}


def save_stats(stats):
    with STATS_FILE.open("w", encoding="utf-8") as file:
        json.dump(stats, file, indent=4)


def normalize_name(name):
    return name.strip().lower()


def get_player_name(prompt, disallowed_name=None):
    while True:
        name = input(prompt).strip()

        if not name:
            print("Name cannot be empty.")
            continue

        if (
            disallowed_name
            and normalize_name(name) == normalize_name(disallowed_name)
        ):
            print("Players must use different names.")
            continue

        return name


def ensure_player(stats, name):
    key = normalize_name(name)

    if key not in stats:
        stats[key] = {
            "display_name": name,
            "vs_computer": {
                "games": 0,
                "wins": 0,
                "losses": 0,
                "wars_won": 0,
                "wars_lost": 0,
                "longest_game": 0,
            },
            "vs_player": {
                "games": 0,
                "wins": 0,
                "losses": 0,
                "wars_won": 0,
                "wars_lost": 0,
                "longest_game": 0,
            },
        }

    return key


def choose_player_mode():
    while True:
        print("\nChoose player mode:")
        print("1. One Player - Player vs Computer")
        print("2. Two Players - Player vs Player")

        choice = input("Enter your choice: ").strip().lower()

        if choice in ("1", "one", "one player"):
            return "computer"

        if choice in ("2", "two", "two players"):
            return "player"

        print("Invalid choice. Please choose 1 or 2.")


def choose_rules():
    while True:
        print("\nChoose rules:")
        print("1. Classic War")
        print("   3 cards face down during War.")
        print("2. Quick War")
        print("   1 card face down during War.")

        choice = input("Enter your choice: ").strip().lower()

        if choice in ("1", "classic", "classic war"):
            return "classic"

        if choice in ("2", "quick", "quick war"):
            return "quick"

        print("Invalid choice. Please choose 1 or 2.")


def display_player_stats(stats, name):
    key = normalize_name(name)

    if key not in stats:
        print(f"\nNo saved statistics for {name}.")
        return

    profile = stats[key]

    print(f"\n--- Player Stats: {profile['display_name']} ---")

    for mode_key, label in (
        ("vs_computer", "VS COMPUTER"),
        ("vs_player", "VS PLAYERS"),
    ):
        record = profile[mode_key]
        games = record["games"]
        wins = record["wins"]

        win_rate = (wins / games * 100) if games else 0

        print(f"\n{label}")
        print(f"Games: {games}")
        print(f"Wins: {wins}")
        print(f"Losses: {record['losses']}")
        print(f"Win rate: {win_rate:.1f}%")
        print(f"Wars won: {record['wars_won']}")
        print(f"Wars lost: {record['wars_lost']}")
        print(f"Longest game: {record['longest_game']} rounds")


def display_leaderboard(stats):
    if not stats:
        print("\nNo player statistics yet.")
        return

    rankings = []

    for profile in stats.values():
        computer = profile["vs_computer"]
        player = profile["vs_player"]

        wins = computer["wins"] + player["wins"]
        games = computer["games"] + player["games"]
        win_rate = (wins / games * 100) if games else 0

        rankings.append(
            (
                profile["display_name"],
                wins,
                games,
                win_rate,
            )
        )

    rankings.sort(
        key=lambda entry: (entry[1], entry[3]),
        reverse=True,
    )

    print("\n--- Leaderboard ---")

    for position, entry in enumerate(rankings, start=1):
        name, wins, games, win_rate = entry

        print(
            f"{position}. {name} - "
            f"{wins} wins / {games} games "
            f"({win_rate:.1f}%)"
        )


class Game:
    def __init__(
        self,
        player1,
        player2,
        rule_key,
        mode,
        stats,
    ):
        self.player1 = player1
        self.player2 = player2
        self.rule_key = rule_key
        self.rules = RULES[rule_key]
        self.mode = mode
        self.stats = stats

        self.rounds = 0
        self.wars_won = {
            normalize_name(player1.name): 0,
            normalize_name(player2.name): 0,
        }

    def display_score(self):
        print(
            f"\n{self.player1.name}: "
            f"{self.player1.card_count()} cards"
        )
        print(
            f"{self.player2.name}: "
            f"{self.player2.card_count()} cards"
        )

    def battle(self, pot):
        card1 = self.player1.draw_card()
        card2 = self.player2.draw_card()

        if card1 is None:
            return self.player2

        if card2 is None:
            return self.player1

        pot.extend((card1, card2))

        print(f"\n{self.player1.name}: {card1}")
        print(f"{self.player2.name}: {card2}")

        if card1.rank > card2.rank:
            return self.player1

        if card2.rank > card1.rank:
            return self.player2

        return self.handle_war(pot)

    def handle_war(self, pot):
        print("\n*** WAR! ***")

        face_down = self.rules["face_down"]
        required_cards = face_down + 1

        if self.player1.card_count() < required_cards:
            print(
                f"{self.player1.name} does not have "
                "enough cards to continue the War."
            )
            return self.player2

        if self.player2.card_count() < required_cards:
            print(
                f"{self.player2.name} does not have "
                "enough cards to continue the War."
            )
            return self.player1

        for _ in range(face_down):
            pot.append(self.player1.draw_card())
            pot.append(self.player2.draw_card())

        print(
            f"Each player places {face_down} "
            "card(s) face down."
        )

        winner = self.battle(pot)

        if winner is not None:
            winner_key = normalize_name(winner.name)
            self.wars_won[winner_key] += 1

        return winner

    def play_round(self):
        if not self.player1.cards:
            return self.player2

        if not self.player2.cards:
            return self.player1

        self.rounds += 1
        pot = []

        print(f"\n--- Round {self.rounds} ---")

        winner = self.battle(pot)

        if winner:
            winner.collect_cards(pot)
            print(
                f"{winner.name} wins the round "
                f"and collects {len(pot)} cards."
            )

        self.display_score()

        return None

    def determine_winner(self):
        if not self.player1.cards:
            return self.player2

        if not self.player2.cards:
            return self.player1

        if self.player1.card_count() > self.player2.card_count():
            return self.player1

        if self.player2.card_count() > self.player1.card_count():
            return self.player2

        return None

    def update_stats(self, winner):
        mode_key = (
            "vs_computer"
            if self.mode == "computer"
            else "vs_player"
        )

        players_to_record = [self.player1]

        if self.mode == "player":
            players_to_record.append(self.player2)

        for player in players_to_record:
            key = ensure_player(self.stats, player.name)
            record = self.stats[key][mode_key]

            record["games"] += 1
            record["longest_game"] = max(
                record["longest_game"],
                self.rounds,
            )

            if winner and normalize_name(winner.name) == key:
                record["wins"] += 1
            else:
                record["losses"] += 1

            wars_won = self.wars_won.get(key, 0)
            record["wars_won"] += wars_won

        if self.mode == "player" and winner:
            winner_key = normalize_name(winner.name)

            loser = (
                self.player2
                if winner is self.player1
                else self.player1
            )

            loser_key = normalize_name(loser.name)

            winner_wars = self.wars_won.get(winner_key, 0)
            loser_wars = self.wars_won.get(loser_key, 0)

            self.stats[loser_key][mode_key]["wars_lost"] += (
                winner_wars
            )

            self.stats[winner_key][mode_key]["wars_lost"] += (
                loser_wars
            )

        elif self.mode == "computer":
            player_key = normalize_name(self.player1.name)

            computer_wars = self.wars_won.get(
                normalize_name(self.player2.name),
                0,
            )

            self.stats[player_key][mode_key]["wars_lost"] += (
                computer_wars
            )

        save_stats(self.stats)

    def play(self):
        autoplay = False
        quit_game = False

        print(
            f"\nStarting {self.rules['name']}!"
        )
        self.display_score()

        while self.player1.cards and self.player2.cards:
            if not autoplay:
                print("\nChoose an action:")
                print("Enter - Draw next round")
                print("A     - Autoplay")
                print("S     - View stats")
                print("Q     - Quit game")

                action = input("> ").strip().lower()

                if action == "a":
                    autoplay = True
                    print("\nAutoplay enabled.")

                elif action == "s":
                    display_player_stats(
                        self.stats,
                        self.player1.name,
                    )

                    if self.mode == "player":
                        display_player_stats(
                            self.stats,
                            self.player2.name,
                        )

                    continue

                elif action == "q":
                    quit_game = True
                    break

                elif action != "":
                    print(
                        "Invalid choice. Press Enter, "
                        "A, S, or Q."
                    )
                    continue

            game_winner = self.play_round()

            if game_winner:
                break

        if quit_game:
            print("\nGame ended early.")

            winner = self.determine_winner()

            if winner:
                print(
                    f"{winner.name} was leading with "
                    f"{winner.card_count()} cards."
                )
            else:
                print("The players were tied.")

            print(
                "Statistics were not recorded because "
                "the game was not completed."
            )
            return

        winner = self.determine_winner()

        print("\n=== GAME OVER ===")

        if winner:
            print(
                f"{winner.name} wins after "
                f"{self.rounds} rounds!"
            )
        else:
            print(
                f"The game ends in a tie after "
                f"{self.rounds} rounds."
            )

        self.update_stats(winner)

        display_player_stats(
            self.stats,
            self.player1.name,
        )

        if self.mode == "player":
            display_player_stats(
                self.stats,
                self.player2.name,
            )


def create_game(stats):
    mode = choose_player_mode()
    rule_key = choose_rules()

    deck = Deck()
    cards1, cards2 = deck.deal()

    if mode == "computer":
        name1 = get_player_name(
            "\nEnter your name: "
        )

        player1 = Player(name1, cards1)
        player2 = Player(
            "Computer",
            cards2,
            is_computer=True,
        )

        ensure_player(stats, name1)

    else:
        name1 = get_player_name(
            "\nPlayer 1 name: "
        )

        name2 = get_player_name(
            "Player 2 name: ",
            disallowed_name=name1,
        )

        player1 = Player(name1, cards1)
        player2 = Player(name2, cards2)

        ensure_player(stats, name1)
        ensure_player(stats, name2)

    save_stats(stats)

    return Game(
        player1,
        player2,
        rule_key,
        mode,
        stats,
    )


def play_again():
    while True:
        choice = input(
            "\nPlay another game? (y/n): "
        ).strip().lower()

        if choice in ("y", "yes"):
            return True

        if choice in ("n", "no"):
            return False

        print("Please enter y or n.")


def main():
    stats = load_stats()

    print("========================")
    print("     ENHANCED WAR")
    print("========================")

    while True:
        game = create_game(stats)
        game.play()

        if not play_again():
            break

    display_leaderboard(stats)

    print("\nThanks for playing!")


if __name__ == "__main__":
    main()