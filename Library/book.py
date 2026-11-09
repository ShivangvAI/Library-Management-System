class LibraryItem:
    def __init__(self, item_id, title):
        self.item_id = item_id
        self.title = title
        self.available = True

    def display_info(self):
        print("Item Id:", self.item_id)
        print("Title:", self.title)
        print("Available:", self.available)

    def __del__(self):
        print("Library item", self.title, "is being destroyed.")

class Book(LibraryItem):

    def __init__(self, item_id, Title, author):
        super().__init__(item_id, Title)
        self.author = author

    def display_info(self):
        super().display_info()
        print("Author:", self.author)

class Magazine(LibraryItem):
    def __init__(self, item_id, title, issue_number):
        super().__init__(item_id, title)
        self.issue_number = issue_number

    def display_info(self):
        super().display_info()
        print("Issue Number:", self.issue_number)