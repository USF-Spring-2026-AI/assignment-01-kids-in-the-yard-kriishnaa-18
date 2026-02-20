class Person:
    """
    Represents one person in the family tree.
    """
    def __init__(self, first_name, last_name, year_born, year_died):
        """
        Creates a new Person object.
        """
        self.first_name = first_name
        self.last_name = last_name
        self.year_born = year_born
        self.year_died = year_died

        self.partner = None
        self.children = []

    def add_child(self, child):
        """
        Adds a child to this person.
        """
        self.children.append(child)
    
    def set_partner(self, partner):
        """
        Sets this person's partner.
        """
        self.partner = partner
    
    def get_full_name(self):
        """
        Returns the person's full name.
        """
        return self.first_name + " " + self.last_name