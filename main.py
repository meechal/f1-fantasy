# This is a simple code to generate teams for F1 fantasy game, based on average scoring in previous races.
from copy import deepcopy

from constants import BUDGET, MEGAMAX_LIMIT, STREAK_CONSTRUCTOR, STREAK_DRIVER, STREAK_R, STREAK_Q
from src.asset import Asset
from src.fetch_data import fetch
from src.result import Result

CONSTRUCTORS = list()
DRIVERS = list()


def add_asset(item: Asset, results: list[Result], turbo: bool = False) -> list[Result]:
    for result in results:
        item_to_add = deepcopy(item)
        item_to_add.is_turbo = turbo
        result.add_asset(item_to_add)
    return deepcopy(results)


def get_best_results(a: list[Result], b: list[Result]) -> list[Result]:
    results = a + b
    results = [r for r in results if r.is_complete and not r.price > BUDGET]
    return deepcopy(sorted(results, key=lambda r: r.score, reverse=True)[:MEGAMAX_LIMIT])


def find_results(remaining_budget: float,
                 remaining_constructor: int, remaining_drivers: int,
                 constructor_idx: int = 0, driver_idx: int = 0,
                 td_picked: bool = False) -> list[Result]:
    must_pick_constructor = remaining_constructor > 0
    must_pick_driver = not must_pick_constructor and remaining_drivers > 0
    if not remaining_budget > 0:
        return deepcopy([Result(score=0, price=0)])

    if must_pick_constructor and constructor_idx < len(CONSTRUCTORS):
        constructor = CONSTRUCTORS[constructor_idx]
        with_picked = add_asset(constructor,
                                find_results(remaining_budget=remaining_budget - constructor.price,
                                             remaining_constructor=remaining_constructor - 1,
                                             remaining_drivers=remaining_drivers,
                                             constructor_idx=constructor_idx + 1,
                                             driver_idx=driver_idx,
                                             td_picked=td_picked))
        without_picked = find_results(remaining_budget=remaining_budget,
                                      remaining_constructor=remaining_constructor,
                                      remaining_drivers=remaining_drivers,
                                      constructor_idx=constructor_idx + 1,
                                      driver_idx=driver_idx,
                                      td_picked=td_picked)
        return get_best_results(with_picked, without_picked)

    if must_pick_driver and driver_idx < len(DRIVERS):
        driver = DRIVERS[driver_idx]
        with_picked = add_asset(driver,
                                find_results(remaining_budget=remaining_budget - driver.price,
                                             remaining_constructor=remaining_constructor,
                                             remaining_drivers=remaining_drivers - 1,
                                             constructor_idx=constructor_idx,
                                             driver_idx=driver_idx + 1,
                                             td_picked=td_picked))
        if not td_picked and driver.price < 20.:
            with_td_picked = add_asset(driver,
                                       find_results(remaining_budget=remaining_budget - driver.price,
                                                    remaining_constructor=remaining_constructor,
                                                    remaining_drivers=remaining_drivers - 1,
                                                    constructor_idx=constructor_idx,
                                                    driver_idx=driver_idx + 1,
                                                    td_picked=True),
                                       turbo=True)
            with_picked = with_picked + with_td_picked
        without_picked = find_results(remaining_budget=remaining_budget - driver.price,
                                      remaining_constructor=remaining_constructor,
                                      remaining_drivers=remaining_drivers,
                                      constructor_idx=constructor_idx,
                                      driver_idx=driver_idx + 1,
                                      td_picked=td_picked)
        return with_picked + without_picked

    return deepcopy([Result(score=0, price=0)])


if __name__ == '__main__':
    data = fetch()
    number_of_rounds = None
    for d in data.players:
        number_of_rounds = len(d.season_prices) if number_of_rounds is None else number_of_rounds
        streak = 0.
        if d.is_constructor:
            streak += STREAK_R if d.streak_events_progress.top_ten_in_a_row_race_progress == STREAK_CONSTRUCTOR - 1 else 0.
            streak += STREAK_Q if d.streak_events_progress.top_ten_in_a_row_qualifying_progress == STREAK_CONSTRUCTOR - 1 else 0.
        else:
            streak += STREAK_R if d.streak_events_progress.top_ten_in_a_row_race_progress == STREAK_DRIVER - 1 else 0.
            streak += STREAK_Q if d.streak_events_progress.top_ten_in_a_row_qualifying_progress == STREAK_DRIVER - 1 else 0.
        asset = Asset(
            is_constructor=d.is_constructor,
            is_driver=not d.is_constructor,
            name=d.team_abbreviation if d.is_constructor else d.last_name[:3].upper(),
            score=d.season_score,
            streak=streak,
            number_of_rounds=number_of_rounds,
            price=d.price
        )
        if d.is_constructor:
            CONSTRUCTORS.append(asset)
        else:
            DRIVERS.append(asset)

    sorted(CONSTRUCTORS, key=lambda c: c.predicted_score, reverse=True)
    sorted(DRIVERS, key=lambda d: d.predicted_score, reverse=True)

    teams = find_results(BUDGET, 1, 5)
    for result in teams:
        print(result)
