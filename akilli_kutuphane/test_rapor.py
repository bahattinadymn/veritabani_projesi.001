import requests

base_url = "http://127.0.0.1:5000/api/reports"

print("--- RAPOR 1: Şu An Kimde Hangi Kitap Var? ---")
resp1 = requests.get(f"{base_url}/active-loans")
print(resp1.json())

print("\n--- RAPOR 2: En Çok Kitap Okuyanlar (Top 5) ---")
resp2 = requests.get(f"{base_url}/leaderboard")
print(resp2.json())