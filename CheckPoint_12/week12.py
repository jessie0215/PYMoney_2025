# Version9: Generator
import sys

# File Paths
CATEGORIESFILE = 'categories.txt'
RECORDSFILE = 'records.txt'

# Default Categories List
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

class Record: 
    """Represent a record.""" 
    # constructor
    def __init__  (self , category, description, amount):
        self._category = category
        self._description = description
        self._amount = amount

    @property
    def category(self):
        return self._category
    
    @property
    def description(self):
        return self._description
    
    @property
    def amount(self):
        return self._amount
 
class Records:
    """Maintain a list of all the 'Record's and the initial amount of money.""" 
    # constructor
    def __init__(self):
        """
        This constructor calls initialize()
        The initialize() method is expected to return a tuple 
        containing the initial amount of money and a list of existing records,
        which are then stored in the instance attributes _initial_money 
        and _records.
        """
        self._initial_money,self._records = self.initialize()
        # records is a list of Record()

    # load records if it already exists, else prompt the user to input inital money
    @staticmethod
    def initialize():
        """
        Initialize program by loading previous records if available, 
        or prompt user to input initial money if file not found or corrupted.

        Returns:
            tuple: (initial_money (int), records (list of Record))
        """
        initial_money = 0
        records = []
        try:
            with open(RECORDSFILE, 'r') as fh:
                firstline = fh.readline()
                if not firstline:
                    raise FileNotFoundError # empty file is treated as file not found

                L = firstline.split()

                try:
                    initial_money = int(L[1])
                except (IndexError, ValueError):
                    sys.stderr.write('[ERR]: Cannot Read Initial Money.\n')
                    sys.stderr.write('[ERR]: Deleting Content....\n')
                    open(RECORDSFILE, 'w').close()   # clear the file
                    raise FileNotFoundError

                for line in fh.readlines():
                    try:
                        cat, des, amt = line.split()
                        records.append(Record(cat, des, int(amt)))
                    except ValueError:
                        sys.stderr.write('[ERR]: Cannot Read Records Properly. Your File May Be Corrupted\n')
                        sys.stderr.write('[ERR]: Deleting Content....\n')
                        open(RECORDSFILE, 'w').close()   # clear the file
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
    def add(self,categories):
        """
        Add new expense or income records.

        Prompts user to input comma-separated entries in the form:
            category description amount
        Example:
            food Fruit -50, drink Coffee -70, salary Part-Time 10000

        Args:
            categories (object): Category for validation.

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

                    if not categories.is_category_valid(cat):
                        print('[ERR]: The specified category is not in the category list. ')
                        print('[ERR]: Fail to add a record.')
                        print('You can check the category list by command "view categories"')
                        print('Or add a new category by command "add categories"')
                        break

                except ValueError:
                    sys.stderr.write('[ERR]: Add Fail! Invalid Record Format. Input Should Be Like This: food Fruit -50, drink Coffee -70 ...\n')
                
                else:
                    try:
                        self._records.append(Record(cat,des,int(amount)))
                    except ValueError:
                        sys.stderr.write(f'[ERR]: Add Fail! Invalid Value For Money.\n') 
        
        except Exception as err:
            sys.stderr.write(f'[ERR]: {err}. Add Fail!\n')
            print(f'Recent Records: {self._records}')

    # show the record(s)    
    def view(self, mode = 0, found = []):
        """
        Display expense and income records in a formatted table.

        Depending on the display mode, this method prints either all records or 
        a filtered subset to the console, along with their total or subtotal amounts.

        Behavior:
            - mode = 0: Displays all existing records, computes and shows the 
            current total balance based on the initial amount.
            - mode != 0: Displays only the given subset of records (e.g., search results) 
            and shows the subtotal of those records.

        Args:
            mode (int, optional): 
                Display mode selector. Defaults to 0.
                0 → Show all records and current balance.
                Non-zero → Show only filtered results with subtotal.
            found (list, optional): 
                A list of filtered records to display when mode != 0.
                Each record should be a Record object (contains category, description, amount).
                Defaults to an empty list.

        Returns:
            None
                Prints formatted records directly to the console.
        """
        total = self._initial_money if mode == 0 else 0 # print matched records with initial amount = 0

        if mode == 0 : # mode 0 : print all the records
            print("Here's your expense and income records:") 

        print(f"No.{' ' * SPACELEN}Category{' ' * SPACELEN}Description{' ' * SPACELEN}Amount")
        print('-' * TOTALLEN)
        
        if mode == 0 and not self._records:
            print('Empty....')
            print('-' * TOTALLEN)
            print(f'Now you have {total} dollars.')
            return

        targetlist = self._records if mode == 0 else found # print the targetlist we want
        
        count = 1 # for line number

        for entry in targetlist:
            cat = entry.category
            des = entry.description
            amt = entry.amount
            cat_alignment = NUMLEN + SPACELEN + CATLEN - (len(str(count))+ 1 + len(cat)) # number of space before 'categories'
            des_alignment = SPACELEN + DESLEN - len(des) # number of space before 'description'
            amt_alignment = SPACELEN + AMOLEN - len(str(amt)) # number of space before 'amount'
            print(f"{count}.{' '*cat_alignment}{cat}{' '*des_alignment}{des}{' ' * amt_alignment}{str(amt)}")
            count += 1
            total += amt # accumulate total amount

        print('-' * TOTALLEN)

        if mode == 0:
            print(f'Now you have {total} dollars.')
            if total <= 0:
                print("Go Work for your bread!!!!!")
        else :
            print(f'The total amount above is {total}.')
        return
    
    # delete a specific record
    def delete(self):
        """Delete a specific record by its line number."""

        self.view() # print all the existing records for the user's reference

        if not self._records:
            print(f'Empty List ! Cannot Perform Deletion')
            return
        
        # prompt the user to input a line number for deletion
        num = input('Which record do you want to delete? (Enter the line number) ')
        
        try:
            linenum = int(num)
            if linenum <= 0 or linenum > len(self._records):
                raise ValueError
            del self._records[linenum-1]
            self.view()
            return
        
        except ValueError:
            sys.stderr.write(f"[ERR]: Delete Fail! Invalid Line Number.\n")
            return

    # Find records that belongs to specified category
    def find(self, candidate, target_categories):
        """
        Find and display all records belonging to a specific category.

        Utilize the <view> function to display matched results.

        Args:
            candidate(str): category the user wishes to find 
            target_categories (list): flatten list containing targetting categoriy and its subcategories

        Returns:
            None
        """
        
        found_records = list(filter(lambda r:r.category in target_categories, self._records)) # filter out the records not belonging to any of the categories in result
        
        if not found_records:
            print('No Record Found.')
            return
        
        print(f"Here's your expense and income records under category \"{candidate}\":")
        self.view(mode=1,found=found_records) # set view mode to 1 to print different messages

        return 
    
    # save user records to 'records.txt'          
    def save(self):
        """Save all user data to 'records.txt'."""

        try:
            with open(RECORDSFILE,'w') as fh:
                fh.write(f"initial_money: {self._initial_money}\n")
                lines = []
                for entry in self._records:
                    lines.append( f"{entry.category} {entry.description} {str(entry.amount)}\n")
                
                fh.writelines(lines)

            print('Records saved successfully')
            
        except OSError as err:
            sys.stderr.write(f"[ERR]: Save Fail! {err}")
        
        return

class Categories: 
    """Maintain the category list and provide some methods."""

    def __init__(self):
        """This constructor calls initialize_categories() to get the correct content for self._categories"""

        self._categories = []
        self.initialize_categories()
    
    # initialize catagories before start
    def initialize_categories(self):
        """
        Read Categories From 'categories.txt' if it exists. Otherwise, Set to Default Categories.

        Returns:
            list: Nested list representing the category tree.
        """
        try:
            with open(CATEGORIESFILE, 'r') as fh:
                lines = fh.readlines() # read all the lines in file

            self._categories = []
            for line in lines:
                parts = [p.strip().lower() for p in line.split('/') if p.strip()] # split the line and remove redundant space 
                if parts[0] not in ('expense', 'income'): # root must be 'expense' or 'income'
                    raise Exception('Invalid Root')
                
                self.insert_path(parts) # insert the categories into the nested list 

        except Exception as err:
            sys.stderr.write('[ERR]: '+ str(err) + '\n')
            sys.stderr.write('[ERR]: Can Not Read Categories Properly, Categories Is Set To Default Categories\n')
            self._categories = DEFAULTCATEGORIES # set categories to default
    
    # print all the existing categories
    def view(self,categories = None, level = 0):
        """
        Print the nested category tree in an indented structure.

        Args:
            node (list): Nested category list.
            level (int): Current recursion depth (used for indentation).
        """
        if categories == None:
            categories = self._categories

        if not isinstance(categories, list):
            return
        
        for i in range(0, len(categories), 2):
            name = categories[i]
            sub  = categories[i + 1]
            print(' ' * 4 * level + '- ' + name)
            self.view(sub, level + 1)
    
    # Find a category and all of its subcategories from a nested category tree 
    def find_subcategories(self, category):
        """
        Use a recursive generator to find the target category and
        yield it and all its subcategories in a flat sequence.

        Args:
            category (str): The name of the category to search for.

        Returns:
            list: A flat list of the category and its subcategories, or [] if not found.
        """

        def find_subcategories_gen(category, categories, found=False):
            
            if isinstance(categories, list):

                # walk through the list
                for index, child in enumerate(categories):
                    
                    # try move down with current found
                    yield from find_subcategories_gen(category, child, found)

                    # if we find the target category and it has subtree 
                    if (child == category and index + 1 < len(categories)
                        and isinstance(categories[index + 1], list)):

                        # recursively find in subtree and set found = True
                        yield from find_subcategories_gen(category, categories[index + 1], True)
            else:
                # base case: a single string representing a specific category
                # yield when:
                # (1) it is exactly target category
                # (2) it is in the subtree of the target category（found=True）
                if categories == category or found:
                    yield categories

        # collect the result, convert it into list and return.
        return list(find_subcategories_gen(category, self._categories))

    # check whether a category is in categories 
    def is_category_valid(self,category,node=None):
        """
        Check whether a specific category exists within the category tree.

        Args:
            category (str): The category name to check.

        Returns:
            bool: True if category exists, False otherwise.
        """
        if node is None:
            node = self._categories

        if not isinstance(node, list):
            return False

        for i in range(0, len(node), 2):
            name = node[i]
            sub  = node[i + 1]
            if name == category:
                return True
            if self.is_category_valid(category, sub):
                return True

        return False
        
    # helper function to insert a category into list
    def insert_path(self, parts):
        """
        Insert a path like ['expense','food','meal'] into nested list.
        """
        ptr = self._categories  # point to current level
        i = 0
        while i < len(parts):
            name = parts[i]
            # if there's no category in this level, add it followed by an empty list
            if name not in ptr:
                ptr.extend([name, []])
            # fine the sublist behind 'name'
            idx = ptr.index(name)
            ptr = ptr[idx + 1]
            i += 1

    # add new category to categories list
    def add_categories(self):
        print('Existing Categories: ')
        self.view()
        path = input( 'Please give the path for your categories\n'
                    'Example: expense/entertainment/ticket\n'
                    ) 
        if not path:
            print('[ERR]: Empty path. Cancelled.')
            return

        parts = [p.strip().lower() for p in path.split('/') if p.strip()]

        if not parts:
            print('[ERR]: Invalid input.')
            return

        if parts[0] not in ('expense', 'income'):
            print('[ERR]: Root must be "expense" or "income".')
            return

        self.insert_path(parts)
        print(f'Add Sucessfully ! Here\'s your new categories list:')
        self.view()
        return 

    # save all the categories into 'categories.txt'
    def save_categories(self):
        """
        store a nexted list into 'categrories.txt', each line represents a path.
        """
        def dfs(node, prefix, lines):
            if not isinstance(node, list):
                raise TypeError("root should be list")

            if len(node) % 2 != 0:
                raise ValueError("Invalid category tree: list length must be even ")

            for i in range(0, len(node), 2):
                name = node[i]
                sub  = node[i + 1]
                if not isinstance(name, str):
                    raise TypeError(f"Invalid node name: {name!r}")
                if not isinstance(sub, list):
                    raise TypeError(f"Invalid children for {name!r}: {sub!r}")

                # the node itself is a path
                path = '/'.join(prefix + [name])
                lines.append(path)

                # subcategories
                if sub:
                    dfs(sub, prefix + [name], lines)

        lines = []
        dfs(self._categories, [], lines)

        lines = sorted(set(lines))

        with open(CATEGORIESFILE, 'w', encoding='utf-8') as fh:
            fh.write('\n'.join(lines))
            
        print('Categories saved successfully.')

# Main Function
def main():

    # Intialization
    records =  Records() # instantiate a Records object that maintain initial money and records collection
    categories = Categories() # instantiate a Categories object that maintain categories

    while True: 
        # prompt user to input command
        command = input('\nWhat do you want to do ? \n'
                    'ADD-[A] VIEW-[V] DELETE-[D] '
                    'EXIT-[E] FIND-[F] VIEW CATEGORIES-[VC] ADD CATEGORIES-[AC] \n') 
        
        if command == 'add' or command.lower() == 'a' : 
            records.add(categories) # add a new record
            continue

        elif command == 'view' or command.lower() == 'v': 
            records.view() # print all records
            continue
        
        elif command == 'delete' or command.lower() == 'd': 
            records.delete() # delete specific records
            continue
        
        elif command == 'view categories' or command.lower() == "vc":
            categories.view() # print all the categories 
        
        elif command == 'find' or command.lower() == 'f':
            print('Here are categories we have in the system:')
            categories.view() # let user know the existing categories
            candidate = input('Which category do you want to find? ')
            target = categories.find_subcategories(candidate) # get the subcategories list containing all the category the user want 
            records.find(candidate, target) # find all the records belong to specific category 
            continue
        
        elif command == 'add categories' or command.lower() == 'ac':
            categories.add_categories() # add a user-defined categories
            continue

        elif command == 'exit' or command.lower() == 'e': 
            print('Processing...')
            records.save() # save all the existing records to 'records.txt'
            categories.save_categories() # save all the categories to 'categories.txt' 
            print('\n~~~~ THANKS FOR USING THE PYMONEY SYSTEM ~~~~\n')
            break 
        
        else: # error handling: undefined command
            sys.stderr.write('[ERR]: Unknown Command. Please Try Again\n')


if __name__ == "__main__":
    main()