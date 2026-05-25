import google.generativeai as genai


genai.configure(
    api_key="********************************"
)

model = genai.GenerativeModel(
    'gemini-flash-latest'
)

# =====================================
# MAIN ANALYSIS FUNCTION
# =====================================

def generate_agri_analysis(data):

    prompt = f"""
    IMPORTANT OUTPUT FORMAT RULES

Generate the report in clean structured plain text.

Formatting Rules:
- Use numbered sections only.
- Use section titles like:
  1. Soil Classification
  2. Soil Nature
  3. Fertility Analysis
- Use simple bullet points with "-"
- Keep spacing clean and professional.
- Do not use markdown.
- Do not use HTML tags.
- Do not use **bold**
- Do not use tables
- Do not use special formatting syntax.
- Write in professional agricultural report format.
- Keep paragraphs readable for PDF generation.
- Use farmer-friendly but scientific explanations.

You are an advanced agricultural scientist,
soil microbiologist,
climate analyst,
crop specialist,
fertilizer expert,
and pest management advisor.

IMPORTANT OUTPUT RULES:

- Do NOT use markdown syntax.
- Do NOT use ### headings.
- Do NOT use **bold** text.
- Do NOT use tables using | |
- Use clean structured plain text.
- Keep sections clearly separated.
- Use numbered sections.
- Use readable farmer-friendly formatting.
- Keep spacing professional for PDF generation.

Generate a highly detailed professional
agricultural intelligence report.

========================
LOCATION & CLIMATE
========================

Location: {data.get("location")}

Climate Zone: {data.get("climate_zone")}

Rainfall: {data.get("average_rainfall")}

Temperature Range: {data.get("temperature_range")}

Seasonal Pattern:
{data.get("seasonal_pattern")}

========================
SOIL INFORMATION
========================

Soil Color:
{data.get("soil_color")}

Soil Texture:
{data.get("soil_texture")}

Soil Depth:
{data.get("soil_depth")}

========================
SENSOR DATA
========================

Moisture:
{data.get("moisture")}

pH:
{data.get("ph")}

TDS:
{data.get("tds")}

========================
NPK PREDICTION
========================

Nitrogen:
{data.get("nitrogen")}

Phosphorus:
{data.get("phosphorus")}

Potassium:
{data.get("potassium")}

========================
OUTPUT FORMAT
========================

Generate sections:

1. Soil Classification
2. Soil Nature
3. Fertility Analysis
4. Nutrient Deficiency
5. Water Retention
6. Kharif Crops
7. Rabi Crops
8. Zaid Crops
9. Unsuitable Crops
10. Organic Fertilizers
11. Chemical Fertilizers
12. Irrigation Strategy
13. Pest Risks
14. Pest Prevention
15. Long-Term Improvement
17. climate and weather (considerations very very very important)
16. Final Conclusion

VERY IMPORTANT:

- Write highly detailed scientific explanations
- Use professional agricultural language
- Explain WHY every crop is recommended
- Explain WHY crops are unsuitable
- Include regional agricultural logic
- Mention possible fungal and pest threats
- Include irrigation logic
- Mention soil chemistry behavior
- Use proper headings
- Make report extremely detailed

IMPORTANT OUTPUT FORMAT RULES:

Generate the complete report in CLEAN HTML FORMAT.

STRICT REQUIREMENTS:

1. Use semantic HTML formatting.
2. Use:
   - <h1> for report title
   - <h2> for major sections
   - <h3> for sub-sections
   - <p> for paragraphs
   - <ul> and <li> for recommendations
   - <b> for important findings
   - <i> where needed
3. Keep spacing clean and professional.
4. Make output PDF-friendly.
5. No markdown syntax.
6. No code block formatting.
7. No ```html tags.
8. Return ONLY valid HTML body content.
9. Keep report visually structured and professional.
10. Use farmer-friendly but scientific language.

The report should look like a professional agricultural consultancy report.

"""

    response = model.generate_content(prompt)

    return response.text