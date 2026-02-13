# =========================
# Bangladesh News Mapping Pipeline
# =========================

# Install dependencies first:
# pip install langchain openai geojson requests beautifulsoup4

from langchain.document_loaders import WebBaseLoader
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import geojson

# -------------------------
# 1. Configuration
# -------------------------
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"
ARTICLE_URL = "https://www.dailystar.net/news/bangladesh/news/sharsha-waiting-the-border-breathe-again-4092116"

# Coordinates mapping for locations (manual or from a geocoding API)
LOCATION_COORDS = {
    "Sharsha, Bangladesh": (23.37, 89.15)
}

# -------------------------
# 2. Load Article
# -------------------------
loader = WebBaseLoader(ARTICLE_URL)
documents = loader.load()  # returns list of documents
article_text = documents[0].page_content

# -------------------------
# 3. Set up LLM
# -------------------------
llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)

prompt = PromptTemplate(
    input_variables=["article_text"],
    template="""
You are a news analyst. Extract the following from the article and output JSON:
1. title
2. short_summary (3-5 sentences)
3. date_of_event (if available)
4. locations mentioned
5. type_of_event (political, social, violence, economic, etc.)

Article:
{article_text}

Output JSON:
"""
)

chain = LLMChain(llm=llm, prompt=prompt)

# -------------------------
# 4. Summarize and Extract Metadata
# -------------------------
import json

result_text = chain.run(article_text=article_text)

try:
    result_json = json.loads(result_text)
except json.JSONDecodeError:
    # fallback: print raw output
    print("LLM output could not be parsed as JSON:")
    print(result_text)
    result_json = None

# -------------------------
# 5. Convert to GeoJSON
# -------------------------
if result_json:
    features = []
    for loc in result_json.get("locations", []):
        coords = LOCATION_COORDS.get(loc)
        if coords:
            feature = geojson.Feature(
                geometry=geojson.Point(coords),
                properties={
                    "title": result_json.get("title", ""),
                    "summary": result_json.get("short_summary", ""),
                    "date": result_json.get("date_of_event", ""),
                    "type": result_json.get("type_of_event", "")
                }
            )
            features.append(feature)

    feature_collection = geojson.FeatureCollection(features)

    # Save GeoJSON
    with open("bangladesh_news.geojson", "w") as f:
        geojson.dump(feature_collection, f, indent=2)

    print("✅ GeoJSON saved as bangladesh_news.geojson")
else:
    print("No valid data to create GeoJSON.")
