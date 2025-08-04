from datetime import date, time, datetime

class Profile:
    def __init__(self):
        self.name = None
        self.last_imported = None
        
    def __init__(self, name, last_imported):
        self.name = name
        self.last_imported = last_imported

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_last_imported(self, last_imported):
        self.last_imported = last_imported

    def get_last_imported(self):
        return self.last_imported
    
    def to_json(self):
        profile_dict = {
            "name": self.name,
            "last_imported": self.last_imported
        }
        return profile_dict