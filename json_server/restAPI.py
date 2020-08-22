import requests
import json

url_items = "http://localhost/lot/1"
response = requests.get(url_items)

print(response.text)
print(response.json()["ultrasonic"])

# Making a PATCH request 
r = requests.patch(url_items, data ={'number':'28너1818'}) 
  
# check status code for response recieved 
# success code - 200 
print(r) 
  
# print content of request 
print(r.content) 
