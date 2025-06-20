import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

import subprocess

servidor = subprocess.Popen(["python", "main.py"])

time.sleep(5)

def digitar_lento(elemento, texto, delay=0.1):
    for letra in texto:
        elemento.send_keys(letra)
        time.sleep(delay)

def test_e2e_ui_integracao():
    options = Options()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.maximize_window()
    driver.get("http://localhost:5000/")

    time.sleep(2)
    botao_cadastrar =  driver.find_element(By.LINK_TEXT, "Cadastre-se")
    botao_cadastrar.click()

    time.sleep(2)
    digitar_lento(driver.find_element(By.ID, "nome"), "Hanna Soares")
    digitar_lento(driver.find_element(By.ID, "email"), "hannasoaresc@gmail.com")
    digitar_lento(driver.find_element(By.ID, "senha"), "hanna123")  
    digitar_lento(driver.find_element(By.ID, "confirmsenha"), "hanna123")
    driver.find_element(By.ID, "cadastroForm").submit()  

    time.sleep(2)
    alert = Alert(driver)
    alert.accept()
    time.sleep(2)
    digitar_lento(driver.find_element(By.ID, "email"), "hannasoaresc@gmail.com")
    digitar_lento(driver.find_element(By.ID, "senha"), "hanna123")
    driver.find_element(By.ID, "mostrarSenha").click()
    time.sleep(1)
    driver.find_element(By.ID, "loginForm").submit()
    alert = Alert(driver)
    time.sleep(2)       
    alert.accept()

    assert driver.find_element(By.LINK_TEXT, "Catálogo").is_displayed()
    time.sleep(2)
    slider_container = driver.find_element(By.ID, "slider-lancamentos").find_element(By.XPATH, "..")
    seta_direita = slider_container.find_element(By.CSS_SELECTOR, ".slider-arrow.right")
    seta_direita.click()
    time.sleep(1)
    seta_direita.click()
    time.sleep(2)

    seta_esquerda = slider_container.find_element(By.CSS_SELECTOR, ".slider-arrow.left")
    seta_esquerda.click()
    time.sleep(1)
    seta_esquerda.click()
    time.sleep(2)
    
    botao_pesquisa = driver.find_element(By.ID, "search-btn")
    ActionChains(driver).double_click(botao_pesquisa).perform()
    time.sleep(2) 
    campo_pesquisa = WebDriverWait(driver, 3).until(
    EC.element_to_be_clickable((By.ID, "search-input")))

    campo_pesquisa.click() 
    digitar_lento(driver.find_element(By.ID, "search-input"), "godzilla 2")

    # ...existing code...

    # Após pesquisar "godzilla 2"
    time.sleep(1)
    cards = driver.find_elements(By.CLASS_NAME, "card")
    primeiro_card_visivel = next(card for card in cards if card.is_displayed())
    fav_btn = primeiro_card_visivel.find_element(By.CLASS_NAME, "btn-fav")
    ActionChains(driver).move_to_element(fav_btn).click().perform()
    time.sleep(1)
    
    campo_pesquisa.clear()
    digitar_lento(driver.find_element(By.ID, "search-input"), "vinga")
    time.sleep(2)
    
    cards = driver.find_elements(By.CLASS_NAME, "card")
    segundo_card_visivel = next(card for card in cards if card.is_displayed())
    fav_btn2 = segundo_card_visivel.find_element(By.CLASS_NAME, "btn-fav")
    ActionChains(driver).move_to_element(fav_btn2).click().perform()
    time.sleep(1)


    campo_pesquisa.clear()
    campo_pesquisa.send_keys(" ")  # Envia espaço
    campo_pesquisa.send_keys("\b")
    time.sleep(1)  
    time.sleep(5)
    tab_favoritar = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="#favorito"]')))
    tab_favoritar.click()
    assert "Meus Favoritos" in driver.page_source
    time.sleep(2)
    cards_favoritos = driver.find_elements(By.CLASS_NAME, "card")
    primeiro_card_teste = next(card for card in cards_favoritos if card.is_displayed())
    expand_btn_favorito = primeiro_card_teste.find_element(By.CLASS_NAME, "expand-btn")
    ActionChains(driver).move_to_element(expand_btn_favorito).perform()
    time.sleep(1)
    expand_btn_favorito.click()
    time.sleep(6)
    modal_content = driver.find_element(By.CLASS_NAME, "modal-content")
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal_content)
    time.sleep(4)
    driver.execute_script("arguments[0].scrollTop = 0", modal_content)
    time.sleep(1)
    
    close_btn = modal_content.find_element(By.CLASS_NAME, "close-button")
    close_btn.click()
    time.sleep(2)
    tab_categorias = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="#categorias"]')))
    tab_categorias.click()

    time.sleep(2)
    select_genero = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "selecionarGenero")))

    select = Select(select_genero)
    select.select_by_visible_text("Ação")
    time.sleep(2)

 
    select.select_by_visible_text("Fantasia")
    time.sleep(2)   
    cards_fantasia = driver.find_elements(By.CLASS_NAME, "card")
    cards_visiveis_fantasia = [card for card in cards_fantasia if card.is_displayed()]
    assert len(cards_visiveis_fantasia) > 0, "Nenhum filme de Fantasia foi exibido!"

    botao_sair = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Sair"))
    )
    botao_sair.click()
    time.sleep(2)
    assert "Digite o seu e-mail para continuar" in driver.page_source
    driver.quit()