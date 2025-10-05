import shutil
import os
import sqlite3
from fpdf import FPDF
from docx import Document

# Step 1: File Saving
def save_file(file_name, content):
    with open(file_name, 'w') as file:
        file.write(content)
    print(f"File '{file_name}' saved successfully.")

# Step 2: File Copying
def copy_file(source, destination):
    shutil.copy(source, destination)
    print(f"File '{source}' copied to '{destination}'.")

# Step 3: Convert .txt to .pdf
def text_to_pdf(txt_file, pdf_file):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    with open(txt_file, 'r') as file:
        content = file.read()

    pdf.multi_cell(0, 10, content)
    pdf.output(pdf_file)
    print(f"File converted to PDF: {pdf_file}")

# Step 4: Convert .txt to .docx
def text_to_word(txt_file, word_file):
    doc = Document()
    with open(txt_file, 'r') as file:
        content = file.read()

    doc.add_paragraph(content)
    doc.save(word_file)
    print(f"File converted to Word: {word_file}")

# Step 5: SQLite Database for Metadata
def create_db():
    conn = sqlite3.connect('file_metadata.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_name TEXT,
        file_format TEXT,
        file_size INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()

# Step 6: Insert Metadata into SQLite
def insert_metadata(file_name, file_format, file_size):
    conn = sqlite3.connect('file_metadata.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO files (file_name, file_format, file_size)
    VALUES (?, ?, ?)
    ''', (file_name, file_format, file_size))
    conn.commit()
    conn.close()
    print(f"Metadata for '{file_name}' inserted into the database.")

# Step 7: Query Metadata from SQLite (optional)
def query_metadata():
    conn = sqlite3.connect('file_metadata.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM files')
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    conn.close()

# Main Program Flow
if __name__ == '__main__':
    # Create the SQLite database if it doesn't exist
    create_db()

    # Save a text file
    content = "This is a sample text file. It will be converted to PDF and Word."
    save_file('sample.txt', content)

    # Insert metadata into SQLite (example: save file name, format, size)
    insert_metadata('sample.txt', 'txt', os.path.getsize('sample.txt'))

    # Copy the file
    copy_file('sample.txt', 'sample_copy.txt')

    # Convert .txt to .pdf and .docx
    text_to_pdf('sample.txt', 'sample.pdf')
    insert_metadata('sample.pdf', 'pdf', os.path.getsize('sample.pdf'))

    text_to_word('sample.txt', 'sample.docx')
    insert_metadata('sample.docx', 'docx', os.path.getsize('sample.docx'))

    # Query metadata (optional)
    query_metadata()
