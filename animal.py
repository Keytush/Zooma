import uuid 
import datetime 
class Animal: 
    def __init__ (self, species_name, common_name, age): 
        self.animal_id = str(uuid.uuid4())
        self.species_name = species_name 
        self.common_name = common_name 
        self.age = age 
        self.feeding_record = [] 
        self.enclosure = None 
        self.care_taker = None 
        # add more as required here 
        
    # simply store the current system time when this method is called    
    def feed(self): 
        self.feeding_record.append ( datetime.datetime.now()) 
            