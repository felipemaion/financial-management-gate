from django.core.management.base import BaseCommand, CommandError
from selic.models import Selic


# o nome do comando é o nome do arquivo no caso seed excuta ai ./manage.py seed

class Command(BaseCommand):
	help = 'Criação de Dados Basicos para o funcionamento de Sistema '
	
	def handle(self, *args, **options):
		selic = Selic()
		selic.update_me()  # Essa call deveria rodar uma vez por dia. Cron no servidor?

		