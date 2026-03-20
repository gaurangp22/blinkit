import requests

BASE_URL = "http://localhost:8080"

endpoints = [
    ("GET", "/"),
    ("GET", "/api/category/get"),
    ("POST", "/api/subcategory/get"),
    ("POST", "/api/product/get"),
    ("GET", "/api/cart/get"),
    ("GET", "/api/order/order-list"),
    ("GET", "/api/address/get"),
    ("POST", "/api/user/login"),
]

print(f"Testing endpoints on {BASE_URL}...\n")

for method, path in endpoints:
    url = BASE_URL + path
    try:
        if method == "GET":
            response = requests.get(url)
        else:
            response = requests.post(url, json={})
            
        print(f"[{method}] {path} -> Status: {response.status_code}")
    except Exception as e:
        print(f"[{method}] {path} -> ERROR: {e}")

print("\nEndpoint testing complete.")
