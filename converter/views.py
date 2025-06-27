from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
import pdfplumber
import pandas as pd
from docx import Document
import os

def landing_page(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        if file.name.endswith('.pdf'):
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            request.session['uploaded_file'] = filename
            return redirect('choose_conversion')
        else:
            return render(request, 'error.html', {'message': 'Потрібен PDF файл'})
    return render(request, 'base.html')



def choose_conversion(request):
    file_name = request.session.get('uploaded_file')
    if not file_name:
        return redirect('upload_file')
    return render(request, 'choose_conversion.html', {'file_name': file_name})


def convert_to_excel(request):
    file_name = request.session.get('uploaded_file')
    if not file_name:
        return redirect('upload_file')

    input_path = os.path.join('media', file_name)
    output_filename = file_name.replace('.pdf', '.xlsx')
    output_path = os.path.join('media', output_filename)

    os.makedirs('media', exist_ok=True)

    with pdfplumber.open(input_path) as pdf:
        all_tables = []
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                df = pd.DataFrame(table)
                all_tables.append(df)

        if all_tables:
            combined = pd.concat(all_tables)
            combined.to_excel(output_path, index=False)
        else:
            # якщо таблиць нема — створимо порожній файл
            pd.DataFrame([["Немає таблиць у PDF"]]).to_excel(output_path, index=False)

    return render(request, 'download.html', {
        'original': file_name,
        'converted': output_filename
    })

def convert_to_word(request):
    file_name = request.session.get('uploaded_file')
    if not file_name:
        return redirect('upload_file')

    input_path = os.path.join('media', file_name)
    output_filename = file_name.replace('.pdf', '.docx')
    output_path = os.path.join('media', output_filename)

    os.makedirs('media', exist_ok=True)

    doc = Document()
    with pdfplumber.open(input_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                doc.add_paragraph(text)
    doc.save(output_path)

    return render(request, 'download.html', {
        'original': file_name,
        'converted': output_filename
    })
