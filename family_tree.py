from person_factory import PersonFactory

class FamilyTree:
    """
    Builds and manages a family tree starting from two root individuals.
    """
    def __init__(self):
        # Creates a factory object to generate people and read files.
        self.factory = PersonFactory()
        self.factory.read_files()

        # Store all the Person objects created.
        self.people = []

        # Create two root person born in 1950 and storing their last name.
        self.p1 = self.factory.create_person(1950)
        self.p2 = self.factory.create_person(1950)
        self.factory.root_last = ( self.p1.last_name, self.p2.last_name)

        # Setting the two persons as partners
        self.p1.set_partner(self.p2)
        self.p2.set_partner(self.p1)

        # Add them to the list
        self.people.append(self.p1)
        self.people.append(self.p2)

        # Building a family on person 1
        self.build_family(self.p1)

    def build_family(self, person):
        """
        Recursively builds the family tree.
        """
        # Stops recursion once we reach the year 2120
        if person.year_born >= 2120:
            return

        # If person does not have partner, we create one for them.
        if person.partner is None:  
            partner = self.factory.create_partner(person)
            if partner and partner.year_born <= 2120:
                self.people.append(partner)

        # Creating children for the person and adding each child to the list.
        # Continue building the family tree.
        children = self.factory.create_children(person)
        for child in children:
            if child.year_born <= 2120:
                self.people.append(child)
                self.build_family(child)

    def total_people(self):
        """
        Returns total number of people in the family tree.
        """
        return len(self.people)

    def total_by_decade(self):
        """
        Returns how many people were born in each decade.
        """
        counts = {}

        for person in self.people:
            # Calculates decade
            decade = (person.year_born // 10) * 10

            # Increases count for that decade.
            if decade in counts:
                counts[decade] += 1
            else:
                counts[decade] = 1

        return counts

    def duplicate_names(self):
        """
        Finds duplicate full names in the tree and returns a list of duplicate names.
        """
        name_counts = {}

        # Counts how many times each name appears
        for person in self.people:
            name = person.get_full_name()

            if name in name_counts:
                name_counts[name] += 1
            else:
                name_counts[name] = 1

        duplicates = []

        # Collecting the names and adding it to the list.
        for name in name_counts:
            if name_counts[name] > 1:
                duplicates.append(name)

        return duplicates

    def interaction(self):
        """
        Simple console menu for user.
        """
        while True:
            print("\nAre you interested in:")
            print("(T)otal number of people in the tree")
            print("Total number of people in the tree by (D)ecade")
            print("(N)ames duplicated")

            choice = input("> ").upper()

            # Total number of people in the family tree.
            if choice == "T":
                print("The tree contains", self.total_people(), "people total")

            # Total number of people in each decade.
            elif choice == "D":
                counts = self.total_by_decade()
                for decade in sorted(counts):
                    print(decade, ":", counts[decade])

            # List of uplicate names.
            elif choice == "N":
                duplicates = self.duplicate_names()
                print("There are", len(duplicates), "duplicate names:")
                for name in duplicates:
                    print("*", name)

            else:
                print("Invalid choice.")