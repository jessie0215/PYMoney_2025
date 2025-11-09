import sys

# <Optional> make the categories extendable 

# File Path for categories.txt
CATEGORIESPATH = 'categories.txt'
DEFAULTCATEGORIES =  [
    'expense', [
        'food', [
            'meal', [], 'snack', [], 'drink', []
        ],
        'transportation', [
            'bus', [], 'railway', []
        ]
    ],
    'income', [
        'salary', [], 'bonus', []
    ]
]


# Global Variable for Formatting
NUMLEN = 3
SPACELEN = 8
CATLEN = 8
DESLEN = 11
AMOLEN = 6
TOTALLEN = NUMLEN + SPACELEN + CATLEN + SPACELEN + DESLEN + SPACELEN + AMOLEN

# helper function to insert a category into list
def insert_path(categories, parts):
    """
    Insert a path like ['expense','food','meal'] into nested list.
    """
    ptr = categories  # 目前層級指標
    i = 0
    while i < len(parts):
        name = parts[i]
        # 如果這層沒有這個分類，就加上它與空子清單
        if name not in ptr:
            ptr.extend([name, []])
        # 找出這個名稱後面的那個子清單（ptr[j+1]）
        idx = ptr.index(name)
        ptr = ptr[idx + 1]
        i += 1
    
    return categories


# initialize catagories before start
def initialize_categories():
    """
    Read Categories From 'categories.txt' if it exists. Otherwise, Set to Default Categories.

    Returns:
        list: Nested list representing the category tree.
    """
    categories = []
    try:
        with open(CATEGORIESPATH, 'r') as fh:
            lines = fh.readlines()
   
        for line in lines:
            parts = [p.strip().lower() for p in line.split('/') if p.strip()]
            # print('parts=', parts)
            if parts[0] not in ('expense', 'income'):
                raise Exception('Invalid Root')
            
            categories = insert_path(categories, parts)
        
        return categories

    except Exception as err:
        sys.stderr.write('[ERR]: '+ str(err) + '\n')
        sys.stderr.write('[ERR]: Can Not Read Categories Properly, Categories Is Set To Default Categories')
        return DEFAULTCATEGORIES

# check whether a categories is in
def is_catrgory_valid(category, categories):
    """
    Check whether a specific category exists within the category tree.

    Args:
        category (str): The category name to check.
        categories (list): The nested category list.

    Returns:
        bool: True if category exists, False otherwise.
    """
    if type(categories) == list:
        for cat in categories:
            if is_catrgory_valid(category,cat):
                return True
        return False
    return category == categories


# load records already if it already exists, else prompt the user to  input inital money
def initialize():
    """
    Initialize program by loading previous records if available, 
    or prompt user to input initial money if file not found or corrupted.

    Returns:
        tuple: (initial_money (int), records (list of tuples))
    """
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
                    cat, des, amt = line.split()
                    records.append((cat, des, int(amt)))
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
def add(records,categories):
    """
    Add new expense or income records.

    Prompts user to input comma-separated entries in the form:
        category description amount
    Example:
        food Fruit -50, drink Coffee -70, salary Part-Time 10000

    Args:
        records (list): Current list of records.
        categories (list): Category list for validation.

    Returns:
        list: Updated records list.
    """
    try: 
        user_in = input(
            "Add some expense or income records with category, description and amount:\n"
            "Example: food Fruit -50, drink Coffee -70, salary Part-Time 10000\n"
        )
        
        L = [entry.strip() for entry in user_in.split(',')]

        for entry in L: 
            try:
                cat,des,amount = entry.split()
                if not is_catrgory_valid(cat,categories):
                    print('[ERR]: The specified category is not in the category list. ')
                    print('[ERR]: Fail to add a record.')
                    print('You can check the category list by command "view categories"')
                    print('Or add a new categories by command "add categories"')
                    break
            except ValueError:
                sys.stderr.write('[ERR]: Add Fail! Invalid Record Format. Input Should Be Like This: food Fruit -50, drink Coffee -70 ...\n')
            else:
                try:
                    records.append((cat,des,int(amount)))
                except ValueError:
                    sys.stderr.write(f'[ERR]: Add Fail! Invalid Value For Money.\n') 
        return records
    
    except Exception as err:
        sys.stderr.write(f'[ERR]: {err}. Add Fail!\n')
        print(f'Recent Records: {records}')
        return records

# show the record(s)    
def view(initial_money, records, mode = 0):
    """
    Display expense and income records in a formatted table.

    Depending on the display mode, this function either:
        - mode = 0: shows all records and computes the current total balance.
        - mode != 0: shows only the specified subset (e.g., filtered records)
                     and displays the subtotal of the listed items.

    Args:
        initial_money (int): The starting balance before applying records.
        records (list[tuple]): A list of (category, description, amount) tuples.
        mode (int, optional): 
            Display mode flag.
            0 = full view with current balance and motivational message.
            Non-zero = partial view (e.g., for 'find') with subtotal only.

    Returns:
        None
    """
    total = initial_money
    if mode == 0 : # mode 0 : print all the records
        print("Here's your expense and income records:") 
    print(f"No.{' ' * SPACELEN}Category{' ' * SPACELEN}Description{' ' * SPACELEN}Amount")
    print('-' * TOTALLEN)
    if not records:
        print('Empty....')
        print('-' * TOTALLEN)
        print(f'Now you have {total} dollars.')
        return
    
    count = 1
    for entry in records:
        cat = entry[0]
        des = entry[1]
        amt = entry[2]
        cat_alignment = NUMLEN + SPACELEN + CATLEN - (len(str(count))+ 1 + len(cat))
        des_alignment = SPACELEN + DESLEN - len(des)
        amt_alignment = SPACELEN + AMOLEN - len(str(amt))
        print(f"{count}.{' '*cat_alignment}{cat}{' '*des_alignment}{des}{' ' * amt_alignment}{str(amt)}")
        count += 1
        total += amt

    print('-' * TOTALLEN)
    if mode == 0:
        print(f'Now you have {total} dollars.')
        if total <= 0:
            print("Go Work for your bread!!!!!")
    else :
        print(f'The total amount above is {total}.')
    return

# delete a specific record
def delete(initial_money, records):
    """
    Delete a specific record by its line number.

    Args:
        initial_money (int): Starting balance.
        records (list): List of current records.

    Returns:
        list: Updated records list.
    """
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
    """
    Save all user data to 'records.txt'.

    Args:
        initial_money (int): Starting balance.
        records (list): List of records to be saved.

    Returns:
        None
    """
    try:
        with open('records.txt','w') as fh:
            fh.write(f"initial_money: {initial_money}\n")
            lines = []
            for entry in records:
                lines.append( f"{entry[0]} {entry[1]} {str(entry[2])}\n")
            
            fh.writelines(lines)
    except OSError as err:
        sys.stderr.write(f"[ERR]: Save Fail! {err}")
    
    return

# print all the existing categories
def view_categories(categories, level = 0):
    """
    Print the nested category tree in an indented structure.

    Args:
        categories (list): Nested category list.
        level (int): Current recursion depth (used for indentation).

    Returns:
        None
    """
    if categories == None:
           return
    if type(categories) == list:
           for child in categories:
                  view_categories(child, level+1)
    else:
        print(f'{" "*4*(level-1)}- {categories}')

def flatten(L): 
    """
    Recursively flatten a nested list into a one-dimensional list.

    Args:
        L (list or str): A possibly nested list of strings representing categories,
                         or a single string leaf node.

    Returns:
        list: A flat list containing all string elements from the nested structure.
    """
    if type(L) == list: 
        result = [] 
        for child in L: 
            result.extend(flatten(child)) 
        return result 
    else: 
        return [L] 

def find_subcategories(category, categories):
    """
    Find a category and all of its subcategories from a nested category tree.

    This function searches recursively for the given category name.
    If found, it returns a flat list containing the category itself
    and all its subcategories (if any).
    If the category has no subcategories, only itself is returned.
    If not found, an empty list is returned.

    Args:
        category (str): The name of the category to search for.
        categories (list): The nested category list.

    Returns:
        list: A flat list of the category and its subcategories, or [] if not found.
    """
    if type(categories) == list: 
        for v in categories: 
            p = find_subcategories(category, v) 
            if p == True: 
                index = categories.index(v) 
                if index + 1 < len(categories) and \
                        type(categories[index + 1]) == list:  # this category has subcategories
                    return flatten(categories[index:index + 2]) 
                else: 
                    # return only itself if no subcategories 
                    return [v] 
            if p != []: 
                return p 
    return True if categories == category else [] 
                               # return [] instead 

# Find records that belongs to specified category
def find(records, categories):
    """
    Find and display all records belonging to a specific category.

    Hint:
        Utilize the <view> function to display matched results.

    Args:
        initial_money (int): Starting balance.
        records (list): List of current records.
        categories (list): Nested category structure.

    Returns:
        None
    """
    print('Here are categories we have in the system:')
    view_categories(categories)
    candidate = input('Which category do you want to find? ')
    result = find_subcategories(candidate, categories)
    found_records = list(filter(lambda r:r[0] in result, records))
    if not found_records:
        print('No Record Found.')
        return
    print(f"Here's your expense and income records under category \"{candidate}\":")
    view(0, found_records, 1)
    
    return 

def add_categories(categories):
    print('Existing Categories: ')
    view_categories(categories)
    path = input( 'Please give the path for your categories\n'
                  'Example: expense/entertainment/ticket\n'
                ) 
    if not path:
        print('[ERR]: Empty path. Cancelled.')
        return categories

    parts = [p.strip().lower() for p in path.split('/') if p.strip()]
    if not parts:
        print('[ERR]: Invalid input.')
        return categories

    if parts[0] not in ('expense', 'income'):
        print('[ERR]: Root must be "expense" or "income".')
        return categories

    insert_path(categories, parts)
    print(f'Add Sucessfully ! Here\'s your new categories list:')
    view_categories(categories)
    return categories

def save_categories(categories):
    """
    把巢狀 categories 存成 categories.txt（每行一條路徑）。
    會儲存「所有節點」：含中間節點與葉節點。
    """
    def dfs(node, prefix, lines):
        if not isinstance(node, list):
            raise TypeError("root 應該是 list")

        if len(node) % 2 != 0:
            raise ValueError("Invalid category tree: list 長度必須是偶數 (name, children 成對)。")

        for i in range(0, len(node), 2):
            name = node[i]
            sub  = node[i + 1]
            if not isinstance(name, str):
                raise TypeError(f"Invalid node name: {name!r}")
            if not isinstance(sub, list):
                raise TypeError(f"Invalid children for {name!r}: {sub!r}")

            # 1) 先記錄這個節點本身的路徑
            path = '/'.join(prefix + [name])
            lines.append(path)

            # 2) 再往下走子清單
            if sub:
                dfs(sub, prefix + [name], lines)

    lines = []
    dfs(categories, [], lines)

    # 可選：去重 & 排序，讓檔案穩定
    lines = sorted(set(lines))

    with open(CATEGORIESPATH, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(lines))
    print('Categories saved successfully.')





# Main Function
initial_money, records = initialize() 
categories = initialize_categories()

while True: 
    command = input('\nWhat do you want to do (add / view / delete / exit / find / view categories(vc) / add categories(ac) )? ') 
    if command == 'add': 
        records = add(records,categories) 
        continue
    elif command == 'view': 
        view(initial_money, records) 
        continue
    elif command == 'delete': 
        records = delete(initial_money,records) 
        continue
    elif command == 'view categories' or command == "vc":
        view_categories(categories)
    elif command == 'find':
        find(records,categories)
    elif command == 'add categories' or command == 'ac':
        categories = add_categories(categories)
    elif command == 'exit': 
        save(initial_money, records)
        save_categories(categories)
        break 
    else:
        sys.stderr.write('[ERR]: Unknown Command. Please Try Again\n')