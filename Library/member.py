class Member:

    def __init__(self, member_id, name, borrowing_limit):
        self.member_id = member_id
        self.name = name
        self.__borrowing_limit = borrowing_limit
        self.__fine = 0
        self.__borrowed_items = []

    def get_borrowing_limit(self):
        return self.__borrowing_limit

    def get_fine(self):
        return self.__fine

    def add_fine(self, amount):
        self.__fine += amount

    def get_borrowed_count(self):
        return len(self.__borrowed_items)


    def borrow_item(self, item):
        self.__borrowed_items.append(item)


    def return_borrowed_item(self, item):
        if item in self.__borrowed_items:
            self.__borrowed_items.remove(item)

    def display_info(self):
        print("Member ID:", self.member_id)
        print("Name:", self.name)
        print("Borrowing Limit:", self.__borrowing_limit)
        print("Fine:", self.__fine)


class StudentMember(Member):

    def __init__(self, member_id, name):
        super().__init__(member_id, name, 3)

    def calculate_fine(self, overdue_days):
        return overdue_days * 2


class StaffMember(Member):

    def __init__(self, member_id, name):
        super().__init__(member_id, name, 5)

    def calculate_fine(self, overdue_days):
        return overdue_days * 1
    