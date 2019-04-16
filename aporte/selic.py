from urllib import request, parse
import json
# https://github.com/bcfurtado/calculadoradocidadao
url='https://calculadoradocidadao.herokuapp.com/corrigirpelaselic'

def corrigir_selic(valor, data_inicial, data_final):
    if str(valor)[-3] == ".":
        valor = str(valor).replace(".",",")
    values = {'dataInicial': str(data_inicial),
            'dataFinal': str(data_final),
            'valorCorrecao': str(valor)}

    data = parse.urlencode(values).encode('ascii')
    try:
        req = request.Request(url, data)
        with request.urlopen(req) as response:
            return json.loads(response.read())
    except:
        print("Erro ao corrigir valor selic: {}, data_inicial: {}, data_final: {}".format(valor, data_inicial, data_final))
        return {"valorCorrigido": "R$ {} <erro>".format(valor)} 
        

