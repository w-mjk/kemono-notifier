class Profile:
    def __init__(self):
        self.name = None
        self.updated = None
        
    def __init__(self, name, updated):
        self.name = name
        self.updated = updated

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_updated(self, updated):
        self.updated = updated

    def get_updated(self):
        return self.updated
    
    def to_json(self):
        profile_dict = {
            "name": self.name,
            "updated": self.updated
        }
        return profile_dict