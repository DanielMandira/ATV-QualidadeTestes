from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def _add_user(driver, name):
    input_name = driver.find_element(By.ID, "name")
    input_name.clear()
    input_name.send_keys(name)
    driver.find_element(By.ID, "submit").click()


def _get_user_texts(driver):
    return [user.text for user in driver.find_elements(By.CSS_SELECTOR, "#users li")]


def test_create_user_e2e(driver, live_server):
    driver.get(live_server)

    _add_user(driver, "Maylon")

    wait = WebDriverWait(driver, 5)
    wait.until(EC.text_to_be_present_in_element((By.ID, "users"), "Maylon"))

    assert "Maylon" in _get_user_texts(driver)


def test_create_two_users_and_verify_list_e2e(driver, live_server):
    driver.get(live_server)

    _add_user(driver, "Usuario Um")
    _add_user(driver, "Usuario Dois")

    wait = WebDriverWait(driver, 5)
    wait.until(lambda d: len(_get_user_texts(d)) == 2)

    user_texts = _get_user_texts(driver)
    assert "Usuario Um" in user_texts
    assert "Usuario Dois" in user_texts


def test_duplicate_user_not_added_e2e(driver, live_server):
    driver.get(live_server)

    _add_user(driver, "Ana")
    _add_user(driver, "Ana")

    wait = WebDriverWait(driver, 5)
    wait.until(lambda d: len(_get_user_texts(d)) == 1)

    assert _get_user_texts(driver) == ["Ana"]


def test_blank_name_not_added_e2e(driver, live_server):
    driver.get(live_server)

    driver.find_element(By.ID, "submit").click()

    wait = WebDriverWait(driver, 2)
    wait.until(lambda d: len(_get_user_texts(d)) == 0)
