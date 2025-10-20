age = int(input())

if age >= 18:
    print("You can vote")

elif 0 <= age < 18:
    print("Too young to vote")

else:
    print("You are a time traveller")
