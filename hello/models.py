from django.db import models 

class Veicolo(models.Model):
    numero_telaio = models.CharField(max_length=17, primary_key=True)
    marca = models.CharField(max_length=100)
    modello = models.CharField(max_length=100)
    data_produzione = models.DateField()

    def __str__(self):
        return f"{self.marca} {self.modello} ({self.numero_telaio})"

class Targa(models.Model):
    targa = models.CharField(max_length=17, primary_key = True)
    data_emissione = models.DateField()

    def __str__(self):
        return f"{self.targa} {self.data_emissione})"

class TargaAttiva(models.Model):
    targa= models.OneToOneField(Targa, on_delete=models.CASCADE, primary_key=True)
    numero_telaio = models.OneToOneField(Veicolo, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.marca} {self.modello} ({self.numero_telaio})"

class TargaRestituita(models.Model):
    targa = models.OneToOneField(Targa, on_delete=models.CASCADE, primary_key=True)
    numero_telaio = models.OneToOneField(Veicolo, on_delete=models.CASCADE)    
    data_restituzione = models.DateField()

    def __str__(self):
        return f"{self.marca} {self.modello} ({self.numero_telaio})"

class Revisione(models.Model):
    id = models.AutoField(primary_key=True)
    targa = models.ForeignKey(Targa, on_delete=models.CASCADE)
    numero_revisione = models.CharField(max_length=17)
    data_revisione = models.DateField()
    stato = models.CharField(max_length=100)
    motivazione = models.CharField(max_length=100, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['targa', 'numero_revisione'], name='unique_targa_numero_revisione')
        ] 
    def __str__(self):
        return f"{self.numero_revisione} {self.data_revisione} ({self.stato})"
