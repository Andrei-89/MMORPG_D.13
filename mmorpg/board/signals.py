from django.db.models.signals import post_save
from django.dispatch import receiver  # импортируем нужный декоратор
from .models import Post, Response, User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция,
# и в отправители надо передать также модель
@receiver(post_save, sender=Response)
def notify_post_author(sender, instance, created, **kwargs):
        link = f"http://127.0.0.1:8000/board/private/responseview/?response_id={str(instance.id)}"
        user = User.objects.get(pk = instance.responsePost.postUser.pk)

        if created:
            html_content = render_to_string('board/new_response_send.html', {'response': instance, "user": user, "link": link, })

            msg = EmailMultiAlternatives(
                subject=f'Добавлен отклик к объявлению с заголовком:{instance.responsePost.title} от {instance.responseUser}',
                body=instance.text,
                from_email='bulanov-rvp@yandex.ru',
                to=[user.email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()