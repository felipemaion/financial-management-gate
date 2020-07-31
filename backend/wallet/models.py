from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext as _
from django.core.management.base import BaseCommand, CommandError
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

class msg:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    SUCCESS = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    

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
            try:
                prices[asset] = PriceHistory.objects.filter(
                    instrument__tckrSymb=asset).latest('date').adj_close
                print(msg.SUCCESS + 'Price ok for: '+ asset + msg.ENDC)
            except:
                try: 
                    instrument = Instrument.objects.filter(tckrSymb=asset)
                    events_origin = instrument.populate_events()
                except:
                    print(msg.ERROR + 'Error Getting price for ' + asset + msg.ENDC)
            # o try vai ficar aqui mesmo
                try:
                    if not events_origin.empty:
                        for index, event in events_origin.iterrows():  # como pega apenas a data (id) da scrita no terminal
                            Event.objects.get_or_create(
                                instrument=instrument,
                                event_date=index.strftime("%Y-%m-%d"),
                                dividends=event['Dividends'],
                                stock_splits=event['Stock Splits']
                            )
                        print(msg.SUCCESS + 'Criado ' + asset + msg.ENDC)
                            
                except:
                    print(msg.ERROR + 'Error Getting ' + asset + ' at db. \nTry to update assets list from B3' + msg.ENDC)
                    prices[asset] = Decimal(0.00)
                    pass
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
                    "positions":[ Position(wallet)]
                    }
        """
        
        moviments = self.moviments.all()
        assets = set(mov.instrument.tckrSymb for mov in moviments)
        self.assets = assets
        # Carregar preço *atual* (?) do grupo ##
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
            instrument = Instrument.objects.filter(tckrSymb=asset).first()
            # Clean all Positions for this Instrument in this Wallet:
            
            Position.objects.filter(wallet=self,instrument=instrument).delete()
            
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
            size_asset_moviments = len(asset_moviments)
            # earliest_mov = asset_moviments.earliest('date')
            print("Asset:", asset)
            for i, moviment in enumerate(asset_moviments):

                # Começa a criação de novas posições para o ativo:
                if(moviment.category=='COMPRA'):
                    transaction_value=moviment.total_investment + moviment.total_costs
                    net_value = Decimal(0.0)
                else:
                    transaction_value=moviment.total_investment
                    net_value = moviment.total_investment - moviment.total_costs
                p = Position.objects.get_or_create(
                    wallet=self, # like that?
                    instrument=instrument, 
                    date=moviment.date,
                    category=['COMPRA', 'VENDA'][moviment.category],
                    quantity=moviment.quantity,
                    transaction_value=transaction_value,
                    net_value = net_value.quantize(Decimal('.01'), rounding=ROUND_DOWN),
                    # transaction_value: Buy: Price + Costs; Sell: Price only (withou costs).
                    # net_value: # For Selling only: Total Price - Costs
                    
                    total_quantity = moviment.quantity,# Tem que ser feito depois dos eventos??
                    total_value = 0, #net_value.quantize(Decimal('.01'), rounding=ROUND_DOWN)
                    total_selic = 0, # Total R$ corrected by the SELIC Index.  
                    position_selic = moviment.present_value()  
                    )
                                    # O que ocorrerá depois? Mais uma movimentação? Um evento? Nada?
                if i < size_asset_moviments - 1:
                    next_event = asset_moviments[i+1].date
                else:
                    next_event = datetime.today() ## TODO PAREI AQUI... boa sorte...s
                events_splits = moviment.instrument.splits.filter(
                    event_date__range=[moviment.date, next_event]).order_by('event_date')
                for event in events_splits:
                    category = event.category
                    quantity = 1 
                    if category == 'DESDOBRAMENTO':
                        quantity = event.factor
                    elif category == 'GRUPAMENTO':
                        quantity = 1 / event.factor
                    s = Position.objects.get_or_create(
                            wallet=self, # like that?
                            instrument=instrument, 
                            date=event.ex_date,
                            category=category,
                            quantity=quantity,
                            
                        )
            ## In theory all positions (buy/sell/splits/etc) for this wallet and this asset are created
            positions = Position.objects.filter(wallet=self, instrument=instrument).order_by("date")
            for i, position in enumerate(positions):
                if position.category == "COMPRA":
                    position.total_quantity = positions[i-1].total_quantity + Decimal(position.quantity) if i > 1 else position.quantity
                    position.total_value = positions[i-1].total_value + Decimal(position.transaction_value) if i > 1 else position.net_value
                    position.total_selic = positions[i-1].total_selic + Decimal(position.position_selic) if i > 1 else position.position_selic
                    asset_quantity = position.total_quantity
                    # position.total_selic =+ 
                elif position.category == "VENDA":
                    ### Vai dar ruim na venda descoberta!
                    position.total_value = (positions[i-1].total_value + position.quantity * (positions[i-1].total_value / positions[i-1].total_quantity)) if i > 1 else position.net_value
                    position.total_quantity = positions[i-1].total_quantity + Decimal(position.quantity) if i > 1 else position.quantity
                    position.total_selic = positions[i-1].total_selic + Decimal(position.position_selic) if i > 1 else position.position_selic
                    asset_quantity = position.total_quantity
                elif position.category == "DESDOBRAMENTO":
                    position.total_quantity = position.quantity * positions[i-1].total_quantity
                    asset_quantity = position.total_quantity
                    position.total_value = positions[i-1].total_value
                    position.total_selic = positions[i-1].total_selic
                    position.transaction_value = 0
                    position.net_value = 0
                    # position.total_value = total_value # ??
                elif position.category == "GRUPAMENTO": # TODO Parei aqui.
                    position.total_quantity = position.quantity * positions[i-1].total_quantity
                    asset_quantity = position.total_quantity
                    position.total_value = positions[i-1].total_value
                    position.total_selic = positions[i-1].total_selic
                    position.transaction_value = 0
                    position.net_value = 0
                    # pass
                else:
                    pass
                position.save()



            #### AAAhhhhh
            # mov_positions = Position.objects.filter(wallet=wallet,instrument=instrument).order_by('date')
            # events_splits = mov_positions.first().instrument.splits.filter(
            #         event_date__gte=mov_positions.first().date).order_by('event_date')
            # for event in events_splits:
            #     category = event.category
            #     quantity = 1 
            #     if category == 'DESDOBRAMENTO':
            #         quantity = event.factor
            #     elif category == 'GRUPAMENTO':
            #         quantity = 1 / event.factor

            #     s = Position.objects.get_or_create(
            #         wallet=self, # like that?
            #         instrument=instrument, 
            #         date=event.ex_date,
            #         category=category
            #         quantity=quantity 
            #             )

        #         # agora o looping nos eventos que se aplicam para esse movimento:
        #         print(
        #             "Event Date \t \t Dividends \t Splits \t Total Dividends \t Posição para Movimentação")
        #         # ATIVO, Carteira, Data, Tipo, Quantidade, R$ Operação,	R$ Operação Líq., Qtd Total, R$ Total
        #         for event in events_splits:
        #             event_date = event.event_date
        #         # for event in events:
        #         #     # Read events for this asset:
        #         #     event_date = event.event_date
        #         #     div_per_share = event.dividends
        #         #     split_per_share = event.stock_splits

        #         #     if split_per_share != 0.0:
        #         #         # if asset == "LCAM3": print(qt," x",split_per_share)
        #         #         qt *= split_per_share
        #         #     if div_per_share != 0:
        #         #         dividends += qt*div_per_share
        #         #     print(
        #         #         f"Event:\t{event_date} \t {div_per_share} \t {split_per_share} ->\t {qt*div_per_share:.2f} \t \t {qt:.2f}")
        #         asset_dividends += dividends
        #         asset_quantity += qt

        #         asset_networth += qt * asset_price
        #     positions.append({
        #         "ticker": asset_ticker,
        #         "quantity": int(asset_quantity), # Será sempre INT?? Stocks dos EUA sei que não é.
        #         "dividends": asset_dividends.quantize(Decimal('.01'), rounding=ROUND_DOWN),
        #         "investments": asset_investiments.quantize(Decimal('.01'), rounding=ROUND_DOWN),
        #         "costs": asset_cost.quantize(Decimal('.01'), rounding=ROUND_DOWN),
        #         "index_selic": asset_selic.quantize(Decimal('.01'), rounding=ROUND_DOWN),
        #         "networth": asset_networth.quantize(Decimal('.01'), rounding=ROUND_DOWN)
        #     })

        #     total_dividends += asset_dividends
        #     total_invested += asset_investiments
        #     total_selic += asset_selic
        #     total_networth += asset_networth
        #     print(f"\n{asset}: {asset_quantity:.2f} * {asset_price:.2f} = NetWorth R$ {asset_quantity * asset_price:.2f}; Total Dividends Received: R$ {asset_dividends:.2f}")
        # # print(positions[asset])
        # # print('Quantidade', positions[asset]['quantity'])
        # # print('Proventos Recebidos', positions[asset]['dividends'])
        # # print('Total Investido', positions[asset]['investments'] + positions[asset]['sum_costs'])
        # # print('Patrimônio Atual', Decimal(asset_price)*positions[asset]['quantity']) ## PODE DEMORAR PARA PEGAR O PREÇO ONLINE!
        # # its ok
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
        return "ID:{} - User:{} - Description:{}".format(self.id, self.user, self.description)

    class Meta:
        verbose_name = _("Wallet")
        verbose_name_plural = _("Wallets")
        unique_together = [['user', 'description']]


class Position(BaseTimeModel):
    """
        wallet: key Wallet
        instrument: key Instrument
        date: Event Date
        category: COMPRA/VENDA/DESDOBRAMENTO/GRUPAMENTO/etc 
        quantity: Quantity for the event
        total_quantity: Total quantity of the Asset in this Wallet at this date.
        transaction_value: Buy: Price + Costs; Sell: Price only (withou costs).
        net_value: # For Selling only: Total Price - Costs
        total_value: Total R$ invested in this Asset in this Wallet at this date.
        total_selic: Total R$ corrected by the SELIC Index.
        position_selic: This position corrected by the SELIC Index.
    """

    wallet = models.ForeignKey(
        Wallet, related_name="wallet_position", on_delete=models.CASCADE)
    instrument = models.ForeignKey(
        Instrument, related_name="instrument_position", on_delete=models.CASCADE)
    date = models.DateField('date')
    category = models.CharField('category', max_length=255, null=True, blank=True)
    quantity = models.DecimalField('quantity', decimal_places=6, max_digits=20, null=True)
    total_quantity = models.DecimalField('total quantity', decimal_places=2, max_digits=20, null=True)
    transaction_value = models.DecimalField('transaction value', decimal_places=2, max_digits=20, null=True) # Compra: Preço + Custos; Venda: Preço sem custos.
    net_value = models.DecimalField('net value', decimal_places=2, max_digits=20, null=True) # Somente venda: Valor total - Custos.
    total_value = models.DecimalField('total value', decimal_places=2, max_digits=20, null=True) # TODO Não acho q null = True seja correto, mas não sei implementar o "contador", ainda ;-)
    total_selic = models.DecimalField('total selic', decimal_places=2, max_digits=20, null=True)
    position_selic = models.DecimalField('position selic', decimal_places=2, max_digits=20, null=True)
    
    def __str__(self):
        return f"""wallet:{self.wallet}
        instrument:{self.instrument}
        date:{self.date}
        category:{self.category}
        quantity:{self.quantity}
        total_quantity:{self.total_quantity}
        transaction_value:{self.transaction_value}
        net_value:{self.net_value}
        total_value:{self.total_value}
        total_selic:{self.total_selic}
        position_selic:{self.position_selic}"""

    class Meta:
        verbose_name = _("Position")
        verbose_name_plural = _("Positions")
        ordering = ['-date']
        # unique_together = [['wallet', 'instrument', 'date', 'category']]


class Moviment(BaseTimeModel):
    """
        wallet: ForeignKey
        instrument: ForeignKey
        category: (0:'BUY', 1: 'SELL')
        quantity
        total_investment
        total_costs 
        date 
    """
    TYPE_CHOICES = (
        (0, 'COMPRA'),
        (1, 'VENDA'),
    )
    wallet = models.ForeignKey(
        Wallet, related_name='moviments', on_delete=models.CASCADE)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    category = models.IntegerField(
        'category', choices=TYPE_CHOICES, blank=True, null=True)
    quantity = models.IntegerField('quantity')
    total_investment = models.DecimalField(
        'price', decimal_places=2, max_digits=10)
    total_costs = models.DecimalField(
        'costs', decimal_places=2, max_digits=10, blank=True, null=True)
    date = models.DateField('date')

    def present_value(self, final_date=None):
        factor = 1
        if self.category == 1: factor = -1
        return Selic().present_value(self.total_investment*factor, self.date, final_date=final_date)

    def save(self, *args, **kwargs):
        if self.quantity > 0:
            self.category = 0  # C
        else:
            self.category = 1  # V
        if self.total_costs == None:
            self.total_costs = 0

        super(Moviment, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.date} {('C','V')[self.category]} {self.quantity} x {self.instrument} @ R$ {self.total_investment} (costs:R${self.total_costs}) "
