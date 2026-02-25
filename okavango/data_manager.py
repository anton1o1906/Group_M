from pathlib import Path
import requests
import pandas as pd

DOWNLOADS_DIR = Path("downloads")

DATASETS = {
    "annual_change_forest_area": "https://ourworldindata.org/grapher/annual-change-forest-area.csv",
    "annual_deforestation": "https://ourworldindata.org/grapher/annual-deforestation.csv",
    "share_protected_land": "https://ourworldindata.org/grapher/terrestrial-protected-areas.csv",
    "share_degraded_land": "https://ourworldindata.org/grapher/share-degraded-land.csv",
    "red_list_index": "https://ourworldindata.org/grapher/red-list-index.csv",
}


def download_csv(url: str, filename: str) -> Path:
    DOWNLOADS_DIR.mkdir(exist_ok=True)

    response = requests.get(url)
    response.raise_for_status()

    file_path = DOWNLOADS_DIR / filename
    file_path.write_bytes(response.content)
    return file_path


def download_all_datasets() -> dict[str, Path]:
    paths = {}

    for name, url in DATASETS.items():
        filename = f"{name}.csv"
        path = download_csv(url=url, filename=filename)
        paths[name] = path

    return paths


def load_datasets(paths: dict[str, Path]) -> dict[str, pd.DataFrame]:
    dataframes: dict[str, pd.DataFrame] = {}

    for name, path in paths.items():
        df = pd.read_csv(path)
        dataframes[name] = df

    return dataframes