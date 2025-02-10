import requests
import typer
import os


app = typer.Typer()
API_KEY = os.getenv("OWM_API_KEY", Enter api)  # Use environment variable for production


def kelvin_to_celsius(kelvin: float) -> float:
    """Convert Kelvin to Celsius"""
    return kelvin - 273.15


@app.command()
def current_weather(
        lat: float = typer.Option(..., prompt="Enter the latitude", help="Latitude in decimal degrees"),
        lon: float = typer.Option(..., prompt="Enter the longitude", help="Longitude in decimal degrees")
):
    """Get current weather for given coordinates"""
    try:
        response = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}"
        )
        response.raise_for_status()
        data = response.json()

        temperature_data = data.get('main', {})
        weather_list = data.get('weather', [])


        temp_k = temperature_data.get('temp')
        temp_c = kelvin_to_celsius(temp_k) if temp_k else None
        humidity = temperature_data.get('humidity')
        name = data.get('name', 'Unknown Location')

        typer.echo(f"\nWeather details for {name} ({lat:.4f}, {lon:.4f}):")
        typer.echo(f"Temperature: {temp_c:.1f}°C ({temp_k} K)")
        typer.echo(f"Humidity: {humidity}%")

        for weather in weather_list:
            typer.echo(f"Conditions: {weather.get('main', '')} - {weather.get('description', '')}")

    except requests.exceptions.RequestException as e:
        typer.secho(f"Error fetching weather data: {e}", fg=typer.colors.RED)


@app.command()
def reverse_geocoding(
        lat: float = typer.Option(..., prompt="Enter the latitude", help="Latitude in decimal degrees"),
        lon: float = typer.Option(..., prompt="Enter the longitude", help="Longitude in decimal degrees")
):
    """Get location name from coordinates"""
    try:
        response = requests.get(
            f'http://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lon}&limit=1&appid={API_KEY}'
        )
        response.raise_for_status()
        data = response.json()

        if not data:
            typer.secho("No location found for these coordinates", fg=typer.colors.YELLOW)
            return

        location = data[0]
        typer.echo("\nLocation details:")
        typer.echo(f"Name: {location.get('name', 'N/A')}")
        typer.echo(f"State: {location.get('state', 'N/A')}")
        typer.echo(f"Country: {location.get('country', 'N/A')}")

    except requests.exceptions.RequestException as e:
        typer.secho(f"Error fetching location data: {e}", fg=typer.colors.RED)


@app.command()
def geocoding(
        location: str = typer.Argument(..., help="Location name to search for"),
        limit: int = typer.Option(5, help="Number of results to show")
):
    """Get coordinates for a location name"""
    try:
        response = requests.get(
            f'http://api.openweathermap.org/geo/1.0/direct?q={location}&limit={limit}&appid={API_KEY}'
        )
        response.raise_for_status()
        data = response.json()

        if not data:
            typer.secho("No locations found", fg=typer.colors.YELLOW)
            return

        typer.echo("\nMatching locations:")
        for idx, place in enumerate(data, 1):
            typer.echo(
                f"{idx}. {place.get('name', 'N/A')}, "
                f"{place.get('state', '')} {place.get('country', '')} "
                f"(Lat: {place.get('lat', 'N/A')}, Lon: {place.get('lon', 'N/A')})"
            )

    except requests.exceptions.RequestException as e:
        typer.secho(f"Error fetching coordinates: {e}", fg=typer.colors.RED)


@app.command()
def air_pollution(
        lat: float = typer.Option(..., prompt="Enter the latitude", help="Latitude in decimal degrees"),
        lon: float = typer.Option(..., prompt="Enter the longitude", help="Longitude in decimal degrees")
):
    """Get air pollution data for coordinates"""
    try:
        response = requests.get(
            f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
        )
        response.raise_for_status()
        data = response.json()

        aqi = data['list'][0]['main']['aqi']
        components = data['list'][0]['components']

        typer.echo("\nAir Quality Index:")
        aqi_messages = {
            1: ("Good", typer.colors.GREEN),
            2: ("Fair", typer.colors.CYAN),
            3: ("Moderate", typer.colors.YELLOW),
            4: ("Poor", typer.colors.MAGENTA),
            5: ("Very Poor", typer.colors.RED)
        }

        description, color = aqi_messages.get(aqi, ("Unknown", typer.colors.WHITE))
        typer.secho(f"AQI Level {aqi}: {description}", fg=color)

        typer.echo("\nPollutant concentrations:")
        for pollutant, value in components.items():
            typer.echo(f"{pollutant.upper()}: {value:.2f} μg/m³")

    except requests.exceptions.RequestException as e:
        typer.secho(f"Error fetching pollution data: {e}", fg=typer.colors.RED)


if __name__ == "__main__":
    typer.secho("\n🌤️  Welcome to Weather CLI! 🌦️", fg=typer.colors.BLUE, bold=True)
    app()
