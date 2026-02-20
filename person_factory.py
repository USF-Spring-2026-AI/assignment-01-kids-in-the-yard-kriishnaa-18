import random
import math
from person import Person

class PersonFactory:
    """
    Reads CSV data files and generates Person objects (people, partners, children).
    """
    def __init__(self):
        """ Dictionaries to store all the CSV data. """
        # I learnt dictionaries in CS110 in Fall 2023 but to refresh it,
        # I used https://www.w3schools.com/python/python_dictionaries.asp
        self.life_expectancy_data = {}
        self.birth_marriage_data = {}
        self.first_names_data = {}
        self.last_names_data = {}
        self.rank_probability_data = {}
        self.root_last = None

    def read_files(self):
        """Read all CSV files and store data in dictionaries."""
        # life_expectancy.csv file
        with open("life_expectancy.csv", "r") as file:
            lines = file.readlines()

            for line in lines[1:]:  
                parts = line.strip().split(",")

                year = int(parts[0])
                expectancy = float(parts[1])

                self.life_expectancy_data[year] = expectancy

        # birth_and_marriage_rates.csv file
        with open("birth_and_marriage_rates.csv", "r") as file:
            lines = file.readlines()

            for line in lines[1:]:
                parts = line.strip().split(",")

                decade_string = parts[0]
                # Converting from string to int.
                decade = int(decade_string.replace("s", "")) 
                birth_rate = float(parts[1])
                marriage_rate = float(parts[2])

                self.birth_marriage_data[decade] = {"birth_rate": birth_rate, "marriage_rate": marriage_rate}

        # first_names.csv file
        with open("first_names.csv", "r") as file:
            lines = file.readlines()

            for line in lines[1:]:
                parts = line.strip().split(",")

                decade_str = parts[0]
                # Converting from string to int.
                decade = int(decade_str.replace("s", ""))

                name = parts[2].strip()
                freq = float(parts[3])

                # Add (name, frequency) to that decade's list.
                if decade in self.first_names_data:
                    self.first_names_data[decade].append((name, freq))
                else:
                    self.first_names_data[decade] = [(name, freq)]


        # last_names.csv file
        with open("last_names.csv", "r") as file:
            lines = file.readlines()

            for line in lines[1:]:
                parts = line.strip().split(",")

                decade_str = parts[0]
                # Converting string to int.
                decade = int(decade_str.replace("s", ""))

                rank = int(parts[1])
                name = parts[2].strip()

                # Add (name, rank) to that decade's list.
                if decade in self.last_names_data:
                    self.last_names_data[decade].append((name, rank))
                else:
                    self.last_names_data[decade] = [(name, rank)]

        # rank_to_probability.csv file
        with open("rank_to_probability.csv", "r") as file:
            line = file.readline().strip()
            parts = line.split(",")

            for i in range(len(parts)):
                rank = i + 1
                prob = float(parts[i])

                self.rank_probability_data[rank] = prob
        
    def generate_year_died(self, year_born):
        """Generate a death year using life expectancy."""

        # Get birth decade.
        decade = (year_born // 10) * 10

        # Making sure it stays within the range.
        if decade < 1950:
            decade = 1950
        if decade > 2120:
            decade = 2120

        expectancy = self.life_expectancy_data[decade]

        # Random adjustment between -10 and +10
        # Cite: used StackOverflow for the random function [https://stackoverflow.com/questions/8993766/how-to-random-mathematical-operations]
        random_adjustment = random.randint(-10, 10)

        return int(round(year_born + expectancy + random_adjustment))
    
    def generate_first_name(self, year_born):
        """Pick a first name based on birth decade."""
        decade = (year_born // 10) * 10

        # Making sure it stays within the range.
        if decade < 1950:
            decade = 1950
        if decade > 2120:
            decade = 2120

        # Getting all data for that decade.
        names_data = self.first_names_data[decade]
        names = []
        freq = []

        # Separate names and their frequencies
        for item in names_data:
            names.append(item[0])       
            freq.append(item[1]) 

        # Choose name using weights [https://docs.python.org/3/library/random.html#random.choices]
        chosen_name = random.choices(names, weights=freq)[0]

        return chosen_name

    # Cite: Used CHATGPT for is_descendant boolean flag. [Used in generate_last_name, create_person and create_children]
    # I originally attempted to determine which parent was older when generating children 
    # to decide last name inheritance, but I found the logic confusing.
    # I referred to CHATGPT for help and it suggested to use a boolean.
    # The flag is set in create_children to check if it is true or false, 
    # then it is passed through create_person as a middleman, 
    # and evaluated in generate_last_name to determine last name inheritance.

    def generate_last_name(self, year_born, is_descendant=False):
        """
        Choose a last name based on birth decade. If person is a descendant, use root last names.
        """
        decade = (year_born // 10) * 10

        # If is_descendant is True, the last name is randomly chosen
        # from the original root family last names. Otherwise, the
        # last name is selected from the dataset using weighted probability.
        if is_descendant and self.root_last:
            return random.choice(self.root_last)

        # Making sure it stays within the range.
        if decade < 1950:
            decade = 1950
        if decade > 2120:
            decade = 2120

        names = []
        weights = []

        # Converts ranks to probabilities
        for item in self.last_names_data[decade]:
            name = item[0]
            rank = item[1]

            prob = self.rank_probability_data[rank]

            names.append(name)
            weights.append(prob)

        # Choose last name using weighted random selection.
        chosen_name = random.choices(names, weights=weights)[0]

        return chosen_name

    def create_person(self, year_born, is_descendant=False):
        """
        Create and return a new Person object.
        """
        first_name = self.generate_first_name(year_born)
        last_name = self.generate_last_name(year_born, is_descendant) # Passing is_descendant to generate last name
        year_died = self.generate_year_died(year_born)

        return Person(first_name, last_name, year_born, year_died)

    def create_partner(self, person):
        """
        Create a partner based on marriage rate.
        """
        decade = (person.year_born // 10) * 10
        marriage_rate = self.birth_marriage_data[decade]["marriage_rate"]

        # Random chance to get married.
        if random.random() < marriage_rate:
            # Partner born within ±10 years.
            partner_year = random.randint(person.year_born - 10, person.year_born + 10)
            partner = self.create_person(partner_year)

            # Link both partners.
            person.set_partner(partner)
            partner.set_partner(person)

            return partner

        return None

    def create_children(self, person):
        """
        Create children based on birth rate.
        """
        decade = (person.year_born // 10) * 10
        birth_rate = self.birth_marriage_data[decade]["birth_rate"]

        # Calculate range around birth rate.
        # Cite: Learnt ceil from geeksforgeeks. [https://www.geeksforgeeks.org/python/floor-ceil-function-python/]
        min_children = math.ceil(birth_rate - 1.5)
        max_children = math.ceil(birth_rate + 1.5)

        # Prevents negative children.
        if min_children < 0:
            min_children = 0
        if max_children < min_children:
            max_children = min_children

        # Random number of children in range.
        num_children = random.randint(min_children, max_children)

        children = []
        for i in range(num_children):
            # Child is born 25–45 years after parent.
            child_year = person.year_born + random.randint(25, 45)

            child = self.create_person(child_year, is_descendant=True)

            # Adding child to its parent.
            person.add_child(child)

            # Add child to partner if exists.
            if person.partner:
                person.partner.add_child(child)

            children.append(child)

        return children