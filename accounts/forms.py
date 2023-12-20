import phonenumbers
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
# from django.core.exceptions import ValidationError
from django.contrib.auth.forms import (
    UserCreationForm,
    UsernameField,
)
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.forms.widgets import CheckboxSelectMultiple
# from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _
from phonenumbers import is_valid_number
from phonenumbers.phonenumberutil import NumberParseException

from films.models import Categories, Tag, SubCategories, Country

User = get_user_model()


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "telephone"
        )
        widgets = {
            "username": forms.TextInput(attrs={"class": "input"}),
            "email": forms.EmailInput(attrs={"class": "input"}),
            "telephone": forms.TextInput(attrs={"class": "form-control"}),
        }

    username = UsernameField(widget=forms.TextInput(attrs={
        "class": "input",
        "placeholder": "ism_familiya",
        "type": "text",
        "autocomplete": "off",
        "name": "custom-username-field",  # Уникальное значение для имени поля
        "id": "custom-username-field",  # Уникальное значение для идентификатора поля
    }))

    def clean_username(self):
        username = self.cleaned_data.get('username')

        # Проверяем, что имя пользователя не содержит пробелов
        if ' ' in username:
            raise forms.ValidationError('Имя пользователя не может содержать пробелы.')

        # Проверяем уникальность имени пользователя
        user = User
        # if User.objects.filter(username=username).exists():
        if user.objects.filter(username=username).exists():
            raise forms.ValidationError('Это имя пользователя уже занято.')

        return username

    email = forms.EmailField(widget=forms.TextInput(attrs={
        "class": "input",
        "type": "email",
        "placeholder": "user@gmail.com",
        "autocomplete": "email",
    }))

    telephone = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input",
        "placeholder": "телефон номер или @имя пользователя",
    }))

    password1 = forms.CharField(
        label=_("Password"),
        strip=True,
        widget=forms.PasswordInput(attrs={
            "autocomplete": "new-password",
            "class": "input",
            "placeholder": "Пароль",
        }),
        validators=[MinLengthValidator(limit_value=8, message="Пароль должен содержать минимум 8 символов.")],
    )

    password2 = None

    # password2 = forms.CharField(
    #     label=_("Password confirmation"),
    #     widget=forms.PasswordInput(attrs={
    #         "autocomplete": "new-password",
    #         "class": "input",
    #         "placeholder": "Подтвердите пароль",
    #     }),
    # )

    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone')

        try:
            parsed_telephone = phonenumbers.parse(telephone, None)
            if phonenumbers.is_valid_number(parsed_telephone):
                formatted_telephone = phonenumbers.format_number(parsed_telephone, phonenumbers.PhoneNumberFormat.E164)
                return formatted_telephone
        except NumberParseException:
            pass

        raise ValidationError(_('Пожалуйста, введите правильный номер телефона.'))

    def clean_email(self):
        email = self.cleaned_data.get('email')

        user = User
        # if User.objects.filter(email=email).exists():
        if user.objects.filter(email=email).exists():
            raise ValidationError(_("Этот email уже используется."))

        return email


class UserLoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={
        "autofocus": True,
        "class": "input",
        "placeholder": "Имя пользователя",
    }))

    password = forms.CharField(
        label=_("Password"),
        strip=True,
        widget=forms.PasswordInput(attrs={
            "autocomplete": "current-password",
            "class": "password",
            "placeholder": "Пароль",
            "type": "password",
        }),
        error_messages={
            'required': _('Поле "Пароль" обязательно для заполнения.'),
            'invalid': _('Неверный формат пароля.'),
        },
    )


class CompanyInfoForm(forms.ModelForm):
    class Meta:
        # model = User()
        model = User
        fields = ['company_name', 'category', 'sub_category', 'tags']

    company_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "company-input", "id": "id_company_name"}),
        required=False,
    )

    category = forms.ModelChoiceField(
        queryset=Categories.objects.filter(is_linked=True),
        empty_label='Выберите категорию',
        widget=forms.Select(attrs={"class": "company-select", "id": "id_category"}),
        required=False,
    )

    sub_category = forms.ModelChoiceField(
        queryset=SubCategories.objects.all(),  # Replace with your actual queryset
        widget=forms.Select(attrs={"class": "company-select", "id": "id_sub_category"}),
        required=False,
    )

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=CheckboxSelectMultiple(attrs={"class": "company-input", "id": "id_tags"}),
        error_messages={
            'required': 'Выберите хотя бы один тег.',
        },
        required=False,
    )


def validate_phone_number(value):
    try:
        # Попробуйте разобрать введенный номер телефона
        parsed_number = phonenumbers.parse(value, None)

        # Проверьте, является ли разобранный номер действительным
        if not is_valid_number(parsed_number):
            raise ValidationError("Введите корректный номер телефона")
    except phonenumbers.phonenumberutil.NumberParseException:
        raise ValidationError("Введите корректный номер телефона")


class ContactInfoForm(forms.ModelForm):
    class Meta:
        # model = User()
        model = User
        fields = ['telegram', 'whatsapp', 'website', 'url_maps']

    telegram = forms.CharField(
        widget=forms.TextInput(attrs={"class": "company-input", "id": "id_telegram"}),
        # validators=[validate_phone_number],  # Валидатор для проверки, что это номер телефона
        error_messages={"invalid": "Введите корректный номер телефона"},
        required=False,
    )
    whatsapp = forms.CharField(
        widget=forms.TextInput(attrs={"class": "company-input", "id": "id_whatsapp"}),
        # validators=[validate_phone_number],
        error_messages={"invalid": "Введите корректный номер телефона"},
        required=False,
    )
    website = forms.CharField(
        widget=forms.TextInput(attrs={"class": "company-input", "id": "id_website"}),
        # validators=[URLValidator()],  # Валидатор для проверки, что это ссылка
        error_messages={"invalid": "Введите корректную ссылку"},
        required=False,
    )
    url_maps = forms.CharField(
        widget=forms.TextInput(attrs={"class": "company-input", "id": "id_url_maps"}),
        # validators=[URLValidator()],  # Валидатор для проверки, что это ссылка
        error_messages={"invalid": "Введите корректную ссылку"},
        required=False,
    )


def validate_logo_size(value):
    max_size = 2 * 1024 * 1024  # 2 MB
    if value.size > max_size:
        raise forms.ValidationError("Файл слишком большой. Максимальный размер: 2 МБ.")


def validate_banner_size(value):
    max_size = 4 * 1024 * 1024  # 4 MB
    if value.size > max_size:
        raise forms.ValidationError("Файл слишком большой. Максимальный размер: 4 МБ.")


class LogoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['logo']

    logo = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'id': 'input-file', 'hidden': 'true', 'accept': 'image/*'}),
        error_messages={
            'invalid_image': "Формат файла не поддерживается. Разрешенные форматы: jpg, png, gif и другие изображения.",
        },
        validators=[validate_logo_size],
        required=False,
    )


class BannerForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['banner']

    # Установка атрибутов виджета и текста ошибки на уровне класса
    banner = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'id': 'input-file', 'hidden': 'true', 'accept': 'image/*'}),
        error_messages={
            'invalid_image': "Формат файла не поддерживается. Разрешенные форматы: jpg, png, gif и другие изображения."},
        validators=[validate_banner_size],
        # required=False,
    )


class DescriptionCountryForm(forms.ModelForm):
    class Meta:
        # model = User()
        model = User
        fields = ['description', 'country']

    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-textarea', 'placeholder': _('Введите описание'), 'rows': '4'}),
        max_length=800,
        required=False,
    )

    country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        widget=forms.Select(attrs={"class": "company-select", "id": "id_country"}),
        empty_label='Выберите страну',
        # required=False,
    )


class NotificationForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea)
    send_to_all = forms.BooleanField(required=False, initial=False)
    # user = get_user_model()
    # filtered_users = forms.ModelMultipleChoiceField(queryset=user.objects.all(), required=False)

    # Добавьте поля для фильтрации
    category = forms.ModelChoiceField(queryset=Categories.objects.all(), required=False)
    subcategory = forms.ModelChoiceField(queryset=SubCategories.objects.all(), required=False)
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)


# user = get_user_model()
# message = forms.CharField(widget=forms.Textarea)
# send_to_all = forms.BooleanField(required=False)
# filtered_users = forms.ModelMultipleChoiceField(
#     queryset=user.objects.all(),
#     widget=forms.CheckboxSelectMultiple,
#     required=False
# )

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'company_name', 'description', 'category', 'sub_category', 'tags']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'username_id'}),
            'company_name': forms.TextInput(attrs={'class': 'company-name_id'}),
            'description': forms.Textarea(attrs={'class': 'description_id'}),
            'category': forms.Select(attrs={'class': 'category_id'}),
            'sub_category': forms.Select(attrs={'class': 'sub_category_id'}),
            # 'tags': forms.CheckboxSelectMultiple(attrs={'class': 'tag_id'}),
            'tags': forms.CheckboxSelectMultiple,
        }

    category = forms.ModelChoiceField(
        queryset=Categories.objects.filter(is_linked=True),
        empty_label='Выберите категорию',
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False


class ComplaintForm(forms.Form):
    COMPLAINT_CHOICES = [
        ('spam', 'Спам'),
        ('inappropriate_content', 'Неуместный контент'),
        ('harassment', 'Домогательство'),
        # Добавьте другие варианты по вашему усмотрению
    ]

    complaint_type = forms.ChoiceField(
        choices=COMPLAINT_CHOICES,
        widget=forms.RadioSelect,
        label='Тип жалобы',
        # help_text='Выберите тип жалобы из списка.'
    )

    description = forms.CharField(
        label='Описание проблемы',
        widget=forms.Textarea(attrs={'rows': 5, 'style': 'resize: none'}),
        # help_text='Уточните вашу проблему.'
    )
