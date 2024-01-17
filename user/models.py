from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        email =email.lower()
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_realtor(self, email, name, password=None):
        user = self.create_user(email, name, password)
        user.is_realtor = True
        user.save(using=self._db)
        return user
        

    def create_superuser(self, email, name, password=None):
        user = self.create_user(email, name, password)
        
        user.is_staff =  True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    

    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=161, unique=True)
    name = models.CharField(max_length=161)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_realtor = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email
    
    
# class Tenant(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
#     document_proofs = models.TextField(blank=True)

#     def __str__(self):
#         return self.user.name
    
# class Tenant(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, blank=True)
#     document_proofs = models.TextField(blank=True)
#     agreement_end_date = models.DateField(null=True, blank=True)
#     monthly_rent_date = models.IntegerField(null=True, blank=True)

#     def __str__(self):
#         return self.user.name