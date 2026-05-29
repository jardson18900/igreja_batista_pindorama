import pandas as pd
import random
from datetime import date, timedelta

random.seed(42)

NOMES = [
    "Ana Clara", "Maria José", "João Pedro", "Carlos Eduardo", "Fernanda Lima",
    "Lucas Oliveira", "Beatriz Santos", "Rafael Costa", "Juliana Mendes", "Pedro Henrique",
    "Larissa Ferreira", "Marcos Vinícius", "Camila Rocha", "Diego Alves", "Priscila Nunes",
    "Anderson Souza", "Tatiane Ribeiro", "Felipe Carvalho", "Natalia Gomes", "Roberto Araújo",
    "Vanessa Melo", "Thiago Barbosa", "Elisangela Dias", "Rodrigo Pinto", "Simone Castro",
    "Gabriel Silva", "Daniela Martins", "Eduardo Ferreira", "Aline Moura", "Fábio Nascimento",
    "Renata Cavalcante", "Bruno Azevedo", "Mônica Torres", "Leandro Cardoso", "Patricia Lopes",
    "Vinícius Macedo", "Adriana Freitas", "Gustavo Pereira", "Lorena Campos", "André Teixeira",
    "Rosangela Borges", "Henrique Vieira", "Clarice Ramos", "Matheus Correia", "Sandra Queiroz",
    "Igor Batista", "Luciana Figueiredo", "Alexandre Cunha", "Eliane Monteiro", "Sérgio Paiva",
    "Raquel Andrade", "Caio Barros", "Viviane Prado", "Wilson Vasconcelos", "Carla Nogueira",
    "Tiago Medeiros", "Márcia Cavalcanti", "Renato Coelho", "Isabela Duarte", "Cláudio Rangel",
    "Débora Amaral", "Flávia Leite", "Osmar Albuquerque", "Nelma Soares", "Paulo César",
    "Irene Magalhães", "José Carlos", "Edilson Tavares", "Sueli Guimarães", "Neuza Patriota",
    "Antônio Filho", "Tereza Cristina", "Waldir Lacerda", "Cícero Bezerra", "Francisca Helena",
    "Joaquim Reis", "Geralda Souza", "Benedito Lira", "Aparecida Fonseca", "Manoel Rodrigues",
    "Lurdes Braga", "Everaldo Maia", "Conceição Paz", "Arnaldo Brito", "Iracema Leal",
    "Sebastião Cruz", "Dilma Porto", "Oswaldo Sampaio", "Edna Falcão", "Geraldo Uchoa",
    "Nilda Cabral", "Altino Menezes", "Diva Siqueira", "Raimundo Holanda", "Diva Salles",
    "Clovis Barreiros", "Zilda Farias", "Adilson Neto", "Elza Pontes", "Herculano Lima",
]

BAIRROS = [
    "Pindorama", "Centro", "Santa Maria", "Bom Jesus", "São Francisco",
    "Alto do Cruzeiro", "Esperança", "Vila Nova", "Jardim Tropical", "Mangabeira",
]

GENEROS = ["Masculino", "Feminino"]

def gerar_data_nascimento():
    hoje = date.today()
    dias = random.randint(365 * 5, 365 * 80)
    return hoje - timedelta(days=dias)

membros = []
for i, nome in enumerate(NOMES[:100]):
    nascimento = gerar_data_nascimento()
    membro = {
        "Nome Completo": nome,
        "Data de Nascimento": nascimento.strftime("%d/%m/%Y"),
        "Gênero": random.choice(GENEROS),
        "Bairro": random.choice(BAIRROS),
        "Telefone": f"(82) 9{random.randint(1000,9999)}-{random.randint(1000,9999)}",
        "Email": f"{nome.split()[0].lower()}.{nome.split()[-1].lower()}{random.randint(1,99)}@email.com",
        "Membro Ativo": random.choices(["Sim", "Não"], weights=[85, 15])[0],
        "Data de Cadastro": (date.today() - timedelta(days=random.randint(0, 365))).strftime("%d/%m/%Y"),
    }
    membros.append(membro)

df = pd.DataFrame(membros)
df.to_csv("dados_membros.csv", index=False, encoding="utf-8-sig")
print(f"✅ {len(df)} membros gerados com sucesso!")
print(df.head())
