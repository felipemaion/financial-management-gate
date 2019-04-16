import io
import requests
import rows

class Cotacoes:
    def __init__(self):
        self.response, self.table = self.atualizar()

    def atualizar(self):
        self.response = requests.get('https://ptax.bcb.gov.br/ptax_internet/consultarTodasAsMoedas.do?method=consultaTodasMoedas')
        self.table = rows.import_from_html(io.BytesIO(self.response.content), encoding=self.response.encoding)
#    Cod_Moeda,	Tipo,	Moeda,	Taxa_Compra,	Taxa_Venda,	Paridade_Compra,	Paridade_Venda
        # Moedas do Tipo "A":
# - Para calcular o valor equivalente em US$ (dólar americano), divida o montante na moeda consultada pela respectiva paridade.
# - Para obter o valor em R$ (reais), multiplique o montante na moeda consultada pela respectiva taxa.
        # Moedas do Tipo "B":
# - Para calcular o valor equivalente em US$ (dólar americano), multiplique o montante na moeda consultada pela respectiva paridade.
# - Para obter o valor em R$ (reais), multiplique o montante na moeda consultada pela respectiva taxa.

        return self.response, self.table
# for field_name, field_type in table.fields.items():
#     print('{} is {}'.format(field_name, field_type))

    def taxa_compra(self, moeda):
        self.atualizar()
        taxa = [row.taxa_compra for row in self.table if row.moeda==moeda]
        return taxa[0] if taxa else False

    def taxa_venda(self, moeda):
        self.atualizar()
        taxa = [row.taxa_venda for row in self.table if row.moeda==moeda]
        return taxa[0] if taxa else False