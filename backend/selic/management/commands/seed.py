from django.core.management.base import BaseCommand, CommandError
from aporte.models import Instrument
import pandas as pd
# o nome do comando é o nome do arquivo no caso seed excuta ai ./manage.py seed

class Command(BaseCommand):
	help = 'Criação de Dados Basicos para o funcionamento de Sistema '
	
	def handle(self, *args, **options):

		print("Opening CSV File:")
		df = pd.read_csv("InstrumentsConsolidatedFile_20200424_1.csv", sep=";", encoding='latin', low_memory=False)
		print(df.head())
		# For quick reference:
		# all_fields = ["RptDt", "TckrSymb", "Asst", "AsstDesc", "SgmtNm", "MktNm", "SctyCtgyNm", "XprtnDt", "XprtnCd",
		# 			  "TradgStartDt", "TradgEndDt", "BaseCd", "ConvsCritNm", "MtrtyDtTrgtPt", "ReqrdConvsInd", "ISIN", "CFICd",
		# 			  "DlvryNtceStartDt", "DlvryNtceEndDt", "OptnTp", "CtrctMltplr", "AsstQtnQty", "AllcnRndLot", "TradgCcy",
		# 			  "DlvryTpNm", "WdrwlDays", "WrkgDays", "ClnrDays", "RlvrBasePricNm", "OpngFutrPosDay", "SdTpCd1",
		# 			  "UndrlygTckrSymb1", "SdTpCd2", "UndrlygTckrSymb2", "PureGoldWght", "ExrcPric", "OptnStyle", "ValTpNm",
		# 			  "PrmUpfrntInd", "OpngPosLmtDt", "DstrbtnId", "PricFctr", "DaysToSttlm", "SrsTpNm", "PrtcnFlg", "AutomtcExrcInd",
		# 			  "SpcfctnCd", "CrpnNm", "CorpActnStartDt", "CtdyTrtmntTpNm", "MktCptlstn", "CorpGovnLvlNm"]

		# db_fields = [tckrSymb, sgmtNm, mktNm, sctyCtgyNm, isin, cFICd, crpnNm, corpGovnLvlNm]

		csv_fields = ["TckrSymb", "SgmtNm", "MktNm", "SctyCtgyNm", "ISIN", "CFICd", "CrpnNm", "CorpGovnLvlNm"]
		acoes = df.loc[df["SgmtNm"]=="CASH"]
		info = acoes[csv_fields] # [2203 rows x 8 columns]
		print("Trying to populate database:")
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
			print("Error creating Instruments into database. Is it populated already?")
			self.stdout.write(self.style.ERROR('Not able to create Instruments.'))
