import phonenumbers
from django import forms
from django.core.exceptions import ValidationError

from .models import Products, City, Country, Categories, SubCategories, Tag


def validate_image_size(value):
    max_size = 4 * 1024 * 1024
    if value.size > max_size:
        raise forms.ValidationError("Файл слишком большой. Максимальный размер: 4 МБ.")


class FilmsForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = [
            "title",
            "description",
            "category",
            "subcategories",
            "tags",
            "telephone",
            "telegram",
            "country",
            "city",
            "price",
            "is_price_negotiable",
        ]

    title = forms.CharField(
        label="Название",
        widget=forms.TextInput(attrs={"class": "form-input"}),
        max_length=100,
    )

    price = forms.CharField(
        label="Цена",
        widget=forms.TextInput(attrs={"class": "form-input"}),
        max_length=100,
        required=False,
    )

    is_price_negotiable = forms.BooleanField(
        label="Договорный", required=False, widget=forms.CheckboxInput(attrs={})
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-textarea",
                "placeholder": "",
                "rows": "4",
            }
        ),
        max_length=800,
    )

    category = forms.ModelChoiceField(
        label="",
        queryset=Categories.objects.all(),
        empty_label="",
        to_field_name="id",
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "id": "id_category",
                "name": "category",
            }
        ),
    )

    subcategories = forms.ModelMultipleChoiceField(
        label="",
        queryset=SubCategories.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    tags = forms.ModelMultipleChoiceField(
        label="",
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    telephone = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-input", "placeholder": "+998 66 666 66 66"}
        ),
        required=False,
    )

    def clean_telephone(self):
        telephone = self.cleaned_data.get("telephone")
        try:
            phone_number = phonenumbers.parse(telephone, None)
            if not phonenumbers.is_valid_number(phone_number):
                raise ValidationError("Некорректный номер телефона")
        except phonenumbers.NumberParseException:
            raise ValidationError("Некорректный номер телефона")
        return telephone

    telegram = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "placeholder": "t.me/+",
            }
        ),
        error_messages={
            "required": "Это поле обязательно для заполнения.",
            "invalid":
                "Пожалуйста, введите правильный номер телефона или имя пользователя в Telegram."
            ,
        },
        required=False,
    )

    def clean_telegram(self):
        telegram = self.cleaned_data.get("telegram")

        try:
            phone_number = phonenumbers.parse(telegram, None)
            if phonenumbers.is_valid_number(phone_number):
                return telegram
        except phonenumbers.NumberParseException:
            pass

        if telegram.startswith("@") and len(telegram) > 1:
            return telegram

        raise ValidationError(
            "Неверный номер телефона или имя пользователя в Telegram"

        )

    country = forms.ModelChoiceField(
        label="",
        queryset=Country.objects.all(),
        empty_label="Выберите страну",
        to_field_name="id",
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "id": "id_country",
                "name": "country",
            }
        ),
    )

    city = forms.ModelChoiceField(
        label="",
        queryset=City.objects.all(),
        empty_label="Выберите город",
        to_field_name="id",
        widget=forms.Select(attrs={
            "class": "form-select",
            "id": "id_city",
            "name": "city",
        }
        ),
        required=False,
    )

    images = forms.ImageField(
        label="Выберите фотографии",
        widget=forms.ClearableFileInput(),
        required=False,
    )


class ProductFilterForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ["category", "sub_category", "tags", "country", "city", "type"]

    category = forms.ModelChoiceField(
        queryset=Categories.objects.filter(is_linked=False),
        empty_label="Выберите категорию",
        required=False,
    )

    company_category = forms.ModelChoiceField(
        queryset=Categories.objects.filter(is_linked=True),
        empty_label="Выберите категорию",
        required=False,
    )

    sub_category = forms.ModelChoiceField(
        queryset=SubCategories.objects.all(),
        empty_label="Выберите субкатегорию",
        required=False,
    )

    company_sub_category = forms.ModelChoiceField(
        queryset=SubCategories.objects.filter(category__is_linked=True),
        empty_label="Выберите субкатегорию",
        required=False,
    )

    tags = forms.ModelMultipleChoiceField(
        label="",
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        if not tags:
            raise forms.ValidationError('Выберите хотя бы один тег.')
        return tags

    country = forms.ModelChoiceField(
        label="",
        queryset=Country.objects.all(),
        empty_label="Выберите страну",
        to_field_name="id",
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "id": "id_country",
                "name": "country",
            }
        ),
        required=False,
    )

    city = forms.ModelChoiceField(
        label="",
        queryset=City.objects.all(),
        empty_label="Выберите город",
        to_field_name="id",
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "id": "id_city",
                "name": "city",
            }
        ),
        required=False,
    )

    TYPE_CHOICES = (
        ("all", "Все"),
        ("buy", "Купить"),
        ("sell", "Продать"),
        ("company", "Компании"),
    )

    type = forms.ChoiceField(
        label="Тип объявления",
        choices=TYPE_CHOICES,
        widget=forms.Select(
            attrs={"class": "form-select", "id": "id_type", "name": "type"}
        ),
        required=False,
    )


class SearchForm(forms.Form):
    query = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={"class": "input", "placeholder": "Поиск...", "autocomplete": "off"}
        ),
    )
