import requests

def get_conversion_rate(from_currency, to_currency, amount):
    url = "https://exchange-rate-api1.p.rapidapi.com/latest"

    querystring = {"base":from_currency.upper()}

    headers = {
        "x-rapidapi-key": "",
        "x-rapidapi-host": "exchange-rate-api1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    # print(response.json())
    rate = response.json()["rates"][to_currency.upper()]
    print(f"{from_currency} is equal to {rate} {to_currency}")

    converted_amount = amount * rate
    print(f"{amount} {from_currency} is equal to {converted_amount} {to_currency}") 
    return converted_amount
    
#pep8    

class BankAccount:
    def __init__(self, holder_first_name, holder_last_name, holder_address, initial_balance, currency="USD"):
        self.balance = initial_balance
        self.holder_first_name = holder_first_name
        self.holder_last_name = holder_last_name
        self.holder_address = holder_address
        self.currency = currency
        # print(self.__dict__)

    def converted_amount(self, amount, currency):
        return get_conversion_rate(self.currency, currency, amount)
    
    def deposit(self, amount, currency="USD"):
        if currency != self.currency:
            amount = self.converted_amount(amount, currency)
        if amount > 0:
            self.balance += amount
            print(f"Deposited ${amount}. Current balance: ${self.balance}")
            return True
        else:
            print("Invalid deposit amount. Please deposit a positive value.")
            return False

    def withdraw(self, amount, currency="USD"):
        if currency != self.currency:
            amount = self.converted_amount(amount, currency)
        if 0 < amount <= self.balance:
            self.balance -= amount
            print(f"Withdrew ${amount}. Current balance: ${self.balance}")
            return True
        else:
            print("Insufficient funds or invalid withdrawal amount.")
            return False

    def get_balance(self):
        return self.balance


# Create a bank account with an initial balance of $100
account = BankAccount("John", "Doe", "123 Main St", 100)


# Perform transactions
account.deposit(50)     # Deposit $50
account.deposit(100, "EUR")     # Deposit €100
account.withdraw(30)    # Withdraw $30
print("Current balance:", account.get_balance())  # Print current balance
