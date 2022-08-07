import variable_names
import exceptions

class Person():
    genders = variable_names.GENDER_NAMES
    persons = {g:[] for g in genders}
    proposer_side = genders[0]
    
    def __init__(self, name, gender, preference=()):
        """Constructor method for Person class.

        Args:
            name (str): Name of the person.
            gender (any): Gender of the person.
            preference (tuple, optional): Preference input for person, lower indices are more preferred. Defaults to ().

        Raises:
            TypeError: If name is not a string.
            exceptions.GenderError: If gender name is not in the GENDER_NAMES tuple from variable_names.py.
        """
        try:
            self.name = name.lower()
        except AttributeError as e:
            raise TypeError(f'Name should be a string. Got {type(name)} instead') from e

        if gender in Person.genders:
            self.gender = gender
        else:
            raise exceptions.GenderError(gender, Person.genders)

        self.match = self
        self.next = self
        self.set_preference(preference)
        self.proposals = {}
                
        Person.persons[self.gender].append(self)
        
    def __del__(self):
        """Destructor method for Person class.
        """
        print(f'{self.name} is being deleted')

    def __repr__(self):
        """Repr method for Person class.

        Returns:
            str: Name and gender of the person. If you want to print preferences, use print_preferences method.
        """
        return f'Name: {self.name} | Gender: {self.gender}'
    
    def print_preferences(self):
        """Prints the preferences of the person.
        """
        print(f'{self.name} has the following preferences:')
        for person, rank in self.preference.items():
            print(f'{rank}. {person.name}')

    def set_preference(self, preference):
        """Setter method for preference attribute.

        Args:
            preference (tuple): Preference input for person, lower indices are more preferred.
        """
        if isinstance(preference, tuple):
            if all(isinstance(person, Person) for person in preference):
                if all(self.gender != person.gender for person in preference):
                    if len(set(preference)) == len(preference):
                        self.preference = {person:preference.index(person)+1 for person in preference}
                        try:
                            self.next = preference[0]
                        except IndexError:
                            self.next = self
                    else:
                        raise ValueError('Preference input should not contain duplicate Person objects')
                else:
                    raise ValueError('Preference input can only contain Person objects from the opposite gender')
            else:
                raise TypeError('Preference input should contain Person objects')
        else:
            raise TypeError(f'Preference input should be a tuple. Got {type(preference)} instead')

    def is_single(self):
        """Checks if the person is single.

        Returns:
            bool: True if the person is single, False otherwise.
        """
        return self.match == self

    def make_single(self):
        """Makes the person single.
        """
        self.match = self
        
    def set_match(self, match):
        """Setter method for match attribute.

        Args:
            match (Person): Current match of the person.
        """
        self.match = match
    
    def propose(self, to_propose):
        """Proposes to a person, adds the person to the proposals dictionary of the proposed, and updates the next attribute.

        Args:
            to_propose (Person): Person to propose to.
        """
        print(f'{self.name} is proposing to {to_propose.name}')
        to_propose.proposals[self] = to_propose.preference[self]
        next_to_propose_rank = self.preference[to_propose] + 1
        try:
            self.next = list(self.preference.keys())[list(self.preference.values()).index(next_to_propose_rank)]
        except ValueError:
            self.next = self
    
    def engage(self, proposer):
        """Engages the person with the proposer."""
        print(f'{self.name} is engaged to {proposer.name}')
        self.set_match(proposer)
        proposer.set_match(self)
    
    def get_most_preferred(self, proposals):
        """Returns the most preferred person from an input proposals dictionary.

        Args:
            proposals (dict): Current proposals of the person as keys and their preference ranks as values.

        Returns:
            Person: The most preferred person from the input proposals dictionary.
        """
        return min(proposals, key=proposals.get)
        
    def respond_to_proposals(self):
        """If the person has proposals, responds to them, else does nothing.
        If the person is single, accepts the best proposal.
        If the person is not single, accepts the best proposal only if the best proposal is better than the current match.
        Makes the current match single if current match changes.
        """ 
        if len(self.proposals) > 0:
            print(f'{self.name} is responding to proposals')
            to_accept = self.get_most_preferred(self.proposals)
            if self.is_single():
                self.engage(to_accept)
            else:
                if self.preference[to_accept] < self.preference[self.match]:
                    self.match.make_single()
                    self.engage(to_accept)
            self.proposals = {}
            
    def get_opposite_gender(self):
        """Getter method for the opposite gender.

        Returns:
            str: Opposite gender of the person.
        """
        first_gender, second_gender = Person.genders[0], Person.genders[1]
        return first_gender if first_gender != self.gender else second_gender
    
    @classmethod
    def delete_persons(cls):
        """Class method to delete all persons in the persons dictionary.
        """
        cls.persons = {g:[] for g in cls.genders}
        
    @classmethod
    def print_matches(cls):
        """Class method to print all matches in the persons dictionary.
        """
        for person in cls.persons[cls.proposer_side]:
            print(f'{person.name} ------: {person.match.name}')
            