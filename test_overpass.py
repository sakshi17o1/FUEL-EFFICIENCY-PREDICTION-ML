import requests

query = """
[out:json][timeout:25];
node["amenity"="fuel"](around:5000,28.6139,77.2090);
out body;
"""

try:
    response = requests.post(
        "https://overpass-api.de/api/interpreter",
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        data={"data": query},
        timeout=60
    )

    print("Status Code:", response.status_code)
    print(response.text[:500])

except Exception as e:
    print(e)