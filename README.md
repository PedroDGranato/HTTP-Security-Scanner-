# HTTP Security Scanner

Scanner de segurança web em Python que analisa os headers HTTP de resposta de um site e identifica vulnerabilidades de configuração.

## Funcionalidades do Projeto

O script faz uma requisição HTTP para uma URL informada e verifica se os principais headers de segurança estão presentes na resposta do servidor. Cada header ausente representa uma vulnerabilidade real que pode ser explorada por atacantes.

## Importância

Muitos sites, inclusive grandes empresas, não configuram corretamente os headers de segurança HTTP. Essa falha abre brechas para ataques como:

- **Clickjacking**: quando `X-Frame-Options` está ausente
- **XSS (Cross-Site Scripting)**: quando `Content-Security-Policy` está ausente
- **Interceptação de conexão (MITM)**: quando `Strict-Transport-Security` está ausente
- **Vazamento de URLs sensíveis**: quando `Referrer-Policy` está ausente
- **Execução de arquivos maliciosos**: quando `X-Content-Type-Options` está ausente

## Headers verificados na requisição

| Header | O que protege |
|--------|--------------|
| `Strict-Transport-Security` | Garante que o navegador sempre use HTTPS, nunca HTTP puro |
| `X-Frame-Options` | Impede que o site seja carregado em iframe de outro site (clickjacking) |
| `X-Content-Type-Options` | Impede o navegador de adivinhar o tipo de um arquivo malicioso |
| `Content-Security-Policy` | Define de onde o site pode carregar recursos — defesa contra XSS |
| `Referrer-Policy` | Controla quanta informação é enviada ao navegar para outro site |

## Tecnologias utilizadas

- Python 3.13
- Biblioteca `requests`

## Como instalar e rodar

**1. Clone o repositório**
```bash
git clone https://github.com/seu-usuario/http-security-scanner.git
cd http-security-scanner
```

**2. Instale a dependência**
```bash
pip install requests
```

**3. Rode o scanner**
```bash
python scanner.py
```

## Exemplos de saídas

# Linkedin
```
Analisando: https://linkedin.com
Status: 200

   OK         Strict-Transport-Security
   OK         X-Frame-Options
   OK         X-Content-Type-Options
   OK         Content-Security-Policy
   AUSENTE    Referrer-Policy


# Netflix
Analisando: https://netflix.com
Status: 200

   OK         Strict-Transport-Security
   OK         X-Frame-Options
   OK         X-Content-Type-Options
   AUSENTE    Content-Security-Policy
   AUSENTE    Referrer-Policy
```
  
## Relatórios gerados

O scanner salva automaticamente um arquivo `.txt` para cada análise, com o nome seguindo este formato -> `dominio_data_hora.txt`.

![arquivos gerados](Exemplos/arquivos_gerados.png)
![conteudo do relatorio](Exemplos/relatorio_google.png)
![conteudo do relatorio](Exemplos/relatorio_linkedin.png)


## Autor

Pedro Granato — graduado em ADS pelo IFSP, estudante de cibersegurança.  
[GitHub](https://github.com/PedroDGranato)  