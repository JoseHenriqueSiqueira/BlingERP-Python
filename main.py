from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView, QProgressBar
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.uic import loadUi
from threading import Thread
import requests, numpy as np, sys

class MainWindow(QMainWindow):
    signal=pyqtSignal(list)
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi(r"UI's\MainUI.ui",self)
        self.signal.connect(self.signalResponse)
        self.btnpedidos.clicked.connect(self.btnPedidos)
        self.btnprodutos.clicked.connect(self.btnProdutos)
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(480, 10, 25, 100)
        self.pbar.setOrientation(Qt.Vertical)
    
    def btnPedidos(self,event):
        if self.getapikey.text():
            self.signal.emit(["GetPedidosStart"])
        else:
            QMessageBox.warning(self,"ATENÇÃO","O Campo 'APIKEY' não pode ficar em branco")
    #Obter Informações sobre os pedidos
    def getpedidos(self):
        APIKEY=self.getapikey.text()
        FILTERS="FILTROS" #Filtros para restringir o retorno de dados (Tipos de filtros na documentação da API do BLING)
        totalpddos=np.array([],int)
        valorvenda=np.array([],float)
        fim=0
        page=1
        while fim==0: #Esse loop é necessário, pois a API do BLING retorna 100 linhas por REQUEST. Esse loop funcionara até retornar todos os pedidos em todas as paginas.
            try:
                #Caso nao queria adicionar filtros, substitua a URL para "f'https://bling.com.br/Api/v2/pedidos/page={page}/json/?apikey={apikey}'" 
                request=requests.get(f'https://bling.com.br/Api/v2/pedidos/page={page}/json/?apikey={APIKEY}')
                try:
                    request.json()['retorno']['erros']['erro']['msg']
                    self.signal.emit(['API Key invalida'])
                    fim=1
                    return
                except:
                    data=request.json()['retorno']['pedidos']
                    for pedidos in data:
                        totalpddos=np.append(totalpddos,int(pedidos['pedido']['numero'])) #Obtendo o número de cada pedido
                        valorvenda=np.append(valorvenda,float(pedidos['pedido']['totalvenda'])) #Obtendo o valor de cada pedido
                    page=page+1
                    self.signal.emit(['ProgressBar',page])
            except:
                fim=1
                page=page-1
        totalpddos=np.unique(totalpddos)
        self.signal.emit(["GetPedidosEnd",len(totalpddos),page,valorvenda,totalpddos])

    def btnProdutos(self,event):
        if self.getapikey.text():
            self.signal.emit(["GetProdutosStart"])
            Thread(target=self.getproducts).start()
        else:
            QMessageBox.warning(self,"ATENÇÃO","O Campo 'APIKEY' não pode ficar em branco")
    #Obter Informações sobre os produtos
    def getproducts(self):
        APIKEY=self.getapikey.text()
        codigos=np.array([])
        estoques=np.array([],int)
        fim=0
        page=1
        while fim==0:
            try:
                request=requests.get(f'https://bling.com.br/Api/v2/produtos/page={page}/json/?apikey={APIKEY}&estoque=S')
                try:
                    request.json()['retorno']['erros']['erro']['msg']
                    self.signal.emit(['API Key invalida'])
                    fim=1
                    return
                except:
                    data=request.json()["retorno"]["produtos"]
                    for valor in data:
                        codigos=np.append(codigos,valor['produto']['codigo'])#Obtendo o 'codigo' de cada produto
                        estoques=np.append(estoques,valor['produto']['estoqueAtual'])#Obtendo o 'Estoque Atual' de cada produto
                    page=page+1
            except:
                fim=1
                page-page-1
        self.signal.emit(["GetProdutosEnd",codigos,estoques])

    def signalResponse(self,response):
        if response[0]=='GetPedidosStart':
            Thread(target=self.getpedidos).start()
            self.statusbar.showMessage("Obtendo informações dos pedidos...")
            self.btnpedidos.disconnect()

        if response[0]=='API Key invalida':
            self.statusbar.showMessage("Erro")
            QMessageBox.critical(self,"ERRO","API KEY Inválida")
            self.btnpedidos.clicked.connect(self.btnPedidos)
            self.btnprodutos.clicked.connect(self.btnProdutos)

        if response[0]=='GetPedidosEnd':
            self.pbar.setMaximum(response[2]+1)
            self.statusbar.showMessage("Informações dos pedidos retornadas")
            self.btnpedidos.clicked.connect(self.btnPedidos)
            self.pbar.setValue(0)
            QMessageBox.information(self,"SUCESSO",f"Total de Vendas {response[1]}")
            self.tableWidget = QTableWidget()
            self.tableWidget.setRowCount(response[1]+1)
            self.tableWidget.setColumnCount(2)
            Numero=QTableWidgetItem("NÚMERO")
            Numero.setTextAlignment(Qt.AlignCenter)
            ValorVenda=QTableWidgetItem("VALOR VENDA")
            ValorVenda.setTextAlignment(Qt.AlignCenter)
            self.tableWidget.setItem(0,0, Numero)
            self.tableWidget.setItem(0,1, ValorVenda)
            cont=1
            for value in response[4]:
                value=QTableWidgetItem(str(value))
                value.setTextAlignment(Qt.AlignCenter)
                self.tableWidget.setItem(cont,0, value)
                cont=cont+1
            cont=1
            for value in response[3]:
                value=QTableWidgetItem("R$ "+str(value))
                value.setTextAlignment(Qt.AlignCenter)
                self.tableWidget.setItem(cont,1, value)
                cont=cont+1
            cont=1
            self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
            self.tableWidget.show()

        if response[0]=='GetProdutosStart':
            self.statusbar.showMessage("Obtendo informações dos Produtos...")
            self.btnprodutos.disconnect()

        if response[0]=='GetProdutosEnd':
            self.statusbar.showMessage("Informações dos produtos retornadas")
            self.tableWidget = QTableWidget()
            self.tableWidget.setRowCount(len(response[1])+1)
            self.tableWidget.setColumnCount(2)
            Produto=QTableWidgetItem("PRODUTO")
            Produto.setTextAlignment(Qt.AlignCenter)
            Estoque=QTableWidgetItem("ESTOQUE")
            Estoque.setTextAlignment(Qt.AlignCenter)
            self.tableWidget.setItem(0,0, Produto)
            self.tableWidget.setItem(0,1, Estoque)
            cont=1
            for value in response[1]:
                value=QTableWidgetItem(value)
                value.setTextAlignment(Qt.AlignCenter)
                self.tableWidget.setItem(cont,0, value)
                cont=cont+1
            cont=1
            for value in response[2]:
                value=QTableWidgetItem(str(value))
                value.setTextAlignment(Qt.AlignCenter)
                self.tableWidget.setItem(cont,1, value)
                cont=cont+1
            self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
            self.tableWidget.show()
            self.btnprodutos.clicked.connect(self.btnProdutos)
        
        if response[0]=="ProgressBar":
            self.pbar.setMaximum(response[1]+1)
            self.pbar.setValue(response[1])

        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())