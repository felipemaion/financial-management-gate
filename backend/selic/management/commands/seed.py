from django.core.management.base import BaseCommand, CommandError
from aporte.models import Instrument
import pandas as pd
# o nome do comando é o nome do arquivo no caso seed excuta ai ./manage.py seed

class Command(BaseCommand):
	help = 'Criação de Dados Basicos para o funcionamento de Sistema '
	
	def handle(self, *args, **options):

		# try:
		# df = pd.read_csv("InstrumentsConsolidatedFile_20200424_1.csv", sep=";", encoding='latin',
		# 				 iterator=True, low_memory=False,
		# 				 chunksize=10000,
		# 				 usecols = ["TckrSymb","CrpnNm", "RptDt", "ISIN", "TradgCcy", "MktCptlstn"])
		# for i in df:
		# 	print(i)

		df = pd.read_csv("InstrumentsConsolidatedFile_20200424_1.csv", sep=";", encoding='latin', low_memory=False)

		for index, row in df.iterrows():
			print(index, row['TckrSymb'], row['ISIN'])
		# print(df.loc[df['TckrSymb'] == "AFCR11"])
		# está dando erro com utf-8
		# print(df.loc[df['TckrSymb'] == "AFCR11"]['CrpnNm'])
		# except:
		# 	print('Deu eror')

		self.stdout.write(self.style.SUCCESS('Executou'))