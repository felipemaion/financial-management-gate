from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext as _
from account.models import User
from instrument.models import Instrument, Event
from core.models import BaseTimeModel
from datetime import datetime
from decimal import Decimal


class WalletQuerySetManager(models.Manager):
    def assets(self, asset):
        return Instrument.objects.filter(tckrSymb=asset)


class Wallet(models.Model):
    user = models.ForeignKey(
        User, related_name="wallets", on_delete=models.CASCADE)
    description = models.TextField(_("Description"), max_length=80)
    assets = []

    objects = WalletQuerySetManager()

    def position(self, date=datetime.now()):
        """
        Should return the Position, i.e:
        ASSETS = [{INTRUMENT QUANTITY PAID/INSTRUMENT CurrentPRICE/INSTRUMENT PL(=QTD*CurrPRICE)}]
        VALUE = $ (sum(ASSETS[PL]))
        """

        moviments = self.moviments.all()
        assets = set(mov.instrument.tckrSymb for mov in moviments)
        position = {}
        for asset in assets:
            dividends_total = 0
            print("Getting Online Price for", asset)
            current_price = Instrument.objects.filter(tckrSymb=asset)[0].get_price() 
            position[asset] = {"sum_quantity": 0, "sum_dividends": 0,
                               "sum_investments": 0.00, "sum_costs": 0.00}
            asset_moviments = moviments.filter(instrument__tckrSymb=asset).order_by(
                'date')  # de modo reverso -date
            qt_total = 0
            total_investments = 0
            total_costs = 0
            # earliest_mov = asset_moviments.earliest('date')
            for moviment in asset_moviments:
                # quantidade inicial no movimento:

                qt = moviment.quantity
                total_investments += moviment.total_investment
                total_costs += moviment.total_costs
                dividends = 0
                # Pega os eventos depois do movimento:
                events = moviment.instrument.events.all().filter(event_date__gte=moviment.date).order_by('event_date')
                # agora o looping nos eventos que se aplicam para esse movimento:
                for event in events:  # continua
                    div_per_share = event.dividends
                    split_per_share = event.stock_splits

                    if split_per_share != 0.0:
                        qt *= split_per_share
                    if div_per_share != 0:
                        dividends += qt*div_per_share

                dividends_total += dividends
                qt_total += qt
                position[asset] = {
                    "sum_quantity": qt_total, "sum_dividends": dividends_total, "sum_investments": total_investments, "sum_costs": total_costs}
                # print(position[asset])
        print('Quantidade', position[asset]['sum_quantity'])
        print('Proventos Recebidos', position[asset]['sum_dividends'])
        print('Total Investido', position[asset]['sum_investments'] + position[asset]['sum_costs'])
        print('Patrimônio Atual', Decimal(current_price)*position[asset]['sum_quantity']) ## PODE DEMORAR PARA PEGAR O PREÇO ONLINE!
        # its ok
        return position

        # for mov in moviments_asset:
        #     events = mov.instrument.events.all()
        #     print('Events')
        #     print(events)

        return events  # TODO

    def __str__(self):
        return "{}:{}".format(self.user, self.description)

    class Meta:
        verbose_name = _("Wallet")
        verbose_name_plural = _("Wallets")
        unique_together = [['user', 'description']]


class Position(BaseTimeModel):
    wallet = models.ForeignKey(
        Wallet, related_name="wallet_position", on_delete=models.CASCADE)
    position = {}  # {'MGLU3':{"quantity":100, "total_investment":16000}}
    assets = []
    quantities = []
    total_investments = []


class Moviment(BaseTimeModel):

    TYPE_CHOICES = (
        (0, 'COMPRA'),
        (1, 'VENDA'),
    )
    wallet = models.ForeignKey(
        Wallet, related_name='moviments', on_delete=models.CASCADE)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    type = models.IntegerField(
        'type', choices=TYPE_CHOICES, blank=True, null=True)
    quantity = models.IntegerField('quantity')
    total_investment = models.DecimalField(
        'price', decimal_places=2, max_digits=10)
    total_costs = models.DecimalField(
        'costs', decimal_places=2, max_digits=10, blank=True, null=True)
    date = models.DateField('date')

    def save(self, *args, **kwargs):
        if self.quantity > 0:
            self.type = 0  # C
        else:
            self.type = 1  # V
        if self.total_costs == None:
            self.total_costs = 0

        super(Moviment, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.date} {('C','V')[self.type]} {self.quantity} x {self.instrument} @ R$ {self.total_investment} (costs:R${self.total_costs}) "
