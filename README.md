# War

A command-line implementation of the card game War written in Python.

This repository contains both my original beginner implementation and an enhanced version created later to demonstrate the progression of my Python and software-development skills.

## Project Background

`war.py` was originally created while I was learning introductory Python programming.

The project introduced me to object-oriented programming through four primary classes:

* `Card`
* `Deck`
* `Player`
* `Game`

The original program uses a shuffled 52-card deck, compares cards between two players, tracks round wins, and determines a winner when the deck is exhausted.

I later revisited the project, repaired the original implementation while preserving its beginner-level design, and created `war_enhanced.py` as a more complete interpretation of the actual card game.

## Project Structure

```text
war/
├── README.md
├── war.py
├── war_enhanced.py
└── player_stats.json
```

### `war.py`

The restored version of the original beginner project.

It demonstrates early practice with:

* Classes and objects
* Special methods
* Card comparisons
* Lists
* Loops
* Conditionals
* User input
* Random deck shuffling
* Basic game state

The original design is intentionally preserved rather than rewritten to resemble the enhanced version.

### `war_enhanced.py`

A redesigned version using a more structured object-oriented architecture and rules closer to the traditional card game War.

## Player Modes

The enhanced game supports:

### One Player

Player vs Computer.

The player enters a name and plays against the computer.

### Two Players

Player vs Player.

Both players enter their names and their individual statistics are maintained between games.

## Rule Sets

Two rule variants are available.

### Classic War

When equal-ranked cards are drawn:

* War begins.
* Each player places three cards face down.
* Each player then draws another face-up card.
* The higher card wins the entire pot.

If another tie occurs, War continues recursively.

### Quick War

Uses the same rules but places only one card face down during War.

This reduces the number of cards consumed during a War and provides a faster alternative rule set.

## Game Controls

During a game:

```text
Enter - Draw next round
A     - Autoplay
S     - View stats
Q     - Quit game
```

Autoplay allows a complete game to continue without requiring input for every round.

Quitting ends the current game without recording it as a completed win or loss.

## Persistent Player Profiles

Player statistics are stored in:

```text
player_stats.json
```

Player names are treated case-insensitively for identity purposes.

For example:

```text
Javi
javi
JAVI
```

refer to the same saved player profile.

The original capitalization is retained for display.

## Separate Game Records

Statistics against the computer are kept separately from games against human players.

Each player profile maintains:

### VS Computer

* Games played
* Wins
* Losses
* Win rate
* Wars won
* Wars lost
* Longest game

### VS Players

* Games played
* Wins
* Losses
* Win rate
* Wars won
* Wars lost
* Longest game

This prevents Player vs Computer results from being mixed with Player vs Player results.

## Leaderboard

When the program exits, saved players are displayed on a persistent leaderboard.

The leaderboard includes:

* Total wins
* Total games
* Win percentage

Rankings prioritize total wins and use win percentage as an additional ranking factor.

## War Edge Cases

A player must have enough cards to complete the selected War sequence.

If a player cannot supply the required face-down cards and another face-up card during War, that player loses.

This prevents incomplete War sequences and provides a consistent rule for low-card situations.

## Deck Management

The enhanced version uses Python's `collections.deque`.

A deque provides efficient operations at both ends of a collection, making it well suited for a card deck where cards are drawn from the front and won cards are returned to the back.

## Running the Original Version

From PowerShell:

```powershell
python .\war.py
```

## Running the Enhanced Version

From PowerShell:

```powershell
python .\war_enhanced.py
```

No third-party packages are required.

## What This Project Demonstrates

Keeping both implementations in the same repository shows the progression from an introductory Python exercise to a more structured application.

The enhanced version demonstrates:

* Object-oriented design
* Separation of responsibilities
* Persistent JSON data
* File handling with `pathlib`
* `collections.deque`
* Input validation
* Recursive game behavior
* Multiple game modes
* Configurable rule sets
* Persistent player identities
* Statistics and leaderboard calculations
* Game-state management
* Edge-case handling
* Manual and automated execution modes

The goal of the enhanced version is not to erase the original project, but to demonstrate how the same concept can be redesigned as programming experience grows.
