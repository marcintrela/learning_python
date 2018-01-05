from django.db import models

# Create your models here.
class Person(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Movie(models.Model):
    RATING = (
        (0, ''),
        (1, '*'),
        (2, '**'),
        (3, '***'),
        (4, '****'),
        (5, '*****'),
    )

    title = models.CharField(max_length=128)
    director = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='director')
    screenplay = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='screenplay')
    starring = models.ManyToManyField(Person, through='Role')
    year = models.IntegerField(null=True, blank=True)
    ranking = models.IntegerField(null=True, blank=True, choices=RATING)

    def __str__(self):
        return '{}, {}r.'.format(self.title, self.year)


class Role(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='role_play')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    role = models.CharField(max_length=128, null=True)

    def __str__(self):
        return '{} w {} jako {}'.format(self.person, self.movie, self.role)

