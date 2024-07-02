from django.db import models

class Veicolo(models.Model):
    numero_telaio = models.CharField(max_length=17)
    marca = models.CharField(max_length=100)
    modello = models.CharField(max_length=100)
    data_produzione = models.DateField()

    def __str__(self):
        return f"{self.marca} {self.modello} ({self.numero_telaio})"

class Targa(models.Model):
    targa = models.CharField(max_length=17)
    data_emissione = models.DateField()
    stato = models.CharField(max_length=100)
    data_restituzione = models.DateField()

    def __str__(self):
        return f"{self.targa} {self.data_emissione} ({self.stato})"

class TargaAttiva(models.Model):
    numero_telaio = models.CharField(max_length=17)
    marca = models.CharField(max_length=100)
    modello = models.CharField(max_length=100)
    data_produzione = models.DateField()

    def __str__(self):
        return f"{self.marca} {self.modello} ({self.numero_telaio})"

class TargaRestituita(models.Model):
    numero_telaio = models.CharField(max_length=17)
    marca = models.CharField(max_length=100)
    modello = models.CharField(max_length=100)
    data_produzione = models.DateField()

    def __str__(self):
        return f"{self.marca} {self.modello} ({self.numero_telaio})"

class Revisione(models.Model):
    targa = models.CharField(max_length=17)
    numero_revisione = models.CharField(max_length=17)
    data_revisione = models.DateField()
    stato = models.CharField(max_length=100)
    motivazione = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.numero_revisione} {self.data_revisione} ({self.stato})"
