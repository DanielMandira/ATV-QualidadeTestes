from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_create_user_e2e():
    driver = webdriver.Chrome()
    driver.get("http://localhost:5000")
    
    input_name = driver.find_element(By.ID, "name")
    input_name.send_keys("Maylon")
    
    button = driver.find_element(By.ID, "submit")
    button.click()
    
    time.sleep(1)
    
    users = driver.find_elements(By.TAG_NAME, "li")
    
    assert any("Maylon" in user.text for user in users)
    
    driver.quit()

def test_create_two_users_and_verify_list_e2e():
    driver = webdriver.Chrome()
    driver.get("http://localhost:5000")
    wait = WebDriverWait(driver, 10)

    # Usuário 1
    input_name1 = driver.find_element(By.ID, "name")
    input_name1.send_keys("Usuario Um")
    button1 = driver.find_element(By.ID, "submit")
    button1.click()

    # Espera o primeiro usuário aparecer na lista
    wait.until(EC.presence_of_element_located((By.XPATH, "//li[contains(text(), 'Usuario Um')]")))

    # Usuário 2
    input_name2 = driver.find_element(By.ID, "name")
    input_name2.send_keys("Usuario Dois")
    button2 = driver.find_element(By.ID, "submit")
    button2.click()

    # Espera o segundo usuário aparecer na lista
    wait.until(EC.presence_of_element_located((By.XPATH, "//li[contains(text(), 'Usuario Dois')]")))

    # Valida se os dois usuários estão na lista
    users_list = driver.find_element(By.ID, "user-list")
    users = users_list.find_elements(By.TAG_NAME, "li")
    user_texts = [user.text for user in users]

    assert "Usuario Um" in user_texts
    assert "Usuario Dois" in user_texts

    driver.quit()
    