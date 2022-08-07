## variable_names exceptions
        
class TwoSidedMatchingError(Exception):
    def __init__(self, genders):
        self.genders = genders
        self.message = f'There are {len(self.genders)} sides to be matched. There should be exactly two'
        super().__init__(self.message)
        
        
## person exceptions

class GenderError(Exception):
    def __init__(self, gender, gender_names):
        self.gender = gender
        gender_names_with_quotes = [f"'{g}'" for g in gender_names]
        self.message = \
            f'Gender should be a {" or a ".join(gender_names_with_quotes)}'
        super().__init__(self.message)
