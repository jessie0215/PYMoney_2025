# Version2: using date structure to store records
money = int(input('How much money do you have? '))

print('Add some expense or income record with description and amount:')
Collection = input().split(',')

DB = {}
for records in Collection:
    L = records.split()
    DB[L[0]] = int(L[1])

print("Here's your expense and income records: ")
for key in DB.keys():
    print(f"{key} {DB[key]}")
    money += DB[key]

print(f"Now you have {money} dollars.")