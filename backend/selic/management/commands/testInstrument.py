from django.core.management.base import BaseCommand, CommandError
from aporte.models import Instrument
# o nome do comando é o nome do arquivo no caso seed excuta ai ./manage.py seed

class Command(BaseCommand):
	help = 'Criação de Dados Basicos para o funcionamento de Sistema '
	
	def handle(self, *args, **options):
		# entendeu?	
		# VOu por apenas os obrigatorios
		# Faz o makemigrations criar as tabelas 
		try:
			print('Get or create:') 
			petr= Instrument.objects.get_or_create(tckrSymb="PETR4", crpNm="exemplo") 
			print(petr[0].crpNm)
			if petr[1] == True:
				print("\tObject created.")
			else:
				print("\tObject already exists.")
			print('Get or create (again):') 
			petr = Instrument.objects.get_or_create(tckrSymb="PETR4", crpNm="exemplo") 
			if petr[1] == True:
				print("\tObject created.")
			else:
				print("\tObject already exists.")
			print(petr[0].crpNm)
			print("Updating:")
			petr = Instrument.objects.get(tckrSymb="PETR4")
			print("\tFrom:", petr.crpNm)
			petr.crpNm = "PETROLEO BRASILEIRO S.A. PETROBRAS"
			petr.save()
			petr = Instrument.objects.get(tckrSymb="PETR4")
			print("\tTo:", petr.crpNm)
			print('\tUpdated!') # Só o create não?
			print("Deleting:")
			item = Instrument.objects.get(tckrSymb="PETR4").delete() # deixa aqui comigo
			print('\tDeleted!')

			# Cria
			print("Creating:")
			um_instrumento = Instrument.objects.create(
				tckrSymb="PETR4",
			 	crpNm="exemplo"
			 )
			print('\tCreated!')

			print("Deleting:")
			item = Instrument.objects.get(tckrSymb="PETR4").delete() # deixa aqui comigo
			print('\tDeleted!')

			# pera OK. existe o get_or_create
			# Bora escrever os testes? pq ai já fica para eu saber como faz tudo! ahahah
			# Vamos criar um, editar, apagar, get_or_create, e apagar.(tá faltando algo? CRUD n)
		except:
			print('Deu eror')
# Quando cria não precisa .save()? nao ele blz.. update tbm nao se nao me engado pera ai precisa sim pensei que nao
# Entendeu
# na segunda deu errro pq ja existe.
# Poutz... eu perdi a primeira... pq estava tentando pegar os dados, pq achei q iria precisar... 
# TckrSymb	SgmtNm	MktNm	ISIN	CFICd	crpNm
# PETR4	CASH	EQUITY-CASH	BRPETRACNPR6	EPNNPR	PETROLEO BRASILEIRO S.A. PETROBRAS
#  mas peguei o q rolou... como tem q ser unique deu erro... e para mudar o mktNm?
# do que ja foi cadastrado isso?
#  sim... colocar "PETROLEO BRASILEIRO S.A. PETROBRAS" agora
		self.stdout.write(self.style.SUCCESS('Executou'))