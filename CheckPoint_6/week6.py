import CheckPoint_7.function as f 

# Missing function.py

# Data
total_amount = int(input('How much money do you have? '))
DB = {}

# Main Loop
while True:

    cmd = input("What do you want to do (add / view / delete / exit)? ")

    if cmd == 'add': # add record
        L = input("Add some expense or income records with description and amount:\ndesc1 amt1, desc2 amt2, desc3 amt3, ...\n").split(', ')
        total_amount = f.add(total_amount,DB,L)
        # print(DB)
        continue

    elif cmd == 'view': # show history
        f.show(DB,total_amount)
        continue

    elif cmd == 'delete': # delete record
        f.show(DB,total_amount)
        num = int(input('Which record do you want to delete? (Enter the line number) '))
        total_amount = f.delete(DB,num,total_amount)
        continue

    elif cmd == 'exit': # exit 
        break

    else: # error handling
        print('Unknown Command. Please try again')