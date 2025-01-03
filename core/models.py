from django.db import models, IntegrityError
from django.db.utils import OperationalError
from django.core.validators import MinValueValidator
import uuid
import time
import hashlib


class TransactionStatus(models.TextChoices):
    Pending = "pending"
    Rejected = "rejected"
    Approved = "approved"


class TransactionApprovedManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(transaction_status=TransactionStatus.Approved)


class Transaction(models.Model):
    transaction_id = models.TextField(
        null=False, blank=False, unique=True, editable=False)
    name = models.CharField(max_length=255, null=False, blank=False,)
    phone = models.CharField(max_length=10, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    amount = models.FloatField(null=False, blank=False, validators=[
                               MinValueValidator(0)])
    transaction_date = models.DateField(
        null=False, blank=False, editable=False)
    transaction_status = models.CharField(
        max_length=15, choices=TransactionStatus.choices, default=TransactionStatus.Pending)

    objects = models.Manager()
    approved = TransactionApprovedManager()

    def __str__(self) -> str:
        return f"{self.transaction_id}-{self.email}"

    def __generate_rnd_tnx_id(self) -> str:
        """
        Combines uuid4 with UNIX EPOC to generate sha256 digest
        5 bytes of the hash will be used to generate transaction id
        the method can handle 2^40 unique ids. 
        Chance of 50% collision after ~ 1,233,212 unique ids generation
        Increase default 5 bytes to reduce change of collison

        Returns:
            str: transaction id in the format of integer prefiexed by TNX
        """
        EXTRACTED_BYTES = 4
        FIXED_LENGTH = 12
        uuid4 = uuid.uuid4()
        epoch_time = int(time.time())
        combined_string = f"{uuid4}{epoch_time}"

        # Hash the combined string using SHA256
        hashed = hashlib.sha256(combined_string.encode()).digest()
        hashed_int = int.from_bytes(hashed[:EXTRACTED_BYTES], byteorder='big')
        formatted_int = f"{hashed_int:0{FIXED_LENGTH}d}"
        return f"TXNID{formatted_int}"

    def save(self, *args, **kwargs):
        '''
        To furthur any collision, max_attemps of 10 is used.
        '''

        self.email = self.email.lower()
        if not self.transaction_id:
            max_attempts = 10

            for attempt in range(max_attempts):
                try:
                    self.transaction_id = self.__generate_rnd_tnx_id()
                    super().save(*args, **kwargs)

                    break  # if successful
                except IntegrityError as e:
                    if 'unique constraint' in str(e).lower():
                        if attempt == max_attempts - 1:
                            raise IntegrityError(
                                "Failed to generate a unique transaction_id after multiple attempts.")
                        continue  # Try again with a new ID
                    else:
                        raise  # Re-raise if it's not a uniqueness issue

                except OperationalError as e:
                    # Handle potential database-level errors
                    raise OperationalError(f"Database error occurred: {e}")
        else:
            super().save(*args, **kwargs)
