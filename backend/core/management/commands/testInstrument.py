from django.core.management.base import BaseCommand, CommandError
from wallet.models import Instrument
# o nome do comando é o nome do arquivo no caso seed excuta ai ./manage.py seed

class Command(BaseCommand):
	help = 'Testes Basicos para o funcionamento de Sistema '
	
	def handle(self, *args, **options):

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
			item = Instrument.objects.get(tckrSymb="PETR4").delete() 
			print('\tDeleted!')

			# Cria
			print("Creating:")
			um_instrumento = Instrument.objects.create(
				tckrSymb="PETR4",
			 	crpNm="exemplo"
			 )
			print('\tCreated!')

			print("Deleting:")
			item = Instrument.objects.get(tckrSymb="PETR4").delete() 
			print('\tDeleted!')

		except:
			print('Deu eror')

		self.stdout.write(self.style.SUCCESS('Executou'))