from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

import csv
import time
import datetime

# Nesse código foi utilizado o selenium em sua última versão e o webdriver do Chrome (No código se encontra o Firefox comentado, mas não realizei nenhum teste com ele). Devido à políticas do LinkedIn que impossibilita o web scraping foi necessário colocar alguns time.sleep() as variáveis abaixo altera o valor de algum deles caso seja necessário

ts1 = 2
ts2 = 2
ts3 = 2
SCROLL_PAUSE_TIME = 1.5

# Define as opções do navegador  e inicia o Google Chrome

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument('--disable-infobars')
options.add_argument('--disable-notifications')
driver = webdriver.Chrome(options=options)

# Define as opções do navegador e inicia o Firefox

# options = webdriver.FirefoxOptions()
# options.add_argument('--ignore-certificate-errors')
# options.add_argument('--ignore-ssl-errors')
# options.add_argument('--disable-infobars')
# options.add_argument('--disable-notifications')
# driver = webdriver.Firefox(options=options)

url = 'https://www.linkedin.com/jobs/search'
pais = 'Br'
setor = 'Marketing e Publicidade'
# É possível aplicar outros filtros caso saiba a ID
tipo_contratacao = ['f_JT-0']
nivel_experiencia = ['f_E-0']

# Navega até a página de busca de vagas
driver.maximize_window()
driver.get(url)

# Adiciona filtro de país
country_filter = driver.find_element(By.XPATH, '//*[@id="job-search-bar-location"]')
country_filter.click()
country_filter.clear()
for char in pais:
    country_filter.send_keys(char)
    time.sleep(0.3)

time.sleep(ts2)

country_filter.send_keys(Keys.ENTER)
time.sleep(ts1)

# Adiciona filtro de setor da empresa
department_filter = driver.find_element(By.XPATH, '//*[@id="job-search-bar-keywords"]')
department_filter.click()
department_filter.clear()
for char in setor:
    department_filter.send_keys(char)
    time.sleep(0.3)

time.sleep(ts2)

# Pesquisa por país e cargo
department_filter.send_keys(Keys.ENTER)
time.sleep(ts1)

# Adiciona filtro de tipo de vaga e experiência
employment_filter = driver.find_element(By.XPATH, '//*[@id="jserp-filters"]/ul/li[4]/div/div/button')
employment_filter.click()
for tipo in tipo_contratacao:
    search_employment = driver.find_element(By.XPATH, f'//*[@id="{tipo}"]')
    search_employment.click()

time.sleep(ts2)
driver.find_element(By.XPATH, '//*[@id="jserp-filters"]/ul/li[4]/div/div/div/button').click()

time.sleep(ts3)
experience_filter = driver.find_element(By.XPATH, '//*[@id="jserp-filters"]/ul/li[5]/div/div/button')
experience_filter.click()
for nivel in nivel_experiencia:
    search_experience = driver.find_element(By.XPATH, f'//*[@id="{nivel}"]')
    search_experience.click()

time.sleep(ts2)
driver.find_element(By.XPATH, '//*[@id="jserp-filters"]/ul/li[5]/div/div/div/button').click()


# Armazena as informações das vagas em uma lista de dicionários
x = 1
jobs_list = []
horario = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
# Scrollar a página para atualizar as vagas
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    time.sleep(0.5)
    try: 
        driver.find_element(By.XPATH, f'//*[@id="main-content"]/section/ul/li[{x}]/div/a').click()
        time.sleep(2)
        try:
            job_dict = {}
            try:
                job_dict['url'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/a').get_attribute('href')
            except NoSuchElementException:
                job_dict['url'] = 'NULL'
            try:
                job_dict['titulo'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/a/h2').text
            except NoSuchElementException:
                job_dict['titulo'] = 'NULL'
            try:
                job_dict['empresa'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/h4/div[1]/span[1]/a').text
            except NoSuchElementException:
                job_dict['empresa'] = 'NULL'
            try:
                job_dict['url_empresa'] = driver.find_element(By.XPATH, '//html/body/div[1]/div/section/div[2]/section/div/div[1]/div/h4/div[1]/span[1]/a').get_attribute('href')
            except NoSuchElementException:
                job_dict['url_empresa'] = 'NULL'
            try:
                job_dict['tipo_contrato'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li[2]/span')\
                .text.split('\n')[0]
            except NoSuchElementException:
                job_dict['tipo_contrato'] = 'NULL'
            try:
                job_dict['experiencia'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li[1]/span')\
                .text.split('\n')[0]
            except NoSuchElementException:
                job_dict['experiencia']= 'NULL'
            try:
                job_dict['candidatos'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/h4/div[2]/span[2]')\
                .text.split(' ')[0]
            except NoSuchElementException:
                job_dict['candidatos'] = 'NULL'
            try:
                job_dict['postado'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/h4/div[2]/span[1]').text
            except NoSuchElementException:
                job_dict['postado'] = 'NULL'
            try:
                job_dict['horario'] = horario
            except NoSuchElementException:
                job_dict['horario'] = 'NULL'

            jobs_list.append(job_dict)
        except NoSuchElementException:
            continue
# Há no site alguns xpath diferentes por isso essa parte do código
    except NoSuchElementException:
        driver.find_element(By.XPATH, f'//*[@id="main-content"]/section/ul/li[{x}]/a').click()
        time.sleep(2)
        try:
            job_dict = {}
            try:
                job_dict['url'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/a').get_attribute('href')
            except NoSuchElementException:
                job_dict['url'] = 'NULL'
            try:
                job_dict['titulo'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/a/h2').text
            except NoSuchElementException:
                job_dict['titulo'] = 'NULL'
            try:
                job_dict['empresa'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/h4/div[1]/span[1]/a').text
            except NoSuchElementException:
                job_dict['empresa'] = 'NULL'
            try:
                job_dict['url_empresa'] = driver.find_element(By.XPATH, '//html/body/div[1]/div/section/div[2]/section/div/div[1]/div/h4/div[1]/span[1]/a').get_attribute('href')
            except NoSuchElementException:
                job_dict['url_empresa'] = 'NULL'
            try:
                job_dict['tipo_contrato'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li[2]/span')\
                .text.split('\n')[0]
            except NoSuchElementException:
                job_dict['tipo_contrato'] = 'NULL'
            try:
                job_dict['experiencia'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li[1]/span')\
                .text.split('\n')[0]
            except NoSuchElementException:
                job_dict['experiencia']= 'NULL'
            try:
                job_dict['candidatos'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/h4/div[2]/span[2]')\
                .text.split(' ')[0]
            except NoSuchElementException:
                job_dict['candidatos'] = 'NULL'
            try:
                job_dict['postado'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/h4/div[2]/span[1]').text
            except NoSuchElementException:
                job_dict['postado'] = 'NULL'
            try:
                job_dict['horario'] = horario
            except NoSuchElementException:
                job_dict['horario'] = 'NULL'
        except NoSuchElementException:
            continue
    html = driver.find_element(By.TAG_NAME, 'html')
    html.send_keys(Keys.END)
    time.sleep(SCROLL_PAUSE_TIME)
    try:
        driver.find_element(By.XPATH, '//*[@id="main-content"]/section[2]/button').click()
        time.sleep(SCROLL_PAUSE_TIME)
    except NoSuchElementException:
        continue
    if x == int(driver.find_element(By.XPATH, '//*[@id="main-content"]/div/h1/span[1]').text): # interrompe o loop se x é igual ao número de vagas
        break

    x += 1

# Exporta os resultados para um arquivo CSV
filename = f'Scraping - Lucas Moura Alcantara.csv'
with open(filename, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['url', 'titulo', 'empresa', 'url_empresa',             'tipo_contrato','experiencia', 'candidatos', 'postado','horario'])
    writer.writeheader()
    writer.writerows(jobs_list)
f.close()

#Fecha o navegador
driver.quit()

