from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import CustomUserManager
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


GENDER_CHOICE = (
    ('male', 'MALE'),
    ('female', 'FEMALE'),
    ('other', 'OTHER')
)


def user_profile(instance, filename):
    """  create media file folder with name create"""
    print("filename: ", filename)
    return "/user_profile/{}/{}".format(instance.name, filename)


class User(AbstractUser):
    """Admin/User table
    """
    username = None
    # override username and email(unique)
    name = models.CharField(max_length=100, blank=False)
    email = models.EmailField(max_length=200, unique=True)
    gender = models.CharField(max_length=200, choices=GENDER_CHOICE, blank=True)
    attachment_date = models.DateField(auto_now_add=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=150, blank=True, null=True)
    contact = PhoneNumberField(unique=True, null=True, blank=True)
    date_of_birth = models.DateField(default=None, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='user_profile', blank=True, null=True,
                                        default='/user_profile/default_image/default-user-photo-79.jpg')

    USERNAME_FIELD = 'email'
    objects = CustomUserManager()
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

# access phonenumber_field value:-
# person = models.Person.objects.get(id = 25)
# phoneNumber = person.phoneNumber.as_e164

# contact = models.PositiveIntegerField(max_length=12, validators=[MaxValueValidator(9999999999),
#                                                                  MinValueValidator(100000000)],
#                                       blank=True, null=True)
