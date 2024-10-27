import random

options = ['rock', 'paper', 'scissors']
computer_choice = random.choice(options)

user_choice = input("Enter your choice (rock, paper, scissors): ").lower()

if user_choice not in options:
    print("Invalid choice!")
elif user_choice == computer_choice:
    print(f"Both chose {computer_choice}. It's a tie!")
elif (user_choice == 'rock' and computer_choice == 'scissors') or \
        (user_choice == 'paper' and computer_choice == 'rock') or \
        (user_choice == 'scissors' and computer_choice == 'paper'):
    print(f"You win! Computer chose {computer_choice}.")
else:
    print(f"You lose! Computer chose {computer_choice}.")
