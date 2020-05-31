class Competition:
    def __init__(self):
        self.title = None
        self.location = None
        self.start_date = None
        self.end_date = None
        self.description = None
        self.type = None
        self.image = None
        self.link = None

    def set_title(self, title: str):
        self.title = title
        return self

    def set_location(self, location: str):
        self.location = location
        return self

    def set_start_date(self, start_date: str):
        self.start_date = start_date
        return self

    def set_description(self, description: str):
        self.description = description

    def set_end_date(self, end_date: str):
        self.end_date = end_date

    def set_type(self, competition_type: str):
        self.type = competition_type

    def set_image(self, image: object):
        self.image = image

    def set_link(self, link: str):
        self.link = link

    def __str__(self):
        return f"{self.title} , {self.type} , {self.link}, {self.location}, {self.description}"
