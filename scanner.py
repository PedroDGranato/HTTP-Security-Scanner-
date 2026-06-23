from urllib.parse import urlparse
from datetime import datetime
import requests
import os

headers_seguranca = {
    "Strict-Transport-Security": "Risco: conexão pode ser interceptada antes de usar o protocolo HTTPS",
    "X-Frame-Options": "Risco: site pode ser carregado como iframe de outro site",
    "X-Content-Type-Options": "Risco: navegador pode executar arquivo malicioso como script",
    "Content-Security-Policy": "Risco: ausência de defesa contra injeção de código malicioso",
    "Referrer-Policy": "Risco: URLs com dados sensíveis podem vazar ao navegar para outro site",
}


def calcular_nota(total_headers, presentes):
    # Calcula a nota com base na quantidade de headers presentes
    if presentes == total_headers:
        return "A"
    elif presentes == total_headers - 1:
        return "B"
    elif presentes == total_headers - 2:
        return "C"
    elif presentes == total_headers - 3:
        return "D"
    else:
        return "F"


# verificação de url para garantir que seja uma url válida:
# * garantir que utilize os protocolos http ou https.
# * garantir que tenha um domínio

def validar_url(url):
    partes = urlparse(url)

    if partes.scheme not in ["http", "https"]:
        print("Não foi possível validar o protocolo da url inserida!")
        return False

    if not partes.netloc:  # se o domínio estiver vazio
        print("Não foi possível validar o domínio da url inserida!")
        return False

    return True


def verificar_headers(url):
    if not validar_url(url):
        return
    # tratamento de segurança para caso a URL não existir ou estiver fora do ar.
    try:
        # armazena o que o servidor retornar ao método GET requisitado.
        # timeout de 10 segundos para o código não ficar esperando para sempre.
        # requests.get retorna um objeto do tipo Response.
        resposta = requests.get(url, timeout=10)

    except requests.exceptions.RequestException as e:
        # print na tela caso dê erro de requisição
        print(f"Erro ao conectar em {url}:   {e}")
        return

    # são dicionários armazenados no objeto Response, que o método requests.get retorna.
    headers = resposta.headers
    presentes = 0  # contador de headers que foram encontrados

    dominio = urlparse(url).netloc  # pega o dominio da url
    # criando a variável de data com o horário atual
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    os.makedirs("relatorios", exist_ok=True)
    # exemplo de saída:
    nome_arquivo = os.path.join("relatorios", f"{dominio}_{timestamp}.txt")

    resultado = ""

    resultado += f"\n{'='*60}"
    resultado += f"\nAnalisando: {url}"
    resultado += f"\nStatus: {resposta.status_code}\n"
    resultado += f"{'='*60}\n"

    # iteração em cima do dicionário headers_seguranca
    for header, risco in headers_seguranca.items():
        if headers.get(header):
            resultado += f"   OK         {header}\n"
            # se tiver um header OK (header presente), o contador aumenta em 1
            presentes += 1
        else:
            resultado += f"   AUSENTE    {header}\n"
            # risco encontrado logo abaixo do header ausente respectivo.
            resultado += f"              {risco}\n"

    nota = calcular_nota(len(headers_seguranca), presentes)

    resultado += f"\nNota de segurança: {nota}   ({presentes}/{len(headers_seguranca)})  "
    resultado += f"\n{'='*60}"
    print(resultado)

    #criar o arquivo de registro/log de cada analise
    with open(nome_arquivo, "w", encoding="utf-8") as nome:
        nome.write(resultado)


while True:
    url = input("Informe a URL que deseja analisar (OU 'sair' para finalizar): ")

    if url.lower() == "sair":
        break

    verificar_headers(url)
