import random as rand

# Constants
numbers = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"]
suits = ["Hearts", "Diamonds", "Clubs", "Spades"]

# Create and shuffle a new deck
def create_deck():
    deck = [(str(num), suit) for num in numbers for suit in suits]
    rand.shuffle(deck)
    return deck

# Deal a card from the deck
def deal_card(deck):
    if len(deck) == 0:
        deck.extend(create_deck())
    return deck.pop()

# Calculate the value of a blackjack hand
def calculate_hand(hand):
    value = 0
    num_aces = 0
    for num, _ in hand:
        if num in ["J", "Q", "K"]:
            value += 10
        elif num == "A":
            value += 11
            num_aces += 1
        else:
            value += int(num)

    while value > 21 and num_aces:
        value -= 10
        num_aces -= 1

    return value

# Get player's bet
def get_bet(balance):
    while True:
        try:
            bet = int(input(f"Place your bet (1-{balance}): "))
            if 1 <= bet <= balance:
                return bet
            print(f"Invalid bet. Must be between 1 and {balance}.")
        except ValueError:
            print("Enter a valid number.")

# Player turn (handles splits and double downs clearly)
def player_turn(deck, balance, initial_bet, player_hand):
    hands = [player_hand]
    hand_bets = [initial_bet]
    hand_results = []

    hand_index = 0
    while hand_index < len(hands):
        hand = hands[hand_index]  
        bet = hand_bets[hand_index]

        while True:
            hand_value = calculate_hand(hand)
            print(f"\nPlaying Hand {hand_index + 1}: {hand} (Value: {hand_value})")

            # ✅ Blackjack is an instant win (dealer does not play)
            if hand_value == 21 and len(hand) == 2:
                print(f"🎉 Blackjack! Hand {hand_index + 1} automatically wins.")
                return [hand], [('blackjack_win', bet)], balance, False  # Dealer skips turn

            if hand_value > 21:
                print(f"Hand {hand_index + 1} busted!")
                hand_results.append(('lose', bet))
                break

            choices = ['h', 's']
            prompt_choices = "h/s"
            if len(hand) == 2 and balance >= bet:
                choices.append('dd')
                prompt_choices += "/dd"
                if hand[0][0] == hand[1][0]:
                    choices.append('sp')
                    prompt_choices += "/sp"

            choice = input(f"Choose ({prompt_choices}): ").lower()

            if choice == 'h':
                hand.append(deal_card(deck))
                print(f"Hand {hand_index + 1}: {hand} (Value: {calculate_hand(hand)})")

            elif choice == 's':
                print(f"Hand {hand_index + 1} stands at {calculate_hand(hand)}.")
                hand_results.append(('stand', bet))
                break

            elif choice == 'dd' and 'dd' in choices:
                balance -= bet
                bet *= 2
                hand_bets[hand_index] = bet
                hand.append(deal_card(deck))
                print(f"Hand {hand_index + 1} doubled down: {hand} (Value: {calculate_hand(hand)})")
                if calculate_hand(hand) > 21:
                    print("You busted after doubling down!")
                    hand_results.append(('lose', bet))
                else:
                    hand_results.append(('stand', bet))
                break

            elif choice == 'sp' and 'sp' in choices:
                balance -= bet
                card1, card2 = hand
                new_hand1 = [card1, deal_card(deck)]
                new_hand2 = [card2, deal_card(deck)]

                hands[hand_index] = new_hand1
                hands.insert(hand_index + 1, new_hand2)
                hand_bets.insert(hand_index + 1, bet)

                print("\nHand split into:")
                print(f" Hand {hand_index + 1}: {new_hand1} (Value: {calculate_hand(new_hand1)})")
                print(f" Hand {hand_index + 2}: {new_hand2} (Value: {calculate_hand(new_hand2)})")
                
                hand = hands[hand_index]
                continue

            else:
                print("Invalid choice. Please try again.")
                continue

        hand_index += 1

    all_busted = all(result[0] == 'lose' for result in hand_results)

    return hands, hand_results, balance, all_busted

# Game outcome logic
def evaluate_results(hands, results, dealer_hand, balance):
    dealer_value = calculate_hand(dealer_hand)
    print(f"\nDealer's final hand ({dealer_value}): {dealer_hand}\n")

    for i, ((result, bet), hand) in enumerate(zip(results, hands)):
        player_value = calculate_hand(hand)
        print(f"Hand {i+1} ({player_value}): {hand}")
        if result == 'lose':
            print(f"😢 Hand {i+1} loses {bet} chips.")
        elif dealer_value > 21 or player_value > dealer_value:
            print(f"🎉 Hand {i+1} wins! Gained {bet} chips.")
            balance += bet * 2
        elif player_value == dealer_value:
            print(f"😐 Hand {i+1} pushes. Bet returned.")
            balance += bet
        else:
            print(f"😢 Hand {i+1} loses {bet} chips.")
    return balance

# Main game loop
def play_blackjack(balance=100):
    deck = create_deck()
    print("\n=== WELCOME TO BLACKJACK! 🃏 ===\n")

    while balance > 0:
        # ✅ Check if deck needs reshuffling before the round starts
        if len(deck) < 0.25 * 52:
            print("\n🔄 Deck penetration reached! Reshuffling the deck...\n")
            deck = create_deck()  # ✅ Completely reset the deck

        print(f"\nBalance: {balance} chips")
        bet = get_bet(balance)
        balance -= bet

        # 🃏 Deal player’s hand first!
        player_hand = [deal_card(deck), deal_card(deck)]
        print(f"\nYour hand: {player_hand} (Value: {calculate_hand(player_hand)})")

        # 👇 Show the dealer’s first card AFTER player’s hand
        dealer_hand = [deal_card(deck), deal_card(deck)]
        print(f"\nDealer's first card: {dealer_hand[0]}")
        print("Dealer's second card: 🃏 Hidden Card")

        # ✅ Check if dealer has Blackjack before the player plays
        if calculate_hand(dealer_hand) == 21:
            print(f"\n🚨 Dealer has Blackjack! Revealing second card...")
            print(f"Dealer's full hand: {dealer_hand} (Value: 21)")

            if calculate_hand(player_hand) == 21:
                print("😐 Push! You both have Blackjack. Bet returned.")
                balance += bet
            else:
                print("😢 Dealer wins with Blackjack. You lose this round.")

            print(f"\nNew balance: {balance}")
            continue  # Skip to next round immediately

        # If dealer doesn't have Blackjack, continue with player's turn
        player_hands, player_results, balance, all_busted = player_turn(deck, balance, bet, player_hand)

        # ✅ If player won with Blackjack, dealer loses instantly
        if any(result[0] == 'blackjack_win' for result in player_results):
            print("\n🚀 Blackjack! You win instantly. Dealer does not play.")
            balance += bet * 2  # Pays out 1:1 (adjust if using 3:2 payout)
            print(f"\nNew balance: {balance}")
            continue  # Skip to next round

        if not all_busted:
            print(f"\nDealer reveals second card: {dealer_hand[1]}")
            print(f"Dealer's full hand: {dealer_hand} (Value: {calculate_hand(dealer_hand)})")

            while calculate_hand(dealer_hand) < 17:
                dealer_hand.append(deal_card(deck))
                print(f"Dealer draws: {dealer_hand[-1]} (Value now: {calculate_hand(dealer_hand)})")
        else:
            print("All player hands busted. Dealer does not draw further cards.")

        balance = evaluate_results(player_hands, player_results, dealer_hand, balance)

        print(f"\nNew balance: {balance}")

        if balance == 0:
            print("\nYou're out of chips! Game over.")
            break

        
        while True:  # ✅ Keep asking until input is valid
            again = input("\nPlay again? (y/n): ").lower().strip()
        
            if again == 'n':
                print(f"Final balance: {balance}. Thanks for playing!")
                return  # ✅ Exit the loop and end the game
            elif again == 'y':
                break  # ✅ Start a new round
            else:
                print("Invalid input. Please enter 'y' or 'n'.")  # ✅ Re-prompt without extra continue

        
    

if __name__ == "__main__":
    play_blackjack()
