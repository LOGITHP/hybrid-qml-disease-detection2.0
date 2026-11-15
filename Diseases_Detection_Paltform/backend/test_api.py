from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
response = client.post('/api/v1/auth/login', data={'username': 'admin@hybridqml.com', 'password': 'admin'})
token = response.json().get('access_token')
print(client.get('/api/v1/models/defaults', headers={'Authorization': f'Bearer {token}'}).json())
