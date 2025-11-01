import sys

# Global Variable
NUMLEN = 3
SPACELEN = 8
DESLEN = 11
AMOLEN = 6
TOTALLEN = NUMLEN + SPACELEN + DESLEN + SPACELEN + AMOLEN


# get initial amount
def get_initial_amount():
    try:
        with open('records.txt') as fh: 
            firstline = fh.readline()
            L = firstline.split()
            return int(L[2])
        
    except:
        sys.stderr.write('[ERR]: Get Initial(total) Amount Failed\n')
        exit(1)
# add
def add(L):
    try: 
        with open('records.txt', 'a') as fh:
            for entry in L: 
                try:
                    description,amount = entry.split()
                    fh.write(f'{description} {int(amount)}\n')
                except ValueError:
                    sys.stderr.write('[ERR] ADD FAIL! Invalid Record Format. Input should be like this: Fruit -50, Drink, -70 ...\n')
                    return
    except:
        sys.stderr.write(f'[ERR]: Cannot Open files.\n')
        exit(1)
        
# view
def show():
    total = get_initial_amount()
    print("Here's your expense and income records:")
    print(f"No.{' ' * SPACELEN}Description{' ' * SPACELEN}Amount")
    print('-' * TOTALLEN)
    try:
        with open('records.txt') as fh:
            firstline = fh.readline() # firstline is not used
            secondline = fh.readline() 

            if not secondline.strip():          # no records
                print('Empty....')
                print('-' * TOTALLEN)
                print(f'Now you have {total} dollars.')
                return
            
            # handle second line
            count = 1 # for line numbers
            des,amt = secondline.split()
            des_alignment = NUMLEN + SPACELEN + DESLEN - (len(str(count)) + 1 + len(des))
            amt_alignment = SPACELEN + AMOLEN - len(str(amt))
            print(f"{count}.{' '*des_alignment}{des}{' ' * amt_alignment}{str(amt)}")
            count += 1
            total += int(amt)
            
            for line in fh.readlines():
                if not line.strip():
                    sys.stderr.write(f'[ERR]: Line {count} Is Corrupted.\n')
                    return
                des,amt = line.split()
                des_alignment = NUMLEN + SPACELEN + DESLEN - (len(str(count)) + 1 + len(des))
                amt_alignment = SPACELEN + AMOLEN - len(str(amt))
                print(f"{count}.{' '*des_alignment}{des}{' ' * amt_alignment}{str(amt)}")
                count += 1
                total += int(amt)
        
        print('-' * TOTALLEN)
        print(f'Now you have {total} dollars.')
        if total <= 0:
            print("Go Working for your bread!!!!!")

    except (OSError,ValueError) as err:
        sys.stderr.write(f'[ERR]: {err}\n')
        sys.stderr.write(f'Failed to print normally, please check the staus of your file\n')
        return 
    
# delete
def delete(num):
    lines= ''
    try:
        with open('records.txt') as fh1:
            lines = fh1.readlines()
        try:
            del lines[num]
            with open('records.txt','w') as fh2:
                fh2.writelines(lines)
            print('Delete Successfully.')
            return
        except:
            sys.stderr.write(f'[ERR]: Cannot Delete Record {num}\n')
            return
        
    except:
        sys.stderr.write(f'[ERR]: Cannot Open files.\n')
        exit(1)
        
    sys.stderr.write('[ERR]: Cannot find such record!\n')
    return
