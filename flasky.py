from flask import Flask, render_template, redirect, url_for, session
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from datetime import datetime

# -----------------------------------
# Configuração básica da aplicação
# -----------------------------------
app = Flask(__name__)
app.config.from_object('config.Config')

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)

# -----------------------------------
# MODELOS DO BANCO DE DADOS
# -----------------------------------
class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64), unique=False)
    disciplina = db.Column(db.String(64))

    def __repr__(self):
        return f'<Professor {self.nome}>'

# -----------------------------------
# FORMULÁRIO
# -----------------------------------
class ProfessorForm(FlaskForm):
    nome = StringField("Nome do Professor:", validators=[DataRequired()])
    disciplina = SelectField(
        "Disciplina associada:",
        choices=[
            ('DSWA5', 'DSWA5'),
            ('GPSA5', 'GPSA5'),
            ('FPW', 'FPW'),
            ('ED', 'Estrutura de Dados')
        ],
        validators=[DataRequired()]
    )
    submit = SubmitField('Cadastrar')

# -----------------------------------
# ROTA PRINCIPAL
# -----------------------------------
@app.route('/')
def index():
    return render_template('index.html',
                           current_time=datetime.utcnow())

# -----------------------------------
# ROTA EXIGIDA NA PROVA: /professores
# -----------------------------------
@app.route('/professores', methods=['GET', 'POST'])
def professores():
    form = ProfessorForm()

    if form.validate_on_submit():
        novo = Professor(
            nome=form.nome.data,
            disciplina=form.disciplina.data
        )
        db.session.add(novo)
        db.session.commit()

        return redirect(url_for('professores'))

    lista = Professor.query.order_by(Professor.nome).all()

    return render_template('professores.html',
                           form=form,
                           professores=lista,
                           current_time=datetime.utcnow())

# -----------------------------------
# ROTAS NÃO IMPLEMENTADAS
# -----------------------------------
@app.route('/disciplinas')
@app.route('/alunos')
@app.route('/cursos')
@app.route('/ocorrencias')
def nao_disponivel():
    return render_template("nao_disponivel.html",
                           current_time=datetime.utcnow())

# -----------------------------------
# ERRO 404
# -----------------------------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# -----------------------------------
if __name__ == '__main__':
    app.run(debug=True)
