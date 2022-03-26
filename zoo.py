class Zoo: 
    def __init__ (self): 
        self.animals = []
        self.enclosures = []
        
    def addAnimal(self, animal): 
        self.animals.append(animal)
        
    def removeAnimal(self, animal): 
        self.animals.remove(animal) 
    
    def getAnimal(self, animal_id): 
        for animal in self.animals: 
            if animal.animal_id == animal_id: 
                return animal 
  
    def addEnclosure(self, enclosure):
        self.enclosures.append(enclosure)

    def getEnclosure(self, enclosure_id):
        for enclosure in self.enclosures:
            if enclosure.enclosure_id == enclosure_id:
                return enclosure

    def removeEnclosure(self, enclosure):
        self.enclosures.remove(enclosure)
