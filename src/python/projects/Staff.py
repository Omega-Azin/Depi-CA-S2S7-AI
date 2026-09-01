from person import Person


class Staff(Person):
    """
    Class representing hospital staff members, inheriting from the Person base class.
    """

    def __init__(self, name: str, age: int, position: str):
        """
        Initialize a new Staff object.

        :param name: The name of the staff member (validated by Person class)
        :param age: The age of the staff member (validated by Person class)
        :param position: The job position/role of the staff member
        """
        super().__init__(name, age)

        if not isinstance(position, str) or not position.strip():
            raise ValueError("Position must be a non-empty string.")

        self.position = position.strip()

    def view_info(self):
        """
        Override view_info to display name, age, and position.
        """
        print(
            f"Staff Name: {self.name} | Age: {self.age} | Position: {self.position}"
        )

    def __str__(self) -> str:
        """
        String representation of the staff member.
        """
        return f"Staff(Name: '{self.name}', Age: {self.age}, Position: {self.position}')"


if __name__ == "__main__":
    try:
        doctor = Staff(name="Dr. Ahmed", age=42, position="Cardiologist")

        print("--- Testing view_info() ---")
        doctor.view_info()

        print("\n--- Testing __str__() ---")
        print(doctor)

    except ValueError as e:
        print(f"Validation Error: {e}")