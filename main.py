
import fitz  # PyMuPDF
from PIL import Image
import os
from datetime import datetime
from pathlib import Path

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

def get_latest_pdf_path(folder_path):
    # Überprüfe, ob der Ordner existiert
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Der Ordner '{folder_path}' existiert nicht.")

    # Durchsuche den Ordner nach PDF-Dateien
    pdf_files = [file for file in os.listdir(folder_path) if file.lower().endswith('.pdf')]

    # Überprüfe, ob PDF-Dateien gefunden wurden
    if not pdf_files:
        raise FileNotFoundError(f"Im Ordner '{folder_path}' wurden keine PDF-Dateien gefunden.")

    # Erhalte die neueste PDF-Datei basierend auf dem Änderungsdatum
    latest_pdf_path = max(pdf_files, key=lambda file: os.path.getmtime(os.path.join(folder_path, file)))

    # Gib den vollen Dateipfad zur neuesten PDF-Datei zurück
    return os.path.join(folder_path, latest_pdf_path)

if __name__ == "__main__":
    folder_path = r"C:\Users\gkuen\Downloads"  # Passe den Pfad zu deinem Ordner an
    pdf_path = get_latest_pdf_path(folder_path)
    base_output_folder = r"C:\Users\gkuen\Pictures\Welcomecards"  # Passe den Basis-Ausgabeordner an
    resolution = 300  # Passe die gewünschte Auflösung an

    pdf_to_images(pdf_path, base_output_folder, resolution)

    # Name des Ordners
    current_date = datetime.now().strftime("%Y-%m-%d")
    input_folder = os.path.join(base_output_folder, current_date)

    process_images(input_folder)
