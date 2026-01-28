from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.db import transaction
from .models import UserProfile
from django import forms


class RegisterForm(forms.ModelForm):
    """Formulario de registro"""
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirmar contraseña')
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        labels = {
            'username': 'Usuario',
            'email': 'Correo electrónico',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Las contraseñas no coinciden')
        
        if User.objects.filter(username=cleaned_data.get('username')).exists():
            raise forms.ValidationError('Este usuario ya existe')
        
        if User.objects.filter(email=cleaned_data.get('email')).exists():
            raise forms.ValidationError('Este email ya está registrado')
        
        return cleaned_data


class LoginForm(forms.Form):
    """Formulario de login"""
    username = forms.CharField(label='Usuario', max_length=150)
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
    remember_me = forms.BooleanField(required=False, label='Recuérdame')


class ProfileForm(forms.ModelForm):
    """Formulario de perfil de usuario"""
    class Meta:
        model = UserProfile
        fields = ['phone', 'document_type', 'document_number', 'address', 'city', 'zipcode', 'bio', 'profile_image', 'notify_email', 'notify_sms']
        labels = {
            'phone': 'Teléfono',
            'document_type': 'Tipo de documento',
            'document_number': 'Número de documento',
            'address': 'Dirección',
            'city': 'Ciudad',
            'zipcode': 'Código postal',
            'bio': 'Biografía',
            'profile_image': 'Foto de perfil',
            'notify_email': 'Recibir notificaciones por email',
            'notify_sms': 'Recibir notificaciones por SMS',
        }
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }


@require_http_methods(["GET", "POST"])
def register(request):
    """Registro de nuevo usuario"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # Crear usuario
                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                )
                # Crear perfil
                UserProfile.objects.create(user=user)
                
                # Login automático
                login(request, user)
                messages.success(request, f'¡Bienvenido {user.first_name}!')
                return redirect('home')
    else:
        form = RegisterForm()
    
    return render(request, 'accounts/register.html', {'form': form})


@require_http_methods(["GET", "POST"])
def login_view(request):
    """Login de usuario"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido de nuevo, {user.first_name or user.username}!')
                return redirect('home')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


@require_http_methods(["GET"])
def logout_view(request):
    """Logout de usuario"""
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente')
    return redirect('home')


@require_http_methods(["GET", "POST"])
@login_required(login_url='login')
def profile(request):
    """Perfil del usuario"""
    user = request.user
    
    # Crear perfil si no existe
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(
            user=user,
            phone='',
            address='',
            city=''
        )
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado exitosamente')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    
    context = {
        'form': form,
        'user': user,
        'profile': profile,
    }
    return render(request, 'accounts/profile.html', context)
