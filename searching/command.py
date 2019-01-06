class Command:
    def __init__(self, field: str, value: str, weight: float):
        self.field: str = field
        self.value: str = value
        self.weight: float = weight
