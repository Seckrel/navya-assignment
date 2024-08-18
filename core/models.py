from django.db import models, IntegrityError
from django.db.utils import OperationalError
import uuid
import time
import hashlib


class Transaction(models.Model):
    transaction_id = models.TextField(
        null=False, blank=False, unique=True, editable=False)
    name = models.CharField(max_length=255, null=False, blank=False,)
    phone = models.CharField(max_length=10, null=False, blank=False)
    email = models.EmailField(null=True, blank=True)
    transaction_date = models.DateField(auto_now_add=True, editable=False)
    transaction_status = models.BooleanField(default=False)

    def __generate_rnd_tnx_id(self) -> str:
        """
        Combines uuid4 with UNIX EPOC to generate sha256 digest
        8 bytes of the hash will be used to generate transaction id

        Returns:
            str: transaction id in the format of integer prefiexed by TNX
        """
        uuid4 = uuid.uuid4()
        epoch_time = int(time.time())
        combined_string = f"{uuid4}{epoch_time}"

        # Hash the combined string using SHA256
        hashed = hashlib.sha256(combined_string.encode()).digest()
        hashed_int = int.from_bytes(hashed[:8], byteorder='big')
        return f"TXN{hashed_int}"

    def save(self, *args, **kwargs):
        '''
        custom __generate_rnd_tnx_id method can handle 2^64 (i.e. 64 bit integer) unique ids.
        To furthure any collision, max_attemps of 10 is used.
        '''
        if not self.transaction_id:
            max_attempts = 10

            for attempt in range(max_attempts):
                try:
                    self.transaction_id = self.generate_rnd_tnx_id()
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
