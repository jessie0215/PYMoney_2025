
import sys

# Global formatting constants
NUMLEN = 3
SPACELEN = 8
DESLEN = 11
AMOLEN = 6
TOTALLEN = NUMLEN + SPACELEN + DESLEN + SPACELEN + AMOLEN


# ---------- Parsing & Serialization Utilities ----------

def _parse_record_line(line: str):
    """Parse a single 'desc amt' line into (desc, int_amt). Raises ValueError on bad format."""
    parts = line.strip().split()
    if len(parts) != 2:
        raise ValueError("Invalid record format")
    desc, amt = parts
    return (desc, int(amt))


def load_records_from_lines(lines):
    """Build the in-memory data structure (list of tuples) from readlines()."""
    records = []
    for i, line in enumerate(lines, start=1):
        if not line.strip():
            # skip blank/whitespace-only lines
            continue
        try:
            records.append(_parse_record_line(line))
        except ValueError:
            sys.stderr.write(f"[WARN]: Skipped malformed record on line {i+1}.\n")
            continue
    return records


def serialize_records(records):
    """Convert the in-memory records into a list of 'desc amt\n' strings for writelines()."""
    return [f"{desc} {amt}\n" for (desc, amt) in records]


# ---------- Operations on the in-memory structure ----------

def add(records, entries):
    """
    Add records given a list like ['Food -50', 'Salary 1000'].
    Returns the updated list.
    """
    for raw in entries:
        if not raw.strip():
            continue
        try:
            desc, amt = raw.split()
            records.append((desc, int(amt)))
        except ValueError:
            sys.stderr.write("[ERR] ADD FAIL! Use format like: Fruit -50, Drink -70, ...\n")
            # continue adding others; do not abort entirely
            continue
    return records


def delete(records, num):
    """
    Delete the record by 1-based index. Returns True if deleted, False if out of range.
    """
    index = num - 1
    if 0 <= index < len(records):
        del records[index]
        return True
    return False


def _line_alignments(count, desc, amt):
    des_alignment = NUMLEN + SPACELEN + DESLEN - (len(str(count)) + 1 + len(desc))
    amt_alignment = SPACELEN + AMOLEN - len(str(amt))
    if des_alignment < 1:
        des_alignment = 1
    if amt_alignment < 1:
        amt_alignment = 1
    return des_alignment, amt_alignment


def show(initial_amount, records):
    """
    Pretty-print the table of records and the current total.
    No file I/O here; purely uses the provided data.
    """
    print("Here's your expense and income records:")
    print(f"No.{ ' ' * SPACELEN }Description{ ' ' * SPACELEN }Amount")
    print("-" * TOTALLEN)

    if not records:
        print("Empty....")
        print("-" * TOTALLEN)
        print(f"Now you have {initial_amount} dollars.")
        if initial_amount <= 0:
            print("Go Working for your bread!!!!!")
        return

    total = initial_amount
    for i, (desc, amt) in enumerate(records, start=1):
        des_alignment, amt_alignment = _line_alignments(i, desc, amt)
        print(f"{i}.{' ' * des_alignment}{desc}{' ' * amt_alignment}{amt}")
        total += int(amt)

    print("-" * TOTALLEN)
    print(f"Now you have {total} dollars.")
    if total <= 0:
        print("Go Working for your bread!!!!!")
