from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import csv
import pandas as pd

# --------------------------------------
# usare il seguente comando su console browser nel caso si volesse freezare la pagina per analizzare determinati elementi
# setTimeout(() => { debugger; }, 5000)  si freeza dopo 5 secondi
# --------------------------------------


# Disabilito la richiesta di notifiche
firefox_options = webdriver.FirefoxOptions()
firefox_options.set_preference("dom.webnotifications.enabled", False)

browser = webdriver.Firefox(options=firefox_options)

browser.get("https://www.eurosport.it/")

# Aspetto che il pulsante accetta cookie appaia per poi cliccarlo
WebDriverWait(browser, 3).until(EC.visibility_of_element_located((By.ID, "onetrust-accept-btn-handler"))).click()
sleep(2)

# A seconda di quanto ho la pagina allargata, potrei vedere o non vedere("hidden") il pulsante "Calcio"
# Nel try tento di cliccarlo direttamente, altrimenti nell'except faccio un hover col mouse per attivare un menù a discesa e cliccarlo
try:
    WebDriverWait(browser, 3).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div/div[2]/div/div/div[1]/header/div[1]/div/div[1]/div/a[3]"))).click()
except:
    menu = browser.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div/div[1]/header/div[1]/div/div[1]/div/div/div/div/div/div")
    ActionChains(browser).move_to_element(menu).perform()
    sleep(1)
    WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex-grow > div:nth-child(2) > div:nth-child(1) > a:nth-child(1)"))).click()

# Do tempo al browser di caricare tutto
sleep(2)

# Sotto sono tutti i passaggi per individuare il pulsante da cliccare per arrivare alla classifica
WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div/div[2]/div/div/div[1]/div[2]/div/div/button[2]"))).click()

WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "ul.flex > li:nth-child(10) > a:nth-child(1)"))).click()

WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div/div[4]/div[2]/div/div/a[1]"))).click()

WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div/div[2]/div/div/div[1]/div[2]/div/div/div/ul/li[4]/a/div/div"))).click()

WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, "bg-br-2-100")))

# Ecco la classifica che è contenuta in una tabella
table = browser.find_elements(By.CLASS_NAME, "bg-br-2-100")


with open("sport_scraper.csv", mode="w", newline="") as file_csv:  # Creo il file
    writer = csv.writer(file_csv)  # preparo il csv writer
    writer.writerow(["Position", "Team", "Played", "Won", "Drawn", "Lost", "Scored", "Conceded", "Difference", "Points"])
    for row in table:  # loopo l'obj table che contiene tanti td quanti sono i teams
        team_stats = []
        tds = row.find_elements(By.TAG_NAME, "td")  # individuo tutti i td
        for td in tds:
            if td.text:  # solo alcuni td contengono testo che rappresenta le stats della classifica di ogni team
                team_stats.append(td.text)
        writer.writerow(team_stats)

df = pd.read_csv("sport_scraper.csv")

print(df)
