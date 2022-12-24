from django.db.models.deletion import CASCADE
from accounts.models import CustomUser
from django.db import models
from django.db.models import Avg
from multiselectfield import MultiSelectField
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date
from ckeditor_uploader.fields import RichTextUploadingField
from django.template.defaultfilters import slugify

# Create your models here.

DEGREES = (
    ('10th', '10th'),
    ('12th', '12th'),
    ('UG', 'UG'),
    ('PG', 'PG'),
    ('Ph.D.', 'Ph.D.')
)

STUDY_MODES = (
    ('Part-Time', 'Part-Time'),
    ('Full-Time', 'Full-Time'),
    ('Distance Learning', 'Distance Learning')
)

EXAM_MODES = (
    ('Online', 'Online'),
    ('Offline', 'Offline'),
)

RATINGS = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
)

STATES = (
    ("Andhra Pradesh", "Andhra Pradesh"),
    ("Arunachal Pradesh", "Arunachal Pradesh"),
    ("Assam", "Assam"),
    ("Bihar", "Bihar"),
    ("Chhattisgarh", "Chhattisgarh"),
    ("Delhi", "Delhi"),
    ("Goa", "Goa"),
    ("Gujarat", "Gujarat"),
    ("Haryana", "Haryana"),
    ("Himachal Pradesh", "Himachal Pradesh"),
    ("Jammu and Kashmir ", "Jammu and Kashmir "),
    ("Jharkhand", "Jharkhand"),
    ("Karnataka", "Karnataka"),
    ("Kerala", "Kerala"),
    ("Madhya Pradesh", "Madhya Pradesh"),
    ("Maharashtra", "Maharashtra"),
    ("Manipur", "Manipur"),
    ("Meghalaya", "Meghalaya"),
    ("Mizoram", "Mizoram"),
    ("Nagaland", "Nagaland"),
    ("Odisha", "Odisha"),
    ("Punjab", "Punjab"),
    ("Rajasthan", "Rajasthan"),
    ("Sikkim", "Sikkim"),
    ("Tamil Nadu", "Tamil Nadu"),
    ("Telangana", "Telangana"),
    ("Tripura", "Tripura"),
    ("Uttar Pradesh", "Uttar Pradesh"),
    ("Uttarakhand", "Uttarakhand"),
    ("West Bengal", "West Bengal"),
    ("Andaman and Nicobar Islands", "Andaman and Nicobar Islands"),
    ("Chandigarh", "Chandigarh"),
    ("Lakshadweep", "Lakshadweep"),
    ("Puducherry", "Puducherry")
)


class EducationDetails(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    degree = models.CharField(
        max_length=5, choices=DEGREES, blank=True, null=True)
    passing_year = models.CharField(max_length=4, blank=True, null=True)
    university = models.CharField(max_length=64, blank=True, null=True)
    score = models.CharField(max_length=4, blank=True, null=True)
    stream = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'degree'], name='user_degree')
        ]
        verbose_name_plural = 'Educational Details'

    def __str__(self):

        return f'{self.degree} {self.passing_year} {self.university} {self.score} {self.stream}'


class Course(models.Model):
    name = models.CharField(max_length=64, verbose_name='Course')
    type = models.CharField(max_length=64, blank=True, null=True,
                            help_text='e.g. Under Graduate, Post Graduate, etc.')
    mode = MultiSelectField(choices=STUDY_MODES, blank=True, null=True)
    fees = models.CharField(max_length=64, blank=True, null=True)
    duration = models.CharField(max_length=4, blank=True, null=True)
    college = models.ForeignKey(
        'College', on_delete=CASCADE, related_name='courses')

    def __str__(self) -> str:
        return self.name


class Stream(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Facility(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        verbose_name_plural = 'Facilities'

    def __str__(self):
        return self.name


class College(models.Model):
    name = models.CharField(max_length=128)
    city = models.CharField(max_length=32)
    state = models.CharField(max_length=32, choices=STATES)
    stream = models.ManyToManyField(to=Stream)
    slug = models.SlugField(max_length=164, unique=True)
    established_in = models.CharField(max_length=4, null=True, blank=True)
    college_type = models.CharField(max_length=32, null=True, blank=True)
    approved_by = models.CharField(max_length=32, null=True, blank=True)
    college_ranking = models.CharField(max_length=5, null=True, blank=True)
    campus_size = models.CharField(max_length=32, null=True, blank=True)
    student_intake = models.IntegerField(null=True, blank=True)
    highest_placement = models.CharField(max_length=16, null=True, blank=True)
    avg_placement = models.CharField(max_length=16, null=True, blank=True)
    facilities = models.ManyToManyField(to=Facility, blank=True)
    summary = models.TextField(null=True, blank=True)
    logo = models.ImageField(null=True, blank=True)
    college_overall_score = models.DecimalField(
        max_digits=3, decimal_places=1, null=True, blank=True)

    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name + '-' + self.city)
        super(College, self).save(*args, **kwargs)

    def __str__(self):
        return self.name + ', ' + self.city + ', ' + self.state

    @property
    def avg_rating(self):
        return round(self.reviews.all().aggregate(Avg('ratings')).get('ratings__avg'), 1)


class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.RESTRICT)
    ratings = models.IntegerField(choices=RATINGS)
    college = models.ForeignKey(
        College, on_delete=models.CASCADE, related_name='reviews')
    comment = models.TextField()
    published_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-published_on']

    def __str__(self):
        return self.college.name + "  -- " + str(self.ratings) + "  -- " + self.comment


class Inquiry(models.Model):

    name = models.CharField(max_length=128)
    email = models.EmailField()
    contact_number = models.CharField(max_length=10)
    message = models.TextField()
    is_solved = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Inquiries"

    def __str__(self):
        return self.name


class Testimonial(models.Model):
    name = models.CharField(max_length=128)
    college_name = models.CharField(max_length=128)
    image = models.ImageField()
    message = models.TextField()


class ExamDetail(models.Model):
    name = models.CharField(max_length=128)
    exam_year = models.IntegerField(validators=[
        MinValueValidator(1984), MaxValueValidator(date.today().year + 1)])
    slug = models.SlugField(max_length=164, unique=True)
    stream = models.ManyToManyField(to=Stream)
    exam_mode = MultiSelectField(choices=EXAM_MODES)
    application_start_date = models.DateField(blank=True, null=True)
    application_end_date = models.DateField(blank=True, null=True)
    exam_start_date = models.DateField(blank=True, null=True)
    exam_end_date = models.DateField(blank=True, null=True)
    information = RichTextUploadingField(blank=True, null=True)

    class Meta:
        ordering = ['-exam_year']
        constraints = [
            models.UniqueConstraint(fields=['name', 'exam_year'], name='unique_exam')
        ]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name + '-' +  (str)(self.exam_year))
        super(ExamDetail, self).save(*args, **kwargs)

    def __str__(self):
        return self.name + " " + str(self.exam_year)
