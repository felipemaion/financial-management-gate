from urllib import request, parse
import json
import re

# https://github.com/bcfurtado/calculadoradocidadao
url='https://calculadoradocidadao.herokuapp.com/corrigirpelaselic'

def corrigir_selic(valor, data_inicial, data_final):
    if str(valor)[-3] == ".":
        valor_corr = str(valor).replace(".",",")

# Corrige para poder trabalhar com número negatívo
    valor_corr = valor_corr.replace(",",".")
    if float(valor_corr) < 0:
        valor_corr = valor_corr.replace("-","")
    valor_corr = valor_corr.replace(".",",")

    values = {'dataInicial': str(data_inicial),
            'dataFinal': str(data_final),
            'valorCorrecao': str(valor_corr)}

    data = parse.urlencode(values).encode('ascii')
    try:
        req = request.Request(url, data)
        with request.urlopen(req) as response:
            # print(json.loads(response.read()))
            # re.search('(?<=\ )(.*?)(?=\ )', selic["valorCorrigido"]).group(1)
            return re.search('(?<=\ )(.*?)(?=\ )', json.loads(response.read())["valorCorrigido"]).group(1).replace(".","").replace(",",'.')
    except:
        print("Erro ao corrigir valor selic: {}, data_inicial: {}, data_final: {}".format(valor, data_inicial, data_final))
        return {"valorCorrigido": "R$ {} <erro>".format(valor)} 
        

