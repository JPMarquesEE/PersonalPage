# -*- coding: latin-1 -*-

from flask import Blueprint, render_template, request, send_file
from pdf2image import convert_from_path
import io
import zipfile
import os
from tempfile import TemporaryDirectory

pdf_para_imagem_bp = Blueprint('pdf_para_imagem', __name__, template_folder='../templates/tools')

@pdf_para_imagem_bp.route('/', methods=['GET', 'POST'])
def pdf_para_imagem():
    if request.method == 'POST':
        pdf_file = request.files['pdf_file']
        resolution = int(request.form.get('resolution', 300))  # Resolução padrão de 300 DPI

        if pdf_file and pdf_file.filename.endswith('.pdf'):
            try:
                # Cria um diretório temporário para salvar as imagens
                with TemporaryDirectory() as temp_dir:
                    pdf_path = os.path.join(temp_dir, pdf_file.filename)
                    pdf_file.save(pdf_path)  # Salva o PDF temporariamente

                    # Converte o PDF em uma lista de imagens (cada página é uma imagem)
                    pages = convert_from_path(pdf_path, dpi=resolution, poppler_path=r'C:/Poppler/Library/bin')
                    
                    # Cria um arquivo zip em memória para armazenar as imagens
                    zip_buffer = io.BytesIO()
                    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                        for i, page in enumerate(pages):
                            # Salva cada página como uma imagem PNG no diretório temporário
                            image_path = os.path.join(temp_dir, f'pagina_{i + 1}.png')
                            page.save(image_path, 'PNG')
                            # Adiciona a imagem ao arquivo zip
                            zip_file.write(image_path, f'pagina_{i + 1}.png')

                    zip_buffer.seek(0)  # Reposiciona o ponteiro para o início do buffer
                    
                    # Envia o arquivo zip para download
                    return send_file(zip_buffer, download_name="imagens_paginas.zip", as_attachment=True)
            
            except Exception as e:
                print(f"Erro na conversão de PDF para imagens: {e}")
                return render_template('ferramentas.html', selected_tool="pdf_para_imagem", error="Erro ao processar o PDF.")
        
        return render_template('ferramentas.html', selected_tool="pdf_para_imagem", error="Arquivo inválido. Envie um PDF.")
    
    return render_template('ferramentas.html', selected_tool="pdf_para_imagem")