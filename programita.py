# Program to send bulk messages through WhatsApp web from an excel sheet without saving contact numbers
# Author @inforkgodara

import sqlite3
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import pandas
import openpyxl


# create a database called contacts.db and check if it already exists
conn = sqlite3.connect('contactos.db')
c = conn.cursor()

#create a table called contactosvalidos and check if it already exists with a column called numero
c.execute('''CREATE TABLE IF NOT EXISTS contactosvalidos (numero text)''')

#create a table called contactosinvalidos and check if it already exists with a column called numero
c.execute('''CREATE TABLE IF NOT EXISTS contactosinvalidos (numero text)''')

count = 0

# open the excel file
df = pandas.read_excel(r'C:\Users\Marcelo\Desktop\OngoingProjects\WhatsAppBulkMessage\seccional24.xlsx')

# create a list of numbers from the excel file
lista = df['CELULAR'].tolist()

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://web.whatsapp.com')
input("PRESIONAR ENTER UNA VEZ QUE WHATSAPP WEB YA ESTE LOGEADO Y LOS CHATS SEAN VISIBLES.")

mensaje = "Hola! Soy *Melissa Lacasa Pagani* y quiero presentarte mis propuestas como la única diputada mujer para Capital. Soy de la Lista 3, Opción 5 y me gustaría contar contigo para este 18 de diciembre. Gracias por leerme!"

# create a loop that goes through the list of numbers
for i in range(30000, len(lista)):
    # first check if the number is already in the database
    c.execute("SELECT * FROM contactosvalidos WHERE numero = ?", (lista[i],))
    if c.fetchone() is None:
        # if the number is not in the database, then it will try to send a message
        try:
            url = 'https://web.whatsapp.com/send?phone=' + lista[i]
            sent = False
            # It tries 3 times to send a message in case if there any error occurred
            driver.get(url)
            try:
                botonparaenviar = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[2]/button")))
                botonparaadjuntar = driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/div/span")
                botonparaadjuntar.click()
                sleep(1)
                botonimagen = driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/span/div/div/ul/li[1]/button/input")
                botonimagen.send_keys(r"C:\Users\Marcelo\Desktop\OngoingProjects\WhatsAppBulkMessage\meli.jpeg")
                sleep(1)
                botontexto = driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/div/div[1]/div[3]/div/div/div[2]/div[1]/div[1]/p")
                botontexto.send_keys(mensaje)    
            except Exception as e:
                print("Mensaje no pudo ser enviado a  " + lista[i])
                # insert into the database the number that could not be sent
                c.execute("INSERT INTO contactosinvalidos VALUES (?)", (lista[i],))
                conn.commit()
            else:
                sleep(2)
                botonenviado = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/div/div[2]/div[2]/div/div")
                botonenviado.click()
                sent = True
                sleep(3)
                print('Mensaje enviado: ' + lista[i])
                # insert into the database the number that was sent
                c.execute("INSERT INTO contactosvalidos VALUES (?)", (lista[i],))

                conn.commit()

                tresbotones = driver.find_elements(By.XPATH, "/html/body/div[1]/div/div/div[4]/div/header/div[3]/div/div[2]/div/div/span")
                tresbotones[0].click()

                sleep(1.5)

                eliminardiscusion = driver.find_element(By.XPATH, "/html/body/div[1]/div/span[4]/div/ul/div/div/li[7]")
                eliminardiscusion.click()

                sleep (1.5)

                eliminar = driver.find_element(By.XPATH, "/html/body/div[1]/div/span[2]/div/div/div/div/div/div/div[3]/div/div[2]")
                eliminar.click()

                sleep(2)
            count = count + 1
        except Exception as e:
            print('Mensaje no enviado a:' + lista[i] + str(e))

driver.quit()
print("Ejecutado correctamente.")

# close the database connection
conn.close()

