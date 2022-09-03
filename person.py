import variable_names
import exceptions

class Person():
    
    # class attributes
    genders = variable_names.GENDER_NAMES
    persons = {g:[] for g in genders}
    proposing_side = genders[0]
    
    def __init__(self, name, gender, preferences=()):
        """Constructor method for Person class.

        Args:
            name (str): Name of the person.
            gender (any): Gender of the person.
            preferences (tuple, optional): preferences input for person, lower indices are more preferred. Defaults to ().

        Raises:
            TypeError: If name is not a string.
            exceptions.GenderError: If gender name is not in the GENDER_NAMES tuple from variable_names.
        """
        try:
            self.name = name.lower()
        except AttributeError as e:
            raise TypeError(f'Name should be a string. Got {type(name)} instead') from e

        if gender in Person.genders:
            self.gender = gender
        else:
            raise exceptions.GenderError(Person.genders)

        self.preferences = preferences
        
        self.match = self
        self.next = None
        self.proposals = {}
                
        Person.persons[self.gender].append(self)
        
    def __del__(self):
        """Destructor method for Person class.
        """
        print(f'{self.name} is being deleted')

    def __repr__(self):
        """Repr method for Person class.

        Returns:
            str: Name and gender of the person. If you want to print preferencess, use print_preferencess method.
        """
        return f'Name: {self.name}, Gender: {self.gender}'
    
    def print_preferencess(self):
        """Prints the preferencess of the person.
        """
        print(f'{self.name} has the following preferencess:')
        for person, rank in self.preferences_with_ranks_dict.items():
            print(f'{rank}. {person.name}')
    
    @property
    def preferences_with_ranks_dict(self):
        """Getter method for preferences with ranks dictionary.

        Returns:
            dict: Preferences with ranks dictionary.
        """
        return {person:self.preferences.index(person) for person in self.preferences}

    def set_preferences(self, preferences):
        """Setter method for preferences attribute.

        Args:
            preferences (tuple): preferences input for person, lower indices are more preferred.
        """
        if isinstance(preferences, tuple):
            if all(isinstance(person, Person) for person in preferences):
                if all(self.gender != person.gender for person in preferences):
                    if len(set(preferences)) == len(preferences):
                        self.preferences = preferences
                        try:
                            self.next = self.preferences[0]
                        except IndexError:
                            self.next = self
                    else:
                        raise ValueError('preferences input should not contain duplicate Person objects')
                else:
                    raise ValueError('preferences input can only contain Person objects from the opposite gender')
            else:
                raise TypeError('preferences input should contain Person objects')
        else:
            raise TypeError(f'preferences input should be a tuple. Got {type(preferences)} instead')

    @property
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
        to_propose.proposals[self] = to_propose.preferences_with_ranks_dict[self]
        next_to_propose_rank = self.preferences_with_ranks_dict[to_propose] + 1
        try:
            self.next = list(self.preferences_with_ranks_dict.keys())[list(self.preferences_with_ranks_dict.values()).index(next_to_propose_rank)]
        except ValueError:
            self.next = self
    
    def engage(self, proposer):
        """Engages the person with the proposer."""
        self.set_match(proposer)
        proposer.set_match(self)
        print(f'{self.name} is engaged to {proposer.name}')
    
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
            print(f'{self.name} is responding to proposal{"s" if len(self.proposals) > 1 else ""} from {", ".join(list(map(lambda x: x.name,self.proposals.keys())))}')
            to_accept = self.get_most_preferred(self.proposals)
            if self.is_single:
                self.engage(to_accept)
            else:
                if self.preferences_with_ranks_dict[to_accept] < self.preferences_with_ranks_dict[self.match]:
                    self.match.make_single()
                    print(f'{self.name} breaks the engagement with {self.match.name}')
                    self.engage(to_accept)
                else:
                    print(f'{self.name} is not interested in {to_accept.name}')
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
        if any(len(cls.persons[g]) for g in cls.genders) != 0:
            print('Deleting all persons')
            cls.persons = {g:[] for g in cls.genders}
        else:
            print('No persons to delete')
            
    @classmethod
    def print_matches(cls, final=False):
        """Class method to print all matches in the persons dictionary.
        """
        if final:
            print(f'********** PRINTING {cls.proposing_side.upper()} OPTIMAL MATCH **********')
        else:
            print('***** PRINTING CURRENT PROPOSER ENGAGEMENTS *****')
        for person in cls.persons[cls.proposing_side]:
            if person.is_single:
                print(f'{person.name} is not engaged')
            else:
                print(f'{person.name} <----------> {person.match.name}')
            
    @classmethod
    def set_proposing_side(cls, side):
        """Class method to set the proposing side.
        """
        cls.proposing_side = side
            