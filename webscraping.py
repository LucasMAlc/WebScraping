from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import csv
import time
import datetime


# Define as opções do navegador  e inicia o Google Chrome

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument('--disable-infobars')
options.add_argument('--disable-notifications')
driver = webdriver.Chrome(options=options)

# Define as opções do navegador  e inicia o Firefox

# options = webdriver.FirefoxOptions()
# options.add_argument('--ignore-certificate-errors')
# options.add_argument('--ignore-ssl-errors')
# options.add_argument('--disable-infobars')
# options.add_argument('--disable-notifications')
# driver = webdriver.Firefox(options=options)

url = 'https://www.linkedin.com/jobs/search'
pais = 'Br'
setor = 'Marketing e Publicidade'
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
    time.sleep(0.2)

time.sleep(1)

country_filter.send_keys(Keys.ENTER)
time.sleep(2)

# Adiciona filtro de setor da empresa
department_filter = driver.find_element(By.XPATH, '//*[@id="job-search-bar-keywords"]')
department_filter.click()
department_filter.clear()
for char in setor:
    department_filter.send_keys(char)
    time.sleep(0.3)

time.sleep(3)

# Pesquisa por país e cargo
department_filter.send_keys(Keys.ENTER)
time.sleep(2)

# Adiciona filtro de tipo de vaga e experiência
employment_filter = driver.find_element(By.XPATH, '//*[@id="jserp-filters"]/ul/li[4]/div/div/button')
employment_filter.click()
for tipo in tipo_contratacao:
    search_employment = driver.find_element(By.XPATH, f'//*[@id="{tipo}"]')
    search_employment.click()

time.sleep(1)
driver.find_element(By.XPATH, '//*[@id="jserp-filters"]/ul/li[4]/div/div/div/button').click()

time.sleep(2)
experience_filter = driver.find_element(By.XPATH, '//*[@id="jserp-filters"]/ul/li[5]/div/div/button')
experience_filter.click()
for nivel in nivel_experiencia:
    search_experience = driver.find_element(By.XPATH, f'//*[@id="{nivel}"]')
    search_experience.click()

time.sleep(4)
driver.find_element(By.XPATH, '//*[@id="jserp-filters"]/ul/li[5]/div/div/div/button').click()


# Armazena as informações das vagas em uma lista de dicionários
x = 1
jobs_list = []

time.sleep(1)
while True:
    driver.find_element(By.XPATH, f'//*[@id="main-content"]/section/ul/li[{x}]/div/a').click()
    time.sleep(5)
    try:
        job_dict = {}
        try:
            job_dict['url'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/a/h2').get_attribute('href')
        except NoSuchElementException:
            job_dict['url'] = None
        try:
            job_dict['title'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/a/h2').text
        except NoSuchElementException:
            job_dict['title'] = None
        try:
            job_dict['company'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/h4/div[1]/span[1]/a').text
        except NoSuchElementException:
            job_dict['company'] = None
        try:
            job_dict['company_url'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/a/h2').get_attribute('href')
        except NoSuchElementException:
            job_dict['company_url'] = None
        try:
            job_dict['employment_type'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li[2]/span')\
            .text.split('\n')[0]
        except NoSuchElementException:
            job_dict['employment_type'] = None
        try:
            job_dict['experience_level'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li[1]/span')\
            .text.split('\n')[0]
        except NoSuchElementException:
            job_dict['experience_level']= None
        try:
            job_dict['num_applicants'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/h4/div[2]/span[2]')\
            .text.split(' ')[0]
        except NoSuchElementException:
            job_dict['num_applicants'] = None
        try:
            job_dict['post_date'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/h4/div[2]/span[1]').text
        except NoSuchElementException:
            job_dict['post_date'] = None
        jobs_list.append(job_dict)
    except NoSuchElementException:
        continue

    # if x+1 is None: # interrompe o loop se x+1 é None
    if x == 5: # Limitei o número de vagas para 5 para o scraping ser mais rápido
        break  

    x += 1

# Exporta os resultados para um arquivo CSV
    current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f'scraping-Horario_{current_time}.csv'
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['url', 'title', 'company', 'company_url',             'employment_type','experience_level', 'num_applicants', 'post_date',])
        writer.writeheader()
        writer.writerows(jobs_list)

#Fecha o navegador
driver.quit()

