from django.db import models
from django.core.mail import send_mail, mail_admins, send_mass_mail


class Documento(models.Model):
    num_doc = models.CharField(max_length=50)

    def __str__(self):
        return self.num_doc


class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.IntegerField()
    salary = models.DecimalField(max_digits=5, decimal_places=2)
    bio = models.TextField()
    photo = models.ImageField(upload_to='clients_photos', null=True, blank=True)
    doc = models.OneToOneField(Documento, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        permissions = (
            ('deletar_clientes', 'Deletar clientes'),
        )

    @property
    def nome_completo(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def save(self, *args, **kwargs):
        from django.template.loader import render_to_string

        data = {'cliente': self.first_name}
        plain_text = render_to_string('clientes/emails/novo_cliente.txt', data)
        html_email = render_to_string('clientes/emails/novo_cliente.html', data)
        send_mail(
            'Novo cliente cadastrado.',
            plain_text,
            'testelisa9@gmail.com',
            ['testelisa9@gmail.com'],
            html_message=html_email,
            fail_silently=False,
        )
        mail_admins(
            'Novo cliente cadastrado.',
            plain_text,
            html_message=html_email,
            fail_silently=False,
        )
        message1 = (
        'Subject here', 'Here is the message', 'testelisa9@gmail.com', ['testelisa9@gmail.com', 'testelisa9@gmail.com']
        )
        message2 = (
            'Another Subject', 'Here is another message', 'testelisa9@gmail.com', ['testelisa9@gmail.com']
        )
        send_mass_mail((message1, message2), fail_silently=False)
        super().save(args, **kwargs)

