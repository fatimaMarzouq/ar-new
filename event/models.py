from django.db import models
import uuid
# from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import get_user_model
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from django_better_admin_arrayfield.models.fields import ArrayField
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

User = get_user_model()


class Asset(models.Model,DynamicArrayMixin):

    id = models.UUIDField(
        primary_key=True,
        # db_index=True,  # new
        default=uuid.uuid4,
        editable=False)
    user = models.ForeignKey(
        User,
        default=1,
        on_delete=models.CASCADE,
    )

    # Multi_Locations = ArrayField(
    #     ArrayField(
    #         models.CharField(max_length=100, null=True),size=2,
    #     ),
    #     null=True,
    #     size=255
    # )
    longitude1 = ArrayField(
        models.CharField(max_length=100, null=True), size=2,
        null=True,

    )
    latitude1 = ArrayField(
        models.CharField(max_length=100, null=True), size=2,
        null=True,

    )
    Expiry_date = models.DateField(null=True)
    Expiry_time = models.TimeField(null=True)
    multi_uploads = ArrayField(
        models.FileField(blank=True, upload_to="covers/"),
        null=True,

    )
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True,null=True)

    def save(self, *args,**kwargs):
        qrcode_img = qrcode.make("https://mighty-garden-90398.herokuapp.com/"+str(self.id)+"/assets_details")
        canvas = Image.new('RGB',(450,450),'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.id}.png'
        buffer = BytesIO()
        canvas.save(buffer, 'png')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        # self.do_something_to_invoice()
        super().save(*args, **kwargs)

    # def do_something_to_invoice(self):
    #     location, _ = Location.objects.update_or_create(visit=self.id,defaults={ "patient": self.patient, "professional" = self.professional})

    # def __str__(self):
    #     return self.Longitude

    def get_absolute_url(self):
        return reverse('Assets_list')


class Location(models.Model):
    id = models.UUIDField(
        primary_key=True,
        # db_index=True,  # new
        default=uuid.uuid4,
        editable=False)
    # user = models.ForeignKey(
    #     User,
    #     default=1,
    #     on_delete=models.CASCADE,
    # )
    # Name = models.CharField(max_length=200)
    Longitude1 = models.CharField(max_length=100, null=True)
    Latitude1 = models.CharField(max_length=100, null=True)
    # Google_maps_link = models.CharField(max_length=200)
    # Plus_code = models.CharField(max_length=200)
    # Radius = models.DecimalField(null=True, max_digits=10, decimal_places=5)
    # Events = models.ForeignKey(
    #     Event,
    #     on_delete=models.CASCADE,
    #     null=True,
    #     related_name='Events',
    # )
    Assets = models.ManyToManyField(Asset , null=True)
    # qr_code = models.ImageField(upload_to='qr_codes/', blank=True,null=True)


    def __str__(self):
        return self.Longitude1+" , "+self.Latitude1

    def get_absolute_url(self):
        return reverse('location_list')

    # def save(self, *args,**kwargs):
    #     qrcode_img = qrcode.make("https://mighty-garden-90398.herokuapp.com/"+str(self.id)+"/assets_details")
    #     canvas = Image.new('RGB', (350, 350), 'white')
    #     canvas.paste(qrcode_img)
    #     fname = f'qr_code-{self.name}.png'
    #     buffer = BytesIO()
    #     canvas.save(buffer, 'PNG')
    #     self.qr_code.save(fname, File(buffer), save=False)
    #     canvas.close()
    #     super().save(*args, **kwargs)


class Event(models.Model):
    id = models.UUIDField(
        primary_key=True,
        # db_index=True,  # new
        default=uuid.uuid4,
        editable=False)
    Name = models.CharField(max_length=200)
    Photo = models.ImageField(upload_to='covers/', blank=True,null=True)
    starting_date = models.DateField(null=True)
    ending_date = models.DateField(null=True)
    user = models.ForeignKey(
        User,
        default=1,
        on_delete=models.CASCADE,
    )
    Locations = models.ManyToManyField(Location)
    Assets = models.ManyToManyField(Asset)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True,null=True)

    def __str__(self):
        return self.Name

    def get_absolute_url(self):
        return reverse('events')

    def save(self, *args,**kwargs):
        qrcode_img = qrcode.make("https://mighty-garden-90398.herokuapp.com/"+str(self.id)+"/event_details")
        canvas = Image.new('RGB',(290,290),'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.id}.png'
        buffer = BytesIO()
        canvas.save(buffer, 'png')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)


