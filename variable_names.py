import exceptions

GENDER_NAMES = ('man', 'woman')

if len(GENDER_NAMES) != 2:
    raise exceptions.TwoSidedMatchingError(GENDER_NAMES)