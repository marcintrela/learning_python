from django.db import models

# Create your models here.


class Room(models.Model):
    name = models.CharField(max_length=128)
    capacity = models.IntegerField()
    projector = models.BooleanField(default=True)

    def __str__(self):
        return 'Sala {} o pojemności {} projector {}'.format(self.name, self.capacity, self.projector)


class Reservation(models.Model):
    surname = models.CharField(max_length=64)
    description = models.TextField()
    date = models.DateField(null=False)
    room = models.ForeignKey(Room)

    def __str__(self):
        return 'Rzerwujący : {} na dzień: {}. Temat spotkania: {}'.format(self.surname, self.date, self.description)


