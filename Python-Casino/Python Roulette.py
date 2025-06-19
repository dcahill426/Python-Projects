import random as rd

black = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
red = []
green = 0

colours = ["red", "green", "black"]

high = []
low = []
half = ["high", "low"]

even = []
odd = []
parity = ["even", "odd"]

for i in range(1, 37):
    if i not in black: # red and black
        red.append(i)
    
    if i < 19:
        low.append(i)
    else:
        high.append(i)
    
    
    if i % 2 == 0: # even and odd
        even.append(i)
    else:
        odd.append(i)
    

first = []
second = []
third = []
non_3rd = 0
dozen = ["first", "second", "third"]

for i in range(0,37):
    if i <13:
        first.append(i)
    elif i > 12 and i < 25:
        second.append(i)
    elif i > 24:
        third.append(i)
        
def get_bet(balance):
    while True:
        try:
            raw_bet = input("Place your bets (e.g., '10 on 12, 5 on red, 20 on first'): ")
            individual_bets = raw_bet.split(',')
            bets = []
            total_amount = 0
            for bet in individual_bets:
                bet = bet.split('on')
                if len(bet) != 2:  # Changed to != 2 for clarity
                    print("Invalid format. Use 'amount on target', e.g., '10 on 12' or '5 on red'.")
                    break
                bet = [part.strip() for part in bet]
                try:
                    amount = int(bet[0])
                except ValueError:
                    print(f"Invalid amount: '{bet[0]}'. Must be a number (1–{balance}).")
                    break
                
                if bet[1].isdigit():
                    target = int(bet[1])
                    btype = "number"
                elif bet[1].lower() in colours:
                    target = bet[1].lower()
                    btype = "colour"
                elif bet[1].lower() in parity:
                    target = bet[1].lower()
                    btype = "parity"
                elif bet[1].lower() in half:
                    target = bet[1].lower()
                    btype = "half"
                elif bet[1].lower() in dozen:
                    target = bet[1].lower()
                    btype = "dozen"
                else:
                    print(f"Invalid target: '{bet[1]}'. Use a number (0–36), colour (red, black, green), dozen (first, second, third), high/low, or even/odd.")
                    break
                
                if not 1 <= amount <= balance:
                    print(f"Invalid amount: {amount}. Must be between 1 and {balance}.")
                    break
                
                if btype == "number":
                    if not 0 <= target <= 36:
                        print(f"Invalid number: {bet[1]}. Must be between 0 and 36.")
                        break
                elif btype == "colour":
                    if target not in colours:
                        print(f"Invalid colour: {bet[1]}. Must be red, black, or green.")
                        break
                elif btype == "parity":
                    if target not in parity:
                        print(f"Invalid parity: {bet[1]}. Must be even or odd.")
                        break
                elif btype == "half":
                    if target not in half:
                        print(f"Invalid high/low: {bet[1]}. Must be high or low.")
                        break
                elif btype == "dozen":
                    if target not in dozen:
                        print(f"Invalid dozen: {bet[1]}. Must be first, second, or third.")
                        break
                
                bets.append((amount, target, btype))
                total_amount += amount
            else:
                if total_amount == 0:
                    print("No bets placed. Please place at least one valid bet.")
                    continue
                if total_amount > balance:
                    print(f"Total bets ({total_amount}) exceed balance ({balance}). Try again.")
                    continue
                return total_amount, bets
        except ValueError:
            print("Invalid input. Use format 'amount on target', e.g., '10 on 12, 5 on red'.")

def spin_wheel():
    number = rd.randint(0, 36)

    if number in black:
        colour = "Black"
    elif number in red:
        colour = "Red"
    else:
        colour = "Green"

    if number in first:
        third = "First 3rd"
    elif number in second:
        third = "Second 3rd"
    elif number in third:
        third = "Third 3rd"
    else:
        third = "0"

    if number in even:
        parity = "Even"
    elif number in odd:
        parity = "Odd"
    else:
        parity = "0"
        
    if number in high:
        half = "High"
    elif number in low:
        half = "Low"
    else:
        half = "0"

    print(f"The ball landed on {colour} {number}, {parity}, {third}, {half}")


    return number, colour, parity, third, half


def evaluate_results(bets, balance, number, colour, parity, third, half):
    j=0
    number_result = number
    colour_result = colour.lower()
    parity_result = parity.lower()
    dozen_result = third.lower()
    half_result = half.lower()
    for j in range(len(bets)):
        if bets[j][1] == number_result:
            balance += bets[j][0] * 35 + bets[j][0]
        
        if bets[j][1] == colour_result: 
            if colour_result == "green":
                balance += bets[j][0] * 35 + bets[j][0]
            else: 
                balance += bets[j][0] * 2
            
        if bets[j][1] == parity_result: 
            balance += bets[j][0] * 2
            
        if bets[j][1] == dozen_result: 
            balance += bets[j][0] * 3
            
        if bets[j][1] == half_result: 
            balance += bets[j][0] * 2
            
    return balance
        

def play_roulette(balance=100):
    
    print("""
-------------------------------------
|  1  |  2  |  3  |                |
-------------------------------------
|  4  |  5  |  6  |                |
-------------------------------------
|  7  |  8  |  9  |                |
-------------------------------------
| 10  | 11  | 12  | First (1–12)   |
-------------------------------------
| 13  | 14  | 15  |                |
-------------------------------------
| 16  | 17  | 18  |                |
-------------------------------------
| 19  | 20  | 21  |                |
-------------------------------------
| 22  | 23  | 24  | Second (13–24) |
-------------------------------------
| 25  | 26  | 27  |                |
-------------------------------------
| 28  | 29  | 30  |                |
-------------------------------------
| 31  | 32  | 33  |                |
-------------------------------------
| 34  | 35  | 36  | Third (25–36)  |
-------------------------------------
Bet Options:
- Numbers: 0–36 (pays 35:1)
- Colours: red, black, green (pays 1:1, green 35:1)
- Dozens: first, second, third (pays 2:1)
- High/Low: high (19–36), low (1–18) (pays 1:1)
- Even/Odd: even, odd (pays 1:1)
""")
    
    history = []

    while balance > 0:
        total_bet, bets = get_bet(balance)  # Unpack both values
        balance -= total_bet  # Subtract total amount
        number, colour, parity, third, half = spin_wheel()
        history.append([number, colour, parity, third])
        balance = evaluate_results(bets, balance, number, colour, parity, third, half)
        
        print(f"\nYour balance: {balance}")       
        print("\nHistory:")
        for i, spin in enumerate(history, 1):
            number, colour, parity, third = spin
            print(f"Spin {i}: {colour} {number}, {parity}, {third}")
            
        exit = input("\nType 'n' to exit or press Enter to continue: ").lower().strip()

        while True:                    
            if exit == 'n':
                print("\nThanks for playing! Here's the spin history:")
                for spin in history: 
                    print(spin)
                return  # Exit the game
            else:
                 break
            print(f"Your balance is: {balance}")
                         
play_roulette()
