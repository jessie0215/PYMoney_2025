# Version 4: exception handling
import sys
import CheckPoint_7.function_1 as f

def load_or_init():
    """
    Spec (2): At the beginning, try opening 'records.txt' in a try-except.
      (a) If exists: use readline() for initial amount, readlines() for records,
          then build the in-memory structure.
      (b) If not exists: prompt for initial amount and init variables.
    """
    try:
        with open('records.txt') as fh:
            # Read first line as initial amount
            first_line = fh.readline().strip()
            try:
                # Expect format: 'Initial Amount: <int>'
                initial_amount = int(first_line.split(':', 1)[1])
            except Exception:
                sys.stderr.write("[WARN]: Corrupted first line. Set initial amount to 0.\n")
                initial_amount = 0

            # Read the remaining lines as records
            record_lines = fh.readlines()
            records = f.load_records_from_lines(record_lines)

        print("Existing records loaded.")
        return initial_amount, records

    except FileNotFoundError:
        # File doesn't exist: prompt user
        try:
            initial_amount = int(input("How much money do you have? "))
        except ValueError:
            sys.stderr.write("[ERR]: Input should be a number. Initial money is set to $0\n")
            initial_amount = 0
        records = []
        return initial_amount, records


def persist_and_exit(initial_amount, records):
    """
    Spec (1): Before program terminates, write initial amount and records using:
      a) write() for initial line
      b) writelines() for records serialized list
      c) newlines placed properly
    """
    try:
        with open('records.txt', 'w') as fh:
            fh.write(f"Initial Amount: {initial_amount}\n")
            fh.writelines(f.serialize_records(records))
        print("All records saved. Goodbye!")
    except OSError as e:
        sys.stderr.write(f"[ERR]: Failed to save records: {e}\n")


def main():
    initial_amount, records = load_or_init()

    while True:
        cmd = input("What do you want to do (add / view / delete / exit)? ").strip().lower()

        if cmd == "add":
            # Expect input like: desc1 amt1, desc2 amt2, ...
            entries = input(
                "Add records with 'description amount' pairs, separated by comma and space.\n"
                "Example: Fruit -50, Salary 1000, Coffee -60\n"
            ).split(", ")
            records = f.add(records, entries)

        elif cmd == "view":
            f.show(initial_amount, records)

        elif cmd == "delete":
            f.show(initial_amount, records)
            try:
                num = int(input("Which record do you want to delete? (Enter the line number) "))
                if num <= 0:
                    sys.stderr.write("[ERR]: Line number should be a positive integer\n")
                    continue
                ok = f.delete(records, num)
                if ok:
                    print(f"Record {num} deleted successfully.")
                else:
                    sys.stderr.write(f"[ERR]: Cannot find record {num}.\n")
            except ValueError:
                sys.stderr.write("[ERR]: Line number should be an integer\n")

        elif cmd == "exit":
            persist_and_exit(initial_amount, records)
            break

        else:
            sys.stderr.write("[ERR]: Unknown Command. Please try again\n")


if __name__ == "__main__":
    main()
