from flask import Blueprint, render_template, request, send_file
from PyPDF2 import PdfMerger
import requests
import io

mesclar_pdfs_bp = Blueprint('mesclar_pdfs', __name__, template_folder='../templates/tools')

@mesclar_pdfs_bp.route('/', methods=['GET', 'POST'])
def mesclar_pdfs():
    if request.method == 'POST':
        links = request.form.get('links').splitlines()  # Links separados por linhas
        merger = PdfMerger()
        
        for link in links:
            response = requests.get(link)
            pdf_file = io.BytesIO(response.content)
            merger.append(pdf_file)
        
        # Salvando o arquivo final em memória
        merged_pdf = io.BytesIO()
        merger.write(merged_pdf)
        merged_pdf.seek(0)
        
        return send_file(merged_pdf, download_name="mesclado.pdf", as_attachment=True)
    
    # Renderiza o conteúdo no contexto do template "ferramentas.html"
    return render_template('ferramentas.html', selected_tool="mesclar_pdfs")
