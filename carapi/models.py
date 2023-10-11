from django.db import models

# Create your models here.

class User(models.Model):
    nome = models.CharField ('Nome',max_length=100)
    sobrenome = models.CharField ('Sobrenome',max_length=100)
    email = models.EmailField('Email',max_length=150, unique=True)
    data_nascimento = models.DateField ('Data Nascimento', blank=True, null=True)

    def __str__(self):
        return self.nome

class Carro(models.Model):
    id= models.AutoField(primary_key=True)
    nome = models.CharField ('Nome',max_length=40)
    marca = models.CharField ('Marca',max_length=10, blank= True, null = True)
    modelo = models.CharField ('Modelo',max_length=40)
    preco = models.DecimalField ('Preco',decimal_places=2, max_digits=15, blank= True, null = True)
    kilometro = models.IntegerField('Kilometro', blank= True, null = True)
    imagem = models.ImageField ('IMG', blank=False, null=False, upload_to="core")
    tempo_post =  models.DateTimeField(auto_now_add=True)
    tags=models.SlugField()
    is_active= models.BooleanField(default=True)
    usuario = models.ForeignKey (User,
    null=True, 
    blank=True, 
    on_delete=models.SET_NULL,
    related_name="usuarios_produto",)
    

    def __str__(self) -> str:
        return super().__str__()