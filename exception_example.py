class NegativeAgeError(Exception):
    def __init__(self, message):
        print(message)



def validate_age(age):
    if age < 0:
        raise NegativeAgeError("Age cannot be negative.")
    else:
        print(f"Age is {age}")


age = input("Enter your age: ")

try:
    validate_age(int(age))
except NegativeAgeError as e:
    age = str(age.replace("-", ""))
    validate_age(int(age))