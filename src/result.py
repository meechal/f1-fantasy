from src.asset import Asset


class Result():
    def __init__(self,
                 constructor: Asset = None,
                 drivers: list[Asset] = list(),
                 score: float = 0.,
                 price: float = 0.,
                 has_constructor: bool = False,
                 has_turbo: bool = False
                 ) -> None:
        self.constructor = constructor
        self.drivers = drivers
        self.score = score
        self.price = price
        self.has_constructor = has_constructor
        self.has_turbo = has_turbo
        self.is_complete = False

    def __repr__(self) -> str:
        return f"{self.constructor} | {', '.join(map(lambda d: str(d), self.drivers))} | {self.score:.2f} | ${self.price:.1f}"

    def __calculate_score_and_price(self):
        self.price = self.constructor.price if self.has_constructor else 0
        self.score = self.constructor.predicted_score if self.has_constructor else 0
        for driver in self.drivers:
            self.price += driver.price
            self.score += driver.predicted_score if not driver.is_turbo else driver.predicted_score * 2

    def __mark_completion(self):
        if self.has_constructor and len(self.drivers) == 5 and self.has_turbo:
            self.is_complete = True

    def __sort_drivers(self):
        if self.is_complete:
            self.drivers = sorted(self.drivers, key=lambda d: d.price, reverse=True)

    def add_asset(self, asset: Asset) -> None:
        assert asset.is_constructor or asset.is_driver, f"Asset has to be constructor or driver."
        if asset.is_constructor:
            self.constructor = asset
            self.has_constructor = True
        else:
            self.drivers.append(asset)
            assert not self.has_turbo or not asset.is_turbo, f"Cannot have more than 1 TD."
            self.has_turbo = self.has_turbo or asset.is_turbo
        self.__calculate_score_and_price()
        self.__mark_completion()
        self.__sort_drivers()
