import random as rd

black = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
red = []
green = 0

def get_bet(balance):
    while True:
        try:
            raw_bet = input("Place your bets (e.g., '10 on 12, 5 on 7'): ")
            individual_bets = raw_bet.split(',')
            bets = []
            total_amount = 0
            for bet in individual_bets:
                bet = bet.split('on')
                if len(bet) % 2 != 0:  # Fix: Check exactly one "on"
                    print("Wrong format for a bet, use 'amount on number', e.g., '10 on 12'")
                    break
                bet = [part.strip() for part in bet]
                amount = int(bet[0])
                number = int(bet[1])
                if not (1 <= amount <= balance and 0 <= number <= 36):
                    print(f"Invalid bet: {bet[0]} on {bet[1]}. Amount must be 1-{balance}, number must be 0-36")
                    break
                bets.append((amount, number))
                total_amount += amount
            else:
                if total_amount == 0:
                    print("No bets placed. Try again.")
                    continue
                if total_amount <= balance:
                    return total_amount, bets  # Return both
                print(f"Total bets ({total_amount}) exceed balance ({balance}).")
        except ValueError:
            print("Enter valid numbers, e.g., '10 on 12, 5 on 7'.")

for i in range(1, 37):
    if i not in black:
        red.append(i)

even = []
odd = []

for i in range(1, 37):
    if i % 2 == 0:
        even.append(i)
    else:
        odd.append(i)

first_3rd = []
second_3rd = []
third_3rd = []
non_3rd = []

for i in range(0,37):
    if i <13:
        first_3rd.append(i)
    elif i > 12 and i < 25:
        second_3rd.append(i)
    elif i > 24:
        third_3rd.append(i)
    else:
        non_3rd.append(i)

def spin_wheel():
    number = rd.randint(0, 36)
    number = 1 #test

    if number in black:
        colour = "Black"
    elif number in red:
        colour = "Red"
    else:
        colour = "Green"

    if number in first_3rd:
        third = "First 3rd"
    elif number in second_3rd:
        third = "Second 3rd"
    elif number in third_3rd:
        third = "Third 3rd"
    else:
        third = "Non 3rd number"

    if number in even:
        parity = "Even"
    elif number in odd:
        parity = "Odd"
    else:
        parity = "0"

    print(f"The ball landed on {colour} {number}, {parity}, {third}")


    return number, colour, parity, third


def evaluate_results(bets, balance, number, colour, parity, third):
    j=0
    number_result = number
    for j in range(len(bets)):
        if bets[j][1] == number_result:
            balance += bets[j][0] * 35 + bets[j][0]
            
    return balance
        

def play_roulette(balance=100):
    history = []

    while balance > 0:
        total_bet, bets = get_bet(balance)  # Unpack both values
        balance -= total_bet  # Subtract total amount
        number, colour, parity, third = spin_wheel()
        balance = evaluate_results(bets, balance, number, colour, parity, third)
        history.append([number, colour, parity, third])

        while True:
            print("\nHistory:")
            for i, spin in enumerate(history, 1):
                number, colour, parity, third = spin
                print(f"Spin {i}: {colour} {number}, {parity}, {third}")
                print(f"\nYour balance: {balance}")    
                again = input("\nPlay again? (y/n): ").lower().strip()
                
            
            if again == 'n':
                print("\nThanks for playing! Here's the spin history:")
                for spin in history: 
                    print(spin)
                return  # Exit the game
            elif again == 'y':
                break  # Break inner loop and spin again
            else:
                print("Invalid input. Please enter 'y' or 'n'.")
            print(f"Your balance is: {balance}")
            
                
            






play_roulette()