
import os

# Get the main project folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Create the data folder path
DATA_DIR = os.path.join(BASE_DIR, "data")


def ensure_data_files():

    # Create data folder if it does not exist
    os.makedirs(DATA_DIR, exist_ok=True)

    # Create required text files
    files = ["books.txt", "members.txt", "transactions.txt"]

    for filename in files:

        file_path = os.path.join(DATA_DIR, filename)

        if not os.path.exists(file_path):

            with open(file_path, "w") as file:
                pass


def append_record(filename, record):

    file_path = os.path.join(DATA_DIR, filename)

    with open(file_path, "a") as file:
        file.write(record + "\n")


def read_records(filename):

    file_path = os.path.join(DATA_DIR, filename)

    with open(file_path, "r") as file:
        return file.readlines()


def write_records(filename, records):

    file_path = os.path.join(DATA_DIR, filename)

    with open(file_path, "w") as file:

        for record in records:
            file.write(record + "\n")


def save_book(book):

    if hasattr(book, "author"):
        record = f"{book.item_id}|Book|{book.title}|{book.author}|{book.available}"

    elif hasattr(book, "issue_number"):
        record = f"{book.item_id}|Magazine|{book.title}|{book.issue_number}|{book.available}"
    else:
        raise TypeError("Unsupported book type")

    append_record("books.txt", record)


def save_member(member):

    record = f"{member.member_id}|{member.name}|{member.get_borrowing_limit()}"

    append_record("members.txt", record)



def search_book(book_id):

    books = read_records("books.txt")

    for record in books:

        details = record.strip().split("|")

        if details[0] == str(book_id):
            return details

    return None


def search_member(member_id):

    members = read_records("members.txt")

    for record in members:

        details = record.strip().split("|")

        if details[0] == str(member_id):
            return details

    return None


def migrate_book_records():

    books = read_records("books.txt")

    updated_books = []

    for record in books:

        details = record.strip().split("|")

        # Convert old book records into the new format
        if len(details) == 3:
            details.append("True")

        if len(details) == 4:
            details.insert(1, "Book")

        updated_books.append("|".join(details))

    write_records("books.txt", updated_books)


def update_book_record(book):

    records = read_records("books.txt")

    updated_records = []
    found = False

    for record in records:

        details = record.strip().split("|")

        if details[0] == str(book.item_id):

            if hasattr(book, "author"):
                new_record = (
                    f"{book.item_id}|Book|{book.title}|"
                    f"{book.author}|{book.available}"
                )

            elif hasattr(book, "issue_number"):
                new_record = (
                    f"{book.item_id}|Magazine|{book.title}|"
                    f"{book.issue_number}|{book.available}"
                )
            else:
                raise TypeError("Unsupported library item type")

            updated_records.append(new_record)
            found = True

        else:
            updated_records.append(record.strip())

    if found:
        write_records("books.txt", updated_records)
        return True

    return False