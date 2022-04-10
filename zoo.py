import random
import datetime
class Zoo:
    def __init__(self):
        self.animals = []
        self.enclosures = []
        self.employees = []
        # Plans
        self.cleaning_plan = {}
        self.medical_plan = {}
        self.feeding_plan = {}

    # Animal
    def addAnimal(self, animal):
        self.animals.append(animal)

    def removeAnimal(self, animal):
        self.animals.remove(animal)

    # Get the animal by animal id
    def getAnimal(self, animal_id):
        for animal in self.animals:
            if animal.animal_id == animal_id:
                return animal

    # Get dictionary of all the species and number of animals being the specie
    def getAnimalSpecies(self):
        # Total number of animals per species
        species = {}
        for animal in self.animals:
            if animal.species_name not in species:
                species[animal.species_name] = 1
            else:
                species[animal.species_name] += 1
        return species

    # Get the stats of animals
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

    # Get enclosure by the enclosure id
    def getEnclosure(self, enclosure_id):
        for enclosure in self.enclosures:
            if enclosure.enclosure_id == enclosure_id:
                return enclosure

    # Remove the enclosure from zoo
    def removeEnclosure(self, enclosure):
        if len(self.enclosures) <= 1:
            return print("Cannot remove enclosure and transfer its animals, due to lack of enclosures")

        # Creates a list of enclosures except the enclosure we want to remove
        enclosures_to_choose = []
        for e in self.enclosures:
            if e != enclosure:
                enclosures_to_choose.append(e)

        # Randomly select an enclosure who inherits the animals
        chosen_enclosure = random.choice(enclosures_to_choose)
        for animal in enclosure.animals:
            chosen_enclosure.addAnimal(animal)
        # Remove enclosure from zoo
        self.enclosures.remove(enclosure)

    # Employee
    def addEmployee(self, employee):
        self.employees.append(employee)

    # Get the employee by employee id
    def getEmployee(self, employee_id):
        for employee in self.employees:
            if employee.employee_id == employee_id:
                return employee

    # Remove employee from zoo
    def removeEmployee(self, employee):
        if len(self.employees) <= 1:
            return print("Cannot remove employee and transfer its animals, due to lack of employees")

        # Creates a list of employees except the employees we want to remove
        employees_to_choose = []
        for e in self.employees:
            if e != employee:
                employees_to_choose.append(e)

        # Randomly select an employee who inherits the animals
        chosen_employee = random.choice(employees_to_choose)
        for animal in employee.list_of_animals:
            chosen_employee.addAnimal(animal)
        # Remove the employee from zoo
        self.employees.remove(employee)


    # The min, max and the average number of
    # animals under the supervision of a single
    # employee
    def getEmployeeStat(self):
        stat = {}
        all_animals = []
        for i in range(0, len(self.employees)):
            all_animals.append(len(self.employees[i].list_of_animals))

        stat["min"] = min(all_animals)
        stat["max"] = max(all_animals)
        stat["average_number"] = sum(all_animals) / len(self.employees)

        return stat


    # Plans
    def createCleaningPlan(self):
        if not self.employees:
            return print("There are no employees, who would clean the enclosures")
        # For every enclosure
        for enclosure in self.enclosures:
            next_cleaned_enclosure = None
            if enclosure.cleaning_record:
                # Find the last cleaning record
                last_cleaned_enclosure = enclosure.cleaning_record[-1]
                next_cleaned_enclosure = last_cleaned_enclosure + datetime.timedelta(days=3)
            else:
                # If not cleaned before, clean today
                next_cleaned_enclosure = datetime.datetime.now()

            # Format the date
            next_cleaned_enclosure = f"{next_cleaned_enclosure.day}.{next_cleaned_enclosure.month}.{next_cleaned_enclosure.year}"
            self.cleaning_plan[enclosure.enclosure_id] = ["Next date for cleaning: " + next_cleaned_enclosure,
                                                          "Responsible employee: " + (random.choice(self.employees)).employee_id]

    def createMedicalPlan(self):
        # For every animal
        for animal in self.animals:
            next_medical_checkup = None
            if animal.vet_record:
                # Find the last vet record
                last_medical_checkup = animal.vet_record[-1]
                next_medical_checkup = last_medical_checkup + datetime.timedelta(days=35)
            else:
                # If not medical check before, check today
                next_medical_checkup = datetime.datetime.now()

            # Format the date
            next_medical_checkup = f"{next_medical_checkup.day}.{next_medical_checkup.month}.{next_medical_checkup.year}"
            self.medical_plan[animal.animal_id] = "Next date for medical check-up: " + next_medical_checkup


    def createFeedingPlan(self):
        if not self.employees:
            return print("There are no employees, who would feed the animals")
        # For every animal
        for animal in self.animals:
            next_feeding = None
            if animal.feeding_record:
                # Find the last feeding record
                last_feeding = animal.feeding_record[-1]
                next_feeding = last_feeding + datetime.timedelta(days=2)
            else:
                # If not fed before, feed today
                next_feeding = datetime.datetime.now()

            # Format the date
            next_feeding = f"{next_feeding.day}.{next_feeding.month}.{next_feeding.year}"
            self.feeding_plan[animal.animal_id] = ["Next date for feeding: " + next_feeding,
                                                   "Responsible employee: " + (random.choice(self.employees)).employee_id]
