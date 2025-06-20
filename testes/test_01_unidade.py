import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

def digitar_lento(elemento, texto, delay=0.1):
    for letra in texto:
        elemento.send_keys(letra)
        time.sleep(delay)

def test_login_cliente():
    options = Options()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.maximize_window()
    driver.get("http://localhost:5000/")
    digitar_lento(driver.find_element(By.ID, "email"), "murilindosgame@gmail.com")
    digitar_lento(driver.find_element(By.ID, "senha"), "murilin")
    driver.find_element(By.ID, "mostrarSenha").click()
    time.sleep(1)
    driver.find_element(By.ID, "loginForm").submit()
    alert = Alert(driver)
    time.sleep(2)       
    alert.accept()
    assert driver.find_element(By.LINK_TEXT, "Catálogo").is_displayed()
    time.sleep(2)
    driver.quit()

def test_login_admim_suc():
    options = Options()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.maximize_window()
    driver.get("http://localhost:5000/")
    digitar_lento(driver.find_element(By.ID, "email"), "matheusguilherme06062005@gmail.com")
    digitar_lento(driver.find_element(By.ID, "senha"), "matheusgalax25")
    driver.find_element(By.ID, "mostrarSenha").click()
    time.sleep(1)
    driver.find_element(By.ID, "loginForm").submit()
    time.sleep(2)
    alert = Alert(driver)
    alert.accept()
    assert driver.find_element(By.LINK_TEXT, "Cadastrar").is_displayed()
    time.sleep(2)
    driver.quit()

def test_login_falha():
    options = Options()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.maximize_window()
    driver.get("http://localhost:5000/")
    digitar_lento(driver.find_element(By.ID, "email"), "matheusguilherme06062005@gmaik.com")
    digitar_lento(driver.find_element(By.ID, "senha"), "senhaerrada")
    driver.find_element(By.ID, "mostrarSenha").click()
    time.sleep(1)
    driver.find_element(By.ID, "loginForm").submit()    
    time.sleep(2)
    alert = Alert(driver)
    assert  "Email ou senha incorretos. Tente novamente. " in alert.text
    time.sleep(5)
    alert.accept()
    driver.quit()


def test_CRUDadmin():
    options = Options()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.maximize_window()
    driver.get("http://localhost:5000/")
    digitar_lento(driver.find_element(By.ID, "email"), "matheusguilherme06062005@gmail.com")
    digitar_lento(driver.find_element(By.ID, "senha"), "matheusgalax25")
    driver.find_element(By.ID, "loginForm").submit()
    time.sleep(2)
    alert = Alert(driver)
    time.sleep(1)
    alert.accept()

    time.sleep(3)

    botao_cadastrar = driver.find_element(By.LINK_TEXT, "Cadastrar")
    botao_cadastrar.click()
    time.sleep(2)

    digitar_lento(driver.find_element(By.ID, "nome"), "Lilo & Stite")
    digitar_lento(driver.find_element(By.ID, "ano"), "2025")
    digitar_lento(driver.find_element(By.ID, "categoria"), "Aventura")
    campo_classificacao = driver.find_element(By.ID, "classificacao")
    campo_classificacao.send_keys("livre")
    driver.find_element(By.ID, "sinopse").send_keys("Stitch, um alienígena, chega ao planeta Terra após fugir de sua prisão e tenta se passar por um cachorro para se camuflar. As coisas mudam quando Lilo, uma travessa menina, o adota de um abrigo de animais. Juntos, eles aprendem os valores da amizade e família.")
    digitar_lento(driver.find_element(By.ID, "nota"), "7.5")
    driver.find_element(By.ID, "imagem").send_keys("https://image.tmdb.org/t/p/original/bLQN6DUNYN4NVzSY3Q53JwBRlgV.jpg")
    time.sleep(2)
    driver.find_element(By.ID, "trailer").send_keys("https://www.youtube.com/watch?v=oLnS1Ij9-Kk")
    driver.find_element(By.ID, "cadastroFilmeForm").submit()
    time.sleep(1)
    alert = Alert(driver)
    assert "Filme cadastrado com sucesso!" in alert.text
    alert.accept()

    botao_voltar = driver.find_element(By.XPATH, "//button[contains(text(), 'Voltar para o Menu')]")
    botao_voltar.click()
    time.sleep(2)

    primeiro_card = driver.find_elements(By.CLASS_NAME, "card")[0]
    expand_btn = primeiro_card.find_element(By.CLASS_NAME, "expand-btn")
    ActionChains(driver).move_to_element(expand_btn).perform()
    time.sleep(1)

    expand_btn.click()
    time.sleep(2)

    modal_content = driver.find_element(By.CLASS_NAME, "modal-content")
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal_content)
    time.sleep(1)
    btn_edit =  driver.find_element(By.ID, "btn-edit")
    ActionChains(driver).move_to_element(btn_edit).perform()
    time.sleep(1)
    btn_edit.click()
    time.sleep(1)
    driver.find_element(By.ID, "edit-title").clear()
    digitar_lento(driver.find_element(By.ID, "edit-title"), "Lilo & Stitch")
    time.sleep(1)
    
    btn_save = driver.find_element(By.ID, "save-edit")
    btn_save.click()
    time.sleep(2)
    modal_title = driver.find_element(By.ID, "modal-title")
    assert "Lilo & Stitch" in modal_title.text

    time.sleep(2)
    btn_delete = driver.find_element(By.ID, "btn-delete")
    ActionChains(driver).move_to_element(btn_delete).perform()
    time.sleep(1)
    btn_delete.click()
    time.sleep(3)

    driver.quit()

