from django.core.management.base import BaseCommand, CommandError
from wallet.models import Wallet, Moviment
from instrument.models import Instrument

from account.models import User
from selic.models import Selic

import pandas as pd
# o nome do comando é o nome do arquivo no caso seed excuta ai ./manage.py seed

class Command(BaseCommand):
	help = 'Criação de Dados Basicos para o funcionamento de Sistema '
	
	def handle(self, *args, **options):
		self.populateInstrument(*args, **options)
		self.walletFullTest(*args, **options)
		selic = Selic()
		selic.update_me()  # Essa call deveria rodar uma vez por dia. Cron no servidor?

		


	def populateInstrument(self, *args, **options):
		'''
		populateInstrument tries to populate the db using an csv file named: InstrumentsConsolidatedFile_20200424_1.csv
		'''
				# For quick reference:
		# all_fields = ["RptDt", "TckrSymb", "Asst", "AsstDesc", "SgmtNm", "MktNm", "SctyCtgyNm", "XprtnDt", "XprtnCd",
		# 			  "TradgStartDt", "TradgEndDt", "BaseCd", "ConvsCritNm", "MtrtyDtTrgtPt", "ReqrdConvsInd", "ISIN", "CFICd",
		# 			  "DlvryNtceStartDt", "DlvryNtceEndDt", "OptnTp", "CtrctMltplr", "AsstQtnQty", "AllcnRndLot", "TradgCcy",
		# 			  "DlvryTpNm", "WdrwlDays", "WrkgDays", "ClnrDays", "RlvrBasePricNm", "OpngFutrPosDay", "SdTpCd1",
		# 			  "UndrlygTckrSymb1", "SdTpCd2", "UndrlygTckrSymb2", "PureGoldWght", "ExrcPric", "OptnStyle", "ValTpNm",
		# 			  "PrmUpfrntInd", "OpngPosLmtDt", "DstrbtnId", "PricFctr", "DaysToSttlm", "SrsTpNm", "PrtcnFlg", "AutomtcExrcInd",
		# 			  "SpcfctnCd", "CrpnNm", "CorpActnStartDt", "CtdyTrtmntTpNm", "MktCptlstn", "CorpGovnLvlNm"]

		# db_fields = [tckrSymb, sgmtNm, mktNm, sctyCtgyNm, isin, cFICd, crpnNm, corpGovnLvlNm]
		print("Populating Instruments:")
		file_name = "InstrumentsConsolidatedFile_20200424_1.csv"
		print("Opening CSV File:")
		try:
			df = pd.read_csv(file_name, sep=";", encoding='latin', low_memory=False)
			print(df.head())
			self.stdout.write(self.style.SUCCESS('Success loading file.'))
		except:
			self.stdout.write(self.style.ERROR('Not able to load file: ' + file_name))

		csv_fields = ["TckrSymb", "SgmtNm", "MktNm", "SctyCtgyNm", "ISIN", "CFICd", "CrpnNm", "CorpGovnLvlNm"]
		acoes = df.loc[df["SgmtNm"]=="CASH"]
		info = acoes[csv_fields] # [2203 rows x 8 columns]
		print("Trying to populate Instrument's into database:")
		try:
			for id, row in info.iterrows():
				new_data = Instrument.objects.create(
					tckrSymb = row[csv_fields[0]],
					sgmtNm = row[csv_fields[1]], 
					mktNm = row[csv_fields[2]],
					sctyCtgyNm = row[csv_fields[3]],
					isin = row[csv_fields[4]],
					cFICd = row[csv_fields[5]],
					crpnNm = row[csv_fields[6]],
					corpGovnLvlNm = row[csv_fields[7]]
				)
			# print("Sucesso!!")
			self.stdout.write(self.style.SUCCESS('Instruments populated.'))
		except:
			print("Error seeding Instruments into database. \n\tIs it populated already?")
			self.stdout.write(self.style.ERROR('Error populating Instruments. Is it populated already?'))
	
	def walletFullTest(self, *args, **options):
		print("Testing Wallet and Moviments:")
		print("\tGetting user 1 to create Wallet:")
		### Atenção que esse User no caso é o Maion - ERROR
		user = list(User.objects.all())[0] 
		## Checar para não criar carteira para um usuário aleatório:
		if user.email != "felipe.maion@gmail.com": raise ValueError("Not able to get correct User for walletFullTest.")

		self.stdout.write(self.style.SUCCESS("User: OK - User.name: " + user.username))

		print("\tTrying to get or create Wallet:")
		wallet = Wallet.objects.get_or_create(user=user, description="On Demand")[0] # Pega ou cria a carteira 
		self.stdout.write(self.style.SUCCESS("Wallet: OK - Wallet.description: " +  wallet.description))

		print("\tTrying to open file :")
	
		file_name = "output.xlsx"
		
		try:
			df = pd.read_excel(file_name)
			print(df)
			self.stdout.write(self.style.SUCCESS('Success loading file.'))
		except:
			self.stdout.write(self.style.ERROR('Not able to load file: ' + file_name))

		print("\tTrying to populate Moviments's into database:")
		try:
			for id, row in df.iterrows():
				ativo = Instrument.objects.get(tckrSymb=row["ATIVO"])
				data = row["DATA"]
				quantidade = row["QUANTIDADE"]
				total_investment = row["VALOR"]
				operacao = Moviment(instrument=ativo, wallet=wallet, date=data, quantity=quantidade, total_investment=total_investment)
				print(operacao.instrument)
				operacao.save()
			self.stdout.write(self.style.SUCCESS('Success populating Moviments into the Wallet.'))
		except:
			self.stdout.write(self.style.ERROR('Not able to populate Moviments into the Wallet.'))
