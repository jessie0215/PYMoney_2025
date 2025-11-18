# fist homework
initial_money = int(input('How much money do you have? '))
print('Add an expense or income record with description and amount:')
description, amount = input().split()
print(f"Now you have {initial_money + int(amount)} dollars.")