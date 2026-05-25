import requests


def get_location_and_climate(
    latitude,
    longitude
):

    # =====================================
    # REVERSE GEOCODING
    # =====================================

    geo_url = (
        "https://nominatim.openstreetmap.org/reverse"
        f"?lat={latitude}"
        f"&lon={longitude}"
        "&format=json"
    )

    headers = {
        "User-Agent": "AGRI-AI"
    }

    geo_response = requests.get(
        geo_url,
        headers=headers
    ).json()

    address = geo_response.get(
        "address",
        {}
    )

    city = (
        address.get("city")
        or address.get("town")
        or address.get("village")
        or "Unknown"
    )

    country = address.get(
        "country",
        "Unknown"
    )

    location = f"{city}, {country}"

    # =====================================
    # OPEN METEO
    # =====================================

    weather_url = (
        "https://archive-api.open-meteo.com/v1/archive"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        "&start_date=2025-01-01"
        "&end_date=2025-12-31"
        "&daily=temperature_2m_max,"
        "temperature_2m_min,"
        "rain_sum"
        "&timezone=auto"
    )

    weather_response = requests.get(
        weather_url
    ).json()

    daily = weather_response.get(
        "daily",
        {}
    )

    max_temp = daily.get(
        "temperature_2m_max",
        []
    )

    min_temp = daily.get(
        "temperature_2m_min",
        []
    )

    rainfall = daily.get(
        "rain_sum",
        []
    )

    # =====================================
    # SAFETY CHECK
    # =====================================

    if not max_temp or not min_temp:

        return {

            "location": location,

            "climate_zone":
            "Unknown",

            "average_rainfall":
            "Unknown",

            "temperature_range":
            "Unknown",

            "seasonal_pattern":
            "Unknown"
        }

    # =====================================
    # TEMPERATURE RANGE
    # =====================================

    avg_max = round(
        sum(max_temp) / len(max_temp)
    )

    avg_min = round(
        sum(min_temp) / len(min_temp)
    )

    temperature_range = (
        f"{avg_min}-{avg_max}°C"
    )

    # =====================================
    # RAINFALL
    # =====================================

    total_rain = sum(rainfall)

    if total_rain < 300:

        rainfall_type = "Low"

    elif total_rain < 800:

        rainfall_type = "Moderate"

    else:

        rainfall_type = "High"

    # =====================================
    # CLIMATE ZONE
    # =====================================

    if total_rain < 500:

        climate_zone = "Semi-arid"

    elif total_rain < 1200:

        climate_zone = "Sub-humid"

    else:

        climate_zone = "Humid"

    # =====================================
    # SEASONAL PATTERN
    # =====================================

    seasonal_pattern = (
        "Hot summers, "
        "moderate monsoon, "
        "cool winters"
    )

    return {

        "location": location,

        "climate_zone":
        climate_zone,

        "average_rainfall":
        rainfall_type,

        "temperature_range":
        temperature_range,

        "seasonal_pattern":
        seasonal_pattern
    }