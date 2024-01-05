class Item:
    def __init__(self, name:str, description:str, status:bool = False):
        if not name:
            raise ValueError("Name cannot be empty")
        
        self.name = name
        self.description = description
        self.status = status