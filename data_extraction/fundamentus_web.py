from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By

options = FirefoxOptions()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
driver.get("http://fundamentus.com.br/detalhes.php?papel=IRBR3")

lucro_3m = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/table[5]/tbody/tr[5]/td[4]/span")

print(lucro_3m.text)
