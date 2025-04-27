from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
import time
import subprocess

servidor = subprocess.Popen(["python", "main.py"])

time.sleep(5)
# Configuração do navegador
driver = webdriver.Chrome()
driver.get("http://localhost:5000/")

time.sleep(2)  # Espera carregar

# Realizar o login
driver.find_element(By.ID, "email").send_keys("matheusguilherme06062005@gmail.com")
time.sleep(2)
driver.find_element(By.ID, "senha").send_keys("matheusgalax")
time.sleep(2)
driver.find_element(By.ID, "loginForm").submit()
time.sleep(2)
alert = Alert(driver)
alert.accept()

time.sleep(3)  # Aguarda o redirecionamento

# Clicar no botão "Cadastrar" no menu
botao_cadastrar = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//a[@href='/cadastrarfilme']"))
)
botao_cadastrar.click()



time.sleep(2)  # Aguarda carregamento
filmes = [
    {"nome": "Homem-Aranha: Sem Volta Para Casa", "ano": "2021", "categoria": "Ação", "classificacao": "+12",
     "sinopse": "Peter Parker é desmascarado e não consegue mais separar sua vida normal dos grandes riscos de ser um super-herói. Quando ele pede ajuda ao Doutor Estranho, os riscos se tornam ainda mais perigosos, e o forçam a descobrir o que realmente significa ser o Homem-Aranha...", "nota": "9.1", 
     "imagem": "https://image.tmdb.org/t/p/original/8qBccgSj0Ru9Odm1Mjv82cxDr7l.jpg", "trailer": "https://www.youtube.com/watch?v=bHzGeci_8wc"},
    
    {"nome": "Capitão América 4", "ano": "2025", "categoria": "Ação", "classificacao": "+14",
     "sinopse": "Após se encontrar com o recém-eleito presidente dos EUA, Thaddeus Ross, Sam se vê no meio de um incidente internacional. Ele deve descobrir o motivo por trás de uma conspiração global nefasta antes que o verdadeiro gênio faça o mundo inteiro ser dominado pelo vermelho.", "nota": "7.5",
     "imagem": "https://image.tmdb.org/t/p/original/t81XT7pvqOIRwZyJ51LADDdPQ5p.jpg", "trailer": "https://www.youtube.com/watch?v=U7JG6FMoEdM"},
    
    {"nome": " Mufasa: O Rei Leão", "ano": "2024", "categoria": "Aventura", "classificacao": "+10",
     "sinopse": "Acompanhe a história épica da ascensão improvável do amado rei das Terras do Reino. Órfão e sozinho, Mufasa se perde até encontrar Taka, herdeiro de uma linhagem real. Isso dá início a uma jornada épica que testa os laços entre os dois enquanto enfrentam um inimigo mortal.", "nota": "8.8",
     "imagem": "https://image.tmdb.org/t/p/original/iMVuv6Gz5fj7vZ51IjRF3AiW87y.jpg", "trailer": "https://www.youtube.com/watch?v=3H9IG_4liiI"},
    
    {"nome": "A Bela e a Fera", "ano": "2017", "categoria": "Fantasia", "classificacao": "+10",
     "sinopse": "Moradora de uma pequena aldeia francesa, Bela tem o pai capturado pela Fera e decide entregar sua vida ao estranho ser em troca da liberdade do progenitor. No castelo ela conhece objetos mágicos e descobre que a Fera é na verdade um príncipe que precisa de amor para voltar à forma humana.", "nota": "7,6",
     "imagem": "https://image.tmdb.org/t/p/original/sMw1k27BDUGpLjYiQ6f2Edx3Df5.jpg", "trailer": "https://www.youtube.com/watch?v=yzHuQPgO3Gs"},
    
    {"nome": "Sempre ao Seu Lado", "ano": "2009", "categoria": "Drama", "classificacao": "livre",
     "sinopse": "Um gênio da computação invade sistemas secretos do governo.", "nota": "9.0",
     "imagem": "https://image.tmdb.org/t/p/original/jVTFkYhlbW7P3YxoA2rsF10nx2T.jpg", "trailer": "https://www.youtube.com/watch?v=UFY8vW5IedY"}
]

#  Cadastrar filmes da lista
for filme in filmes:
    driver.find_element(By.ID, "nome").send_keys(filme["nome"])
    time.sleep(1)
    driver.find_element(By.ID, "ano").send_keys(filme["ano"])
    time.sleep(0.5)
    driver.find_element(By.ID, "categoria").send_keys(filme["categoria"])
    time.sleep(1)
    # Selecionar a classificação indicativa no menu suspenso
    campo_classificacao = Select(driver.find_element(By.ID, "classificacao"))
    campo_classificacao.select_by_value(filme["classificacao"])  
    
    driver.find_element(By.ID, "sinopse").send_keys(filme["sinopse"])
    time.sleep(2)
    driver.find_element(By.ID, "nota").send_keys(filme["nota"])
    time.sleep(0.5)
    driver.find_element(By.ID, "imagem").send_keys(filme["imagem"])
    time.sleep(2)
    driver.find_element(By.ID, "trailer").send_keys(filme["trailer"])
    

    # Enviar o formulário
    driver.find_element(By.XPATH, "//button[contains(text(), 'Cadastrar')]").click()

    time.sleep(2)  # Espera o alerta aparecer

    # Fecha o alerta automaticamente clicando em "OK"
    alert = Alert(driver)
    alert.accept()


    time.sleep(2)  # Aguarda antes de cadastrar o próximo filme
    
print(" Todos os filmes foram cadastrados com sucesso!")

botao_voltar = driver.find_element(By.XPATH, "//button[contains(text(), 'Voltar para o Menu')]")
botao_voltar.click()

print(" Retornando ao menu!")
time.sleep(2)


# Pesquisa os filmes Cadastrados
botao_pesquisa = driver.find_element(By.ID, "search-btn")
ActionChains(driver).double_click(botao_pesquisa).perform()
time.sleep(2)  # 🔹 Aguarda a barra de pesquisa abrir


campo_pesquisa = WebDriverWait(driver, 3).until(
    EC.element_to_be_clickable((By.ID, "search-input"))
)
campo_pesquisa.click()
for filme in filmes:
    campo_pesquisa.clear()  # 🔹 Limpa o campo antes de inserir um novo filme
    campo_pesquisa.send_keys(filme["nome"])
    time.sleep(3)  # 🔹 Aguarda a atualização automática dos resultados
    print(f" Filme '{filme['nome']}' pesquisado!")


# 🔹 Fechar o navegador
driver.quit()
servidor.terminate()