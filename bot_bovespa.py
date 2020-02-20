from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from unicodedata import normalize

driver = webdriver.Chrome()
wait_for = WebDriverWait(driver, 10)
url = 'http://www.bmfbovespa.com.br/pt_br/produtos/' \
      'listados-a-vista-e-derivativos/renda-variavel/empresas-listadas.htm'

# 1. Abra a url
driver.get(url)

# 2. Procure por "Petrobrás"
wait_for.until(ec.frame_to_be_available_and_switch_to_it((By.ID, 'bvmf_iframe')))
search_btn = driver.find_element_by_xpath('//input[contains(@class, "inputCell")]')
search_btn.click()
search_btn.send_keys('Petrobras')
search_btn.send_keys(Keys.RETURN)

# 3. Clique em "PETROLEO BRASILEIRO S.A. PETROBRAS"
result_text = 'PETROLEO BRASILEIRO S.A. PETROBRAS'
wait_for.until(ec.visibility_of_element_located((By.LINK_TEXT, result_text)))
driver.find_element_by_link_text(result_text).click()

# 4. Procure por "Balanço Patrimonial - Consolidado"
balanco_ptrm = 'Balanço Patrimonial - Consolidado'
frame = 'ctl00_contentPlaceHolderConteudo_iframeCarregadorPaginaExterna'
wait_for.until(ec.frame_to_be_available_and_switch_to_it((By.ID, frame)))
target_balanco = driver.find_element_by_xpath('//th[contains(text(), "' + balanco_ptrm + '")]')
driver.execute_script("arguments[0].scrollIntoView();", target_balanco)

# 5. Pegue os campos da tabela
column_balanco = driver.find_elements_by_xpath('//table[contains(., "' + balanco_ptrm +
                                               '")]//td[position() = 1]')
column_year_19 = driver.find_elements_by_xpath('//table[contains(., "' + balanco_ptrm +
                                               '")]//td[position() = 2]')
# 6. Construa o dicionário
results_dict = {}
for value in range(len(column_balanco)):
      format_key_string = column_balanco[value].text.split(',')[0].lower().replace(' ', '_')
      key = normalize('NFKD', format_key_string).encode('ASCII', 'ignore').decode('ASCII')
      format_value_string = round(float(column_year_19[value].text.replace('.', '')))
      results_dict[key] = format_value_string

# Resultado:
print(results_dict)
