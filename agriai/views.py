import json
import time
import requests

from django.http import (
    FileResponse,
    JsonResponse
)

from django.shortcuts import (
    render,
    redirect
)

from django.views.decorators.csrf import (
    csrf_exempt
)

from .utils.report_generator import (
    create_pdf_report
)

from .utils.location_climate import (
    get_location_and_climate
)

from .utils.ai_analysis import (
    generate_agri_analysis
)

from .utils.npk_predictor import (
    predict_npk
)


# ==========================================
# GLOBAL SENSOR STORAGE
# ==========================================

latest_sensor_data = {}


# ==========================================
# HOME PAGE
# ==========================================

def home(request):

    return render(
        request,
        "home.html"
    )


# ==========================================
# ABOUT PAGE
# ==========================================

def about(request):

    return render(
        request,
        "about.html"
    )


# ==========================================
# COLLECT PAGE
# ==========================================

def collect(request):

    return render(
        request,
        "collect.html"
    )


# ==========================================
# TRIGGER ESP32 COLLECTION
# ==========================================

def trigger_collection(request):

    global latest_sensor_data

    # --------------------------------------
    # RESET OLD SENSOR DATA
    # --------------------------------------

    latest_sensor_data = {}

    # --------------------------------------
    # MANUAL SOIL DATA
    # --------------------------------------

    request.session["soil_color"] = (
        request.GET.get("soil_color")
    )

    request.session["soil_texture"] = (
        request.GET.get("soil_texture")
    )

    request.session["soil_depth"] = (
        request.GET.get("soil_depth")
    )

    # --------------------------------------
    # ESP32 URL
    # --------------------------------------

    esp32_url = (
        "http://10.220.214.53/collect"
    )

    try:

        print("\nTriggering ESP32...")

        response = requests.get(
            esp32_url,
            timeout=20
        )

        print("ESP32 Response:")
        print(response.text)

    except Exception as e:

        print("\nESP32 ERROR:")
        print(e)

        return render(
            request,
            "collect.html",
            {
                "error":
                "ESP32 not responding."
            }
        )

    # --------------------------------------
    # WAIT FOR SENSOR DATA
    # --------------------------------------

    print("\nWaiting for sensor data...")

    start_time = time.time()

    while True:

        if latest_sensor_data:

            print(
                "\nSensor data received!"
            )

            print(
                latest_sensor_data
            )

            break

        if time.time() - start_time > 20:

            print(
                "\nSensor timeout!"
            )

            return render(
                request,
                "collect.html",
                {
                    "error":
                    "Sensor data timeout."
                }
            )

        time.sleep(1)

    return redirect(
        "processing"
    )


# ==========================================
# RECEIVE ESP32 SENSOR DATA
# ==========================================

@csrf_exempt
def receive_data(request):

    global latest_sensor_data

    if request.method == "POST":

        try:

            body = json.loads(
                request.body
            )

            latest_sensor_data = body

            print(
                "\nESP32 DATA RECEIVED:"
            )

            print(
                latest_sensor_data
            )

            return JsonResponse({
                "status": "success"
            })

        except Exception as e:

            print(e)

            return JsonResponse({
                "status": "error"
            })

    return JsonResponse({
        "status": "invalid"
    })


# ==========================================
# PROCESSING PAGE
# ==========================================

def processing(request):

    global latest_sensor_data

    print(
        "\nLATEST SENSOR DATA:"
    )

    print(
        latest_sensor_data
    )

    # =====================================
    # SENSOR VALUES
    # =====================================

    moisture = latest_sensor_data.get(
        "moisture", 0
    )

    ph = latest_sensor_data.get(
        "pH", 0
    )

    tds = latest_sensor_data.get(
        "tds", 0
    )

    latitude = latest_sensor_data.get(
        "latitude", 0
    )

    longitude = latest_sensor_data.get(
        "longitude", 0
    )

    # =====================================
    # CLIMATE DATA
    # =====================================

    climate_data = {}

    if latitude != 0 and longitude != 0:

        try:

            climate_data = (
                get_location_and_climate(
                    latitude,
                    longitude
                )
            )

        except Exception as e:

            print(
                "\nClimate Error:"
            )

            print(e)

    print(
        "\nCLIMATE DATA:"
    )

    print(
        climate_data
    )

    # =====================================
    # FINAL DATA
    # =====================================

    combined_data = {

        "soil_color":
        request.session.get(
            "soil_color"
        ),

        "soil_texture":
        request.session.get(
            "soil_texture"
        ),

        "soil_depth":
        request.session.get(
            "soil_depth"
        ),

        "moisture":
        moisture,

        "ph":
        ph,

        "tds":
        tds,

        "latitude":
        latitude,

        "longitude":
        longitude,

        "location":
        climate_data.get(
            "location",
            "GPS unavailable"
        ),

        "climate_zone":
        climate_data.get(
            "climate_zone",
            "Unavailable"
        ),

        "average_rainfall":
        climate_data.get(
            "average_rainfall",
            "Unavailable"
        ),

        "temperature_range":
        climate_data.get(
            "temperature_range",
            "Unavailable"
        ),

        "seasonal_pattern":
        climate_data.get(
            "seasonal_pattern",
            "Unavailable"
        ),
    }

    request.session[
        "combined_data"
    ] = combined_data

    print(
        "\nCOMBINED DATA:"
    )

    print(
        combined_data
    )

    return render(
        request,
        "processing.html",
        combined_data
    )


# ==========================================
# RESULT PAGE
# ==========================================

def result(request):

    combined_data = request.session.get(
        "combined_data",
        {}
    )

    npk_data = predict_npk(
        combined_data.get(
            "moisture"
        ),
        combined_data.get(
            "ph"
        ),
        combined_data.get(
            "tds"
        ),
        combined_data.get(
            "soil_texture"
        )
    )

    combined_data.update({

        "nitrogen":
        npk_data.get(
            "nitrogen"
        ),

        "phosphorus":
        npk_data.get(
            "phosphorus"
        ),

        "potassium":
        npk_data.get(
            "potassium"
        )
    })

    report = generate_agri_analysis(
        combined_data
    )

    request.session[
        "latest_report"
    ] = report

    return render(
        request,
        "result.html",
        {
            "report": report,
            **combined_data
        }
    )


# ==========================================
# DOWNLOAD REPORT
# ==========================================

def download_report(request):

    report = request.session.get(
        "latest_report"
    )

    filename = (
        "soil_report.pdf"
    )

    create_pdf_report(
        report,
        filename
    )

    return FileResponse(
        open(filename, "rb"),
        as_attachment=True
    )