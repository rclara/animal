from django.db import models
import re
from phone_field import PhoneField

#need validations to ensure unique email in system

class UserManager(models.Manager):
    def registration_validator(self, post_data):
        errors = {}
        if len(post_data['first_name']) == 0:
            errors['first_name'] = "First name cannot be blank"
        if len(post_data['last_name']) == 0:
            errors['last_name'] = "Last name cannot be blank"

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):
            errors['last_name'] = "Invalid Email"

        if len(post_data['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        if post_data['password_confirmation'] != post_data['password']:
            errors['password_confirmation'] = "Password and password confirmation do not match"
        
        #prevent registration if account with email already exists
        if len(User.objects.filter(email=post_data['email'])) > 0:
            errors['email'] = "Email already exists"
        return errors

    def login_validator(self, post_data):
        errors = {}
        if len(User.objects.filter(email = post_data['login_email'])) ==0:
            errors['login_email'] = "Email not found"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = PhoneField(blank=True, help_text='Contact phone number')
    password = models.CharField(max_length=60)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = UserManager()
    #Pets is the 1:M relationship

class PetManager(models.Manager):
    def pet_registration_validator(self, post_data):
        errors = {}
        if len(post_data['name']) == 0:
            errors['name'] = "Pet name cannot be blank"
        if len(post_data['species']) == 0:
            errors['species'] = "Species cannot be blank"
        if len(post_data['date_of_birth']) == 0:
            errors['date_of_birth'] = "Birthday cannot be blank. Use format YYYY-MM-DD"
        return errors
    
class Pet(models.Model):
    name = models.CharField(max_length=255)
    species = models.CharField(max_length=20)
    breed = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    comments = models.TextField()
    owner = models.ForeignKey(User, related_name="pets", on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects = PetManager()