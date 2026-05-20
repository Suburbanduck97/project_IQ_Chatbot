from dotenv import load_dotenv
import google.generativeai as investIQ_gen # Importando a IA genarativa do Gemini
import requests
import os

load_dotenv()

GOOGLE_API = os.getenv('API_GEN')
api_IQ = os.getenv('API')
investIQ_gen.configure(api_key=GOOGLE_API)

# define uma saida dicionário obrigatória
def consultar_preco_cripto(nome_cripto: str) -> dict:
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

modelo = investIQ_gen.GenerativeModel(
    model_name='gemini-2.5-flash',
    tools=[consultar_preco_cripto]
)

# Iniciamos o chat 
chatIQ = modelo.start_chat(enable_automatic_function_calling=True) # precisamos entender melhor

print('===== Bem vindo ======')

while True:
    user_question = input('\nPergunte ao InvestIQ: ')

    if user_question.lower() in ['sair', 'encerar']:
        print('InvestIQ: Até logo e bons investimentos conciente!')
        break

    print('InvestIQ: (Pensando e consultando o mercado...)')

    # enviamos e recebemos a mensagem da generativa
    response_api = chatIQ.send_message(user_question)
    print(f'\nInvestIQ: {response_api.text}')