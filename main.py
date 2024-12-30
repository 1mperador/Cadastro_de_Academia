from sqlalchemy import create_engine , Column, String, Integer, Date
from sqlalchemy.orm import sessionmaker, declarative_base


db = create_engine("sqlite:///alunos.db")
Session = sessionmaker(bind=db)
session = Session()

Base= declarative_base()

# 1. Cadastrar aulas com nome, descrição, horário, e número máximo de alunos.
    # Aluno Regular: Alunos que possuem um plano ativo na academia e têm acesso completo às aulas.

class Aluno_Regular(Base):

    __tablename__ = "Aluno_Regular"

    id          = Column("id", Integer, primary_key=True, autoincrement=True)
    nome        = Column("nome", String)
    email       = Column("email", String)
    telefone    = Column("telefone", String)
    data_nasc   = Column("data_nasc", String)
    max_inscritos = Column(Integer, default=20)
    max_inscritos_por_aula = Column(Integer, default=20)  


    def __init__(self, nome, email, telefone, data_nasc, max_inscritos):
        self.nome       = nome
        self.email      = email
        self.telefone   = telefone
        self.data_nasc  = data_nasc
        self.max_inscritos = max_inscritos




#  teste de banco de dados 

# test = Aluno_Regular(nome="Pablo", email="emailexe@gmail.com", telefone="(19)92233-9334", data_nasc="12/01/1998")

# session.add(test)
# session.commit()


# 2. Cadastrar alunos com nome, e-mail, telefone, e data de nascimento.
#     Aluno Visitante: Alunos que estão fazendo aulas experimentais ou possuem um acesso limitado (ex.: apenas um dia).

class Aluno_Visitante(Base):

    __tablename__ = "Aluno_Visitante"

    id          = Column("id", Integer, primary_key=True, autoincrement=True)
    nome        = Column("nome", String)
    email       = Column("email", String)
    telefone    = Column("telefone", String)
    data_nasc   = Column("data_nasc", String)
    prazo       = Column("prazo", String)

    def __init__(self, nome, email, telefone, data_nasc, prazo):
        self.nome       = nome 
        self.email      = email
        self.telefone   = telefone
        self.data_nasc  = data_nasc
        self.prazo      = prazo

test = Aluno_Visitante("Ipman", "emailttst@hotmail.com", "(19) 9 43434 4343","12/05/2001","01/01/2025") 

session.add(test)
session.commit()






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


Base.metadata.create_all(bind=db)