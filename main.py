# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     custom_cell_magics: kql
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.2
#   kernelspec:
#     display_name: Python 3.9.12 ('base')
#     language: python
#     name: python3
# ---

# %% [markdown]
# # IMPORTS

# %%
import random
from person import Person
from gs_algorithm import gs_algorithm


# %% [markdown]
# # AUXILIARY FUNCTIONS

# %%
def make_persons(n):
    first_gender, second_gender = Person.genders[0], Person.genders[1]
    first_gender_first_char, second_gender_first_char = first_gender[0], second_gender[0]
    if first_gender_first_char != second_gender_first_char:
        for i in range(1, int(n/2)+1):
            Person(f'{first_gender_first_char}{i}', first_gender)
            Person(f'{second_gender_first_char}{i}', second_gender)


# %%
def randomize_preferences(person):
    opposite_gender_persons = Person.persons[person.get_opposite_gender()]
    person.set_preference(tuple(random.sample(opposite_gender_persons, len(opposite_gender_persons))))

# %% [markdown]
# # INITIALIZE PERSONS


# %%
Person.delete_persons()
make_persons(20)
for k, v in Person.persons.items():
    for person in v:
        randomize_preferences(person)
        # person.print_preferences()


# %% [markdown]
# # RUN ALGORITHM

# %%
# %%time

if __name__ == '__main__':
    gs_algorithm(Person)

# %%
