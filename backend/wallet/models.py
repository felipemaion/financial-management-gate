from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext as _
from django.core.management.base import BaseCommand, CommandError
from account.models import User
from instrument.models import Instrument, Event, PriceHistory, Dividend, ProventoFII
from core.models import BaseTimeModel
from selic.models import Selic
from datetime import datetime, timedelta
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
    def get_events(self, data=datetime.now()):
        pass

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
                    "positions":[ Position of each Instrument for this Wallet]
                    }
        """
        
        moviments = self.moviments.filter(date__lt=date, wallet=self) 
        
        # Pega apenas uma vez cada ativo:
        assets = set(mov.instrument.tckrSymb for mov in moviments)
        self.assets = assets
        # Carregar preço *atual* (?) do grupo de ativos presentes na carteira.##
        prices = self.get_prices(assets) # TODO: E SE ISSO FOR PARA O FRONT-END??? :-D
        print(prices)
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
        self.positions = []
        positions = []
        for asset in assets:
            instrument = Instrument.objects.filter(tckrSymb=asset).first()

            # Clean all Positions for this Instrument in this Wallet:
            Position.objects.filter(wallet=self,instrument=instrument).delete()
            WalletStockProvent.objects.filter(wallet=self, dividend__instrument=instrument).delete()
            WalletFIIProvent.objects.filter(wallet=self, dividend__instrument=instrument).delete()

            asset_dividends = Decimal(0.0)
            asset_price = prices[asset]
            asset_moviments = moviments.filter(instrument__tckrSymb=asset, wallet=self).order_by('date')  # de modo reverso -date
            print(f"Size of moviments: {len(asset_moviments)}")
            
            asset_investiments = 0
            asset_cost = 0
            asset_selic = 0
            asset_networth = 0
            size_asset_moviments = len(asset_moviments)

            print(f"Asset: {asset}")
            for i, moviment in enumerate(asset_moviments):
                print(i, moviment)
                #The creation of new positions for the asset begins: 
                #Começa a criação de novas posições para o ativo:
                
                if(moviment.category=='COMPRA'):
                    transaction_value=moviment.total_investment + moviment.total_costs
                    net_value = Decimal(0.0)
                else:
                    transaction_value=moviment.total_investment
                    net_value = moviment.total_investment - moviment.total_costs
                p = Position.objects.create(
                    wallet=self, # like that?
                    instrument=instrument, 
                    date=moviment.date + timedelta(days=1),
                    category=['COMPRA', 'VENDA'][moviment.category],
                    quantity=moviment.quantity,
                    transaction_value=transaction_value,
                    net_value = net_value.quantize(Decimal('.01'), rounding=ROUND_DOWN),
                    # transaction_value: Buy: Price + Costs; Sell: Price only (withou costs).
                    # net_value: # For Selling only: Total Price - Costs
                    
                    total_quantity = moviment.quantity,# Tem que ser feito depois dos eventos??
                    total_value = 0, #net_value.quantize(Decimal('.01'), rounding=ROUND_DOWN)
                    total_selic = 0, # Total R$ corrected by the SELIC Index.  
                    position_selic = moviment.present_value(final_date=date)  
                    )
                #What will happen next? Another move? An event? Nothing?
                # O que ocorrerá depois? Mais uma movimentação? Um evento? Nada?
                if i < size_asset_moviments - 1:
                    next_event = asset_moviments[i+1].date
                else:
                    next_event = date
                events_splits = moviment.instrument.splits.filter(
                    event_date__range=[moviment.date + timedelta(days=1), next_event]).order_by('event_date')
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
                ## Now we must find all the dividends/JCP/Amortizações/Correção Selic paid:
                events_dividends = moviment.instrument.dividends.filter(
                    event_date__range=[moviment.date+timedelta(days=1), next_event]).order_by('event_date')
                print(f"Movimento da data {moviment.date+timedelta(days=1)}: {next_event}")
                print(events_dividends)
                
                for event in events_dividends:
                    category = event.category
                    d = WalletStockProvent.objects.get_or_create(
                            wallet=self, # like that?
                            dividend=event
                            
                        )
                
                events_proventosFII = moviment.instrument.proventosFII.filter(
                    ex_date__range=[moviment.date+timedelta(days=1), next_event]).order_by('ex_date')
                print(f"Movimento da data {moviment.date+timedelta(days=1)}: {next_event}")
                print(events_proventosFII)
                
                for event in events_proventosFII:
                    
                    d = WalletFIIProvent.objects.get_or_create(
                            wallet=self, # like that?
                            dividend=event
                            
                        )
            
            ## In theory all positions (buy/sell/splits/etc) for this wallet and this asset are created
            ## Now, apply the to the positions:
            ## THIS SHOULD MOVE!!! #TODO
            positions = Position.objects.filter(wallet=self, instrument=instrument).order_by("date")
            print(f"Size Positions: {len(positions)}")
            asset_quantity = 0
            for i, position in enumerate(positions):
                print(f"position {i}")
                if position.category == "COMPRA":
                    position.total_quantity = positions[i-1].total_quantity + Decimal(position.quantity) if i >= 1 else position.quantity
                    position.total_value = positions[i-1].total_value + Decimal(position.transaction_value) if i >= 1 else position.net_value
                    position.total_selic = positions[i-1].total_selic + Decimal(position.position_selic) if i >= 1 else position.position_selic
                    asset_quantity = position.total_quantity
                    print(position)
                elif position.category == "VENDA":
                    ### Vai dar ruim na venda descoberta!
                    position.total_value = (positions[i-1].total_value + position.quantity * (positions[i-1].total_value / positions[i-1].total_quantity)) if i >= 1 else position.net_value
                    position.total_quantity = positions[i-1].total_quantity + Decimal(position.quantity) if i >= 1 else position.quantity
                    position.total_selic = positions[i-1].total_selic + Decimal(position.position_selic) if i >= 1 else position.position_selic

                    asset_quantity = position.total_quantity
                elif position.category == "DESDOBRAMENTO":
                    position.total_quantity = position.quantity * positions[i-1].total_quantity
                    asset_quantity = position.total_quantity
                    position.total_value = positions[i-1].total_value
                    position.total_selic = positions[i-1].total_selic
                    position.total_dividends = positions[i-1].total_dividends
                    position.transaction_value = 0
                    position.net_value = 0
                    # position.total_value = total_value # ??
                elif position.category == "GRUPAMENTO": 
                    position.total_quantity = position.quantity * positions[i-1].total_quantity
                    asset_quantity = position.total_quantity
                    position.total_value = positions[i-1].total_value
                    position.total_selic = positions[i-1].total_selic
                    position.total_dividends = positions[i-1].total_dividends
                    position.transaction_value = 0
                    position.net_value = 0
                    
               
                else:
                    print(f"ATENÇÃO CATEGORIA NÃO RECONHECIDA!!!! Ver position: {position.category} - {position} ")


                position.total_networth = position.total_quantity * prices[asset]
                position.save()
                last_position = position
            
            provents = WalletFIIProvent.objects.filter(wallet=self, dividend__instrument=instrument)#.order_by("ex date")
            if not provents:
                provents = WalletStockProvent.objects.filter(wallet=self, dividend__instrument=instrument)#.order_by("ex date")
            print(f"Size Provents: {len(provents)}")
            asset_quantity = 0
            for i, provent in enumerate(provents):
                # pega quantidade do ativo na data do proventos. 
                quantity  = Position.objects.filter(wallet=self, instrument=instrument, date__lte=provent.dividend.ex_date).order_by("-date").first().total_quantity
                fator = Decimal(0)
                if provent.dividend.category == "JCP": 
                    fator = Decimal(0.15) # ALIQUOTA DE IR PARA JCP. Recolhido na fonte. HARDCODED??? PQP!!! FELIPE, FELIPE...TODO: ISSUE
                if provent.dividend.category == "3":
                    provent.total_value = 0
                    provent.quantity = 0
                    continue # Rendimento Subscrição TODO: Tratar disso no futuro.
                provent.total_value = (quantity * provent.dividend.value) - (quantity * provent.dividend.value) * fator
                provent.quantity = quantity
                print(f"EM {provent.dividend.ex_date}: {provent.quantity} * {provent.dividend.value} - IR ({(quantity * provent.dividend.value) * fator:.2f}) = {provent.total_value:.2f} ")
                provent.save()
            # print("-----------")
            # print(positions)
            # print("-----------")
            # last_position = positions[-1] # AHHAHA
            # print(last_position)
            self.positions.append({
                "ticker": asset,
                "quantity": last_position.total_quantity, # Será sempre INT?? Stocks dos EUA sei que não é.
                "dividends": sum([provent.total_value for provent in provents]),
                "investments": last_position.total_value,
                "costs": Decimal('.01'),
                "index_selic": last_position.total_selic,
                "networth": last_position.total_networth
                })


        
        wallet = {
            "total_networth": sum([position["networth"] for position in self.positions]),# .quantize(Decimal('.01'), rounding=ROUND_DOWN),
            "total_dividends": sum([position["dividends"] for position in self.positions]),
            "total_invested": sum([position["investments"] for position in self.positions]),
            "total_selic": sum([position["index_selic"] for position in self.positions]),
            "assets": assets,
            "moviments": moviments,
            "positions": self.positions,
            "provents": []
        }
        return wallet

    def __str__(self):
        return f"ID:{self.id} - User:{self.user} - Description:{self.description}"

    class Meta:
        verbose_name = _("Wallet")
        verbose_name_plural = _("Wallets")
        unique_together = [['user', 'description']]


class WalletStockProvent(BaseTimeModel):
    dividend = models.ForeignKey(
        Dividend, related_name="dividend", on_delete=models.CASCADE)

    wallet = models.ForeignKey(
        Wallet, related_name="wallet", on_delete=models.CASCADE)
    
    quantity = models.DecimalField('quantity', decimal_places=6, max_digits=20, null=True)
    total_value = models.DecimalField('total value', decimal_places=2, max_digits=20, null=True) # TODO Não acho q null = True seja correto, mas não sei implementar o "contador", ainda ;-)
    
    def __str__(self):
        return f"ID:{self.id} - User:{self.user} - Wallet:{self.wallet}\nQuantity:{self.quantity}"

    class Meta:
        verbose_name = _("Provent Stock")
        verbose_name_plural = _("Provents Stock")

class WalletFIIProvent(BaseTimeModel): 
    dividend = models.ForeignKey(
        ProventoFII, related_name="provento fii+", on_delete=models.CASCADE)

    wallet = models.ForeignKey(
        Wallet, related_name="wallet fii+", on_delete=models.CASCADE)
    
    quantity = models.DecimalField('quantity', decimal_places=6, max_digits=20, null=True)
    total_value = models.DecimalField('total value', decimal_places=2, max_digits=20, null=True) # TODO Não acho q null = True seja correto, mas não sei implementar o "contador", ainda ;-)
    
    class Meta:
        verbose_name = _("Provent FII")
        verbose_name_plural = _("Provents FII")
   
class Position(BaseTimeModel):
    """
        wallet: key Wallet
        instrument: key Instrument
        date: Event Date
        category: COMPRA/VENDA/DESDOBRAMENTO/GRUPAMENTO/etc 
        quantity: Quantity for the event
        total_quantity: Total quantity of the Asset in this Wallet at this date.
        transaction_value: Buy: Price + Costs; Sell: Price only (withou costs).
        total_networth: # total_quantity * current price.
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
    total_networth = models.DecimalField('current value', decimal_places=2, max_digits=20, null=True)
    total_value = models.DecimalField('total value', decimal_places=2, max_digits=20, null=True) # TODO Não acho q null = True seja correto, mas não sei implementar o "contador", ainda ;-)
    total_selic = models.DecimalField('total selic', decimal_places=2, max_digits=20, null=True)
    total_dividends = models.DecimalField('total dividends', decimal_places=9, max_digits=20, null=True)
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
        total_networth:{self.total_networth}
        total_value:{self.total_value}
        total_dividends:{self.total_dividends}
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
        return f"{{User:{self.wallet.user}@{self.wallet.description} {self.date} {('C','V')[self.category]} {self.quantity} x {self.instrument} @ R$ {self.total_investment} (costs:R${self.total_costs})}}"
