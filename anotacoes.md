# git add .  - prepara todos os arquivos modificados para enviar
# git commit -m "descrição do que você mudou"   - savepoint do projeto com uma descrição
# git push   - envia para o github

from urllib.parse import urlparse
import requests

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


def verificar_headers(url):
    if not validar_url(url):
        return
    # tratamento de segurança para caso a URL não existir ou estiver fora do ar.
    try:
        # armazena o que o servidor retornar ao método GET requisitado.
        # requests.get retorna um objeto do tipo Response.
        # timeout de 10 segundos para o código não ficar esperando para sempre.
        resposta = requests.get(url, timeout=10)
    except requests.exceptions.RequestException as e:
        # print na tela caso dê erro de requisição
        print(f"Erro ao conectar em {url}:   {e}")
        return

    # são dicionários armazenados no objeto Response, que o método requests.get retorna.
    headers = resposta.headers
    presentes = 0  # contador de headers que foram encontrados

    print(f"\n{'='*60}")
    print(f"\nAnalisando: {url}")
    print(f"Status: {resposta.status_code}\n")
    print(f"\n{'='*60}")

    # iteração em cima do dicionário headers_seguranca
    for header, risco in headers_seguranca.items():
        if headers.get(header):
            print(f"   OK         {header}")
            # se tiver um header OK (header presente), o contador aumenta em 1
            presentes += 1
        else:
            print(f"   AUSENTE    {header}")
            # risco encontrado logo abaixo do header ausente respectivo.
            print(f"              {risco}\n")

    nota = calcular_nota(len(headers_seguranca), presentes)

    print(
        f"\nNota de segurança: {nota}   ({presentes}/{len(headers_seguranca)})  ")
    print(f"\n{'='*60}")


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

# partes = urlparse("https://google.com/search?q=python")

# partes.scheme   #https
# partes.netloc   #google.com
# partes.path     #/search
# partes.query    #q=python


verificar_headers("google.com")  # sem protocolo
verificar_headers("https://")  # sem dominio
verificar_headers("https://google.com")  # válida
