from django.db import models

# Create your models here.
SEGMENTATION_CHOICES = (
    ('0', 'Sem Segmento'),
    ('1', 'Informática'),
    ('2', 'Eletro'),
    ('3', 'Materiais de Construção'),
    ('4', 'Veterinário'),
    ('5', 'Varejo Alimentar'),
    ('6', 'Farma')
)

OPT_IN_CHOICES = (
    ('0', 'Sim'),
    ('1', 'Não')
)

CATEGORY_CHOICES = (
    ('0', 'Visitente'),
    ('1', 'Expositor'),
    ('2', 'Apoio')
)

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']


class Event(BaseModel):
    title = models.CharField(max_length=100)
    description = models.TextField()
    cep = models.CharField(max_length=17)
    public_place = models.CharField(max_length=249)
    complement = models.CharField(max_length=249, blank=True, null=True)
    neighborhood = models.CharField(max_length=80)
    city = models.CharField(max_length=80)
    state = models.CharField(max_length=80)
    number = models.IntegerField()
    first_date = models.DateField(auto_now=False)
    first_hour = models.TimeField(auto_now=False)
    last_date = models.DateField(auto_now=False)
    last_hour = models.TimeField(auto_now=False)
    qtd_registration = models.IntegerField(default=10)

    def __str__(self):
        return self.title


class Question(BaseModel):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100)
    question = models.TextField(max_length=100)
    approve = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Company(BaseModel):
    corporate_name = models.CharField(max_length=140)
    fantasy_name = models.CharField(max_length=140, blank=True, null=True)
    cnpj = models.CharField(unique=True, max_length=18)
    cep = models.CharField(max_length=17, blank=True, null=True)
    public_place = models.CharField(max_length=249, blank=True, null=True)
    complement = models.CharField(max_length=249, blank=True, null=True)
    neighborhood = models.CharField(max_length=80, blank=True, null=True)
    city = models.CharField(max_length=80, blank=True, null=True)
    state = models.CharField(max_length=80, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    phone = models.CharField(max_length=17, blank=True, null=True)
    segmentation = models.CharField(choices=SEGMENTATION_CHOICES, default='0', max_length=3)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.corporate_name


def set_default_company():
    return Company.objects.get_or_create(corporate_name='Inexistente')[0]


class Person(BaseModel):
    name = models.CharField(max_length=50)
    name_cracha = models.CharField(max_length=30)
    category = models.CharField(choices=CATEGORY_CHOICES, default='0', max_length=3)
    cpf = models.CharField(unique=True, max_length=14)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=17)
    role = models.CharField(max_length=50)
    company = models.ForeignKey(Company, on_delete=models.SET(set_default_company))
    opt_in = models.CharField(choices=OPT_IN_CHOICES, max_length=3)

    def __str__(self):
        return self.name


class Register(BaseModel):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.person.name + ' - ' + self.event.title    
    
    @property
    def checked_in(self):              
        checked_in = CheckIn.objects.filter(person=self.person).count()
        if checked_in > 0:
            return True
        else:
            return False
    @property
    def checkin(self):
        if self.checked_in:
            return "Sim"
        else:
            return "Não"    
    @property
    def status(self):
        if self.approved == True:
            return "Aprovado"
        else:
            return "Reprovado"    


class CheckIn(BaseModel):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    register = models.ForeignKey(Register, on_delete=models.CASCADE)

    def __str__(self):
        return self.person.name + ' - ' + self.event.title
        

class RafflePrizes(BaseModel):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

