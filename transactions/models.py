from django.db import models, transaction
from .utils import generate_pdf

# Create your models here.


class Transaction(models.Model):

    class Status(models.TextChoices):
        PENDING = "Pending"
        APPROVED = "Approved"
        REJECTED = "Rejected"

    transaction_id = models.CharField(
        max_length=30, primary_key=True, verbose_name="Transaction ID"
    )
    name = models.CharField(
        max_length=100, null=False, blank=False, verbose_name="Name"
    )
    phone = models.CharField(
        max_length=15, null=False, blank=False, verbose_name="Phone"
    )
    email = models.EmailField(verbose_name="Email", null=False, blank=False)
    amount = models.DecimalField(
        verbose_name="Amount", decimal_places=2, null=False, blank=False, max_digits=20
    )
    transaction_date = models.DateField(
        verbose_name="Transaction Date", null=False, blank=False
    )
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True)

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="Status",
    )

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            with transaction.atomic():
                last_transaction = (
                    Transaction.objects.select_for_update()
                    .order_by("-transaction_id")
                    .first()
                )
                if last_transaction:
                    last_id = int(last_transaction.transaction_id.replace("TXNID", ""))
                    new_id = last_id + 1
                else:
                    new_id = 1

                self.transaction_id = f"TXNID{new_id}"


        super(Transaction, self).save(*args, **kwargs)

    class Meta:
        permissions = [("can_change_transaction_status", "Can change transaction status")]

