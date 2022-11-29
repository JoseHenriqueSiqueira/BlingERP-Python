import requests, numpy as np

#Obter Informações sobre os pedidos
def getpedidos(apikey):
    FILTERS="FILTROS" #Filtros para restringir o retorno de dados (Tipos de filtros na documentação da API do BLING)
    totalpddos=np.array([],int)
    fim=0
    page=1
    while fim==0: #Esse loop é necessário, pois a API do BLING retorna 100 linhas por REQUEST. Esse loop funcionara até retornar todos os pedidos em todas as paginas.
        try:
            #Caso nao queria adicionar filtros, substitua a URL para "f'https://bling.com.br/Api/v2/pedidos/page={page}/json/?apikey={apikey}'" 
            request=requests.get(f'https://bling.com.br/Api/v2/pedidos/page={page}/json/?apikey={apikey}')
            data=request.json()['retorno']['pedidos']
            for pedidos in data:
                totalpddos=np.append(totalpddos,int(pedidos['pedido']['numero'])) #Obtendo o número de cada pedido
            page=page+1
        except:
            fim=1
            page=page-1
    totalpddos=np.unique(totalpddos) #Filtrando Pedidos por único CLIENTE.
    print(f'Total Pedidos:{len(totalpddos)}') #Quantidade de pedidos
    print(f'Total Paginas:{page}\n') #Total de páginas percorridas.

#Obter Informações sobre os produtos
def getproducts(apikey):
    codigos=np.array([])
    estoques=np.array([],int)
    fim=0
    page=1
    while fim==0:
        try:
            request=requests.get(f'https://bling.com.br/Api/v2/produtos/page={page}/json/?apikey={apikey}&estoque=S')
            data=request.json()["retorno"]["produtos"]
            for valor in data:
                codigos=np.append(codigos,valor['produto']['codigo'])#Obtendo o 'codigo' de cada produto
                estoques=np.append(estoques,valor['produto']['estoqueAtual'])#Obtendo o 'Estoque Atual' de cada produto
            page=page+1
        except:
            fim=1
            page-page-1
    for sku,estoque in zip(codigos,estoques):#Loop percorrendo os valores em 'Codigos' e 'Estoques'
        print(f'SKU:{sku}')#Imprimindo SKU
        print(f'ESTOQUES:{estoque}\n')#Imprimindo Estoque
    print(f'Total Paginas:{page}\n')

if __name__ == "__main__":
    APIKEY=r'' #APIKEY do seu Bling
    print("OBTENDO PRODUTOS E ESTOQUE...\n")
    getpedidos(APIKEY)
    print("OBTENDO TOTAL DE VENDAS...\n")
    getproducts(APIKEY)
    input("\nPRESSIONE ALGUMA TECLA PARA FINALIZAR")