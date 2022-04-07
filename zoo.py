class Zoo:
    def __init__(self):
        self.animals = []
        self.enclosures = []
        self.employees = []

    # Animal
    def addAnimal(self, animal):
        self.animals.append(animal)

    def removeAnimal(self, animal):
        self.animals.remove(animal)

    def getAnimal(self, animal_id):
        for animal in self.animals:
            if animal.animal_id == animal_id:
                return animal

    def getAnimalSpecies(self):
        # Total number of animals per species
        species = {}
        for animal in self.animals:
            if animal.species_name not in species:
                species[animal.species_name] = 1
            else:
                species[animal.species_name] += 1
        return species

    def getAnimalStat(self):
        stat = {}

        # Total number of animals per species
        stat["total_num_animals_per_species"] = self.getAnimalSpecies()

        # Average number of animals per enclosure
        if len(self.enclosures) > 0:
            stat["avg_num_animals_per_enclosure"] = len(self.animals) / len(self.enclosures)
        else:
            stat["avg_num_animals_per_enclosure"] = None

        # Number of enclosures with animals from multiple species
        num_enclosures = 0
        for enclosure in self.enclosures:
            species = []
            for animal in enclosure.animals:
                if animal.species_name not in species:
                    species.append(animal.species_name)
            if len(species) > 1:
                num_enclosures += 1

        stat["num_enclosures_with_different_species"] = num_enclosures

        # Available space per animal in each enclosure
        avail_space_per_animal_in_enclosure = {}
        for enclosure in self.enclosures:
            avail_space_per_animal_in_enclosure[enclosure.enclosure_id] = enclosure.available_space / len(
                enclosure.animals)

        stat["avail_space_per_animal_in_enclosure"] = avail_space_per_animal_in_enclosure

        return stat

    # Enclosure
    def addEnclosure(self, enclosure):
        self.enclosures.append(enclosure)

    def getEnclosure(self, enclosure_id):
        for enclosure in self.enclosures:
            if enclosure.enclosure_id == enclosure_id:
                return enclosure

    def removeEnclosure(self, enclosure):
        self.enclosures.remove(enclosure)

    # Employee
    def addEmployee(self, employee):
        self.employees.append(employee)

    def getEmployee(self, employee_id):
        for employee in self.employees:
            if employee.employee_id == employee_id:
                return employee

    def removeEmployee(self, employee):
        self.employees.remove(employee)
