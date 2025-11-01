#原本的作法:存在DB然後program結束後writelines() >> 下次進入檢查file在不在，在則直接問operation 不在則問initial
#現在則變成了另外一個方式....

import CheckPoint_7.function as f
import sys 

# Prompt the user to input intial money
used = input('Have you ever saved some record in this system? [Y/N] ')
if used != 'Y' and used != 'N':
    sys.stderr.write('[ERR]: Invalid Input! Syetem Terminated.\n')
    exit(1)
elif used == 'Y':
    # print('Here are your history records:')
    f.show() # should be modified according to the method
else:
    try:    
        total_amount = int(input('How much money do you have? '))
    except ValueError:
        sys.stderr.write(f'[ERR]: Input should be a number. Initial money is set to $0\n')
        total_amount = 0
    try:
        with open('records.txt','w') as fh:
            fh.write(f'Initial Amount: {total_amount}\n')
    except:
        sys.stderr.write(f'[ERR]: Cannot Open files.\n')
        exit(1)

# Main Loop
while True:

    cmd = input("What do you want to do (add / view / delete / exit)? ")

    if cmd == 'add': # add record
        L = input("Add some expense or income records with description and amount:\ndesc1 amt1, desc2 amt2, desc3 amt3, ...\n").split(', ')
        total_amount = f.add(L)
        # print(DB)
        continue

    elif cmd == 'view': # show history
        f.show()
        continue

    elif cmd == 'delete': # delete record
        f.show()
        try:
            num = int(input('Which record do you want to delete? (Enter the line number) '))
            if num <= 0:
                print(f"[ERR]: Line number should be a integer")
                continue
            total_amount = f.delete(num)
            continue
        except:
            sys.stderr.write(f"[ERR]: Line number should be a integer\n")
            continue

    elif cmd == 'exit': # exit 
        break

    else: # error handling
        sys.stderr.write('[ERR]: Unknown Command. Please try again\n')