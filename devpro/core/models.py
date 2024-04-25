from django.db import models
from django.urls import reverse
from django.utils.timezone import localdate
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from devpro.core.tenant import get_current_tenant, is_default_tenant


class TenantManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset()
        tenant = get_current_tenant()
        if tenant and not is_default_tenant(tenant):
            queryset = queryset.filter(library=tenant)

        return queryset

    def bulk_create(self, objs, *args, **kwargs):
        tenant = get_current_tenant()
        if tenant and not is_default_tenant(tenant):
            for obj in objs:
                obj.library = tenant

        return super().bulk_create(objs, *args, **kwargs)


class TenantModel(models.Model):
    library = models.ForeignKey(
        "core.Library",
        on_delete=models.PROTECT,
        null=True,
    )

    objects = TenantManager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk:
            tenant = get_current_tenant()
            if tenant and not is_default_tenant(tenant):
                self.library = tenant

        super().save(*args, **kwargs)


class Author(TenantModel):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name

    def to_dict(self):
        return {"id": self.id, "name": self.name}


class Book(TenantModel):
    name = models.CharField(max_length=128)
    edition = models.PositiveSmallIntegerField()
    publication_year = models.PositiveSmallIntegerField()
    authors = models.ManyToManyField(Author, related_name="books")
    available = models.BooleanField(default=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return f"{self.name} | {self.library}"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "edition": self.edition,
            "publication_year": self.publication_year,
            "authors": list(self.authors.values_list("id", flat=True)),
        }

    def get_absolute_url(self):
        return reverse("core:read-update-delete-book", kwargs={"pk": self.id})


class Borrow(TenantModel):
    user = models.ForeignKey(
        "auth.User", related_name="borrows", on_delete=models.PROTECT
    )
    book = models.ForeignKey(Book, related_name="borrows", on_delete=models.PROTECT)
    start_date = models.DateField(default=localdate)
    end_date = models.DateField()
    returned_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} | {self.book} | {self.start_date:%d/%m/%Y} - {self.end_date:%d/%m/%Y}"


class Library(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=256, unique=True)

    def __str__(self):
        return self.name


class UserProfile(TenantModel):
    user = models.OneToOneField(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="profile",
    )

    def __str__(self):
        return f"{self.user.email} -> {self.library}"


@receiver(post_save, sender=User)
def create_profile(instance, created, *args, **kwargs):
    if created:
        UserProfile.objects.create(
            user=instance,
            library=get_current_tenant(),
        )
