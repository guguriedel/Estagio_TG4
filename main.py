from typing import List
from typing import Union

from fastapi import FastAPI

app = FastAPI()

def metas(mes, qtd):

    metas = [
    {"mes": 1, "qtd": 5},
    {"mes": 2, "qtd": 3},
    {"mes": 3, "qtd": 2},
    {"mes": 4, "qtd": 2},
    {"mes": 5, "qtd": 5},
    {"mes": 6, "qtd": 60},
    {"mes": 8, "qtd": 2},
    {"mes": 9, "qtd": 4},
    {"mes": 10, "qtd": 4},
    {"mes": 11, "qtd": 7},
    {"mes": 12, "qtd": 2},
]
    
    for elem in metas:
        if elem[mes] == mes and qtd >= elem[qtd]:
            return 1
    return 0


@app.post("/")
def pedidos(pedidos: dict):

    bonus = {}
    qtd = {}
    comissoes = []
    adicional = 0

    #Pego a lista dentro do dicionario "pedidos"
    pedidos = pedidos.get("pedidos", [])

    #Percorro a lst salvando os valores
    for request in pedidos:
        vendedor = request["vendedor"]
        data = request["data"]
        valor = request["valor"]
        data = int(data.split("-")[1])

    #Calcula o valor da comissão:
        if valor < 300:
            adicional = 1%valor
        elif valor > 1000:
            adicional = 5%valor
        else:
            adicional = 3%valor

    #Adiciona a comissao a cada vendedor
        if vendedor in bonus:
            bonus[vendedor] += adicional
            qtd[vendedor]+=1
        else:
            bonus[vendedor] = adicional
            qtd[vendedor] = 1

    #Calcula comissao adicional de vendas



        
        final = {"vendedor": vendedor, "mes":data, "valor": bonus[vendedor]}
        comissoes.append(final)

    return {"comissoes": comissoes }


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}