class Asset:
    def __init__(self,
                 is_constructor: bool = False,
                 is_driver: bool = False,
                 name: str = None,
                 score: float = 0.,
                 streak: float = 0.,
                 price: float = 0.,
                 number_of_rounds: int = -1,
                 is_turbo: bool = False) -> None:
        self.is_constructor = is_constructor
        self.is_driver = is_driver
        self.name = name
        self.is_turbo = is_turbo
        self.score = score
        self.streak = streak
        self.avg_score = self.score / number_of_rounds
        self.predicted_score = self.avg_score + self.streak
        self.price = price
        self.ppm = self.predicted_score / self.price

    def __repr__(self) -> str:
        return f"{self.name}{'(TD)' if self.is_turbo else ''}"
