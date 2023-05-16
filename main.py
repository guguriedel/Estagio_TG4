from typing import List
from pydantic import BaseModel #Criar o tipo estrutrado
from fastapi import FastAPI     #Usar o fastAPI


app = FastAPI()

#Tipo estruturado de uma comissao
class Comissao(BaseModel):
    vendedor: int
    data: str
    valor: float

#Definindo a lista com as metas de cada mes
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


#Função para calcular pedidos de bonus
def pedidos(pedidos):
    comissoes = []
    vendedores = []
    #Lista para armazenar os pedidos e não perder a referencia
    #conforme se avança com o for

    #percorrer as metas salvando o mes e a qtd referencia
    for meta in metas:
        mes = meta["mes"]
        qtd_ref = meta["qtd"]
        qtd = 0
        #Contador de vendas
        tot_bonus = 0
        #Defino bonus como 0 para evitar erros

        for pedido in pedidos:
            data = int(pedido.data.split("-")[1])
            #Transformo a str da data em um numero referente ao mes

            #Comparações para definir a qtd de bonus de acordo com a regra
            if data == mes:
                if pedido.valor <= 300:
                    bonus = (pedido.valor) * 0.01
                elif pedido.valor > 1000:
                    bonus = (pedido.valor) * 0.05
                else:
                    bonus = (pedido.valor) * 0.03

                tot_bonus += bonus


                #
                if qtd == qtd_ref:
                    #Lista que registra todos os vendedores ja analisados
                    if pedido.vendedor not in vendedores:
                        vendedores.append(pedido.vendedor)
                        qtd+=1
                    #Caso um vendedor ja tenha feito uma venda ele foi add na lista
                    else:
                        qtd+=1
                    #Checa se a qtd de pedidos é equivalente ao minimo para receber o bonus
                else:
                    #Acrescento o bonus por qtd de vendas
                    tot_bonus += pedido.valor * 0.03
                    #Corto o loop
                    qtd = -1


#é imp definir o tot_bonus como 0 para evitar que o if
#seja feito com uma variavel não iniciada
        if tot_bonus:
            #Checo se a comissão é nula
            comissoes.append({"vendedor": pedido.vendedor, "mes": mes, "valor": tot_bonus})
            #Desse modo adiciono apenas comissões não nulas na lista

    return comissoes


@app.post("/api/calc_comissao")
def calc_comissao(pedido: list[Comissao]):
    comissoes = pedidos(pedido)
    return {"comissoes": comissoes}
