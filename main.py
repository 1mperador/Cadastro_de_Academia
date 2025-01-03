from flask import Flask, render_template,request, redirect, url_for
from sqlalchemy import create_engine , Column, String, Integer, Date
from sqlalchemy.orm import sessionmaker, declarative_base

app = Flask(__name__)

db = create_engine("sqlite:///alunos.db")
Session = sessionmaker(bind=db)
session = Session()

Base= declarative_base()


# 1. Cadastrar aulas com nome, descrição, horário, e número máximo de alunos.
    # Aluno Regular: Alunos que possuem um plano ativo na academia e têm acesso completo às aulas.

class Aluno_Regular(Base):

    __tablename__ = "Aluno_Regular"

    id                     = Column("id",Integer, primary_key=True, autoincrement=True)
    nome                   = Column("nome",String, nullable=True)
    email                  = Column("email",String, nullable=True)
    telefone               = Column("telefone",String, nullable=True)
    data_nasc              = Column("data_nasc",String, nullable=True)
    max_inscritos          = Column("max_inscritos",Integer, nullable=False, default=10)
    alunos_atual           = Column("alunos_atual",Integer, nullable=False, default=0)

    def __init__(self, nome, email, telefone, data_nasc,max_inscritos=None):
        self.nome                   = nome
        self.email                  = email
        self.telefone               = telefone
        self.data_nasc              = data_nasc
        self.max_inscritos          = max_inscritos if max_inscritos is not None else 10
        self.alunos_atual           = 0

    def adicionar_aluno(self):
            if self.alunos_atual < self.max_inscritos:
                self.alunos_atual += 1
                session.commit()
            else:
                raise Exception("Número máximo de alunos atingido")
    
    @staticmethod
    def contar_alunos():
        return session.query(Aluno_Regular).count()
    


# 2. Cadastrar alunos com nome, e-mail, telefone, e data de nascimento.
#     Aluno Visitante: Alunos que estão fazendo aulas experimentais ou possuem um acesso limitado (ex.: apenas um dia).

class Aluno_Visitante(Base):

    __tablename__ = "Aluno_Visitante"

    id              = Column("id", Integer, primary_key=True, autoincrement=True)
    nome            = Column("nome", String, nullable=True)
    descricao       = Column("descrição",String,nullable=True)
    horario         = Column("horario", String, nullable=True)
    max_inscritos   = Column("max_inscritos",Integer,nullable=False, default=10)

    def __init__(self, nome, descricao, horario, max_inscritos=None):
        self.nome           = nome 
        self.descricao      = descricao
        self.horario        = horario
        self.max_inscritos  = max_inscritos if max_inscritos is not None else 10

# Criação do banco de dados
Base.metadata.create_all(bind=db)

@app.route('/relatorio/alunos_por_aula')
def relatorio_alunos_por_aula():
    aulas = session.query(Aluno_Regular).all()
    return render_template('alunos_por_aula.html', aulas=aulas)

@app.route('/relatorio/aulas_com_horarios')
def relatorio_aulas_com_horarios():
    aulas = session.query(Aluno_Regular).all()
    return render_template('aulas_com_horarios.html', aulas=aulas)

@app.route('/relatorio/total_de_alunos')
def relatorio_total_de_alunos():
    total = session.query(Aluno_Regular).count()
    return render_template('total_de_alunos.html', total=total)

@app.route('/adicionar_aluno', methods=['GET', 'POST'])
def adicionar_aluno():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        data_nasc = request.form['data_nasc']
        
        novo_aluno = Aluno_Regular(nome=nome, email=email, telefone=telefone, data_nasc=data_nasc)
        session.add(novo_aluno)
        session.commit()
         
        # Atualiza a contagem de alunos
        novo_aluno.alunos_atual = Aluno_Regular.contar_alunos()
        session.commit()
        
        return redirect(url_for('relatorio_alunos_por_aula'))
    
    return render_template('adicionar_aluno.html')
if __name__ == '__main__':
    app.run(debug=True)
    

def adicionar_aluno(aula_id, session):
    aula = session.query(Aluno_Regular).filter_by(id=aula_id).first()
    if not aula:
        raise Exception("Aula não encontrada.")
    
    if aula.alunos_atual >= aula.max_inscritos:
        raise Exception(f"Limite de {aula.max_inscritos} alunos já atingido para esta aula.")
    
    aula.alunos_atual += 1
    session.commit()
    print(f"Aluno adicionado com sucesso! Total atual: {aula.alunos_atual}/{aula.max_inscritos}")

# def verificar_limite(aula_id, session):
#     aula = session.query(Aluno_Visitante).filter_by(id=aula_id).first()
#     if aula and len(aula.inscritos) >= aula.max_inscritos:
#         raise Exception(f"Limite de {aula.max_inscritos} alunos já atingido para esta aula.")

# test1 = Aluno_Visitante("Ipman", "emailttst@hotmail.com", "(19) 9 43434 4343","12/05/2001","01/01/2025") 

# nova_aula = Aluno_Visitante(nome="Yoga", descricao="Aula de yoga relaxante", horario="18:00")
# session.add(nova_aula)
# session.commit()

# novo_aluno = Aluno_Regular(nome="Pablo", email="emailexe@gmail.com", telefone="(19)92233-9334", data_nasc="12/01/1998")
# session.add(novo_aluno)
# session.commit()
# novo_aluno = Aluno_Regular(nome="Ana", email="anaemail@gmail.com", telefone="(19)92113-9334", data_nasc="01/01/2001")
# session.add(novo_aluno)
# session.commit()

# novo_aluno = Aluno_Regular(nome="João", email="joao@example.com", telefone="123456789", data_nasc="2000-01-01")
# session.add(novo_aluno)
# session.commit()

# # Atualiza a contagem de alunos
# novo_aluno.alunos_atual = Aluno_Regular.contar_alunos()
# session.commit()


# # Listar alunos por aula
# def listar_alunos_por_aula():
#     aulas = session.query(Aluno_Regular).all()
#     for aula in aulas:
#         print(f"Aula: {aula.nome}")
#         print(f"Alunos inscritos: {aula.alunos_atual}/{aula.max_inscritos}")
#         print("-" * 30)

# # Exemplo de uso
# listar_alunos_por_aula()

# # Listar aulas com horários
# def listar_aulas_com_horarios():
#     aulas = session.query(Aluno_Regular).all()
#     for aula in aulas:
#         print(f"Aula: {aula.nome}")
#         print(f"Horário: {aula.horario}")
#         print("-" * 30)

# # Exemplo de uso
# listar_aulas_com_horarios()

# # Total de alunos na academia
# def total_de_alunos():
#     total = session.query(Aluno_Regular).count()
#     print(f"Total de alunos na academia: {total}")

# # Exemplo de uso
# total_de_alunos()

# # Adiciona um aluno à aula
# novo_aluno.adicionar_aluno()

# print("Aula cadastrada com sucesso!")


# TODO VALIDAÇÃO DE NUMEROS DE TELEFONE
#         import phonenumbers

# def validar_telefone(numero):
#     try:
#         telefone = phonenumbers.parse(numero, "BR")  # Exemplo: "BR" para Brasil
#         return phonenumbers.is_valid_number(telefone)
#     except phonenumbers.NumberParseException:
#         return False

# # Exemplo de uso
# numero = "+55 11 91234-5678"
# if validar_telefone(numero):
#     print("Número válido!")
# else:
#     print("Número inválido!")


