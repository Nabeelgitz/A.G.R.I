def predict_npk(moisture, ph, tds, soil_texture):

    # =========================
    # NITROGEN
    # =========================

    if moisture > 60:
        nitrogen = "Medium"

    else:
        nitrogen = "Low"

    # =========================
    # PHOSPHORUS
    # =========================

    if ph >= 6 and ph <= 7.5:
        phosphorus = "Good"

    else:
        phosphorus = "Moderate"

    # =========================
    # POTASSIUM
    # =========================

    if tds > 300:
        potassium = "High"

    else:
        potassium = "Medium"

    return {

        "nitrogen": nitrogen,
        "phosphorus": phosphorus,
        "potassium": potassium
    }