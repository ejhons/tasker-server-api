import requests

#graças ao uso do OAuth2, precisamos que toda requisição que acessa rotas em que o usuário precisa estar logado precisa ter o Header abaixo.
headers={
    'Authorization':'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwiZXhwIjoxNzcwMDg0MzMyfQ.8voRPNLDJ5FEK5dTZ1yWW-hZCbo8DlzVevnGF__ZImY',
}

requisicao = requests.get('http://127.0.0.1:8000/auth/refresh', headers=headers)
print(requisicao)
print(requisicao.json())