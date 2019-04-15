from money import Money

class EUR(Money):
    def __init__(self, amount='0', currency="EUR"): # Needed to include currency on init due to __add__ function.
        if str(amount)[-3] == ",":
            amount = str(amount).replace(".","")
            amount = str(amount).replace(",",".")
        super().__init__(amount=amount, currency='EUR')

class BRL(Money):

    def __init__(self, amount='0', currency='BRL'):
        if str(amount)[-3] == ",":
            amount = str(amount).replace(".","")
            amount = str(amount).replace(",",".")
            # print(amount)
        super().__init__(amount=amount, currency='BRL')


class USD(Money):
    def __init__(self, amount='0', currency='USD'):
        if str(amount)[-3] == ",":
            amount = str(amount).replace(".","")
            amount = str(amount).replace(",",".")
        super().__init__(amount=amount, currency='USD')
