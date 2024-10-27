import random

number_to_guess = random.randint(1, 100)
attempts = 0
max_attempts = 3

while True:
    attempts +=1
    if attempts == max_attempts:
        print(f"Sorry, you've reached the maximum of {max_attempts} attemps")
        break
    guess = int(input("Guess the number (between 1 and 100): "))
    if guess < 1 or guess > 100:
        print("Invalid guess! Please enter a number between 1 and 100.")
        continue
    if guess < number_to_guess:
        print("Too low!")
    elif guess > number_to_guess:
        print("Too high!")
    else:
        print(f"Correct! You guessed the number in {attempts} attempts.")
        break
