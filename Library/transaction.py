
import random
from datetime import date, timedelta

from .file_utils import append_record, update_book_record


class Transaction:

    def __init__(self, member, item):

        self.transaction_id = random.randint(1000, 9999)

        self.member = member
        self.item = item

        self.issue_date = date.today()
        self.due_date = self.issue_date + timedelta(days=14)

        self.return_date = None
        self.fine = 0
        self.status = "Pending"

    # Issue a book
    def issue_item(self):

        # Check book availability
        if not self.item.available:
            print("Sorry! This item is already issued.")
            return False

        # Check member borrowing limit
        if self.member.get_borrowed_count() >= self.member.get_borrowing_limit():
            print("Borrowing limit reached!")
            return False

        # Issue the book
        self.item.available = False
        self.member.borrow_item(self.item)

        self.status = "Issued"

        # Update book availability in books.txt
        update_book_record(self.item)

        # Save transaction in transactions.txt
        record = (
            f"ISSUED|{self.transaction_id}|"
            f"{self.member.member_id}|{self.item.item_id}|"
            f"{self.issue_date}|{self.due_date}"
        )

        append_record("transactions.txt", record)

        print("\nBook issued successfully!")
        print("Transaction ID:", self.transaction_id)
        print("Issue Date:", self.issue_date)
        print("Due Date:", self.due_date)

        return True

    # Return a book
    def return_item(self):

        # Check whether the book was issued
        if self.status != "Issued":
            print("This transaction is not currently active.")
            return False

        # Record return date
        self.return_date = date.today()

        # Calculate overdue days
        overdue_days = (self.return_date - self.due_date).days

        # Calculate fine if the book is overdue
        if overdue_days > 0:

            self.fine = self.member.calculate_fine(overdue_days)

            self.member.add_fine(self.fine)

        # Update book and member records
        self.item.available = True

        self.member.return_borrowed_item(self.item)

        self.status = "Returned"

        # Update book availability in books.txt
        update_book_record(self.item)

        # Save return information in transactions.txt
        record = (
            f"RETURNED|{self.transaction_id}|"
            f"{self.return_date}|{self.fine}"
        )

        append_record("transactions.txt", record)

        print("\nBook returned successfully!")
        print("Return Date:", self.return_date)
        print("Overdue Days:", max(0, overdue_days))
        print("Fine: ₹", self.fine)

        return True

    # Display transaction details
    def display_transaction(self):

        print("\n--- TRANSACTION DETAILS ---")
        print("Transaction ID:", self.transaction_id)
        print("Member:", self.member.name)
        print("Item:", self.item.title)
        print("Issue Date:", self.issue_date)
        print("Due Date:", self.due_date)
        print("Return Date:", self.return_date)
        print("Status:", self.status)
        print("Fine: ₹", self.fine)
