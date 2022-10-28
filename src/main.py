import random

from gs_algorithm import gs_algorithm
from person import Person


def make_persons(n: int) -> None:
    first_gender, second_gender = Person.genders[0], Person.genders[1]
    first_gender_first_char, second_gender_first_char = (
        first_gender[0],
        second_gender[0],
    )
    if first_gender_first_char != second_gender_first_char:
        for i in range(1, int(n / 2) + 1):
            Person(f"{first_gender_first_char}{i}", first_gender)
            Person(f"{second_gender_first_char}{i}", second_gender)


def randomize_preferences(person: Person) -> None:
    opposite_gender_persons = Person.persons[person.get_opposite_gender()]
    person.set_preferences(
        tuple(random.sample(opposite_gender_persons, len(opposite_gender_persons)))
    )


NUMBER_OF_PERSONS = 500

Person.delete_persons()
make_persons(NUMBER_OF_PERSONS)
for v in Person.persons.values():
    for person in v:
        randomize_preferences(person)


if __name__ == "__main__":
    gs_algorithm(Person)
