from django.db import models, IntegrityError
from django.db.utils import OperationalError


class Transaction(models.Model):
    transaction_id = models.TextField(null=False, blank=False, unique=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    phone = models.CharField(max_length=10, null=False, blank=False)
    email = models.EmailField(null=True, blank=True)
    transaction_date = models.DateField(auto_now_add=True)
    transaction_status = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        '''
        custom generate_random_tnx_id psql function can handle 2^64 (i.e. 64 bit integer) unique ids.
        To furthure any collision, max_attemps of 10 is used.
        '''
        if not self.transaction_id:
            max_attempts = 10

            for attempt in range(max_attempts):
                try:
                    self.transaction_id = Transaction.objects.raw(
                        'SELECT generate_random_tnx_id() AS id')[0].id
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
