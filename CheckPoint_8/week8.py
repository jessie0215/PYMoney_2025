# Version5: Wrap in functions
import sys

# Global Variable for Formatting
NUMLEN = 3
SPACELEN = 8
DESLEN = 11
AMOLEN = 6
TOTALLEN = NUMLEN + SPACELEN + DESLEN + SPACELEN + AMOLEN

# load records already if it already exists, else prompt the user to  input inital money
def initialize():
    initial_money = 0
    records = []
    try:
        with open('records.txt', 'r') as fh:
            firstline = fh.readline()
            if not firstline:
                raise FileNotFoundError

            L = firstline.split()
            try:
                initial_money = int(L[1])
            except (IndexError, ValueError):
                sys.stderr.write('[ERR]: Cannot Read Initial Money.\n')
                sys.stderr.write('[ERR]: Deleting Content....\n')
                open('records.txt', 'w').close()   # clear the file
                raise FileNotFoundError

            for line in fh.readlines():
                try:
                    des, amt = line.split()
                    records.append((des, int(amt)))
                except ValueError:
                    sys.stderr.write('[ERR]: Cannot Read Records Properly. Your File May Be Corrupted\n')
                    sys.stderr.write('[ERR]: Deleting Content....\n')
                    open('records.txt', 'w').close()   # clear the file
                    raise FileNotFoundError
        print("Welcome Back!")
        return initial_money, records

    except FileNotFoundError:

        try:
            initial_money = int(input("How much money do you have? "))
        except ValueError:
            sys.stderr.write("[ERR]: Input Should Be A Number. Initial Money Is Set To $0\n")
            initial_money = 0
        return initial_money, records

    except Exception:
        sys.stderr.write('[ERR]: Cannot Read Records Properly\n')
        return initial_money, records


# add record(s)
def add(records):
    try: 
        user_in = input(
            "Add some expense or income records with description and amount:\n"
            "Example: Fruit -50, Drink -70, Salary 10000\n"
        )
        
        L = [entry.strip() for entry in user_in.split(',')]

        for entry in L: 
            try:
                des,amount = entry.split()
            except ValueError:
                sys.stderr.write('[ERR]: Add Fail! Invalid Record Format. Input Should Be Like This: Fruit -50, Jackpot 1000 ...\n')
            else:
                try:
                    records.append((des,int(amount)))
                except ValueError:
                    sys.stderr.write(f'[ERR]: Add Fail! Invalid Value For Money.\n') 
        return records
    
    except Exception as err:
        sys.stderr.write(f'[ERR]: {err}. Add Fail!\n')
        print(f'Recent Records: {records}')
        return records

# show the record(s)    
def view(initial_money, records):
    total = initial_money
    print("Here's your expense and income records:")
    print(f"No.{' ' * SPACELEN}Description{' ' * SPACELEN}Amount")
    print('-' * TOTALLEN)
    if not records:
        print('Empty....')
        print('-' * TOTALLEN)
        print(f'Now you have {total} dollars.')
        return
    
    count = 1
    for entry in records:
        des = entry[0]
        amt = entry[1]
        des_alignment = NUMLEN + SPACELEN + DESLEN - (len(str(count)) + 1 + len(des))
        amt_alignment = SPACELEN + AMOLEN - len(str(amt))
        print(f"{count}.{' '*des_alignment}{des}{' ' * amt_alignment}{str(amt)}")
        count += 1
        total += amt

    print('-' * TOTALLEN)
    print(f'Now you have {total} dollars.')
    if total <= 0:
        print("Go Work for your bread!!!!!")
    
    return

# delete a specific record
def delete(initial_money, records):
    view(initial_money,records)

    if not records:
        print(f'Empty List ! Cannot Perform Deletion')
        return records
    num = input('Which record do you want to delete? (Enter the line number) ')
    
    try:
        linenum = int(num)
        if linenum <= 0 or linenum > len(records):
            raise ValueError
        del records[linenum-1]
        view(initial_money,records)
        return records
    except ValueError:
        sys.stderr.write(f"[ERR]: Delete Fail! Invalid Line Number.\n")
        return records

# save user records to 'records.txt'          
def save(initial_money, records):
    try:
        with open('records.txt','w') as fh:
            fh.write(f"initial_money: {initial_money}\n")
            lines = []
            for entry in records:
                lines.append( f"{entry[0]} {str(entry[1])}\n")
            
            fh.writelines(lines)
    except OSError as err:
        sys.stderr.write(f"[ERR]: Save Fail! {err}")
    
    return




# Main Function
initial_money, records = initialize() 
# print (f'initial money = {initial_money}')
# print(f'records = {records}')
while True: 
    command = input('\nWhat do you want to do (add / view / delete / exit)? ') 
    if command == 'add': 
        records = add(records) 
        # print(f'records = {records}')
        continue
    elif command == 'view': 
        view(initial_money, records) 
        continue
    elif command == 'delete': 
        records = delete(initial_money,records) 
        continue
    elif command == 'exit': 
        save(initial_money, records) 
        break 
    else:
        sys.stderr.write('[ERR]: Unknown Command. Please Try Again\n')