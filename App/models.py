from django.contrib.gis.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    class Meta:
        verbose_name = "user profile"
        verbose_name_plural = "user profiles"

    owner = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    last_location = models.PointField(
        srid=4326,
        null=True
    )
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.owner.email


class County(models.Model):
    class Meta:
        verbose_name_plural = "Counties"

    nuts1 = models.CharField(max_length=3)
    nuts1name = models.CharField(max_length=10)
    nuts2 = models.CharField(max_length=4)
    nuts2name = models.CharField(max_length=30)
    nuts3 = models.CharField(max_length=5)
    nuts3name = models.CharField(max_length=20)
    county = models.CharField(max_length=2)
    countyname = models.CharField(max_length=35)
    male2011 = models.FloatField()
    female2011 = models.FloatField()
    total2011 = models.FloatField()
    ppocc2011 = models.FloatField()
    unocc2011 = models.FloatField()
    hs2011 = models.FloatField()
    vacant2011 = models.FloatField()
    pcvac2011 = models.FloatField()
    total_area = models.FloatField()
    land_area = models.FloatField()
    createdate = models.CharField(max_length=10)
    geogid = models.CharField(max_length=10)
    geom = models.MultiPolygonField(srid=29903)

    def __str__(self):
        return self.countyname

    @property
    def computed_area(self):
        return self.geom.area / 1000000

    @property
    def pop_density(self):
        return self.total2011 / self.land_area


class ElectoralDivision(models.Model):
    nuts1 = models.CharField(max_length=3)
    nuts1name = models.CharField(max_length=10)
    nuts2 = models.CharField(max_length=4)
    nuts2name = models.CharField(max_length=30)
    nuts3 = models.CharField(max_length=5)
    nuts3name = models.CharField(max_length=20)
    county = models.CharField(max_length=2)
    countyname = models.CharField(max_length=35)
    csoed = models.CharField(max_length=15)
    osied = models.CharField(max_length=15)
    edname = models.CharField(max_length=80)
    male2011 = models.FloatField()
    female2011 = models.FloatField()
    total2011 = models.FloatField()
    ppocc2011 = models.FloatField()
    unocc2011 = models.FloatField()
    hs2011 = models.FloatField()
    vacant2011 = models.FloatField()
    pcvac2011 = models.FloatField()
    total_area = models.FloatField()
    land_area = models.FloatField()
    createdate = models.CharField(max_length=10)
    geogid = models.CharField(max_length=100)
    highered = models.IntegerField()
    geom = models.MultiPolygonField(srid=29903)

    def __str__(self):
        return self.edname

    @property
    def computed_area(self):
        return self.geom.area / 1000000

    @property
    def pop_density(self):
        return self.total2011 / self.land_area


class SmallArea(models.Model):
    nuts1 = models.CharField(max_length=3)
    nuts1name = models.CharField(max_length=10)
    nuts2 = models.CharField(max_length=4)
    nuts2name = models.CharField(max_length=30)
    nuts3 = models.CharField(max_length=5)
    nuts3name = models.CharField(max_length=20)
    county = models.CharField(max_length=2)
    countyname = models.CharField(max_length=35)
    csoed = models.CharField(max_length=15)
    osied = models.CharField(max_length=15)
    edname = models.CharField(max_length=80)
    small_area = models.CharField(max_length=65)
    male2011 = models.FloatField()
    female2011 = models.FloatField()
    total2011 = models.FloatField()
    ppocc2011 = models.FloatField()
    unocc2011 = models.FloatField()
    hs2011 = models.FloatField()
    vacant2011 = models.FloatField()
    pcvac2011 = models.FloatField()
    createdate = models.CharField(max_length=10)
    geogid = models.CharField(max_length=255)
    geom = models.MultiPolygonField(srid=29903)

    def __str__(self):
        return self.small_area

    @property
    def computed_area(self):
        return self.geom.area / 1000000

    @property
    def pop_density(self):
        return self.total2011 / self.computed_area


@receiver(post_save, sender=get_user_model())
def save_user_profile(sender, instance, **kwargs):
    try:
        profile = UserProfile.objects.get(owner=instance)
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(owner=instance)
    profile.save()

