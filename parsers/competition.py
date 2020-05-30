class Competition:

    title = None
    location = None
    start_date = None
    end_date = None
    description = None
    type = None
    image = None
    link = None

    def __init__(self):
        pass

    def set_title(self, title: str):
        self.title = title
        return self

    def set_location(self, location: str):
        self.location = location
        return self

    def set_start_date(self, start_date: str):
        self.start_date = start_date
        return self
