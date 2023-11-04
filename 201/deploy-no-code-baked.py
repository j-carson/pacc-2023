import requests
from prefect import flow


@flow()
def fetch_weather(lat: float = 38.736946, lon: float = -9.142685):
    base_url = "https://api.open-meteo.com/v1/forecast/"
    weather = requests.get(
        base_url,
        params=dict(latitude=lat, longitude=lon, hourly="temperature_2m"),
    )
    most_recent_temp = float(weather.json()["hourly"]["temperature_2m"][0])
    print(f"Most recent temp C: {most_recent_temp} degrees")
    return most_recent_temp


if __name__ == "__main__":
    fetch_weather.from_source(
        source="https://github.com/discdiver/pacc-2023",
        entrypoint="deploy-no-code-baked.py:fetch_weather",
    ), deploy(
        name="lisbon-weather",
        work_pool_name="dock1",
        image="discdiver/no-code-image:1.0",
        push=False,
    )
