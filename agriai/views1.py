import json
import requests
from django.http import FileResponse
from .utils.report_generator import create_pdf_report
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .utils.location_climate import get_location_and_climate
from .utils.ai_analysis import generate_agri_analysis
from .utils.npk_predictor import predict_npk

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
        'home.html'
    )


# ==========================================
# ABOUT PAGE
# ==========================================

def about(request):

    return render(
        request,
        'about.html'
    )


# ==========================================
# COLLECT PAGE
# ==========================================

def collect(request):

    return render(
        request,
        'collect.html'
    )


# ==========================================
# TRIGGER ESP32 COLLECTION
# ==========================================

def trigger_collection(request):

    # --------------------------------------
    # GET MANUAL SOIL DATA
    # --------------------------------------

    soil_color = request.GET.get(
        "soil_color"
    )

    soil_texture = request.GET.get(
        "soil_texture"
    )

    soil_depth = request.GET.get(
        "soil_depth"
    )

    # --------------------------------------
    # SAVE MANUAL DATA IN SESSION
    # --------------------------------------

    request.session["soil_color"] = (
        soil_color
    )

    request.session["soil_texture"] = (
        soil_texture
    )

    request.session["soil_depth"] = (
        soil_depth
    )

    # --------------------------------------
    # ESP32 URL
    # --------------------------------------

    esp32_url = (
        "http://10.220.214.53/collect"
    )

    # --------------------------------------
    # TRIGGER ESP32
    # --------------------------------------

    try:

        response = requests.get(
            esp32_url,
            timeout=10
        )

        print("\nESP32 Triggered")
        print(response.text)

    except Exception as e:

        print("\nESP32 ERROR:")
        print(e)

    # --------------------------------------
    # REDIRECT TO PROCESSING
    # --------------------------------------

    return redirect("processing")


# ==========================================
# RECEIVE ESP32 SENSOR DATA
# ==========================================

@csrf_exempt
def receive_data(request):

    global latest_sensor_data

    if request.method == "POST":

        body = json.loads(
            request.body
        )

        latest_sensor_data = body

        print("\nESP32 DATA RECEIVED:")
        print(latest_sensor_data)

        return JsonResponse({
            "status": "success"
        })

    return JsonResponse({
        "status": "error"
    })


# ==========================================
# PROCESSING PAGE
# ==========================================

def processing(request):

    global latest_sensor_data

    print("\nLATEST SENSOR DATA:")
    print(latest_sensor_data)

    # =====================================
    # SENSOR DATA
    # =====================================

    moisture = latest_sensor_data.get(
        "moisture"
    )

    ph = latest_sensor_data.get(
        "pH"
    )

    tds = latest_sensor_data.get(
        "tds"
    )

    latitude = latest_sensor_data.get(
        "latitude"
    )

    longitude = latest_sensor_data.get(
        "longitude"
    )

    # =====================================
    # CLIMATE DATA
    # =====================================

    climate_data = {}

    if latitude and longitude:

        climate_data = (
            get_location_and_climate(
                latitude,
                longitude
            )
        )

    print("\nCLIMATE DATA:")
    print(climate_data)

    # =====================================
    # COMBINED DATA
    # =====================================

    combined_data = {

        # ---------------------------------
        # MANUAL SOIL DATA
        # ---------------------------------

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

        # ---------------------------------
        # SENSOR DATA
        # ---------------------------------

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

        # ---------------------------------
        # CLIMATE DATA
        # ---------------------------------

        "location":
        climate_data.get(
            "location"
        ),

        "climate_zone":
        climate_data.get(
            "climate_zone"
        ),

        "average_rainfall":
        climate_data.get(
            "average_rainfall"
        ),

        "temperature_range":
        climate_data.get(
            "temperature_range"
        ),

        "seasonal_pattern":
        climate_data.get(
            "seasonal_pattern"
        ),
    }

    # =====================================
    # SAVE EVERYTHING IN SESSION
    # =====================================

    request.session[
        "combined_data"
    ] = combined_data

    print("\nCOMBINED DATA:")
    print(combined_data)

    # =====================================
    # SEND TO FRONTEND
    # =====================================

    return render(
        request,
        "processing.html",
        combined_data
    )


# ==========================================
# AI ANALYSIS RESULT PAGE
# ==========================================

def result(request):

    global latest_sensor_data

    # =========================
    # SENSOR
    # =========================

    moisture = latest_sensor_data.get("moisture")

    ph = latest_sensor_data.get("pH")

    tds = latest_sensor_data.get("tds")

    latitude = latest_sensor_data.get("latitude")

    longitude = latest_sensor_data.get("longitude")

    # =========================
    # CLIMATE
    # =========================

    climate_data = get_location_and_climate(
        latitude,
        longitude
    )

    # =========================
    # NPK PREDICTION
    # =========================

    npk_data = predict_npk(
        moisture,
        ph,
        tds,
        request.session.get("soil_texture")
    )

    # =========================
    # COMBINED DATA
    # =========================

    combined_data = {

        # SOIL

        "soil_color":
        request.session.get("soil_color"),

        "soil_texture":
        request.session.get("soil_texture"),

        "soil_depth":
        request.session.get("soil_depth"),

        # SENSOR

        "moisture": moisture,
        "ph": ph,
        "tds": tds,

        # CLIMATE

        "location":
        climate_data.get("location"),

        "climate_zone":
        climate_data.get("climate_zone"),

        "average_rainfall":
        climate_data.get("average_rainfall"),

        "temperature_range":
        climate_data.get("temperature_range"),

        "seasonal_pattern":
        climate_data.get("seasonal_pattern"),

        # NPK

        "nitrogen":
        npk_data.get("nitrogen"),

        "phosphorus":
        npk_data.get("phosphorus"),

        "potassium":
        npk_data.get("potassium"),
    }

    # =========================
    # AI REPORT
    # =========================
    

    report = generate_agri_analysis(
        combined_data
    )
    
    request.session["latest_report"] = report
    
    context = {

        "report": report,

        **combined_data
    }

    return render(
        request,
        "result.html",
        context
    )

def download_report(request):

    report = request.session.get(
        "latest_report"
    )

    filename = "soil_report.pdf"

    create_pdf_report(
        report,
        filename
    )

    return FileResponse(
        open(filename, "rb"),
        as_attachment=True
    )