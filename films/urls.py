from django.urls import path

from .views import (
    IndexView,
    ProductSaveView,
    FilmsListView,
    ProductDetailView,
    FilmsUpdateView,
    related_to_it,
    add_to_favorites,
    favorite_list,
    send_message,
    get_suggestions,
    access_denied_page,
    AdditionalServicesView,
)

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("request/", ProductSaveView.as_view(), name="add_film"),
    path("update-film/<int:pk>/", FilmsUpdateView.as_view(), name="update_film"),
    path("product-list/", FilmsListView.as_view(), name="product-list"),
    path("related_to_it/", related_to_it, name="related_to_it"),
    # add del read favorites
    path("add/<int:pk>/", add_to_favorites, name="add_to_favorites"),
    path("favorite_list/", favorite_list, name="favorite_list"),
    path("send-message/<str:text>", send_message, name="send_message"),
    path("get_suggestions/", get_suggestions, name="get_suggestions"),
    path("access-denied/", access_denied_page, name="access_denied_page"),

    path("product-status/", AdditionalServicesView.as_view(), name="product_update_status"),

]
