class Item:
    def __init__(self, name:str, description:str, status:bool = False):
        self.name = name
        self.description = description
        self.status = status