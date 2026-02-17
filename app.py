from flask import Flask, render_template, request, redirect, url_for, jsonify
import datetime

app = Flask(__name__)

# Lista inicial
tarefas = [
    {'id': 1, 'titulo': 'Acordar e Café', 'subtitulo': 'Iniciar o dia', 'horario': '07:00', 'icone': 'fa-mug-hot',
     'cor': '#f1c40f', 'feita': True},
    {'id': 2, 'titulo': 'Mate Academy', 'subtitulo': 'Programação', 'horario': '08:00', 'icone': 'fa-code',
     'cor': '#3498db', 'feita': False},
    {'id': 3, 'titulo': 'Xadrez', 'subtitulo': 'Estudar teoria e jogar', 'horario': '10:00', 'icone': 'fa-chess-knight',
     'cor': '#9b59b6', 'feita': False},
    {'id': 4, 'titulo': 'Unicesumar', 'subtitulo': 'Faculdade', 'horario': '13:00', 'icone': 'fa-graduation-cap',
     'cor': '#e67e22', 'feita': False},
    {'id': 5, 'titulo': 'Fluency Academy', 'subtitulo': 'Inglês focado', 'horario': '15:00', 'icone': 'fa-language',
     'cor': '#e74c3c', 'feita': False},
    {'id': 6, 'titulo': 'Duolingo', 'subtitulo': 'Inglês, Esp, Música', 'horario': '16:30', 'icone': 'fa-crow',
     'cor': '#2ecc71', 'feita': False},
    {'id': 7, 'titulo': 'Libras', 'subtitulo': 'Prática diária', 'horario': '17:30',
     'icone': 'fa-hands-asl-interpreting', 'cor': '#1abc9c', 'feita': False},
    {'id': 8, 'titulo': 'Piano e Música', 'subtitulo': 'Teoria e Prática', 'horario': '19:00', 'icone': 'fa-music',
     'cor': '#e91e63', 'feita': False},
    {'id': 9, 'titulo': 'Leitura e Bíblia', 'subtitulo': 'Momento espiritual', 'horario': '21:00',
     'icone': 'fa-book-bible', 'cor': '#ecf0f1', 'feita': False}
]
id_counter = 3


@app.route('/')
def index():
    agora = datetime.datetime.now()
    # Ordena as tarefas pelo horário automaticamente
    tarefas_ordenadas = sorted(tarefas, key=lambda x: x['horario'])
    return render_template('index.html', tarefas=tarefas_ordenadas, dia_atual=agora.day)


@app.route('/adicionar', methods=['POST'])
def adicionar():
    global id_counter
    titulo = request.form.get('titulo')
    subtitulo = request.form.get('subtitulo')
    horario = request.form.get('horario')
    icone = request.form.get('icone')
    cor = request.form.get('cor')

    if titulo:
        tarefas.append({
            'id': id_counter,
            'titulo': titulo,
            'subtitulo': subtitulo if subtitulo else 'Nova atividade',
            'horario': horario if horario else '00:00',
            'icone': icone if icone else 'fa-circle',
            'cor': cor if cor else '#ffffff',
            'feita': False
        })
        id_counter += 1
    return redirect(url_for('index'))


@app.route('/atualizar/<int:id>')
def atualizar(id):
    for tarefa in tarefas:
        if tarefa['id'] == id:
            tarefa['feita'] = not tarefa['feita']
            break
    return redirect(url_for('index'))


@app.route('/deletar/<int:id>')
def deletar(id):
    global tarefas
    tarefas = [t for t in tarefas if t['id'] != id]
    return redirect(url_for('index'))


# Rota de reordenar (mantida caso queira usar drag and drop, mas a ordenação por horário tem prioridade na visualização inicial)
@app.route('/reordenar', methods=['POST'])
def reordenar():
    global tarefas
    nova_ordem_ids = request.json.get('ordem')
    tarefas_map = {str(t['id']): t for t in tarefas}
    nova_lista = []
    for id_tarefa in nova_ordem_ids:
        if str(id_tarefa) in tarefas_map:
            nova_lista.append(tarefas_map[str(id_tarefa)])
    for t in tarefas:
        if t not in nova_lista:
            nova_lista.append(t)
    tarefas = nova_lista
    return jsonify({'status': 'sucesso'})


if __name__ == '__main__':
    app.run(debug=True)
