import requests
from box import Box

from constants import DATA_URL, ASSETS_NUMBER


def check_assets_number(cnt) -> None:
    assert cnt == ASSETS_NUMBER, str(
        f"Wrong number of assets, "
        f"should be {ASSETS_NUMBER}, but got {cnt}"
    )


def fetch() -> Box:
    try:
        data = requests.get(DATA_URL)
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

    content = Box(data.json())
    check_assets_number(content.meta.total)

    return content
