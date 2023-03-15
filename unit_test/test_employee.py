from employee import Scientist
import unittest

class TestPilot(unittest.TestCase):
    def setUp(self) -> None:
        self.employee_1 = Scientist("Linus", "Torvald", 4000)
        self.employee_2 = Scientist("Yann", "LeCun", 2500)
        self.employee_3 = Scientist("Nando", "Freitas", 1500)
    
    def test_email(self):
        self.assertEqual(self.employee_1.email, "linus.torvald@google.com")
        self.assertEqual(self.employee_2.email, "yann.lecun@google.com")
        self.assertEqual(self.employee_3.email, "nando.freitas@google.com")

        self.employee_3.name = "Matheus"
        self.employee_3.surname = "Cardoso"

        self.assertEqual(self.employee_3.email, "matheus.cardoso@google.com")

    def test_full_name(self):
        self.assertEqual(self.employee_1.full_name, "Linus Torvald")
        self.assertEqual(self.employee_2.full_name, "Yann LeCun")
        self.assertEqual(self.employee_3.full_name, "Nando Freitas")

    def test_increase_wage(self):
        self.employee_1.increase_wage(1.1)
        self.employee_2.increase_wage(1.1)
        self.employee_3.increase_wage(2)

        self.assertEqual(self.employee_1.wage, 4400)
        self.assertEqual(self.employee_2.wage, 2750)
        self.assertEqual(self.employee_3.wage, 4000)


if __name__ == "__main__":
    unittest.main()