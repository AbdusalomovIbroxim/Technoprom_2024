import emoji
import asyncio
from cyrtranslit import to_cyrillic, to_latin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.translation import get_language
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from fuzzywuzzy import fuzz

from accounts.models import Message
from .forms import FilmsForm, ProductFilterForm, SearchForm
from .models import (Products, SubCategories, Favorite, Tag, Image, Categories, SubCategoryCategory, )
from .utils import send_message_to_channel


def get_product_with_subcategories(pk):
    product = get_object_or_404(
        Products.objects.select_related('category').prefetch_related('subcategories'),
        pk=pk
    )
    return product


class IndexView(ListView):
    template_name = "index.html"
    context_object_name = "films_buy"

    def get_queryset(self):
        return Products.objects.filter(
            type="buy", is_active=True, is_published=True
        ).order_by("-create_date")[:8]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["films_sell"] = Products.objects.filter(
            type="sell", is_active=True, is_published=True
        ).order_by("-create_date")[:8]
        context["title"] = "Запросы: "
        context["form"] = FilmsForm()
        if self.request.user.is_authenticated:
            in_favorite = list(
                Favorite.objects.filter(user=self.request.user).values_list(
                    "product_id", flat=True
                )
            )
        else:
            in_favorite = []
        context["in_favorite"] = in_favorite
        context["jobs"] = Products.objects.filter(
            is_active=True, is_published=True, category__slug="texnolog"
        )
        return context

    @staticmethod
    def post(request):
        context = {
            "films_buy": Products.objects.filter(
                type="buy", is_active=True, is_published=True
            ).order_by("-create_date")[:8],
            "films_sell": Products.objects.filter(
                type="sell", is_active=True, is_published=True
            ).order_by("-create_date")[:8],
            "title": "Запросы: ",
            # "form": FilmsForm(),
        }
        form = FilmsForm(request.POST)
        selected_tags = request.POST.getlist("tags")
        selected_subcategories = request.POST.getlist("subcategories")
        if form.is_valid():
            film = form.save(commit=False)
            if not request.user.is_anonymous:
                film.author = request.user
                film.email = request.user.email
            film.is_published = True
            film.image = "product-about_us/image.png"
            if form.cleaned_data["telegram"].startswith("@"):
                film.telegram = form.cleaned_data["telegram"][1:]
            message = {}

            for field_name, field_value in form.cleaned_data.items():
                message[field_name] = field_value
            message["тип"] = "Купить"

            try:
                price = float(form.cleaned_data.get("price", 0))
                film.price = price
            except ValueError:
                film.price = None
            film.save()
            film.subcategories.set(selected_subcategories)
            film.tags.set(selected_tags)
            message["film_id"] = film.id
            # asyncio.run(send_message_to_channel(message))
            send_message_to_channel(message)
            messages.success(request, "Отправлено на модерацию")
            return redirect("index")
        else:
            context["form"] = form
            context["errors"] = form.errors
            return render(request, "index.html", context=context)


def user_can_view_product(user, film):
    # Проверка, является ли пользователь автором продукта или администратором
    return user == film.author or user.is_staff


class ProductDetailView(DetailView):
    model = Products
    template_name = "product-details.html"
    context_object_name = "product"

    def dispatch(self, request, *args, **kwargs):
        film = self.get_object()

        if not film.is_active:
            if not user_can_view_product(request.user, film):
                return redirect("access_denied_page")
            # Если продукт неактивен, но пользователь - администратор или автор продукта, разрешить доступ
            pass
        session_key = "film_{}_viewed".format(film.pk)

        if not request.session.get(session_key, False):
            film.view_count += 1
            film.save()
            request.session[session_key] = True

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Products.objects.filter(pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = None if self.request.user.is_anonymous else self.request.user
        film = self.object
        product_author = film.author
        film_pk = film.pk
        product_category = film.category
        product_subcategories = SubCategories.objects.filter(products=self.kwargs['pk']).values_list('name_ru',
                                                                                                     flat=True)
        context["product_subcategories"] = list(product_subcategories)

        if not self.request.user.is_anonymous:
            context["is_favorite"] = Favorite.objects.filter(
                user=user, product_id=film
            ).exists()
        context["author_products"] = Products.objects.filter(
            author=product_author
        ).order_by("-create_date")[:16]

        similar_products = Products.objects.filter(
            category=product_category,
            subcategories__in=product_subcategories
        ).exclude(id=film_pk).order_by("-create_date")[:16]

        if len(similar_products) < 16:
            add = 16 - len(similar_products)
            additional_products = Products.objects.exclude(
                id__in=[product.id for product in similar_products]
            ).order_by("-create_date")[:add]
            similar_products = list(similar_products) + list(additional_products)

        context["similar_products"] = similar_products

        product_images = Image.objects.filter(product=self.kwargs['pk'])
        context["product_images"] = product_images

        # similar_products = Products.objects.filter(
        #     category__in=product_categories,
        #     subcategories__in=product_subcategories
        # ).exclude(id=film.id).order_by("-create_date")[:16]

        # if len(similar_products) < 16:
        #     add = 16 - len(similar_products)
        #     additional_products = Products.objects.exclude(
        #         id__in=[product.id for product in similar_products]).order_by("-create_date")[:add]
        #     similar_products = list(similar_products) + list(additional_products)

        # context["similar_products"] = similar_products

        return context


class ProductSaveView(CreateView):
    model = Products
    form_class = FilmsForm
    template_name = "form.html"

    def form_valid(self, form):
        film = form.save(commit=False)
        message = {}
        selected_tags = self.request.POST.getlist("tags")
        selected_subcategories = self.request.POST.getlist("subcategories")
        images = self.request.FILES.getlist('images')
        if self.request.POST.get("form-name") == "sell":
            film.type = "sell"
            message["тип"] = "Продать"
            user = self.request.user
            if user.currency >= 10:
                user.currency -= 10
                user.save()
        else:
            film.price = None
            message["тип"] = "Купить"

        film.author = self.request.user if not self.request.user.is_anonymous else None
        if form.cleaned_data["is_price_negotiable"] or not form.cleaned_data["price"]:
            film.price = None

        film.is_published = True

        for field_name, field_value in form.cleaned_data.items():
            message[field_name] = field_value

        film.save()
        for image in images:
            Image.objects.create(image=image, product=film)

        film.subcategories.set(selected_subcategories)
        film.tags.set(selected_tags)

        message["film_id"] = film.id
        if images:
            files = [i for i in images]
            asyncio.run(send_message_to_channel(message, files))
        # send_message_to_channel(message, images)
        else:
            # asyncio.run(send_message_to_channel(message))
            send_message_to_channel(message)

        user = self.request.user
        if not user.is_anonymous:
            message = Message.objects.create(
                sender=user,
                message="Вы успешно отправили запрос !.",
                created_at=timezone.now(),
            )

            message.recipients.set([self.request.user])
        messages.success(self.request, "Вы успешно отправили запрос !")

        if self.request.user.is_authenticated:
            self.request.session['product_pk'] = film.pk
            return redirect("product_update_status")
        else:
            return redirect("index")

    def form_invalid(self, form):
        errors = form.errors
        for error in errors:
            messages.error(self.request, f"{errors[f'{error}'][0]}")
        # messages.error(self.request, f'{errors}')
        return render(
            self.request, self.template_name, {"form": form, "errors": errors}
        )


class AdditionalServicesView(View):
    template_name = "additional_services.html"

    def get(self, request):
        product_pk = self.request.session.get("product_pk")
        return render(request, self.template_name, {"product_pk": product_pk})

    def post(self, request):
        service = self.request.POST.get("service", None)
        product_pk = request.POST.get('product', None)
        if service is not None:
            product = Products.objects.get(author_id=product_pk)
            if str(service).endswith("1"):
                product.is_top_film = True
                product.top_duration = 1

            elif str(service).endswith("2"):
                product.is_top_film = True
                product.top_duration = 2

            elif str(service).endswith("3"):
                product.is_top_film = True
                product.top_duration = 3
            product.save()
        messages.success(self.request, "Success")
        return redirect("index")


class FilmsUpdateView(UpdateView):
    model = Products
    form_class = FilmsForm
    template_name = "form.html"  # Update with your templates path
    success_url = "/success/"  # Redirect to a success page after updating
    context_object_name = "film"  # Optional: Customize the context object name

    def get_object(self, queryset=None):
        return Products.objects.get(pk=self.kwargs["pk"])


class FilmsListView(ListView):
    model = Products
    template_name = "product-list.html"
    paginate_by = 8
    context_object_name = "films"

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ProductFilterForm(self.request.GET)
        if self.request.user.is_authenticated:
            in_favorite = list(
                Favorite.objects.filter(user=self.request.user).values_list(
                    "product_id", flat=True
                )
            )
        else:
            in_favorite = []
        context["in_favorite"] = in_favorite
        context["top_films"] = Products.objects.filter(
            is_active=True, is_published=True, is_top_film=True
        ).order_by("-create_date")
        context["search"] = SearchForm()

        # Get the films queryset
        films = Products.objects.filter(is_active=True, is_published=True).order_by(
            "-create_date"
        )

        # Apply additional filtering based on request parameters
        category_id = self.request.GET.get('category_id')
        sub_category_id = self.request.GET.get('sub_category_id')
        tag_id = self.request.GET.get('tag_id')
        country_id = self.request.GET.get('country_id')
        city_id = self.request.GET.get('city_id')

        if category_id:
            films = films.filter(category_id=category_id)
        elif sub_category_id:
            films = films.filter(subcategories__in=sub_category_id)
        elif tag_id:
            films = films.filter(tags__id=tag_id)
        elif country_id:
            films = films.filter(country_id=country_id)
        elif city_id:
            films = films.filter(city_id=city_id)

        # Set up pagination
        paginator = Paginator(films, self.paginate_by)
        page = self.request.GET.get("page", 1)

        try:
            films = paginator.page(page)
        except EmptyPage:
            films = paginator.page(paginator.num_pages)
        except PageNotAnInteger:
            films = paginator.page(1)

        context["films"] = films
        context["paginator"] = paginator
        return context

    def fuzzywuzzy_search(self, latin_query, cyrillic_query, queryset, threshold):
        similar_products = set()

        latin_words = set(latin_query.split())
        cyrillic_words = set(cyrillic_query.split())

        for product in queryset:
            product_title_words = set(product.title.split())
            product_description_words = set(product.description.split())

            latin_similarity_title = any(
                fuzz.token_set_ratio(word1, word2) >= threshold
                for word1 in product_title_words
                for word2 in latin_words
            )

            cyrillic_similarity_title = any(
                fuzz.token_set_ratio(word1, word2) >= threshold
                for word1 in product_title_words
                for word2 in cyrillic_words
            )

            latin_similarity_description = any(
                fuzz.token_set_ratio(word1, word2) >= threshold
                for word1 in product_description_words
                for word2 in latin_words
            )

            cyrillic_similarity_description = any(
                fuzz.token_set_ratio(word1, word2) >= threshold
                for word1 in product_description_words
                for word2 in cyrillic_words
            )

            if (
                    latin_similarity_title
                    or cyrillic_similarity_title
                    or latin_similarity_description
                    or cyrillic_similarity_description
            ):
                similar_products.add(product)

        return list(similar_products)

    def post(self, request, *args, **kwargs):
        search_form = SearchForm(request.POST)
        product_filter_form = ProductFilterForm(request.POST)

        context = {
            "search": search_form,
            "in_favorite": list(Favorite.objects.filter(user=request.user).values_list("product_id",
                                                                                       flat=True)) if request.user.is_authenticated else [],
            "form": product_filter_form,
        }

        queryset = Products.objects.filter(is_active=True, is_published=True)

        if search_form.is_valid():
            query = search_form.cleaned_data.get("query")
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )

        else:
            if product_filter_form.is_valid():
                queryset = product_filter_form.filter_products(queryset)

        paginator = Paginator(queryset, self.paginate_by)
        page_number = request.POST.get('page', 1)

        try:
            films = paginator.page(page_number)
        except (PageNotAnInteger, EmptyPage):
            films = paginator.page(1)

        context["films"] = films
        context["paginator"] = paginator

        return render(request, self.template_name, context=context)


def new_filter(
        queryset,
        companies,
        category="",
        sub_category="",
        tags="",
        country="",
        city="",
        product_type="",
):
    if product_type == "company":
        queryset = companies.all()
    if product_type not in ("all", "company", ""):
        queryset = queryset.filter(type=product_type)
    if category:
        queryset = queryset.filter(category=category)
    if sub_category:
        queryset = queryset.filter(sub_category=sub_category)

    if tags:
        queryset = queryset.filter(tags__in=tags)

    if country:
        queryset = queryset.filter(country=country)

    if city:
        queryset = queryset.filter(city=city)
    return queryset


# from django.shortcuts import get_object_or_404


def related_to_it(request):
    preferred_language = get_language()
    category_id = request.GET.get("category_id", None)
    subcategory_id = request.GET.get("subcategory_id", None)

    tags = {}
    subcategories_names = {}

    if category_id:
        category = get_object_or_404(Categories, pk=category_id)
        subcategories = SubCategoryCategory.objects.filter(category=category)
        subcategory_ids = subcategories.values_list('subcategory_id', flat=True)
        subcategories_data = SubCategories.objects.filter(id__in=subcategory_ids).all()

        if preferred_language == 'en':
            subcategories_names = {
                subcategory.id: subcategory.name_en for subcategory in subcategories_data
            }
        elif preferred_language == 'ru':
            subcategories_names = {
                subcategory.id: subcategory.name_ru for subcategory in subcategories_data
            }
        elif preferred_language == 'uz':
            subcategories_names = {
                subcategory.id: subcategory.name_uz for subcategory in subcategories_data
            }

    if subcategory_id:
        lang = get_language()
        tags_data = Tag.objects.filter(subcategory_tags__subcategory_id=subcategory_id,
                                       category_tags__category_id=category_id)
        tags = {tag.id: getattr(tag, f'name_{lang}') for tag in tags_data}

    return JsonResponse({"subcategories": subcategories_names, "tags": tags})


@login_required()
def add_to_favorites(request, pk):
    product = Products.objects.get(pk=pk)
    try:
        favorite = Favorite.objects.get(user=request.user, product_id=product)
        favorite.delete()
        response_data = {"added": False}
    except Favorite.DoesNotExist:
        Favorite.objects.create(user=request.user, product_id=product)
        response_data = {"added": True}
    return JsonResponse(response_data)


def favorite_list(request):
    favorites = {"favorites": Favorite.objects.filter(user=request.user)}
    return JsonResponse(favorites)


def send_message(request, text=None):
    if request.method == "POST" and text:
        messages.error(request, text)
        return JsonResponse({"message": "Message sent successfully"})
    return JsonResponse({"message": "Invalid request"})


def remove_emoji(text):
    return emoji.replace_emoji(text)


def get_suggestions(request):
    # получаю текст из инпута
    user_query = request.GET.get("term", "")
    # текст на латин и кирилицу переожу салом=salom
    latin_query = to_latin(user_query).lower()
    cyrillic_query = to_cyrillic(user_query).lower()
    # latin_products = Products.objects.filter(title__istartswith=latin_query)
    # cyrillic_products = Products.objects.filter(title__istartswith=cyrillic_query)
    all_words = set()

    # добавляю слова в all_worlds
    for product in Products.objects.values("title", "description"):
        title_words = product["title"].split()
        description_words = product["description"].split()
        all_words.update(title_words)
        all_words.update(description_words)

    # удаляю эмации из текста
    all_words = [remove_emoji(word).lower() for word in all_words]

    filtered_words = [
        word
        for word in all_words
        if word.startswith(latin_query) or word.startswith(cyrillic_query)
    ]

    suggestions = filtered_words[:5]

    # это функция для поиска похожего слово
    def find_suggestions(query, limit):
        return [
            word for word in all_words if fuzz.token_set_ratio(word, query) >= limit
        ]

    if len(suggestions) < 5:
        supplement = 5 - len(suggestions)
        filtered_words = [
            word for word in all_words if latin_query in word or cyrillic_query in word
        ]
        suggestions = filtered_words[:supplement]

    for threshold in [90, 80, 70]:
        if len(suggestions) < 5:
            cyrillic_similar_words = find_suggestions(cyrillic_query, threshold)
            latin_similar_words = find_suggestions(latin_query, threshold)

            similar_words = list(set(cyrillic_similar_words + latin_similar_words))

            if similar_words:
                suggestions = similar_words[: 5 - len(suggestions)]
                break

    return JsonResponse(suggestions, safe=False)


def access_denied_page(request):
    return render(request, "access_denied_page.html")


def about_us_page(request):
    return render(request, "about_us/about_us.html")
