from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext as _
from account.models import User
from instrument.models import Instrument, Event, PriceHistory
from core.models import BaseTimeModel
from selic.models import Selic
from datetime import datetime
from decimal import *
import yfinance as yf


class WalletQuerySetManager(models.Manager):
    def assets(self, asset):
        return Instrument.objects.filter(tckrSymb=asset)


class Wallet(models.Model):
    user = models.ForeignKey(
        User, related_name="wallets", on_delete=models.CASCADE)
    description = models.TextField(_("Description"), max_length=80)
    assets = []

    objects = WalletQuerySetManager()

    def get_assets(self, moviments=None):
        if not moviments:
            moviments = self.moviments.all()
        self.assets = set(mov.instrument.tckrSymb for mov in moviments)
        return self.assets

    def get_prices(self, assets=[], start=datetime.now(), end=datetime.now()):
        # FIX ASSETS (Hey this seems wrong...)
        if assets == []:
            assets = self.get_assets()
        print("Prices for", assets)
        # assets = [asset + ".SA" for asset in assets] # so para o yfinances
        prices = {}
        for asset in assets:
            prices[asset] = PriceHistory.objects.filter(
                instrument__tckrSymb=asset).latest('date').adj_close
        return prices

    def position(self, date=datetime.now()):
        """
        Should return the Position of the Wallet, i.e:
                    {
                    "total_networth": Sum of all current value of the assets
                    "total_dividends": Sum of the total amount of provents (JCP + Div + Rent) of all Assets
                    "total_invested": Sum of the amount of money invested. Without correction of value.
                    "total_selic": Sum of the amout of money invested corrected by the interest rate SELIC
                    "assets": List of the assests in the Wallet
                    "moviments": All the moviments in this Wallet 
                    "positions":positions[asset] = {
                                        "quantity": qt_total for this asset in this wallet, 
                                        "dividends": total dividends for this asset in this wallet, 
                                        "investments": total_investments made in this asset in this wallet, 
                                        "sum_costs": total_costs, 
                                        "index_selic":total invested corrected by selic index}
                    }
        """
        
        moviments = self.moviments.all()
        assets = set(mov.instrument.tckrSymb for mov in moviments)
        self.assets = assets
        # Carregar preço atual do grupo ##
        prices = self.get_prices(assets)
        # print(prices)
        wallet = {
            "total_networth": Decimal(0.0),
            "total_dividends": Decimal(0.0),
            "total_invested": Decimal(0.0),
            "total_selic": Decimal(0.0),
            "assets": assets,
            "moviments": moviments,
            "positions": {}
        }
        total_networth = Decimal(0.0)
        total_dividends = Decimal(0.0)
        total_invested = Decimal(0.0)
        total_selic = Decimal(0.0)
        positions = []
        for asset in assets:
            asset_ticker = asset
            asset_dividends = Decimal(0.0)
            # Instrument.objects.filter(tckrSymb=asset)[0].get_price()
            asset_price = prices[asset]
            # positions[asset] = {"quantity": 0, "dividends": 0,
            #                    "investments": 0.00, "sum_costs": 0.00, "index_selic": 0.0}
            asset_moviments = moviments.filter(instrument__tckrSymb=asset).order_by(
                'date')  # de modo reverso -date
            asset_quantity = 0
            asset_investiments = 0
            asset_cost = 0
            asset_selic = 0
            asset_networth = 0
            # earliest_mov = asset_moviments.earliest('date')
            print("Asset:", asset)
            for moviment in asset_moviments:
                # quantidade inicial no movimento:
                print(f"Applying events to the moviment: {moviment}")
                qt = moviment.quantity
                asset_investiments += moviment.total_investment
                asset_cost += moviment.total_costs
                asset_selic += moviment.present_value()
                dividends = 0
                # Pega os eventos depois do movimento:
                events = moviment.instrument.events.all().filter(
                    event_date__gte=moviment.date).order_by('event_date')
                # agora o looping nos eventos que se aplicam para esse movimento:
                print(
                    "Event Date \t \t Dividends \t Splits \t Total Dividends \t Posição para Movimentação")
                for event in events:
                    # Read events for this asset:
                    event_date = event.event_date
                    div_per_share = event.dividends
                    split_per_share = event.stock_splits

                    if split_per_share != 0.0:
                        # if asset == "LCAM3": print(qt," x",split_per_share)
                        qt *= split_per_share
                    if div_per_share != 0:
                        dividends += qt*div_per_share
                    print(
                        f"Event:\t{event_date} \t {div_per_share} \t {split_per_share} ->\t {qt*div_per_share:.2f} \t \t {qt:.2f}")
                asset_dividends += dividends
                asset_quantity += qt

                asset_networth += asset_quantity * asset_price
            positions.append({
                "ticker": asset_ticker,
                "quantity": int(asset_quantity), # Será sempre INT?? Stocks dos EUA sei que não é.
                "dividends": asset_dividends.quantize(Decimal('.01'), rounding=ROUND_DOWN),
                "investments": asset_investiments.quantize(Decimal('.01'), rounding=ROUND_DOWN),
                "costs": asset_cost.quantize(Decimal('.01'), rounding=ROUND_DOWN),
                "index_selic": asset_selic.quantize(Decimal('.01'), rounding=ROUND_DOWN),
                "networth": asset_networth.quantize(Decimal('.01'), rounding=ROUND_DOWN)
            })

            total_dividends += asset_dividends
            total_invested += asset_investiments
            total_selic += asset_selic
            total_networth += asset_networth
            print(f"\n{asset}: {asset_quantity:.2f} * {asset_price:.2f} = NetWorth R$ {asset_quantity * asset_price:.2f}; Total Dividends Received: R$ {asset_dividends:.2f}")
        # print(positions[asset])
        # print('Quantidade', positions[asset]['quantity'])
        # print('Proventos Recebidos', positions[asset]['dividends'])
        # print('Total Investido', positions[asset]['investments'] + positions[asset]['sum_costs'])
        # print('Patrimônio Atual', Decimal(asset_price)*positions[asset]['quantity']) ## PODE DEMORAR PARA PEGAR O PREÇO ONLINE!
        # its ok
        wallet = {
            "total_networth": total_networth.quantize(Decimal('.01'), rounding=ROUND_DOWN),
            "total_dividends": total_dividends.quantize(Decimal('.01'), rounding=ROUND_DOWN),
            "total_invested": total_invested.quantize(Decimal('.01'), rounding=ROUND_DOWN),
            "total_selic": total_selic.quantize(Decimal('.01'), rounding=ROUND_DOWN),
            "assets": assets,
            "moviments": moviments,
            "positions": positions
        }
        return wallet

    def __str__(self):
        return "{}:{}".format(self.user, self.description)

    class Meta:
        verbose_name = _("Wallet")
        verbose_name_plural = _("Wallets")
        unique_together = [['user', 'description']]


class Position(BaseTimeModel):
    wallet = models.ForeignKey(
        Wallet, related_name="wallet_position", on_delete=models.CASCADE)
    positions = {}  # {'MGLU3':{"quantity":100, "total_investment":16000}}
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

    def present_value(self, final_date=None):
        return Selic().present_value(self.total_investment, self.date, final_date=final_date)

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
