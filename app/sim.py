# app/sim.py

import eval7
import random

def equity_vs_random_opponents(hero, board, opponents=1, iterations=2000):
    """
    hero  = [eval7.Card, eval7.Card]
    board = [eval7.Card, ...] (0–5 cards)
    """

    hero_cards = hero
    board_cards = board

    used = set(hero_cards + board_cards)

    hero_wins = 0
    villain_wins = 0
    ties = 0

    for _ in range(iterations):

        # ---------------------------------
        # Build a FRESH deck every iteration
        # ---------------------------------
        deck = eval7.Deck()
        deck.cards = [c for c in deck.cards if c not in used]
        deck.shuffle()

        # ---------------------------------
        # Deal villain hands
        # ---------------------------------
        villains = []
        for _ in range(opponents):
            v1 = deck.deal(1)[0]
            v2 = deck.deal(1)[0]
            villains.append([v1, v2])

        # ---------------------------------
        # Complete the community board
        # ---------------------------------
        need = 5 - len(board_cards)
        sim_board = board_cards + deck.deal(need)

        # ---------------------------------
        # Evaluate hero
        # ---------------------------------
        hero_val = eval7.evaluate(hero_cards + sim_board)

        # ---------------------------------
        # Evaluate best villain
        # ---------------------------------
        best_val = -1
        for hand in villains:
            val = eval7.evaluate(hand + sim_board)
            if val > best_val:
                best_val = val

        # ---------------------------------
        # Compare
        # ---------------------------------
        if hero_val > best_val:
            hero_wins += 1
        elif hero_val < best_val:
            villain_wins += 1
        else:
            ties += 1

    total = hero_wins + villain_wins + ties

    return (
        hero_wins / total,
        villain_wins / total,
        ties / total,
        {"iterations": iterations},
    )

def preflop_equity(hero_cards, iterations=7500, opponents=1):
    deck = [eval7.Card(card) for card in [
        r+s for r in "23456789TJQKA" for s in "cdhs"
    ]]

    hero = [eval7.Card(c) for c in hero_cards]

    # Remove hero cards from deck
    for c in hero:
        deck.remove(c)

    hero_wins = 0
    total = 0

    for _ in range(iterations):
        random.shuffle(deck)

        # deal opponent(s) 2 cards
        villains = [deck[i:i+2] for i in range(0, opponents * 2, 2)]

        # deal 5 board cards
        board = deck[opponents * 2 : opponents * 2 + 5]

        hero_val = eval7.evaluate(hero + board)
        best_vill = max(eval7.evaluate(v + board) for v in villains)

        if hero_val > best_vill:
            hero_wins += 1
        elif hero_val == best_vill:
            hero_wins += 0.5

        total += 1

    return hero_wins / total
