import requests
import os

url = 'http://127.0.0.1:8000/upload/'

file_path = 'image.jpeg'
output_path = 'outpath.jpeg'

with open(file_path, 'rb') as file:
    response = requests.post(url, files={'file': file})

print('Status Code:', response.status_code)
if response.status_code == 200:
    
    # Abre o arquivo em modo binário para escrita
    with open(output_path, 'wb') as f:
        f.write(response.content)
    
    print(f'Resposta salva em {output_path}')
else:
    print('Falha ao obter a resposta. Código de status:', response.status_code)
