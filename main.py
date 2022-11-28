import requests, numpy as np

def getpedidos():
    totalpddos=np.array([],int)
    FILTERS='-FILTROS PARA RESTRINGIR O RETORNO DE DADOS-'
    APIKEY='-API KEY DO SEU BLING-'
    fim=0
    page=0
    while fim==0:
        try:
            request=requests.get(f'https://bling.com.br/Api/v2/pedidos/page={page}/json/?filters={FILTERS}&apikey={APIKEY}')
            data=request.json()['retorno']['pedidos']
            for pedidos in data:
                totalpddos=np.append(totalpddos,int(pedidos['pedido']['numero']))
            page=page+1
        except Exception as e:
            print("ERROR:",e)
            fim=1
            page=page-1
    totalpddos=np.unique(totalpddos)
    print('Total Pedidos:',len(totalpddos))
    print('Total Paginas:',page)

if __name__ == "__main__":
    print("COMEÇANDO...")
    getpedidos()
    print("FINALIZADO")
    input("PRESSIONE ALGUMA TECLA PARA FINALIZAR")
    