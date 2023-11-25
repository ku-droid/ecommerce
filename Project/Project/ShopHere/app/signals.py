from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import Customer

@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    try:
        customer = Customer.objects.get(user=user)
        
        # Store the customer ID in the session
        request.session['custid'] = customer.id
        
    except Customer.DoesNotExist:
        pass  # Handle the case when no corresponding Customer object exists
