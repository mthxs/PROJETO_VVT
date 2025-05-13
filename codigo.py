import requests, os

api_url = os.getenv("API_URL")
api_key = os.getenv("API_KEY")
cities = [
    "Curitiba", "São Paulo", "Rio de Janeiro", "Belo Horizonte", "Brasília", 
    "Salvador", "Fortaleza", "Manaus", "Porto Alegre", "Recife", 
    "Belém", "Goiânia", "Campinas", "São Luís", "Maceió", 
    "Natal", "Teresina", "João Pessoa", "Campo Grande", "Cuiabá", 
    "Aracaju", "Florianópolis", "Macapá", "Palmas", "Boa Vista", 
    "Vitória", "Santos", "Uberlândia", "Londrina", "Ribeirão Preto"
]

for city in cities:
    request = requests.get(f"{api_url}?key={api_key}&q={city}&lang=pt")
    data = request.json()

    location = data["location"]
    current = data["current"]

    print("\n" + "="*40)
    print(f"Clima Atual: {location['name']}")
    print("="*40)
    print(f"▪ Local: {location['name']}, {location['region']} - {location['country']}")
    print(f"▪ Data/Hora: {location['localtime']}")
    print(f"▪ Condição: {current['condition']['text']}")
    print(f"▪ Temperatura: {current['temp_c']}°C (Sensação: {current['feelslike_c']}°C)")
    print(f"▪ Umidade: {current['humidity']}%")
    print(f"▪ Vento: {current['wind_kph']} km/h (Direção: {current['wind_dir']})")
    print(f"▪ Visibilidade: {current['vis_km']} km")
    print(f"▪ Pressão: {current['pressure_mb']} mb")
    print(f"▪ UV: {current['uv']}")
