from ast import increment_lineno


class Scientist:

    def __init__(self, name, surname, payment_amount) -> None:
        self.name = name
        self.surname = surname
        self.wage = payment_amount

    @property
    def email(self):
        return "{}.{}@google.com".format(self.name.lower(), self.surname.lower())
    
    @property
    def full_name(self):
        return "{} {}".format(self.name, self.surname)


    def increase_wage(self, increase_percentage):
        self.wage = int(self.wage * increase_percentage)
