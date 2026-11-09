from datetime import date
from Library.book import Book, Magazine
from Library.member import StudentMember, StaffMember
from Library.transaction import Transaction

members_in_session = {}

active_transactions = {}

from Library.file_utils import (
    ensure_data_files,
    save_book,
    save_member,
    search_book,
    search_member,
    read_records,
    migrate_book_records
)


def add_book():

    book_id = int(input("Enter Book ID: "))
    title = input("Enter Book Title: ")
    author = input("Enter Author Name: ")

    book = Book(book_id, title, author)

    save_book(book)

    print("Book added successfully!")

def add_magazine():

    magazine_id = int(input("Enter Magazine ID: "))
    title = input("Enter Magazine Title: ")
    issue_number = input("Enter Issue Number: ")

    magazine = Magazine(magazine_id, title, issue_number)

    save_book(magazine)

    print("Magazine added successfully!")

def register_member():

    member_id = int(input("Enter Member ID: "))
    name = input("Enter Member Name: ")

    print("1. Student")
    print("2. Staff")

    choice = input("Select Member Type: ")

    if choice == "1":
        member = StudentMember(member_id, name)

    elif choice == "2":
        member = StaffMember(member_id, name)

    else:
        print("Invalid member type!")
        return

    save_member(member)

    print("Member registered successfully!")


def search_books():

    item_id = input("Enter Book/Magazine ID to search: ")

    item = search_book(item_id)

    if item:

        item_type = item[1]

        print("\nItem Found!")
        print("ID:", item[0])
        print("Type:", item_type)
        print("Title:", item[2])

        if item_type == "Book":
            print("Author:", item[3])

        elif item_type == "Magazine":
            print("Issue Number:", item[3])

        print("Available:", item[4])

    else:
        print("Book or Magazine not found!")


def search_members():

    member_id = input("Enter Member ID to search: ")

    member = search_member(member_id)

    if member:
        print("\nMember Found!")
        print("ID:", member[0])
        print("Name:", member[1])
        print("Borrowing Limit:", member[2])

    else:
        print("Member not found!")

def load_book_object(book_id):

    details = search_book(book_id)

    if details is None:
        return None

    item_type = details[1]

    if item_type == "Book":

        item = Book(
            int(details[0]),
            details[2],
            details[3]
        )

        item.available = details[4].strip().lower() == "true"

    elif item_type == "Magazine":

        item = Magazine(
            int(details[0]),
            details[2],
            details[3]
        )

        item.available = details[4].strip().lower() == "true"

    else:
        return None

    return item

def load_member_object(member_id):

    member_id = str(member_id)

    # Reuse an existing member object
    if member_id in members_in_session:
        return members_in_session[member_id]

    details = search_member(member_id)

    if details is None:
        return None

    borrowing_limit = int(details[2])

    if borrowing_limit == 3:

        member = StudentMember(
            int(details[0]),
            details[1]
        )

    elif borrowing_limit == 5:

        member = StaffMember(
            int(details[0]),
            details[1]
        )

    else:
        print("Unknown member type!")
        return None

    members_in_session[member_id] = member

    return member


def load_active_transactions():

    records = read_records("transactions.txt")

    active_records = {}

    # Find transactions that have not been returned
    for record in records:

        details = record.strip().split("|")

        if len(details) < 2:
            continue

        if details[0] == "ISSUED":
            active_records[details[1]] = details

        elif details[0] == "RETURNED":
            active_records.pop(details[1], None)

    # Recreate active transaction objects
    for transaction_id, details in active_records.items():

        member_id = details[2]
        book_id = details[3]

        book = load_book_object(book_id)
        member = load_member_object(member_id)

        if book is None or member is None:
            continue

        transaction = Transaction(member, book)

        transaction.transaction_id = int(transaction_id)
        transaction.issue_date = date.fromisoformat(details[4])
        transaction.due_date = date.fromisoformat(details[5])
        transaction.status = "Issued"

        member.borrow_item(book)

        active_transactions[transaction_id] = transaction

    print("Active transactions loaded:", len(active_transactions))



def view_member_history():

    member_id = input("Enter Member ID: ")

    records = read_records("transactions.txt")

    history = {}

    for record in records:

        details = record.strip().split("|")

        if details[0] == "ISSUED":

            if details[2] == member_id:

                history[details[1]] = {
                    "book_id": details[3],
                    "issue_date": details[4],
                    "due_date": details[5],
                    "return_date": "Not Returned",
                    "fine": 0,
                    "status": "Issued"
                }

        elif details[0] == "RETURNED":

            transaction_id = details[1]

            if transaction_id in history:

                history[transaction_id]["return_date"] = details[2]
                history[transaction_id]["fine"] = details[3]
                history[transaction_id]["status"] = "Returned"

    if not history:
        print("No borrowing history found!")
        return

    print("\n--- MEMBER BORROWING HISTORY ---")

    for transaction_id, details in history.items():

        print("\nTransaction ID:", transaction_id)
        print("Book ID:", details["book_id"])
        print("Issue Date:", details["issue_date"])
        print("Due Date:", details["due_date"])
        print("Return Date:", details["return_date"])
        print("Fine: ₹", details["fine"])
        print("Status:", details["status"])

def library_summary():

    books = read_records("books.txt")
    members = read_records("members.txt")

    total_books = 0
    total_magazines = 0
    available_items = 0
    issued_items = 0

    for record in books:

        details = record.strip().split("|")

        if len(details) < 5:
            continue

        if details[1] == "Book":
            total_books += 1

        elif details[1] == "Magazine":
            total_magazines += 1

        if details[4].strip().lower() == "true":
            available_items += 1
        else:
            issued_items += 1

    print("\n===== LIBRARY SUMMARY =====")
    print("Total Books:", total_books)
    print("Total Magazines:", total_magazines)
    print("Total Library Items:", total_books + total_magazines)
    print("Available Items:", available_items)
    print("Issued Items:", issued_items)
    print("Registered Members:", len(members))
    print("Active Transactions:", len(active_transactions))


def issue_book():

    book_id = input("Enter Book ID: ")
    member_id = input("Enter Member ID: ")

    book = load_book_object(book_id)
    member = load_member_object(member_id)

    if book is None:
        print("Book not found!")
        return

    if member is None:
        print("Member not found!")
        return

    transaction = Transaction(member, book)

    if transaction.issue_item():

        active_transactions[str(transaction.transaction_id)] = transaction

def return_book():

    transaction_id = input("Enter Transaction ID: ")

    transaction = active_transactions.get(transaction_id)

    if transaction is None:
        print("Active transaction not found in this session!")
        return

    transaction.return_item()

    if transaction.status == "Returned":
        del active_transactions[transaction_id]

def demonstrate_destructor():

    demo_book = Book(9999, "Temporary Demo Book", "Demo Author")

    print("Temporary book object created.")

    del demo_book

    print("Destructor demonstration completed.")


def main():

    ensure_data_files()

    migrate_book_records()

    load_active_transactions()

    while True:

        print("\n========== LIBRARY MANAGEMENT SYSTEM ==========")
        print("1. Add a Book")
        print("2. Add a Magazine")
        print("3. Register a Member")
        print("4. Search for a Book")
        print("5. Search for a Member")
        print("6. Issue a Book")
        print("7. Return a Book")
        print("8. Exit")
        print("9. Demonstrate Destructor")
        print("10. View Member Borrowing History")
        print("11. Library Summary")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_book()

        elif choice == "2":
            add_magazine()

        elif choice == "3":
            register_member()

        elif choice == "4":
            search_books()

        elif choice == "5":
            search_members()

        elif choice == "6":
            issue_book()

        elif choice == "7":
            return_book()

        elif choice == "8":
            print("Thank you for using the Library Management System!")
            break

        elif choice == "9":
            demonstrate_destructor()

        elif choice == "10":
            view_member_history()

        elif choice == "11":
            library_summary()

        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()


