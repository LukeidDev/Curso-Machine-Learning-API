# Construir a API --> Flask
from flask import Flask, request
import joblib
import sqlite3
from datetime import datetime


# Instanciar o Aplicativo
Aplicativo = Flask(__name__)

#--------------CARREGANDO MODELO-------------
# carregar modelo
Modelo = joblib.load('Modelo_Floresta_Aleatorio_v100.pkl')


#------------------- FUNÇÃO DA API-------------
# Função para receber nossa API
@Aplicativo.route('/API_Preditivo/<area>;<rooms>;<bathroom>;<parking_spaces>;<floor>;<animal>;<furniture>;<hoa>;<property_tax>', methods=['GET'])
def funcao_01( area, rooms, bathroom, parking_spaces, floor, animal, furniture, hoa, property_tax ):

    # Data inicial
    Data_Inicio = datetime.now()

    # Recebendo os inputs da API
    Lista = [
        float(area), float(rooms), float(bathroom), float(parking_spaces), 
        float(floor), float(animal), float(furniture), float(hoa), float(property_tax)
    ]

    #Tentar a previsão
    try:

        # Predict
        Previsao = Modelo.predict( [Lista] )

        # Inserir o valor da Previsão
        Lista.append( str(Previsao) )

        # Concatenando lista
        Input = ''
        for valor in Lista:
            Input = Input + ';' + str(valor)

        # Final do processamento
        Data_Final = datetime.now()
        Processamento = Data_Final - Data_Inicio

        #----------------------- CONEXÃO BANCO DE DADOS ------------
        #criar a conexão com o banco de dados
        Conexão_Banco = sqlite3.connect('Banco_Dados_API.db')
        cursor = Conexão_Banco.cursor()

        # query 
        Query_inserindo_dados = f''' 

        INSERT INTO Log_API ( Inputs, Inicio, Fim, Processamento )
        VALUES ( '{Input}',  '{Data_Inicio}', '{Data_Final}', '{Processamento}')
        '''

        # Executar a query
        cursor.execute( Query_inserindo_dados )
        Conexão_Banco.commit()

        cursor.close()

        # Retorno do modelo
        return {'valor_aluguel': str(Previsao), 'Inicio': f'{Data_Inicio}', 'Final': f'{Data_Final}', 'Processamento': f'{Processamento}'}
    except:
        return {'Aviso': 'Deu algum erro!'}

if __name__ == '__main__':
    Aplicativo.run( debug=True )