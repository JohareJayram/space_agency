from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Mission(models.Model):
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    MISSION_TYPE_CHOICES = [
        ('lunar', 'Lunar'),
        ('mars', 'Mars'),
        ('orbit', 'Earth Orbit'),
        ('deep_space', 'Deep Space'),
        ('iss', 'ISS'),
        ('satellite', 'Satellite'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    mission_type = models.CharField(max_length=20, choices=MISSION_TYPE_CHOICES, default='orbit')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    launch_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField()
    objectives = models.TextField()
    crew_count = models.IntegerField(default=0)
    agency = models.CharField(max_length=100, default='COSMOSX Agency')
    image_url = models.URLField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-launch_date']

    def __str__(self):
        return self.name


class Astronaut(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('retired', 'Retired'),
        ('training', 'In Training'),
    ]

    name = models.CharField(max_length=200)
    nationality = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    bio = models.TextField()
    missions_count = models.IntegerField(default=0)
    hours_in_space = models.FloatField(default=0.0)
    birth_date = models.DateField(null=True, blank=True)
    rank = models.CharField(max_length=100, blank=True)
    specialization = models.CharField(max_length=200, blank=True)
    image_url = models.URLField(blank=True, default='')
    missions = models.ManyToManyField(Mission, blank=True, related_name='astronauts')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Launch(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('launched', 'Launched'),
        ('delayed', 'Delayed'),
        ('scrubbed', 'Scrubbed'),
    ]

    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name='launches')
    rocket_name = models.CharField(max_length=200)
    launch_site = models.CharField(max_length=200)
    launch_datetime = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    notes = models.TextField(blank=True)
    countdown_target = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['launch_datetime']

    def __str__(self):
        return f"{self.rocket_name} - {self.mission.name}"


class NewsArticle(models.Model):
    CATEGORY_CHOICES = [
        ('mission', 'Mission Update'),
        ('research', 'Research'),
        ('technology', 'Technology'),
        ('astronaut', 'Astronaut News'),
        ('general', 'General'),
    ]

    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    summary = models.TextField()
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    image_url = models.URLField(blank=True, default='')
    related_mission = models.ForeignKey(Mission, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title


class SpacecraftGallery(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    spacecraft_type = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=200)
    first_flight = models.DateField(null=True, blank=True)
    image_url = models.URLField(blank=True, default='')
    mission = models.ForeignKey(Mission, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=300)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f"{self.user.username} ({self.role})"

    @property
    def is_admin(self):
        return self.role == 'admin'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=UserProfile)
def sync_user_staff_status(sender, instance, **kwargs):
    if instance.role == 'admin' and not instance.user.is_staff:
        instance.user.is_staff = True
        instance.user.save(update_fields=['is_staff'])
    elif instance.role != 'admin' and instance.user.is_staff:
        instance.user.is_staff = False
        instance.user.save(update_fields=['is_staff'])
