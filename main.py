import requests
import fitz  # PyMuPDF
from PIL import Image
import os
from datetime import datetime
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def create_output_folder(base_folder):
    # Erstelle einen Ordner mit dem aktuellen Datum als Namen
    current_date = datetime.now().strftime("%Y-%m-%d")
    output_folder = os.path.join(base_folder, current_date)

    os.makedirs(output_folder, exist_ok=True)
    return output_folder

def pdf_to_images(pdf_path, base_output_folder, resolution=300):
    # Öffne das PDF
    pdf_document = fitz.open(pdf_path)

    # Erstelle den Ausgabeordner mit aktuellem Datum
    output_folder = create_output_folder(base_output_folder)

    # Durchlaufe alle Seiten des PDFs
    for page_number in range(pdf_document.page_count):
        # Lese die Seite ein
        page = pdf_document.load_page(page_number)

        # Erhöhe die Auflösung beim Erstellen des Pixmaps
        image = page.get_pixmap(matrix=fitz.Matrix(resolution / 72.0, resolution / 72.0))

        # Konvertiere die PDF-Seite in ein Bild
        image = Image.frombytes("RGB", [image.width, image.height], image.samples)

        # Erstelle einen Dateipfad für das Bild im Unterordner mit dem aktuellen Datum
        image_path = os.path.join(output_folder, f"{page_number + 1}.png")

        # Speichere das Bild
        image.save(image_path)

    # Schließe das PDF-Dokument
    pdf_document.close()

def process_images(folder):
    # Durchlaufe alle Dateien im Ordner
    for filename in os.listdir(folder):
        if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            # Lese das Bild ein
            image_path = os.path.join(folder, filename)
            original_image = Image.open(image_path)

            # Bestimme die Größe des abzuschneidenden Bereichs
            width, height = original_image.size
            top_cut = int(0.6 * height)
            bottom_cut = int(0.111 * height)
            left_cut = int(0.37 * width)
            right_cut = int(0.37 * width)

            # Schneide den gewünschten Bereich ab
            cropped_image = original_image.crop((left_cut, top_cut, width - right_cut, height - bottom_cut))

            # Speichere das modifizierte Bild im selben Ordner
            output_path = os.path.join(folder, f"WelcomeCard_{filename}")
            cropped_image.save(output_path)

            # Lösche das ursprüngliche Bild
            os.remove(image_path)


def open_browser_and_login(url, username, password):
    # Pfad zu deinem ChromeDriver
    chromedriver_path = r'C:\Users\gkuen\PycharmProjects\GuestcardProgramm\chromedriver-win64\chromedriver.exe'  # Ersetze durch den tatsächlichen Pfad
    driver = webdriver.Chrome(executable_path=chromedriver_path)

    # Navigiere zur URL
    driver.get(url)

    # Warte, bis die Seite vollständig geladen ist
    time.sleep(2)

    # Finde das Benutzername- und Passwortfeld und gib die Werte ein
    username_field = driver.find_element_by_name("UserName")  # Passe an den tatsächlichen Namen des Feldes an
    password_field = driver.find_element_by_name("Password")  # Passe an den tatsächlichen Namen des Feldes an

    username_field.send_keys(username)
    password_field.send_keys(password)

    # Optional: Drücke die Eingabetaste oder klicke auf den Login-Button
    password_field.send_keys(Keys.RETURN)

    print("Navigiere zur PDF der WelcomeCards und schließe dann ale anderen Tabs\n")
    input("Drücke Enter, um den Browser zu schließen und die WelcomeCards zu erstellen...")

    current_url = driver.current_url
    # Schließe den Browser, wenn Enter gedrückt wird
    driver.quit()

    return current_url


def download_pdf_from_url(pdf_url, save_path):
    try:
        # PDF von der URL herunterladen
        response = requests.get(pdf_url)

        # Überprüfen, ob die Anfrage erfolgreich war
        if response.status_code == 200:
            # Inhalt des PDFs speichern
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print(f"PDF wurde erfolgreich heruntergeladen und unter {save_path} gespeichert.")
        else:
            print("Fehler beim Herunterladen des PDFs: Status Code", response.status_code)
    except Exception as e:
        print("Fehler beim Herunterladen des PDFs:", str(e))


if __name__ == "__main__":

    # Dieser CodeBlock ist für die Browser Interaktion verandtwortlich

    url = "https://webclient4.deskline.net/IBK/de/login?dbOv=MT6&ReturnUrl=%2FIBK%2Fde%2Fvisitorregistrationforms%2Foverview%2F126f500b-72a7-45e1-a2b9-784d449fcdd7%3FdbOv%3DMT6"  # Ersetze durch die tatsächliche Login-URL
    username = "VMIBKKUJO"  # Ersetze durch den tatsächlichen Benutzernamen
    password = "start"  # Ersetze durch das tatsächliche Passwort
    url_of_GuestcardPDF = open_browser_and_login(url, username, password) # URL der Seite die bei beenden des Programms offen war

    # Dieser CodeBlock erstellt einen neuen Ordner mit heutigem Datum und speichert die PDF im passenden Unterordner

    current_date = datetime.now().strftime("%Y-%m-%d") # Aktuelles Datum für Ordner Name
    base_output_folder = r"C:\Users\gkuen\Pictures\Welcomecards"  # Passe den Basis-Ausgabeordner an
    input_folder_PDF = os.path.join(base_output_folder, "PDFs") # AusgabeOrdner für PDF
    fileName_PDF = current_date + ".pdf" # Name der Erstellten PDF
    download_pdf_from_url(url_of_GuestcardPDF, os.path.join(input_folder_PDF, fileName_PDF)) # Lädt PDF herunter und speichert sie im darüber angegebenen Ordner
    folder_path = input_folder_PDF  # Passe den Pfad zu deinem Ordner an
    pdf_path = os.path.join(input_folder_PDF, fileName_PDF) # Pfad zum gearde erstellten PDF
    input_folder_GuestCards = os.path.join(base_output_folder, current_date)  # Name des Ordners für Welcomecards

    # Dieser CodeBlock verarbeitet die PDF zu fertigen WelcomeCards

    resolution = 300  # Passe die gewünschte Auflösung der erstellten Bilder an
    pdf_to_images(pdf_path, base_output_folder, resolution) # Erstellt Bilder von der PDF
    process_images(input_folder_GuestCards) # Schneidet die erstellten Bilder richtig zu

