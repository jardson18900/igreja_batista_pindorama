import pandas as pd
import random
from datetime import date, timedelta

random.seed(42)

NOMES_MASC = [
    "João Pedro", "Carlos Eduardo", "Lucas Oliveira", "Rafael Costa", "Pedro Henrique",
    "Marcos Vinícius", "Diego Alves", "Anderson Souza", "Felipe Carvalho", "Roberto Araújo",
    "Thiago Barbosa", "Rodrigo Pinto", "Gabriel Silva", "Eduardo Ferreira", "Fábio Nascimento",
    "Bruno Azevedo", "Leandro Cardoso", "André Teixeira", "Gustavo Pereira", "Vinícius Macedo",
    "Henrique Vieira", "Matheus Correia", "Igor Batista", "Alexandre Cunha", "Sérgio Paiva",
    "Caio Barros", "Wilson Vasconcelos", "Tiago Medeiros", "Renato Coelho", "Cláudio Rangel",
    "Osmar Albuquerque", "Paulo César", "José Carlos", "Edilson Tavares", "Antônio Filho",
    "Waldir Lacerda", "Cícero Bezerra", "Joaquim Reis", "Benedito Lira", "Manoel Rodrigues",
    "Everaldo Maia", "Arnaldo Brito", "Sebastião Cruz", "Oswaldo Sampaio", "Geraldo Uchoa",
    "Altino Menezes", "Raimundo Holanda", "Clovis Barreiros", "Adilson Neto", "Herculano Lima",
    "Davi Almeida", "Samuel Freitas", "Elias Mendonça", "Caleb Rocha", "Josué Nunes",
    "Mateus Brito", "Tito Rangel", "Silas Cardoso", "Ananias Sousa", "Barnabé Torres",
    "Timóteo Leal", "Filipe Cunha", "Estêvão Melo", "Cornélio Barros", "Nicodemos Farias",
    "Ezequiel Moura", "Isaías Campos", "Jeremias Pinto", "Oséias Tavares", "Amós Vieira",
    "Miquéias Lima", "Habacuque Sousa", "Malaquias Neto", "Zacarias Brito", "Daniel Rocha",
    "Neemias Freitas", "Esdras Borges", "Jônatas Cunha", "Gideão Melo", "Gedeão Alves",
    "Boaz Rangel", "Isaque Santos", "Jacó Ferreira", "Rubem Medeiros", "Simão Costa",
    "Levi Araújo", "Juda Martins", "Neftali Gomes", "Zabulom Barros", "Benjamim Cruz",
    "Asafe Torres", "Urias Lacerda", "Salomão Paiva", "Ezra Brito", "Tobias Mendes",
    "Absalão Freire", "Abiatar Soares", "Dotã Lima", "Golias Junior", "Adão Pereira",
    "Elcana Batista", "Ibraim Cavalcante", "Obed Azevedo", "Jessé Prado", "Bezalel Vasconcelos",
    "Rúben Holanda", "Sansão Lacerda", "Mardoqueu Bezerra", "Natanael Reis",
]

NOMES_FEM = [
    "Ana Clara", "Maria José", "Fernanda Lima", "Beatriz Santos", "Juliana Mendes",
    "Larissa Ferreira", "Camila Rocha", "Priscila Nunes", "Tatiane Ribeiro", "Natalia Gomes",
    "Vanessa Melo", "Elisangela Dias", "Simone Castro", "Daniela Martins", "Aline Moura",
    "Renata Cavalcante", "Mônica Torres", "Patricia Lopes", "Adriana Freitas", "Lorena Campos",
    "Rosangela Borges", "Clarice Ramos", "Sandra Queiroz", "Luciana Figueiredo", "Carla Nogueira",
    "Márcia Cavalcanti", "Isabela Duarte", "Débora Amaral", "Flávia Leite", "Nelma Soares",
    "Irene Magalhães", "Tereza Cristina", "Sueli Guimarães", "Neuza Patriota", "Francisca Helena",
    "Geralda Souza", "Aparecida Fonseca", "Lurdes Braga", "Conceição Paz", "Iracema Leal",
    "Dilma Porto", "Edna Falcão", "Nilda Cabral", "Diva Siqueira", "Zilda Farias",
    "Elza Pontes", "Ruth Silva", "Ester Oliveira", "Sara Mendes", "Rebeca Alves",
    "Raquel Costa", "Débora Lima", "Miriã Santos", "Abigail Rocha", "Tamar Ferreira",
    "Suzana Nunes", "Ana Lúcia", "Joana Batista", "Marta Freitas", "Maria Madalena",
    "Elisabete Cunha", "Dorcas Barros", "Priscila Aquila", "Febe Melo", "Lídia Campos",
    "Berenice Torres", "Zipóra Sousa", "Hadassa Lacerda", "Ester Brito", "Noemi Cruz",
    "Rute Borges", "Orpá Martins", "Zelfa Gomes", "Joabe Moura", "Dina Vasconcelos",
    "Júlia Holanda", "Sofia Rangel", "Valentina Cardoso", "Isadora Pinto", "Melissa Tavares",
    "Letícia Vieira", "Giovanna Lima", "Mariana Cunha", "Amanda Pereira", "Bianca Neto",
    "Luana Batista", "Cecília Cavalcante", "Helena Azevedo", "Clara Prado", "Alice Vasconcelos",
    "Lara Holanda", "Maya Lacerda", "Nina Bezerra", "Liz Reis", "Jade Freitas",
    "Catarina Soares", "Agatha Lima", "Elisa Cunha", "Aurora Barros", "Vitória Melo",
    "Yasmin Campos", "Ísis Torres", "Layla Sousa", "Diana Brito", "Selma Cruz",
]

BAIRROS = [
    "Pindorama", "Centro", "Santa Maria", "Bom Jesus", "São Francisco",
    "Alto do Cruzeiro", "Esperança", "Vila Nova", "Jardim Tropical", "Mangabeira",
    "Novo Horizonte", "Cohab", "Frei Damião", "São José", "Palmeira",
]

def gerar_nascimento(faixa: str) -> date:
    hoje = date.today()
    faixas = {
        "crianca":    (5,  12),
        "jovem":      (13, 17),
        "jovem_adul": (18, 29),
        "adulto":     (30, 59),
        "idoso":      (60, 85),
    }
    min_a, max_a = faixas[faixa]
    idade = random.randint(min_a, max_a)
    nascimento = hoje.replace(year=hoje.year - idade)
    delta = random.randint(-180, 180)
    return nascimento + timedelta(days=delta)

# Distribuição etária mais realista para uma igreja
DISTRIBUICAO = {
    "crianca":    0.10,
    "jovem":      0.08,
    "jovem_adul": 0.20,
    "adulto":     0.45,
    "idoso":      0.17,
}

TOTAL = 300

# Gera proporções
faixas_lista = []
for faixa, prop in DISTRIBUICAO.items():
    faixas_lista += [faixa] * round(prop * TOTAL)
# Ajusta para bater exato 300
while len(faixas_lista) < TOTAL:
    faixas_lista.append("adulto")
faixas_lista = faixas_lista[:TOTAL]
random.shuffle(faixas_lista)

# Monta membros
todos_nomes_masc = NOMES_MASC * 3
todos_nomes_fem  = NOMES_FEM  * 3
random.shuffle(todos_nomes_masc)
random.shuffle(todos_nomes_fem)
idx_m = idx_f = 0

membros = []
for i, faixa in enumerate(faixas_lista):
    genero = random.choices(["Masculino", "Feminino"], weights=[44, 56])[0]
    if genero == "Masculino":
        nome = todos_nomes_masc[idx_m % len(todos_nomes_masc)]
        idx_m += 1
    else:
        nome = todos_nomes_fem[idx_f % len(todos_nomes_fem)]
        idx_f += 1

    nascimento = gerar_nascimento(faixa)

    # Membros mais velhos tendem a ser mais ativos
    if faixa == "adulto":   prob_ativo = 0.90
    elif faixa == "idoso":  prob_ativo = 0.85
    elif faixa == "crianca":prob_ativo = 0.95
    else:                   prob_ativo = 0.75

    membros.append({
        "Nome Completo":     nome,
        "Data de Nascimento":nascimento.strftime("%d/%m/%Y"),
        "Gênero":            genero,
        "Bairro":            random.choice(BAIRROS),
        "Telefone":          f"(82) 9{random.randint(1000,9999)}-{random.randint(1000,9999)}",
        "Membro Ativo":      "Sim" if random.random() < prob_ativo else "Não",
        "Data de Cadastro":  (date.today() - timedelta(days=random.randint(0, 730))).strftime("%d/%m/%Y"),
    })

df = pd.DataFrame(membros)
df.to_csv("dados_membros.csv", index=False, encoding="utf-8-sig")

# Relatório de geração
print(f"✅ {len(df)} membros gerados\n")
df["_nasc"] = pd.to_datetime(df["Data de Nascimento"], dayfirst=True)
df["Idade"] = df["_nasc"].apply(lambda d: date.today().year - d.year - ((date.today().month, date.today().day) < (d.month, d.day)))

print("Distribuição por gênero:")
print(df["Gênero"].value_counts().to_string())
print()
print("Distribuição por faixa etária:")
def fx(i):
    if i<13: return "Crianças"
    if i<18: return "Jovens"
    if i<30: return "Jovens adultos"
    if i<60: return "Adultos"
    return "Idosos"
df["Faixa"] = df["Idade"].apply(fx)
print(df["Faixa"].value_counts().to_string())
print()
print("Ativos vs Inativos:")
print(df["Membro Ativo"].value_counts().to_string())
print()
print(f"Idade média: {df['Idade'].mean():.1f} anos")
print(f"Aniversários este mês: {(pd.to_datetime(df['Data de Nascimento'], dayfirst=True).dt.month == date.today().month).sum()}")
