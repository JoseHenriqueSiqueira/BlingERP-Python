import requests, numpy as np

#Obter Informações sobre os pedidos
def getpedidos():
    totalpddos=np.array([],int)
    FILTERS='FILTROS' #Filtros para restringir o retorno de dados (Tipos de filtros na documentação da API do BLING)
    APIKEY='APIKEY' #APIKEY do seu Bling
    fim=0
    page=0
    while fim==0: #Esse loop é necessário, pois a API do BLING retorna 100 linhas por REQUEST. Esse loop funcionara até retornar todos os pedidos em todas as paginas.
        try:
            #Caso nao queria adicionar filtros, substitua a URL para "f'https://bling.com.br/Api/v2/pedidos/page={page}/json/?apikey={APIKEY}'" 
            request=requests.get(f'https://bling.com.br/Api/v2/pedidos/page={page}/json/?filters={FILTERS}&apikey={APIKEY}')
            data=request.json()['retorno']['pedidos']
            for pedidos in data:
                totalpddos=np.append(totalpddos,int(pedidos['pedido']['numero'])) #Obtendo o número de cada pedido
            page=page+1
        except:
            fim=1
            page=page-1
    totalpddos=np.unique(totalpddos) #Filtrando Pedidos por único CLIENTE.
    print('Total Pedidos:',len(totalpddos)) #Quantidade de pedidos
    print('Total Paginas:',page) #Total de páginas percorridas.

if __name__ == "__main__":
    print("COMEÇANDO...")
    getpedidos()
    print("FINALIZADO")
    input("PRESSIONE ALGUMA TECLA PARA FINALIZAR")
    
