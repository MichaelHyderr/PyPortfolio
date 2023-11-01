import requests

# -------------------------------------------

# response = requests.get(url="http://127.0.0.1:5000/all")
#
# data = response.json()
#
# print(data)

# ------------------------------------------

parameters2 = {
    "location": "Peckham"
}

response2 = requests.get(url="http://127.0.0.1:5000/search", params=parameters2)

data2 = response2.json()

print(data2)

# ------------------------------------------

# parameters3 = {
#     "name": "Roma",
#     "map_url": "https://www.google.com/maps/place/Roma+Cafe/data=!4m7!3m6!1s0x4876030deebcea39:0x799a0364a57db460!8m2!3d51.4825518!4d-0.0654481!16s%2Fg%2F1tcywx7t!19sChIJOeq87g0DdkgRYLR9pWQDmnk?authuser=0&hl=it&rclk=1",
#     "img_url": "https://lh3.googleusercontent.com/p/AF1QipM9Dz_QMkOF2da1aNLuTzS_vPvVWBnE84rZLK_G=s0",
#     "location": "Peckham",
#     "has_sockets": True,
#     "has_toilet": False,
#     "has_wifi": True,
#     "can_take_calls": False,
#     "seats": "20-30",
#     "coffee_price": "£3.15",
#     "latitude": 51.4825518,
#     "longitude": -0.0757478}
#
#
# response3 = requests.post(url="http://127.0.0.1:5000/add", json=parameters3)
# response3.raise_for_status()
# data3 = response3.json()

# ------------------------------------------