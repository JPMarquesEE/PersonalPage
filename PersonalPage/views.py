# -*- coding: latin-1 -*-

from flask import Flask, render_template, request, redirect, url_for, flash
from PersonalPage.tools import mesclar_pdfs_bp, pdf_para_imagem_bp
from PersonalPage import app

app.secret_key = "chave_secreta"  # Necess�ria para exibir mensagens flash

# Registrando os Blueprints das ferramentas
app.register_blueprint(mesclar_pdfs_bp, url_prefix='/ferramentas/mesclar_pdfs')
app.register_blueprint(pdf_para_imagem_bp, url_prefix='/ferramentas/pdf_para_imagem')
#app.register_blueprint(calc_area_bp, url_prefix='/calc_area')

# Rota para a p�gina inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para a p�gina de ferramentas principal (inicial)
@app.route('/ferramentas')
def ferramentas():
    return render_template('ferramentas.html', selected_tool=None)

# Rota para a ferramenta "Mesclar PDFs"
@app.route('/ferramentas/mesclar_pdfs')
def mesclar_pdfs():
    return render_template('ferramentas.html', selected_tool="mesclar_pdfs")

# Rota para a ferramenta "PDF2IMAGEM"
@app.route('/ferramentas/pdf_para_imagem')
def pdf_para_imagem():
    return render_template('ferramentas.html', selected_tool="pdf_para_imagem")

# Rota para a p�gina de contato
@app.route('/contato', methods=['GET', 'POST'])
def contato():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        mensagem = request.form.get('mensagem')
        
        # Aqui, voc� poderia adicionar a l�gica para enviar o e-mail ou salvar a mensagem
        flash("Mensagem enviada com sucesso!", "success")
        return redirect(url_for('contato'))
    
    return render_template('contato.html')