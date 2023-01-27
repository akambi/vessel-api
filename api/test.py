import requests

base = "http://127.0.0.1:5000/"

response = requests.post(
    base + "vessels/positions",
    {
        "vessel_id": "5291",
        "received_time_utc": "2017-12-20 22:59:12.000000",
        "latitude": "30.496170",
        "longitude": "123.838630"
    }
)

print('---- Test insert of valid position -----')
print(response.json())
print('---- New vessel position inserted -----')

response = requests.post(
    base + "vessels/positions",
    {
        "vessel_id": "a5291xxxxx",
        "received_time_utc": "2017-12-20 22:59:12.000000",
        "latitude": "30.496170",
        "longitude": "123.838630"
    }
)

print('---- Test insert of invalid position -----')
print(response.json())

response = requests.post(
    base + "vessels/positions",
    {
        "vessel_id": "5213",
        "received_time_utc": "aaaaa",
        "latitude": "30.496170",
        "longitude": "123.838630"
    }
)

print('---- Test insert of invalid position -----')
print(response.json())

response = requests.post(
    base + "vessels/positions",
    {
        "vessel_id": "123ddd",
        "received_time_utc": "aaaaa",
        "latitude": "abc",
        "longitude": "123.838630"
    }
)

print('---- Test insert of invalid position -----')
print(response.json())