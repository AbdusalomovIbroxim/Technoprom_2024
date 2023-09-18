import asyncio

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import ListView, CreateView
from django.db.models import Q
from .forms import FilmsForm, ProductFilterForm
from .models import Categories, Films, SubCategories, City, Favorite, Tag
from .utils import send_message_to_channel


class IndexView(ListView):
    template_name = "index.html"
    context_object_name = "films_buy"

    def get_queryset(self):
        return Films.objects.filter(type='Купить', is_active=True, is_published=True).order_by('-create_date')[:7]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["films_sell"] = Films.objects.filter(type='sell', is_active=True, is_published=True).order_by(
            '-create_date')[:7]
        context["films_buy"] = Films.objects.filter(type='buy', is_active=True, is_published=True).order_by(
            '-create_date')[:7]
        context["title"] = "Запросы: "
        context["form"] = FilmsForm()
        return context

    def post(self, request):
        form = FilmsForm(request.POST)
        if form.is_valid():
            film = form.save(commit=False)
            if not request.user.is_anonymous:
                film.author = request.user
            film.is_published = True
            film.image = 'product-images/image.png'
            message = {}

            for field_name, field_value in form.cleaned_data.items():
                message[field_name] = field_value
            message['тип'] = 'Купить'
            asyncio.run(send_message_to_channel(message))
            film.save()
            messages.success(request, 'Отправилься модерацию')
            return redirect('index')
        else:
            messages.error(request, 'Не отправилься модерацию')
            return redirect('index')


# class ProductFilterView(ListView):
#     template_name = "films/product_list/filtered_products.html"
#     context_object_name = "films"
#     paginate_by = 24
#
#     def get_queryset(self):
#         self.film = Films.objects.filter(is_active=True, is_published=True)
#
#         # Обработка параметров из формы фильтрации
#         form = FilmFilterForm(self.request.GET)
#         if bool(form.data):
#             country = form.data.get('country')
#             city = form.data.get('city')
#             category = form.data.get('category')
#             sub_category = form.data.get('sub_category')
#
#             if country:
#                 self.film = self.film.filter(country=int(country))
#             if city:
#                 self.film = self.film.filter(city=int(city))
#             if category:
#                 self.film = self.film.filter(category=int(category))
#             if sub_category:
#                 self.film = self.film.filter(sub_category=int(sub_category))
#         else:
#             slug = self.kwargs.get('slug')
#             if not slug in ['uskuna', 'texnolog', 'xomashyo', 'xizmat_korsatish']:
#                 sub_category = SubCategories.objects.get(slug=slug).pk
#                 self.film = Films.objects.filter(sub_category=sub_category, is_active=True,
#                                                  is_published=True)
#             else:
#                 category = Categories.objects.get(slug=slug).pk
#                 self.film = Films.objects.filter(category=category, is_active=True,
#                                                  is_published=True)
#         return self.film.order_by('-create_date')
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         paginator = Paginator(self.film, self.paginate_by)
#         page = self.request.GET.get('page')
#         page_obj = paginator.get_page(page)
#         context['page_obj'] = page_obj
#         context["form"] = PersonCreationForm()
#         return context
#
#
# class ProductDetailView(DetailView):
#     model = Films
#     template_name = "films/product_detail.html"
#     context_object_name = "film"
#
#     def dispatch(self, request, *args, **kwargs):
#         film = self.get_queryset().first()
#         film.view_count += 1
#         film.save()
#         return super().dispatch(request, *args, **kwargs)
#
#     def get_queryset(self):
#         self.film = Films.objects.filter(pk=self.kwargs["pk"])
#         return self.film
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["categories"] = Categories.objects.all()
#         context["title"] = self.object.title
#         if not self.request.user.is_anonymous:
#             context["is_favorite"] = Favorite.objects.filter(user=self.request.user,
#                                                              product_id=self.film.first().pk).exists()
#         return context
#
#     def post(self, request, *args, **kwargs):
#         ball = request.POST['ball']
#         return redirect('film_detail', self.object.pk)
#
#
# class ProductsSearchView(ListView):
#     template_name = "films/index.html"
#     context_object_name = "films"
#
#     def get_queryset(self):
#         film_name = self.request.GET.get()
#         return Films.objects.filter(title__icontains=film_name)
#
#     def get_context_data(self, **kwargs):
#         film_name = self.request.GET.get()
#
#         context = super().get_context_data(**kwargs)
#         context["categories"] = Categories.objects.all()
#         context["title"] = f"По вашему запросу: \"{film_name}\". Найдено: {len(self.object_list)} запросов."
#         return context
#
#
# class ProductEditView(View):
#     form_class = EditFilmForm
#     initial = {"key": "value"}
#     template_name = 'films/edit_film.html'
#
#     def get(self, request, pk):
#         film = get_object_or_404(Films, pk=pk)
#         fields = [field.name for field in film._meta.get_fields() if field.concrete]
#         exclude_fields = ['category', 'sub_category']
#         fields = [field for field in fields if field not in exclude_fields]
#         data = model_to_dict(film, fields=fields)
#         form = EditFilmForm(initial=data)
#         return render(request, self.template_name, {"form": form, 'id': film.id})
#
#     def post(self, request, pk):
#         film = get_object_or_404(Films, pk=pk)
#         film.is_active = False
#         form = EditFilmForm(request.POST, instance=film)
#         if form.is_valid():
#             form.save()
#             message = get_object_or_404(Films, pk=pk)
#             asyncio.run(send_message_to_bot(message, message.category, message.sub_category))
#             return redirect('profile', pk=film.author_id)
#
#
# class ProductDeleteView(DeleteView):
#     model = Films
#
#     def dispatch(self, request, *args, **kwargs):
#         film = self.get_queryset().first()
#         if request.user.is_superuser:
#             return super().dispatch(request, *args, **kwargs)
#         messages.error(request, "У вас недостаточно прав для удаления этого запроса !")
#         return redirect("index")
#
#     def render_to_response(self, context, **response_kwargs):
#         messages.success(self.request, f"Запрос: {self.object.title}, был успешно удалён !")
#         super().form_valid(self.form_class)
#         return redirect("index")
#
#     def get_success_url(self):
#         return self.object.get_absolute_url()
#
#


class ProductSaveView(CreateView):
    model = Films
    form_class = FilmsForm
    template_name = 'form.html'

    def form_valid(self, form):
        film = form.save(commit=False)
        message = {}
        image = self.request.FILES
        if self.request.POST.get('form-name') == "sell":
            film.type = 'sell'
            message['тип'] = 'Продать'
        else:
            message['тип'] = 'Купить'

        if not self.request.user.is_anonymous:
            film.author = self.request.user
        if image:
            film.image = image
        else:
            film.image = 'product-images/image.png'
        film.is_published = True

        for field_name, field_value in form.cleaned_data.items():
            message[field_name] = field_value
        # asyncio.run(send_message_to_channel(message))

        film.save()
        messages.success(self.request, "Вы успешно отправили запрос !")
        return redirect('index')

    def form_invalid(self, form):
        error_message = form.errors['__all__'][
            0] if '__all__' in form.errors else "Пожалуйста, исправьте ошибки в форме."
        messages.error(self.request, error_message)
        # messages.error(self.request, "Пожалуйста, исправьте ошибки в форме.")
        return redirect("add_film")


class FilmsListView(ListView):
    model = Films
    template_name = 'product-list.html'  # Здесь укажите путь к вашему HTML-шаблону
    context_object_name = 'films'  # Это имя, по которому вы будете обращаться к объекту списка в шаблоне
    paginate_by = 24

    def get_queryset(self):
        # Извлекаем параметры из запроса
        category = self.request.GET.get('category')
        sub_category = self.request.GET.get('sub_category')
        country = self.request.GET.get('country')
        city = self.request.GET.get('city')

        # Начинаем с полного набора Films, отфильтровываем по активным и опубликованным записям
        queryset = Films.objects.filter(is_active=True, is_published=True)

        # Применяем условные фильтры в зависимости от наличия параметров
        if category:
            queryset = queryset.filter(category__id=category)
        if sub_category:
            queryset = queryset.filter(sub_category__id=sub_category)
        if country:
            queryset = queryset.filter(country__id=country)
        if city:
            queryset = queryset.filter(city__id=city)

        # Возвращаем отфильтрованный набор данных
        return queryset.order_by('-create_date')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProductFilterForm
        return context


class FilterProductsView(View):
    def get(self, request, *args, **kwargs):
        # Получите параметры фильтрации из запроса
        category = request.GET.get('category')
        subcategory = request.GET.get('subcategory')
        country = request.GET.get('country')
        sell_buy = request.GET.get('sell_buy')

        # Фильтруйте ваш список продуктов на основе полученных параметров
        filtered_products = Films.objects.filter(
            category=category,
            subcategory=subcategory,
            country=country,
            type=sell_buy,
            is_active=True,
            is_published=True
        ).order_by('-create_date')

        # Верните отфильтрованные продукты в контексте шаблона
        context = {'films': filtered_products}
        return render(request, 'product-list.html', context)


# class BuyView(ListView):
#     template_name = "films/product_list/buy.html"
#     context_object_name = "films"  # context name Главного queryset
#     paginate_by = 24
#
#     def get_queryset(self):  # Главный queryset
#         category = self.request.GET.get('category')
#         sub_category = self.request.GET.get('sub_category')
#         country = self.request.GET.get('country')
#         city = self.request.GET.get('city')
#         self.film = Films.objects.filter(type='Купить', is_active=True, is_published=True)
#         if category:
#             self.film = Films.objects.filter(type='Купить', is_active=True, is_published=True, category_id=category)
#         if sub_category:
#             self.film = Films.objects.filter(type='Купить', is_active=True, is_published=True,
#                                              sub_category=sub_category)
#         if country:
#             self.film = Films.objects.filter(type='Купить', is_active=True, is_published=True, country=country)
#         if city:
#             self.film = Films.objects.filter(type='Купить', is_active=True, is_published=True, city=city)
#         return self.film.order_by('-create_date')
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         paginator = Paginator(self.film, self.paginate_by)
#         page = self.request.GET.get('page')
#         page_obj = paginator.get_page(page)
#         context['page_obj'] = page_obj
#         context["form"] = PersonCreationForm()
#         return context
#
#
# class SellView(ListView):
#     template_name = "films/product_list/sell.html"
#     context_object_name = "films"  # context name Главного queryset
#     paginate_by = 24
#
#     def get_queryset(self):  # Главный queryset
#         category = self.request.GET.get('category')
#         sub_category = self.request.GET.get('sub_category')
#         country = self.request.GET.get('country')
#         city = self.request.GET.get('city')
#         self.film = Films.objects.filter(type='Продать', is_active=True, is_published=True)
#         if category:
#             self.film = Films.objects.filter(type='Продать', is_active=True, is_published=True, category=category)
#         if sub_category:
#             self.film = Films.objects.filter(type='Продать', is_active=True, is_published=True,
#                                              sub_category=sub_category)
#         if country:
#             self.film = Films.objects.filter(type='Продать', is_active=True, is_published=True, country=country)
#         if city:
#             self.film = Films.objects.filter(type='Продать', is_active=True, is_published=True, city=city)
#         return self.film.order_by('-create_date')
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         paginator = Paginator(self.film, self.paginate_by)
#         page = self.request.GET.get('page')
#         page_obj = paginator.get_page(page)
#         context['page_obj'] = page_obj
#         context["form"] = PersonCreationForm()
#         return context


def related_to_it(request):
    category_id = request.GET.get('category_id', None)
    subcategory_id = request.GET.get('subcategory_id', None)

    sub_categories = {}
    if category_id:
        subcategories = SubCategories.objects.filter(category_id=category_id).all()
        sub_categories = {subcategory.id: subcategory.name for subcategory in subcategories}

    tags = {}
    if subcategory_id:
        tags_query = Tag.objects.filter(subcategory=subcategory_id)
        tags = {tag.id: tag.name for tag in tags_query}

    return JsonResponse({'subcategories': sub_categories, 'tags': tags})


def load_categories(request):
    category_id = request.GET.get('category_id')
    sub_categories = SubCategories.objects.filter(category_id=category_id).all()
    return render(request, 'films/city.html', {'cities': sub_categories})


def load_cities(request):
    country_id = request.GET.get('country_id')
    cities = City.objects.filter(country_id=country_id).all()
    return render(request, 'films/city.html', {'cities': cities})


def filter_category(request, slug):
    if slug in ['uskuna', 'texnolog', 'xom_ashyo', 'xizmat_korsatish']:
        category = Categories.objects.get(slug=slug).pk
        films = Films.objects.filter(category=category)
    else:
        filtered_slug = SubCategories.objects.get(slug=slug).pk
        films = Films.objects.filter(sub_category=filtered_slug)
    return render(request, 'films/product_list/filtered_products.html', {"films": films})


# def up_to_recommendation(request, pk):
#     time_now = datetime.datetime.now().__str__()
#     film = Films.objects.filter(pk=pk).first()
#     film.create_date = time_now
#     user = User.objects.get(pk=request.user.id)
#     if user.score >= 5:
#         user.score = user.score - 5
#         user.save()
#     else:
#         messages.error(request, "Sizda maglag'  yetarli emas")
#         return redirect('profile', request.user.id)
#     film.save()
#     return redirect('profile', request.user.id)


@login_required
def add_to_favorite(request, product_id):
    # Здесь вы должны получить объект, который пользователь хочет добавить в избранное,
    # например, по его идентификатору (object_id), и создать запись в модели Favorite.
    favorite_object = Films.objects.get(pk=product_id)
    favorite = Favorite(user=request.user, product_id=favorite_object)
    favorite.save()
    return redirect('film_detail', product_id)


@login_required
def remove_from_favorite(request, product_id):
    # Здесь вы должны получить объект, который пользователь хочет удалить из избранного,
    # и удалить соответствующую запись из модели Favorite.
    favorite_object = Films.objects.get(pk=product_id)
    favorite = Favorite.objects.get(user=request.user, product_id=favorite_object)
    favorite.delete()
    return redirect('film_detail', product_id)


def my_favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'favorite_list.html', {'favorites': favorites})
