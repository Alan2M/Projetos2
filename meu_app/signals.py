from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Aluno


@receiver(pre_save, sender=Aluno)
def guarda_status_antigo(sender, instance, **kwargs):
    if instance.pk:
        instance._old_status = sender.objects.get(pk=instance.pk).status


@receiver(post_save, sender=Aluno)
def notifica_mudanca_status(sender, instance, created, **kwargs):
    old = getattr(instance, "_old_status", None)
    if old and old != instance.status:
        assunto = mensagem = ""
        if instance.status == Aluno.Status.CONFIRMADA:
            assunto = "Inscrição confirmada!"
            mensagem = "Sua inscrição foi confirmada. Parabéns!"
        elif instance.status == Aluno.Status.ENTREVISTA:
            assunto = "Entrevista agendada"
            dt = instance.data_entrevista.strftime("%d/%m/%Y %H:%M") if instance.data_entrevista else "a definir"
            mensagem = f"Sua entrevista está marcada para {dt}."
        elif instance.status == Aluno.Status.REJEITADA:
            assunto = "Inscrição não aprovada"
            mensagem = f"Motivo: {instance.motivo_rejeicao}"
        if assunto:
            send_mail(
                assunto,
                mensagem,
                settings.DEFAULT_FROM_EMAIL,
                [instance.email],
                fail_silently=False,
            )
