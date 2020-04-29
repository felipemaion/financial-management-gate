from django.core.management.base import BaseCommand, CommandError
from aporte.models import Instrument
import pandas as pd
# o nome do comando é o nome do arquivo no caso seed excuta ai ./manage.py seed

class Command(BaseCommand):
	help = 'Criação de Dados Basicos para o funcionamento de Sistema '
	
	def handle(self, *args, **options):
		# entendeu?	
		# VOu por apenas os obrigatorios
		# Faz o makemigrations criar as tabelas 
		# try:
		df = pd.read_csv("InstrumentsConsolidatedFile_20200424_1.csv", sep=";", encoding='latin',
						 low_memory=False, usecols = ["TckrSymb","CrpnNm"])

		print(df.loc[df['TckrSymb'] == "AFCR11"])
		# está dando erro com utf-8
		# print(df.loc[df['TckrSymb'] == "AFCR11"]['CrpnNm'])
		# except:
		# 	print('Deu eror')

		self.stdout.write(self.style.SUCCESS('Executou'))