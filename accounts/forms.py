from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


class RegisterForm(forms.ModelForm):
    """Formulario de registro"""
    password1 = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirmar contraseña')
    
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
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        # ✅ Validar fortaleza de contraseña usando Django validators
        if password1:
            from django.contrib.auth.password_validation import validate_password
            try:
                validate_password(password1)
            except forms.ValidationError as e:
                self.add_error('password1', e)
        
        # ✅ Validar que las contraseñas coincidan
        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Las contraseñas no coinciden')
        
        # ✅ Validar username único
        if User.objects.filter(username=cleaned_data.get('username')).exists():
            self.add_error('username', 'Este usuario ya existe')
        
        # ✅ Validar email único
        if User.objects.filter(email=cleaned_data.get('email')).exists():
            self.add_error('email', 'Este email ya está registrado')
        
        return cleaned_data


class LoginForm(forms.Form):
    """Formulario de login"""
    username = forms.CharField(label='Usuario', max_length=150)
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
    remember_me = forms.BooleanField(required=False, label='Recuérdame')


class ProfileForm(forms.ModelForm):
    """Formulario de perfil de usuario"""
    email = forms.EmailField(required=False, label='Correo electrónico')
    first_name = forms.CharField(required=False, max_length=150, label='Nombre')
    last_name = forms.CharField(required=False, max_length=150, label='Apellido')
    
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
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        document_type = cleaned_data.get('document_type')
        document_number = cleaned_data.get('document_number')
        
        # ✅ Validar que el email no esté en uso por otro usuario
        if email:
            existing_user = User.objects.filter(email=email).exclude(id=self.instance.user.id)
            if existing_user.exists():
                self.add_error('email', 'Este email ya está registrado')
        
        # ✅ Validar documento según tipo
        if document_type and document_number:
            # Solo validar si ambos campos se proporcionan
            if document_type == 'cedula' and len(document_number) < 5:
                self.add_error('document_number', 'Cédula debe tener al menos 5 dígitos')
            elif document_type == 'pasaporte' and len(document_number) < 5:
                self.add_error('document_number', 'Pasaporte debe tener al menos 5 caracteres')
        
        return cleaned_data
    
    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.email = self.cleaned_data.get('email', user.email)
        user.first_name = self.cleaned_data.get('first_name', user.first_name)
        user.last_name = self.cleaned_data.get('last_name', user.last_name)
        
        if commit:
            user.save()
            profile.save()
        return profile
