from dotenv import load_dotenv
import google.generativeai as investIQ_gen # Importando a IA genarativa do Gemini
import datetime as dt
import requests
import os

load_dotenv()

GOOGLE_API = os.getenv('API_GEN')
api_IQ = os.getenv('API')
investIQ_gen.configure(api_key=GOOGLE_API)

# define uma saida dicionário obrigatória
def consultar_preco_cripto(nome_cripto: str) -> dict:
    # Boloco de docstring = diz a generativa como e o porquê ela deve usar essa função
    """
    Busca o preço atual de uma criptomoeda em Reais (BRL).
    Use esta função sempre que o usuário perguntar o valor ou a cotação de uma criptomoeda.
    Args:
        nome_cripto: O nome da criptomoeda em minúsculo e sem espaços (ex: 'bitcoin', 'ethereum', 'solana').
    """
    url = api_IQ.replace('{nome_cripto}', nome_cripto)
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if not data:
            return {'erro': 'Criptomoeda não encontrada na base de dados.'}

        # no json da api busca a cripto pesquisada['conversão_do_valor_em_BRL']
        brl_price = data[nome_cripto]['brl']
        return {'criptomoeda':nome_cripto, 'preco_brl':brl_price}
    
    except Exception as e:
        return {'erro': f'Falha na comunicação com a API: {e}'}
      
def salvar_historico(pergunta, resposta):
    data_hora = dt.datetime.today().strftime('%d/%m/%Y %H:%M:%S')
    with open ('historico_chat.txt', 'a', encoding='utf-8') as arq:
        arq.write(f'[{data_hora}] Usuário: {pergunta}\n')
        arq.write(f'[{data_hora}] InvestIQ: {resposta}\n\n')

modelo = investIQ_gen.GenerativeModel(
    model_name='gemini-2.5-flash',
    tools=[consultar_preco_cripto],
    system_instruction= os.getenv('INSTRUCTION')
)

# Iniciamos o chat 
chatIQ = modelo.start_chat(enable_automatic_function_calling=True) 

os.system('cls || clear')
print('===== Bem vindo ======')

while True:
    user_question = input('\nPergunte ao InvestIQ: ')

    if user_question.lower() in ['sair', 'encerrar']:
        print('InvestIQ: Até logo e bons investimentos conciente!')
        break

    print('InvestIQ: (Pensando e consultando o mercado...)')

    # enviamos e recebemos a mensagem da generativa
    response_api = chatIQ.send_message(user_question)
    print(f'\nInvestIQ: {response_api.text}')

    salvar_historico(user_question, response_api.text)