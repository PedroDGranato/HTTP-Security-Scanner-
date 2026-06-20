import requests

def verificar_headers(url):
    #tratamento de segurança para caso a URL não existir ou estiver fora do ar.
    try: 
        #armazena o que o servidor retornar ao método GET requisitado.
        #requests.get retorna um objeto do tipo Response.
        resposta = requests.get(url, timeout=10)  #timeout de 10 segundos para o código não ficar esperando para sempre.
    except requests.exceptions.RequestException as e:
        print(f"Erro ao conectar:   {e}") #print na tela caso dê erro de requisição
        return
    
    headers = resposta.headers #são dicionários armazenados no objeto Response, que o método requests.get retorna.

    #listando os headers que serão procurados
    headers_seguranca = [
        "Strict-Transport-Security", #garante que o navegador sempre use HTTPS.
        "X-Frame-Options",  #impede que o site seja carregado em iframe
        "X-Content-Type-Options", #impede o navegador de tentar adivinhar o tipo de um arquivo
        "Content-Security-Policy", #define de onde o site pode carregar recursos
        "Referrer-Policy"
    ]

    print(f"\nAnalisando: {url}") 
    print(f"Status: {resposta.status_code}\n")

    for header in headers_seguranca:
        if headers.get(header):
            print(f"   OK         {header}") 
        else:
            print(f"   AUSENTE    {header}")

verificar_headers("https://linkedin.com")
verificar_headers("https://google.com")
verificar_headers("https://netflix.com")
