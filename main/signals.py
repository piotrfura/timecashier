import logging

from allauth.account.signals import user_logged_in
from allauth.account.signals import user_signed_up
from django.contrib.auth.models import User
from django.dispatch import receiver

from main.models import Organization
from main.models import OrganizationUser


@receiver(user_signed_up)
def create_user_organization(sender, request, user, **kwargs):
    user = User.objects.get(pk=user.id)
    organization = Organization.objects.create(name=user.username)
    OrganizationUser.objects.create(user=user, organization=organization)


@receiver(user_logged_in)
def create_user_organization_if_not_exists(sender, request, user, **kwargs):
    user = User.objects.get(pk=user.id)
    try:
        org = OrganizationUser.objects.get(user=user)
        logging.critical(f"User organization is {org}")
    except OrganizationUser.DoesNotExist:
        organization = Organization.objects.create(name=user.username)
        OrganizationUser.objects.create(user=user, organization=organization)
