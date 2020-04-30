from django.db import models
from django.utils.translation import ugettext as _
from account.models import User


class Wallet(models.Model):
    user = models.ForeignKey(User, related_name="user_wallet", on_delete=models.CASCADE)
    description = models.TextField(_("Description"), max_length=80)

    def __str__(self):
        return "{}:{}".format(self.user, self.description)
    class Meta:
        verbose_name = _("Wallet")
        verbose_name_plural = _("Wallets")
        unique_together = [['user', 'description']]

