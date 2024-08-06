from django.db import models

# Create your models here.

class Estado(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.nome

class Projeto(models.Model):
    nome = models.CharField(max_length=100)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.nome
    
class Tarefa(models.Model):
    nome = models.CharField(max_length=100)
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.nome

class Ponto(models.Model):
    tempo = models.DurationField()
    termino = models.DateTimeField()
    tarefa = models.ForeignKey(Tarefa, on_delete=models.CASCADE)

    def __str__(self) -> str:
        # Formatar o tempo em horas e minutos
        total_seconds = int(self.tempo.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        formatted_time = f"{hours}h {minutes}m"

        # Formatar a data e hora de termino
        formatted_termino = self.termino.strftime('%d/%m/%Y %H:%M')

        return f"{formatted_termino} - {formatted_time} - {self.tarefa}"