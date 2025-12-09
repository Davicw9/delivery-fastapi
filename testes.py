import requests

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0IiwiZXhwIjoxNzY1ODU5NDc5fQ.oqvcrLnIr7w2gqfIFxjjYFTMiB5n38QRtMG4NjorvQQ"
}

requisicao = requests.post("http://127.0.0.1:8000/auth/refresh", headers=headers)
print(requisicao)
print(requisicao.json())
