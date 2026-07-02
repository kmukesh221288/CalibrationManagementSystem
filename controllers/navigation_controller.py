class NavigationController:

    def __init__(self):

        self.pages = {}

        self.current_page = None

    def add_page(self, name, page):

        self.pages[name] = page

    def show_page(self, name):

        if self.current_page:

            self.current_page.pack_forget()

        self.current_page = self.pages[name]

        self.current_page.pack(
            fill="both",
            expand=True
        )