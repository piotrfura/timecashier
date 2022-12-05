from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class OrganizationAddress(models.Model):
    street = models.CharField(max_length=100, blank=True, null=True)
    number = models.CharField(max_length=10, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)


class OrganizationUser(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)


class OrganizationUserRole(models.Model):
    ADMIN = 1
    REGULAR = 2
    ROLES = ((ADMIN, "Administrator"), (REGULAR, "Użytkownik"))
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    role = models.PositiveSmallIntegerField(choices=ROLES)
