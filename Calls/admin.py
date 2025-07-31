from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import Setor, Posto_grad, StatusChamado, PrioridadeChamado, CategoriaChamado, MensagemChamado

User = get_user_model()

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informações Militares', {
            'fields': ('nome_de_guerra', 'setor', 'posto_grad'),
        }),
    )

    list_display = ('username', 'nome_de_guerra', 'setor', 'posto_grad', 'is_staff', 'is_superuser')
    search_fields = ('username', 'nome_de_guerra', 'setor__nome', 'posto_grad__nome')
    list_filter = ('is_staff', 'is_superuser', 'setor', 'posto_grad')
    

# Registra também os modelos relacionados
@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')


@admin.register(Posto_grad)
class PostoGradAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    
@admin.register(StatusChamado)
class StatusChamadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'data_status')
    
@admin.register(PrioridadeChamado)
class PrioridadeChamadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'prioridade')
    
@admin.register(CategoriaChamado)
class CategoriaChamadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'categoria')
    
@admin.register(MensagemChamado)
class MensagemChamadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'mensagem')
