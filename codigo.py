import requests, os

api_url = os.getenv("API_URL")
api_key = os.getenv("API_KEY")
cities = [
    "Aracaju", "Belém", "Belo Horizonte", "Boa Vista", "Brasília",
    "Campinas", "Campo Grande", "Curitiba", "Cuiabá", "Florianópolis",
    "Fortaleza", "Goiânia", "João Pessoa", "Londrina", "Macapá",
    "Maceió", "Manaus", "Natal", "Palmas", "Porto Alegre",
    "Recife", "Ribeirão Preto", "Rio de Janeiro", "Salvador", "Santos",
    "São Luís", "São Paulo", "Teresina", "Uberlândia", "Vitória"
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
