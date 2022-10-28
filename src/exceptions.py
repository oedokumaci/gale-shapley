class TwoSidedMatchingError(Exception):
    def __init__(self, genders: list[str]) -> None:
        self.message = (
            f"There are {len(genders)} sides to be matched. There should be exactly two"
        )
        super().__init__(self.message)


class GenderError(Exception):
    def __init__(self, gender_names: list[str]) -> None:
        gender_names_in_quotes = [f"'{g}'" for g in gender_names]
        self.message = f'Gender should be a {" or a ".join(gender_names_in_quotes)}'
        super().__init__(self.message)
