import requests

def fetch_cep_data(cep):
    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url)
    if response.status_code == 200:
        print("Resposta da API ViaCEP:")
        print(response.json())
    else:
        print(f"Erro ao acessar API: {response.status_code}")

if __name__ == "__main__":
    cep = "81010200"
    fetch_cep_data(cep)
