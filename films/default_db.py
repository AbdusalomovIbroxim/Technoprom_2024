from films.models import Categories, SubCategories, SubCategoryCategory, Tag, TagCategory, TagSubcategory, Country, City
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction


def create_category_if_not_exists(slug, name_en, name_ru, name_uz, is_linked=False):
    if not Categories.objects.filter(slug=slug).exists():
        category = Categories.objects.create(
            slug=slug,
            name_en=name_en,
            name_ru=name_ru,
            name_uz=name_uz,
            is_linked=is_linked
        )
        return category
    else:
        return None


def create_subcategory_if_not_exists(slug, name_en, name_ru, name_uz, is_linked=False):
    if not SubCategories.objects.filter(slug=slug).exists():
        subcategory = SubCategories.objects.create(
            slug=slug,
            name_en=name_en,
            name_ru=name_ru,
            name_uz=name_uz,
            is_linked=is_linked
        )
        return subcategory
    else:
        return None


def create_subcategory_category_relation(subcategory_id, category_id):
    try:
        subcategory = SubCategories.objects.get(pk=subcategory_id)
        category = Categories.objects.get(pk=category_id)
        SubCategoryCategory.objects.get_or_create(
            subcategory=subcategory,
            category=category
        )
    except ObjectDoesNotExist:
        print(f"One of the provided subcategory_id ({subcategory_id}) or category_id ({category_id}) does not exist.")


def create_country_if_not_exists(slug, name_en, name_ru, name_uz):
    if not Country.objects.filter(slug=slug).exists():
        country = Country.objects.create(
            slug=slug,
            name_en=name_en,
            name_ru=name_ru,
            name_uz=name_uz
        )
        return country
    else:
        return None


def create_tags():
    tags_data = [
        (1, "Metal cutting equipment", "Металлорежущее оборудование", "Metal kesish uskunasi", 0),
        (2, "Equipment for heating metal and printing a pattern on it",
         "Оборудование для нагрева металла и печати на нем рисунк", "Metalni qizdirib unga naqsh bosuvchi uskuna", 0),
        (3, "Vacuum presse", "Вакуумные пресс", "Vaakumli presslar", 0),
        (4, "Drilling rig", "Буровые установки", "Burg'ulovchi dastgohlar", 0),
        (5, "Equipment for postforming", "Оборудование для постформинга", "Postforming uchun uskuna", 0),
        (6, "Format open cutting machine", "Форматные машины для открытой резки", "Formatli ochiq kesish dastgohlari",
         0),
        (7, "Laser cutting equipment", "Оборудование для лазерной резки", "Lazer kesish uskunasi", 0),
        (8, "Plating equipment", "Гальваническое оборудование", "Kromkalash uskunasi", 0),
        (9, "2 saw wood cutting equipment", "2 пилы, деревообрабатывающее оборудование",
         "2 arralik yog'och kesish uskunasi", 0),
        (10, "Thermoplastic machine", "Термопласт автомат", "Termoplastavtomat", 0),
        (11, "Plastic granulate production equipment", "Оборудование для производства пластикового гранулята",
         "Plastik garanulalat ishlab chiqarish uskunasi", 0),
        (12, "Equipment for the production of plastic containers", "Оборудование для производства пластиковой тары",
         "Plastik idishlar ishlab chiqarish uskunasi", 0),
        (13, "Plastic Pipe Production Line", "Линия по производству пластиковых труб",
         "Plastik truba ishlab chiqarish liniyasi", 0),
        (14, "Injection Molding Machine", "Машина для литья под давлением", "Inyeksion kaliplama mashinasi", 0),
        (15, "External Vacuum Packaging Equipment", "Внешнее вакуумное упаковочное оборудование",
         "Tashqi vakumli qadoqlash uskunasi", 0),
        (16, "Vacuum packaging equipment", "Вакуумно-упаковочное оборудование", "Vakumli qadoqlash uskunasi", 0),
        (17, "Blister packaging equipment", "Блистерное упаковочное оборудование", "Blister qadoqlash uskunasi", 0),
        (18, "Small Vacuum Packaging Equipment", "Маленькое вакуумное упаковочное оборудование",
         "Kichik vakumli qadoqlash uskunasi", 0),
        (19, "Vertical Single Chamber Vacuum Packaging Equipment",
         "Вертикальное однокамерное вакуумное упаковочное оборудование",
         "Vertikal, bir kamerali vakumli qadoqlash uskunasi", 0),
        (20, "Photos Separator", "Фотографиисепаратор", "Fotoseparator", 0),
        (21, 1, 1, 1, 1),
        (22, 2, 2, 2, 1),
        (23, 3, 3, 3, 1),
        (24, 4, 4, 4, 1),
        (25, 5, 5, 5, 1),
        (26, 6, 6, 6, 1),
        (27, 7, 7, 7, 1),
        (28, 8, 8, 8, 1)
    ]

    for data in tags_data:
        tag_id, name_en, name_ru, name_uz, is_linked = data
        tag, created = Tag.objects.get_or_create(
            id=tag_id,
            defaults={
                'name_en': name_en,
                'name_ru': name_ru,
                'name_uz': name_uz,
                'is_linked': is_linked
            }
        )


def create_tag_category_relations():
    tag_category_data = [
        (1, 1, 1),
        (2, 2, 1),
        (3, 3, 1),
        (4, 4, 1),
        (5, 5, 1),
        (6, 6, 1),
        (7, 1, 2),
        (8, 2, 2),
        (9, 3, 2),
        (10, 4, 2),
        (11, 5, 2),
        (12, 6, 2),
        (13, 1, 20),
        (14, 2, 20),
        (15, 3, 20),
        (16, 4, 20),
        (17, 5, 20),
        (18, 6, 20),
        (19, 1, 19),
        (20, 2, 19),
        (21, 3, 19),
        (22, 4, 19),
        (23, 5, 19),
        (24, 6, 19),
        (25, 1, 18),
        (26, 2, 18),
        (27, 3, 18),
        (28, 4, 18),
        (29, 5, 18),
        (30, 6, 18),
        (31, 1, 17),
        (32, 2, 17),
        (33, 3, 17),
        (34, 4, 17),
        (35, 5, 17),
        (36, 6, 17),
        (37, 1, 16),
        (38, 2, 16),
        (39, 3, 16),
        (40, 4, 16),
        (41, 5, 16),
        (42, 6, 16),
        (43, 1, 15),
        (44, 2, 15),
        (45, 3, 15),
        (46, 4, 15),
        (47, 5, 15),
        (48, 6, 15),
        (49, 1, 14),
        (50, 2, 14),
        (51, 3, 14),
        (52, 4, 14),
        (53, 5, 14),
        (54, 6, 14),
        (55, 1, 13),
        (56, 2, 13),
        (57, 3, 13),
        (58, 4, 13),
        (59, 5, 13),
        (60, 6, 13),
        (61, 1, 12),
        (62, 2, 12),
        (63, 3, 12),
        (64, 4, 12),
        (65, 5, 12),
        (66, 6, 12),
        (67, 1, 11),
        (68, 2, 11),
        (69, 3, 11),
        (70, 4, 11),
        (71, 5, 11),
        (72, 6, 11),
        (73, 1, 10),
        (74, 2, 10),
        (75, 3, 10),
        (76, 4, 10),
        (77, 5, 10),
        (78, 6, 10),
        (79, 1, 9),
        (80, 2, 9),
        (81, 3, 9),
        (82, 4, 9),
        (83, 5, 9),
        (84, 6, 9),
        (85, 1, 8),
        (86, 2, 8),
        (87, 3, 8),
        (88, 4, 8),
        (89, 5, 8),
        (90, 6, 8),
        (91, 1, 7),
        (92, 2, 7),
        (93, 3, 7),
        (94, 4, 7),
        (95, 5, 7),
        (96, 6, 7),
        (97, 1, 6),
        (98, 2, 6),
        (99, 3, 6),
        (100, 4, 6),
        (101, 5, 6),
        (102, 6, 6),
        (103, 1, 5),
        (104, 2, 5),
        (105, 3, 5),
        (106, 4, 5),
        (107, 5, 5),
        (108, 6, 5),
        (109, 1, 4),
        (110, 2, 4),
        (111, 3, 4),
        (112, 4, 4),
        (113, 5, 4),
        (114, 6, 4),
        (115, 1, 3),
        (116, 2, 3),
        (117, 3, 3),
        (118, 4, 3),
        (119, 5, 3),
        (120, 6, 3),
        (121, 7, 21),
        (122, 7, 22),
        (123, 8, 23),
        (124, 8, 24),
        (125, 9, 25),
        (126, 9, 26),
        (127, 10, 27),
        (128, 10, 28)
    ]

    for data in tag_category_data:
        tag_id, category_id, _ = data
        try:
            tag = Tag.objects.get(id=tag_id)
            category = Categories.objects.get(id=category_id)
            TagCategory.objects.get_or_create(tag=tag, category=category)
        except (Tag.DoesNotExist, Categories.DoesNotExist) as e:
            print(f"Error: {e}")


def create_tag_subcategory_relations():
    tag_subcategory_data = [
        (1, 1, 1),
        (2, 2, 1),
        (3, 3, 1),
        (4, 4, 1),
        (5, 5, 1),
        (6, 6, 1),
        (7, 7, 1),
        (8, 8, 1),
        (9, 1, 2),
        (10, 2, 2),
        (11, 3, 2),
        (12, 4, 2),
        (13, 5, 2),
        (14, 6, 2),
        (15, 7, 2),
        (16, 8, 2),
        (17, 1, 3),
        (18, 2, 3),
        (19, 3, 3),
        (20, 4, 3),
        (21, 5, 3),
        (22, 6, 3),
        (23, 7, 3),
        (24, 8, 3),
        (25, 1, 20),
        (26, 2, 20),
        (27, 3, 20),
        (28, 4, 20),
        (29, 5, 20),
        (30, 6, 20),
        (31, 7, 20),
        (32, 8, 20),
        (33, 1, 19),
        (34, 2, 19),
        (35, 3, 19),
        (36, 4, 19),
        (37, 5, 19),
        (38, 6, 19),
        (39, 7, 19),
        (40, 8, 19),
        (41, 1, 18),
        (42, 2, 18),
        (43, 3, 18),
        (44, 4, 18),
        (45, 5, 18),
        (46, 6, 18),
        (47, 7, 18),
        (48, 8, 18),
        (49, 1, 17),
        (50, 2, 17),
        (51, 3, 17),
        (52, 4, 17),
        (53, 5, 17),
        (54, 6, 17),
        (55, 7, 17),
        (56, 8, 17),
        (57, 1, 16),
        (58, 2, 16),
        (59, 3, 16),
        (60, 4, 16),
        (61, 5, 16),
        (62, 6, 16),
        (63, 7, 16),
        (64, 8, 16),
        (65, 1, 15),
        (66, 2, 15),
        (67, 3, 15),
        (68, 4, 15),
        (69, 5, 15),
        (70, 6, 15),
        (71, 7, 15),
        (72, 8, 15),
        (73, 1, 14),
        (74, 2, 14),
        (75, 3, 14),
        (76, 4, 14),
        (77, 5, 14),
        (78, 6, 14),
        (79, 7, 14),
        (80, 8, 14),
        (81, 1, 13),
        (82, 2, 13),
        (83, 3, 13),
        (84, 4, 13),
        (85, 5, 13),
        (86, 6, 13),
        (87, 7, 13),
        (88, 8, 13),
        (89, 1, 12),
        (90, 2, 12),
        (91, 3, 12),
        (92, 4, 12),
        (93, 5, 12),
        (94, 6, 12),
        (95, 7, 12),
        (96, 8, 12),
        (97, 1, 11),
        (98, 2, 11),
        (99, 3, 11),
        (100, 4, 11),
        (101, 5, 11),
        (102, 6, 11),
        (103, 7, 11),
        (104, 8, 11),
        (105, 1, 10),
        (106, 2, 10),
        (107, 3, 10),
        (108, 4, 10),
        (109, 5, 10),
        (110, 6, 10),
        (111, 7, 10),
        (112, 8, 10),
        (113, 1, 9),
        (114, 2, 9),
        (115, 3, 9),
        (116, 4, 9),
        (117, 5, 9),
        (118, 6, 9),
        (119, 7, 9),
        (120, 8, 9),
        (121, 1, 8),
        (122, 2, 8),
        (123, 3, 8),
        (124, 4, 8),
        (125, 5, 8),
        (126, 6, 8),
        (127, 7, 8),
        (128, 8, 8),
        (129, 1, 7),
        (130, 2, 7),
        (131, 3, 7),
        (132, 4, 7),
        (133, 5, 7),
        (134, 6, 7),
        (135, 7, 7),
        (136, 8, 7),
        (137, 1, 6),
        (138, 2, 6),
        (139, 3, 6),
        (140, 4, 6),
        (141, 5, 6),
        (142, 6, 6),
        (143, 7, 6),
        (144, 8, 6),
        (145, 1, 5),
        (146, 2, 5),
        (147, 3, 5),
        (148, 4, 5),
        (149, 5, 5),
        (150, 6, 5),
        (151, 7, 5),
        (152, 8, 5),
        (153, 1, 4),
        (154, 2, 4),
        (155, 3, 4),
        (156, 4, 4),
        (157, 5, 4),
        (158, 6, 4),
        (159, 7, 4),
        (160, 8, 4),
        (161, 9, 21),
        (162, 10, 22),
        (163, 11, 23),
        (164, 12, 24),
        (165, 13, 25),
        (166, 14, 26),
        (167, 15, 27),
        (168, 16, 28),
        # Вставьте сюда данные о связях между тегами и подкатегориями
    ]

    for data in tag_subcategory_data:
        tag_id, subcategory_id, _ = data
        try:
            tag = Tag.objects.get(id=tag_id)
            subcategory = SubCategories.objects.get(id=subcategory_id)
            TagSubcategory.objects.get_or_create(tag=tag, subcategory=subcategory)
        except (Tag.DoesNotExist, SubCategories.DoesNotExist) as e:
            print(f"Error: {e}")


def add_tags():
    create_tags()
    create_tag_category_relations()
    create_tag_subcategory_relations()


def add_categories():
    categories_data = [
        {"slug": "new-machinery", "name_en": "New machinery", "name_ru": "Новые оборудования",
         "name_uz": "Yangi uskunalar"},
        {"slug": "used-machinery", "name_en": "Used machinery", "name_ru": "Б/У оборудования",
         "name_uz": "Ishlatilgan uskuna"},
        {"slug": "raw-material", "name_en": "Raw material", "name_ru": "Сырьё", "name_uz": "Xom ashyo"},
        {"slug": "Technicians", "name_en": "Technologist", "name_ru": "Технолог", "name_uz": "Texnolog"},
        {"slug": "service", "name_en": "Service", "name_ru": "Услуга", "name_uz": "Xizmat ko'rsatish"},
        {"slug": "recycled-raw-materials", "name_en": "Recycled raw materials", "name_ru": "Вторичный сырьё",
         "name_uz": "Ikkilamchi xom ashyo"},
        {"slug": "C1", "name_en": "C1", "name_ru": "C1", "name_uz": "C1", "is_linked": True},
        {"slug": "C2", "name_en": "C2", "name_ru": "C2", "name_uz": "C2", "is_linked": True},
        {"slug": "C3", "name_en": "C3", "name_ru": "C3", "name_uz": "C3", "is_linked": True},
        {"slug": "C4", "name_en": "C4", "name_ru": "C4", "name_uz": "C4", "is_linked": True},
    ]

    for category_data in categories_data:
        create_category_if_not_exists(**category_data)


def add_subcategories():
    subcategories_data = [
        {"slug": "furniture", "name_en": "Furniture", "name_ru": "Мебель", "name_uz": "Mebel"},
        {"slug": "food-processing", "name_en": "Food processing", "name_ru": "Пищевая промышленность",
         "name_uz": "Oziq-ovqat"},
        {"slug": "plastic", "name_en": "Plastic", "name_ru": "Пластмасса", "name_uz": "Plastmassa"},
        {"slug": "packaging", "name_en": "Packaging", "name_ru": "Упаковка", "name_uz": "Qadoqlash"},
        {"slug": "agro", "name_en": "Agro", "name_ru": "Агро", "name_uz": "Agro"},
        {"slug": "metal", "name_en": "Metall", "name_ru": "Металлургия", "name_uz": "Metal"},
        {"slug": "construction", "name_en": "Construction", "name_ru": "Строительство", "name_uz": "Qurilish"},
        {"slug": "c1s1", "name_en": "C1S1", "name_ru": "С1S1", "name_uz": "С1S1", "is_linked": True},
        {"slug": "c1s2", "name_en": "C1S2", "name_ru": "С1S2", "name_uz": "С1S2", "is_linked": True},
        {"slug": "c2s1", "name_en": "C2S1", "name_ru": "С2S1", "name_uz": "С2S1", "is_linked": True},
        {"slug": "c2s2", "name_en": "C2S2", "name_ru": "С2S2", "name_uz": "С2S2", "is_linked": True},
        {"slug": "c3s1", "name_en": "C3S1", "name_ru": "С3S1", "name_uz": "С3S1", "is_linked": True},
        {"slug": "c3s2", "name_en": "C3S2", "name_ru": "С3S2", "name_uz": "С3S2", "is_linked": True},
        {"slug": "c4s1", "name_en": "C4S1", "name_ru": "С4S1", "name_uz": "С4S1", "is_linked": True},
        {"slug": "c4s2", "name_en": "C4S2", "name_ru": "С4S2", "name_uz": "С4S2", "is_linked": True},
    ]
    subcategory_category_data = [
        (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1),  # Категория 1, связь с подкатегориями
        (9, 2), (10, 3), (11, 4), (12, 5), (13, 6),  # Категория 2-6, связь с подкатегориями
        (14, 2), (15, 3), (16, 4), (17, 5), (18, 6),  # Категория 2-6, связь с подкатегориями
        (19, 2), (20, 3), (21, 4), (22, 5), (23, 6),  # Категория 2-6, связь с подкатегориями
        (24, 2), (25, 3), (26, 4), (27, 5), (28, 6),  # Категория 2-6, связь с подкатегориями
        (29, 2), (30, 3), (31, 4), (32, 5), (33, 6),  # Категория 2-6, связь с подкатегориями
        (34, 2), (35, 3), (36, 4), (37, 5), (38, 6),  # Категория 2-6, связь с подкатегориями
        (39, 2), (40, 3), (41, 4), (42, 5), (43, 6),  # Категория 2-6, связь с подкатегориями
        (44, 2), (45, 3), (46, 4), (47, 5), (48, 6),  # Категория 2-6, связь с подкатегориями
        (49, 7), (50, 7),  # Категория 7, связь с подкатегориями
        (51, 8),  # Категория 8, связь с подкатегориями
        (52, 9),  # Категория 9, связь с подкатегориями
        (53, 10), (54, 10),  # Категория 10, связь с подкатегориями
    ]
    for subcategory_data in subcategories_data:
        create_subcategory_if_not_exists(**subcategory_data)
    for subcategory_id, category_id in subcategory_category_data:
        create_subcategory_category_relation(subcategory_id, category_id)


def add_countries():
    countries_data = [
        {"slug": "uzbekistan", "name_en": "Uzbekistan", "name_ru": "Узбекистан", "name_uz": "O'zbekiston"},
        {"slug": "afghanistan", "name_en": "Afghanistan", "name_ru": "Афганистан", "name_uz": "Afg'oniston"},
        {"slug": "albania", "name_en": "Albania", "name_ru": "Албания", "name_uz": "Albaniya"},
        {"slug": "algeria", "name_en": "Algeria", "name_ru": "Алжир", "name_uz": "Jazoir"},
        {"slug": "andorra", "name_en": "Andorra", "name_ru": "Андорра", "name_uz": "Andorra"},
        {"slug": "angola", "name_en": "Angola", "name_ru": "Ангола", "name_uz": "Angola"},
        {"slug": "antigua-and-barbuda", "name_en": "Antigua and Barbuda", "name_ru": "Антигуа и Барбуда",
         "name_uz": "Antigua va Barbuda"},
        {"slug": "argentina", "name_en": "Argentina", "name_ru": "Аргентина", "name_uz": "Argentina"},
        {"slug": "armenia", "name_en": "Armenia", "name_ru": "Армения", "name_uz": "Armaniston"},
        {"slug": "australia", "name_en": "Australia", "name_ru": "Австралия", "name_uz": "Avstraliya"},
        {"slug": "austria", "name_en": "Austria", "name_ru": "Австрия", "name_uz": "Avstriya"},
        {"slug": "azerbaijan", "name_en": "Azerbaijan", "name_ru": "Азербайджан", "name_uz": "Ozarbayjon"},
        {"slug": "bahamas", "name_en": "Bahamas", "name_ru": "Багамы", "name_uz": "Bagama orollari"},
        {"slug": "bahrain", "name_en": "Bahrain", "name_ru": "Бахрейн", "name_uz": "Bahrayn"},
        {"slug": "bangladesh", "name_en": "Bangladesh", "name_ru": "Бангладеш", "name_uz": "Bangladesh"},
        {"slug": "barbados", "name_en": "Barbados", "name_ru": "Барбадос", "name_uz": "Barbados"},
        {"slug": "belarus", "name_en": "Belarus", "name_ru": "Беларусь", "name_uz": "Belarusiya"},
        {"slug": "belgium", "name_en": "Belgium", "name_ru": "Бельгия", "name_uz": "Belgiya"},
        {"slug": "belize", "name_en": "Belize", "name_ru": "Белиз", "name_uz": "Beliz"},
        {"slug": "benin", "name_en": "Benin", "name_ru": "Бенин", "name_uz": "Benin"},
        {"slug": "bhutan", "name_en": "Bhutan", "name_ru": "Бутан", "name_uz": "Butan"},
        {"slug": "bolivia", "name_en": "Bolivia", "name_ru": "Боливия", "name_uz": "Boliviya"},
        {"slug": "bosnia-and-herzegovina", "name_en": "Bosnia and Herzegovina", "name_ru": "Босния и Герцеговина",
         "name_uz": "Bosniya va Gertsegovina"},
        {"slug": "botswana", "name_en": "Botswana", "name_ru": "Ботсвана", "name_uz": "Botsvana"},
        {"slug": "brazil", "name_en": "Brazil", "name_ru": "Бразилия", "name_uz": "Braziliya"},
        {"slug": "brunei", "name_en": "Brunei", "name_ru": "Бруней", "name_uz": "Bruney"},
        {"slug": "bulgaria", "name_en": "Bulgaria", "name_ru": "Болгария", "name_uz": "Bolgariya"},
        {"slug": "burkina-faso", "name_en": "Burkina Faso", "name_ru": "Буркина-Фасо", "name_uz": "Burkina-Faso"},
        {"slug": "burundi", "name_en": "Burundi", "name_ru": "Бурунди", "name_uz": "Burundi"},
        {"slug": "cambodia", "name_en": "Cambodia", "name_ru": "Камбоджа", "name_uz": "Kambodja"},
        {"slug": "cameroon", "name_en": "Cameroon", "name_ru": "Камерун", "name_uz": "Kamerun"},
        {"slug": "canada", "name_en": "Canada", "name_ru": "Канада", "name_uz": "Kanada"},
        {"slug": "cape-verde", "name_en": "Cape Verde", "name_ru": "Кабо-Верде", "name_uz": "Kabo-Verde"},
        {"slug": "central-african-republic", "name_en": "Central African Republic",
         "name_ru": "Центрально-Африканская Республика", "name_uz": "Markaziy Afrika Respublikasi"},
        {"slug": "chad", "name_en": "Chad", "name_ru": "Чад", "name_uz": "Chad"},
        {"slug": "chile", "name_en": "Chile", "name_ru": "Чили", "name_uz": "Chili"},
        {"slug": "china", "name_en": "China", "name_ru": "Китай", "name_uz": "Xitoy"},
        {"slug": "colombia", "name_en": "Colombia", "name_ru": "Колумбия", "name_uz": "Kolumbiya"},
        {"slug": "comoros", "name_en": "Comoros", "name_ru": "Коморские острова", "name_uz": "Komor orollari"},
        {"slug": "congo", "name_en": "Congo", "name_ru": "Конго", "name_uz": "Kongo"},
        {"slug": "costa-rica", "name_en": "Costa Rica", "name_ru": "Коста-Рика", "name_uz": "Kosta-Rika"},
        {"slug": "croatia", "name_en": "Croatia", "name_ru": "Хорватия", "name_uz": "Xorvatiya"},
        {"slug": "cuba", "name_en": "Cuba", "name_ru": "Куба", "name_uz": "Kuba"},
        {"slug": "cyprus", "name_en": "Cyprus", "name_ru": "Кипр", "name_uz": "Kipr"},
        {"slug": "czech-republic", "name_en": "Czech Republic", "name_ru": "Чешская Республика",
         "name_uz": "Chex Respublikasi"},
        {"slug": "denmark", "name_en": "Denmark", "name_ru": "Дания", "name_uz": "Daniya"},
        {"slug": "djibouti", "name_en": "Djibouti", "name_ru": "Джибути", "name_uz": "Jibuti"},
        {"slug": "dominica", "name_en": "Dominica", "name_ru": "Доминика", "name_uz": "Dominika"},
        {"slug": "dominican-republic", "name_en": "Dominican Republic", "name_ru": "Доминиканская Республика",
         "name_uz": "Dominika Respublikasi"},
        {"slug": "east-timor", "name_en": "East Timor", "name_ru": "Восточный Тимор", "name_uz": "Sharqiy Timor"},
        {"slug": "ecuador", "name_en": "Ecuador", "name_ru": "Эквадор", "name_uz": "Ekvador"},
        {"slug": "egypt", "name_en": "Egypt", "name_ru": "Египет", "name_uz": "Misr"},
        {"slug": "el-salvador", "name_en": "El Salvador", "name_ru": "Сальвадор", "name_uz": "El Salvador"},
        {"slug": "equatorial-guinea", "name_en": "Equatorial Guinea", "name_ru": "Экваториальная Гвинея",
         "name_uz": "Ekvatorial Gvineya"},
        {"slug": "eritrea", "name_en": "Eritrea", "name_ru": "Эритрея", "name_uz": "Eritreya"},
        {"slug": "estonia", "name_en": "Estonia", "name_ru": "Эстония", "name_uz": "Estoniya"},
        {"slug": "ethiopia", "name_en": "Ethiopia", "name_ru": "Эфиопия", "name_uz": "Efiopiya"},
        {"slug": "fiji", "name_en": "Fiji", "name_ru": "Фиджи", "name_uz": "Fiji"},
        {"slug": "finland", "name_en": "Finland", "name_ru": "Финляндия", "name_uz": "Finlyandiya"},
        {"slug": "france", "name_en": "France", "name_ru": "Франция", "name_uz": "Fransiya"},
        {"slug": "gabon", "name_en": "Gabon", "name_ru": "Габон", "name_uz": "Gabon"},
        {"slug": "gambia", "name_en": "Gambia", "name_ru": "Гамбия", "name_uz": "Gambiya"},
        {"slug": "georgia", "name_en": "Georgia", "name_ru": "Грузия", "name_uz": "Gruziya"},
        {"slug": "germany", "name_en": "Germany", "name_ru": "Германия", "name_uz": "Germaniya"},
        {"slug": "ghana", "name_en": "Ghana", "name_ru": "Гана", "name_uz": "Gana"},
        {"slug": "greece", "name_en": "Greece", "name_ru": "Греция", "name_uz": "Gretsiya"},
        {"slug": "grenada", "name_en": "Grenada", "name_ru": "Гренада", "name_uz": "Grenada"},
        {"slug": "guatemala", "name_en": "Guatemala", "name_ru": "Гватемала", "name_uz": "Gvatemala"},
        {"slug": "guinea", "name_en": "Guinea", "name_ru": "Гвинея", "name_uz": "Gvineya"},
        {"slug": "guinea-bissau", "name_en": "Guinea-Bissau", "name_ru": "Гвинея-Бисау", "name_uz": "Gvineya-Bisau"},
        {"slug": "guyana", "name_en": "Guyana", "name_ru": "Гайана", "name_uz": "Gayana"},
        {"slug": "haiti", "name_en": "Haiti", "name_ru": "Гаити", "name_uz": "Gaiti"},
        {"slug": "honduras", "name_en": "Honduras", "name_ru": "Гондурас", "name_uz": "Gonduras"},
        {"slug": "hungary", "name_en": "Hungary", "name_ru": "Венгрия", "name_uz": "Vengriya"},
        {"slug": "iceland", "name_en": "Iceland", "name_ru": "Исландия", "name_uz": "Islandiya"},
        {"slug": "india", "name_en": "India", "name_ru": "Индия", "name_uz": "Hindiston"},
        {"slug": "indonesia", "name_en": "Indonesia", "name_ru": "Индонезия", "name_uz": "Indoneziya"},
        {"slug": "iran", "name_en": "Iran", "name_ru": "Иран", "name_uz": "Eron"},
        {"slug": "iraq", "name_en": "Iraq", "name_ru": "Ирак", "name_uz": "Iroq"},
        {"slug": "ireland", "name_en": "Ireland", "name_ru": "Ирландия", "name_uz": "Irlandiya"},
        {"slug": "israel", "name_en": "Israel", "name_ru": "Израиль", "name_uz": "Isroil"},
        {"slug": "italy", "name_en": "Italy", "name_ru": "Италия", "name_uz": "Italiya"},
        {"slug": "jamaica", "name_en": "Jamaica", "name_ru": "Ямайка", "name_uz": "Yamayka"},
        {"slug": "japan", "name_en": "Japan", "name_ru": "Япония", "name_uz": "Yaponiya"},
        {"slug": "jordan", "name_en": "Jordan", "name_ru": "Иордания", "name_uz": "Iordaniya"},
        {"slug": "kazakhstan", "name_en": "Kazakhstan", "name_ru": "Казахстан", "name_uz": "Qozog'iston"},
        {"slug": "kenya", "name_en": "Kenya", "name_ru": "Кения", "name_uz": "Keniya"},
        {"slug": "kiribati", "name_en": "Kiribati", "name_ru": "Кирибати", "name_uz": "Kiribati"},
        {"slug": "korea-north", "name_en": "Korea, North", "name_ru": "«Корея, Север»", "name_uz": "Koreya, Shimoliy"},
        {"slug": "korea-south", "name_en": "Korea, South", "name_ru": "Корея, Юг", "name_uz": "Koreya, Janubiy"},
        {"slug": "kosovo", "name_en": "Kosovo", "name_ru": "Косово", "name_uz": "Kosovo"},
        {"slug": "kuwait", "name_en": "Kuwait", "name_ru": "Кувейт", "name_uz": "Quvayt"},
        {"slug": "kyrgyzstan", "name_en": "Kyrgyzstan", "name_ru": "Кыргызстан", "name_uz": "Qirg'iziston"},
        {"slug": "laos", "name_en": "Laos", "name_ru": "Лаос", "name_uz": "Laos"},
        {"slug": "latvia", "name_en": "Latvia", "name_ru": "Латвия", "name_uz": "Latviya"},
        {"slug": "lebanon", "name_en": "Lebanon", "name_ru": "Ливан", "name_uz": "Livan"},
        {"slug": "lesotho", "name_en": "Lesotho", "name_ru": "Лесото", "name_uz": "Lesoto"},
        {"slug": "liberia", "name_en": "Liberia", "name_ru": "Либерия", "name_uz": "Liberiya"},
        {"slug": "libya", "name_en": "Libya", "name_ru": "Ливия", "name_uz": "Liviya"},
        {"slug": "liechtenstein", "name_en": "Liechtenstein", "name_ru": "Лихтенштейн", "name_uz": "Lixtenshteyn"},
        {"slug": "lithuania", "name_en": "Lithuania", "name_ru": "Литва", "name_uz": "Litva"},
        {"slug": "luxembourg", "name_en": "Luxembourg", "name_ru": "Люксембург", "name_uz": "Lyuksemburg"},
        {"slug": "macedonia", "name_en": "Macedonia", "name_ru": "Македония", "name_uz": "Makedoniya"},
        {"slug": "madagascar", "name_en": "Madagascar", "name_ru": "Мадагаскар", "name_uz": "Madagaskar"},
        {"slug": "malawi", "name_en": "Malawi", "name_ru": "Малави", "name_uz": "Malavi"},
        {"slug": "malaysia", "name_en": "Malaysia", "name_ru": "Малайзия", "name_uz": "Malayziya"},
        {"slug": "maldives", "name_en": "Maldives", "name_ru": "Мальдивы", "name_uz": "Maldiv orollari"},
        {"slug": "mali", "name_en": "Mali", "name_ru": "Мали", "name_uz": "Mali"},
        {"slug": "malta", "name_en": "Malta", "name_ru": "Мальта", "name_uz": "Malta"},
        {"slug": "marshall-islands", "name_en": "Marshall Islands", "name_ru": "Маршалловы острова",
         "name_uz": "Marshall orollari"},
        {"slug": "mauritania", "name_en": "Mauritania", "name_ru": "Мавритания", "name_uz": "Mavritaniya"},
        {"slug": "mauritius", "name_en": "Mauritius", "name_ru": "Маврикий", "name_uz": "Mavrikiy"},
        {"slug": "mexico", "name_en": "Mexico", "name_ru": "Мексика", "name_uz": "Meksika"},
        {"slug": "micronesia", "name_en": "Micronesia", "name_ru": "Микронезия", "name_uz": "Mikroneziya"},
        {"slug": "moldova", "name_en": "Moldova", "name_ru": "Молдова", "name_uz": "Moldova"},
        {"slug": "monaco", "name_en": "Monaco", "name_ru": "Монако", "name_uz": "Monako"},
        {"slug": "mongolia", "name_en": "Mongolia", "name_ru": "Монголия", "name_uz": "Mo'g'uliston"},
        {"slug": "montenegro", "name_en": "Montenegro", "name_ru": "Черногория", "name_uz": "Chernogoriya"},
        {"slug": "morocco", "name_en": "Morocco", "name_ru": "Марокко", "name_uz": "Marokash"},
        {"slug": "mozambique", "name_en": "Mozambique", "name_ru": "Мозамбик", "name_uz": "Mozambik"},
        {"slug": "myanmar", "name_en": "Myanmar", "name_ru": "Мьянма", "name_uz": "Myanma"},
        {"slug": "namibia", "name_en": "Namibia", "name_ru": "Намибия", "name_uz": "Namibiya"},
        {"slug": "nauru", "name_en": "Nauru", "name_ru": "Науру", "name_uz": "Nauru"},
        {"slug": "nepal", "name_en": "Nepal", "name_ru": "Непал", "name_uz": "Nepal"},
        {"slug": "netherlands", "name_en": "Netherlands", "name_ru": "Нидерланды", "name_uz": "Niderlandiya"},
        {"slug": "new-zealand", "name_en": "New Zealand", "name_ru": "Новая Зеландия", "name_uz": "Yangi Zelandiya"},
        {"slug": "nicaragua", "name_en": "Nicaragua", "name_ru": "Никарагуа", "name_uz": "Nikaragua"},
        {"slug": "niger", "name_en": "Niger", "name_ru": "Нигер", "name_uz": "Niger"},
        {"slug": "nigeria", "name_en": "Nigeria", "name_ru": "Нигерия", "name_uz": "Nigeriya"},
        {"slug": "norway", "name_en": "Norway", "name_ru": "Норвегия", "name_uz": "Norvegiya"},
        {"slug": "oman", "name_en": "Oman", "name_ru": "Оман", "name_uz": "Ummon"},
        {"slug": "pakistan", "name_en": "Pakistan", "name_ru": "Пакистан", "name_uz": "Pokiston"},
        {"slug": "palau", "name_en": "Palau", "name_ru": "Палау", "name_uz": "Palau"},
        {"slug": "palestine", "name_en": "Palestine", "name_ru": "Палестина", "name_uz": "Falastin"},
        {"slug": "panama", "name_en": "Panama", "name_ru": "Панама", "name_uz": "Panama"},
        {"slug": "papua-new-guinea", "name_en": "Papua New Guinea", "name_ru": "Папуа - Новая Гвинея",
         "name_uz": "Papua-Yangi Gvineya"},
        {"slug": "paraguay", "name_en": "Paraguay", "name_ru": "Парагвай", "name_uz": "Paragvay"},
        {"slug": "peru", "name_en": "Peru", "name_ru": "Перу", "name_uz": "Peru"},
        {"slug": "philippines", "name_en": "Philippines", "name_ru": "Филиппины", "name_uz": "Filippin"},
        {"slug": "poland", "name_en": "Poland", "name_ru": "Польша", "name_uz": "Polsha"},
        {"slug": "portugal", "name_en": "Portugal", "name_ru": "Португалия", "name_uz": "Portugaliya"},
        {"slug": "qatar", "name_en": "Qatar", "name_ru": "Катар", "name_uz": "Qatar"},
        {"slug": "romania", "name_en": "Romania", "name_ru": "Румыния", "name_uz": "Ruminiya"},
        {"slug": "russia", "name_en": "Russia", "name_ru": "Россия", "name_uz": "Rossiya"},
        {"slug": "rwanda", "name_en": "Rwanda", "name_ru": "Руанда", "name_uz": "Ruanda"},
        {"slug": "saint-kitts-and-nevis", "name_en": "Saint Kitts and Nevis", "name_ru": "Сент-Китс и Невис",
         "name_uz": "Sent-Kitts va Nevis"},
        {"slug": "saint-lucia", "name_en": "Saint Lucia", "name_ru": "Санкт-Люсия", "name_uz": "Sent-Lyusiya"},
        {"slug": "saint-vincent-and-the-grenadines", "name_en": "Saint Vincent and the Grenadines",
         "name_ru": "Святой Винсент и Гренадины", "name_uz": "Sent-Vinsent va Grenadin orollari"},
        {"slug": "samoa", "name_en": "Samoa", "name_ru": "Самоа", "name_uz": "Samoa"},
        {"slug": "san-marino", "name_en": "San Marino", "name_ru": "Сан-Марино", "name_uz": "San-Marino"},
        {"slug": "sao-tome-and-principe", "name_en": "Sao Tome and Principe", "name_ru": "Сан-Томе и Принсипи",
         "name_uz": "San-Tome va Prinsipi"},
        {"slug": "saudi-arabia", "name_en": "Saudi Arabia", "name_ru": "Саудовская Аравия",
         "name_uz": "Saudiya Arabistoni"},
        {"slug": "senegal", "name_en": "Senegal", "name_ru": "Сенегал", "name_uz": "Senegal"},
        {"slug": "serbia", "name_en": "Serbia", "name_ru": "Сербия", "name_uz": "Serbiya"},
        {"slug": "seychelles", "name_en": "Seychelles", "name_ru": "Сейшельские острова",
         "name_uz": "Seyshel orollari"},
        {"slug": "sierra-leone", "name_en": "Sierra Leone", "name_ru": "Сьерра-Леоне", "name_uz": "Syerra-Leone"},
        {"slug": "singapore", "name_en": "Singapore", "name_ru": "Сингапур", "name_uz": "Singapur"},
        {"slug": "slovakia", "name_en": "Slovakia", "name_ru": "Словакия", "name_uz": "Slovakiya"},
        {"slug": "slovenia", "name_en": "Slovenia", "name_ru": "Словения", "name_uz": "Sloveniya"},
        {"slug": "solomon-islands", "name_en": "Solomon Islands", "name_ru": "Соломоновы острова",
         "name_uz": "Solomon orollari"},
        {"slug": "somalia", "name_en": "Somalia", "name_ru": "Сомали", "name_uz": "Somali"},
        {"slug": "south-africa", "name_en": "South Africa", "name_ru": "Южная Африка", "name_uz": "Janubiy Afrika"},
        {"slug": "south-sudan", "name_en": "South Sudan", "name_ru": "южный Судан", "name_uz": "Janubiy Sudan"},
        {"slug": "spain", "name_en": "Spain", "name_ru": "Испания", "name_uz": "Ispaniya"},
        {"slug": "sri-lanka", "name_en": "Sri Lanka", "name_ru": "Шри-Ланка", "name_uz": "Shri-Lanka"},
        {"slug": "sudan", "name_en": "Sudan", "name_ru": "Судан", "name_uz": "Sudan"},
        {"slug": "suriname", "name_en": "Suriname", "name_ru": "Суринам", "name_uz": "Surinam"},
        {"slug": "swaziland", "name_en": "Swaziland", "name_ru": "Свазиленд", "name_uz": "Svazilend"},
        {"slug": "sweden", "name_en": "Sweden", "name_ru": "Швеция", "name_uz": "Shvetsiya"},
        {"slug": "switzerland", "name_en": "Switzerland", "name_ru": "Швейцария", "name_uz": "Shveytsariya"},
        {"slug": "syria", "name_en": "Syria", "name_ru": "Сирия", "name_uz": "Suriya"},
        {"slug": "taiwan", "name_en": "Taiwan", "name_ru": "Тайвань", "name_uz": "Tayvan"},
        {"slug": "tajikistan", "name_en": "Tajikistan", "name_ru": "Таджикистан", "name_uz": "Tojikiston"},
        {"slug": "tanzania", "name_en": "Tanzania", "name_ru": "Танзания", "name_uz": "Tanzaniya"},
        {"slug": "thailand", "name_en": "Thailand", "name_ru": "Таиланд", "name_uz": "Tailand"},
        {"slug": "togo", "name_en": "Togo", "name_ru": "Того", "name_uz": "Togo"},
        {"slug": "tonga", "name_en": "Tonga", "name_ru": "Тонга", "name_uz": "Tonga"},
        {"slug": "trinidad-and-tobago", "name_en": "Trinidad and Tobago", "name_ru": "Тринидад и Тобаго",
         "name_uz": "Trinidad va Tobago"},
        {"slug": "tunisia", "name_en": "Tunisia", "name_ru": "Тунис", "name_uz": "Tunis"},
        {"slug": "turkey", "name_en": "Turkey", "name_ru": "Турция", "name_uz": "Turkiya"},
        {"slug": "turkmenistan", "name_en": "Turkmenistan", "name_ru": "Туркменистан", "name_uz": "Turkmaniston"},
        {"slug": "tuvalu", "name_en": "Tuvalu", "name_ru": "Тувалу", "name_uz": "Tuvalu"},
        {"slug": "uganda", "name_en": "Uganda", "name_ru": "Уганда", "name_uz": "Uganda"},
        {"slug": "ukraine", "name_en": "Ukraine", "name_ru": "Украина", "name_uz": "Ukraina"},
        {"slug": "united-arab-emirates", "name_en": "United Arab Emirates", "name_ru": "Объединенные Арабские Эмираты",
         "name_uz": "Birlashgan Arab Amirliklari"},
        {"slug": "united-kingdom", "name_en": "United Kingdom", "name_ru": "Великобритания",
         "name_uz": "Buyuk Britaniya"},
        {"slug": "united-states", "name_en": "United States", "name_ru": "Соединенные Штаты",
         "name_uz": "Qo'shma Shtatlar"},
        {"slug": "uruguay", "name_en": "Uruguay", "name_ru": "Уругвай", "name_uz": "Urugvay"},
        {"slug": "uzbekistan", "name_en": "Uzbekistan", "name_ru": "Узбекистан", "name_uz": "O'zbekiston"},
        {"slug": "vanuatu", "name_en": "Vanuatu", "name_ru": "Вануату", "name_uz": "Vanuatu"},
        {"slug": "vatican-city", "name_en": "Vatican City", "name_ru": "Ватикан", "name_uz": "Vatikan"},
        {"slug": "venezuela", "name_en": "Venezuela", "name_ru": "Венесуэла", "name_uz": "Venesuela"},
        {"slug": "vietnam", "name_en": "Vietnam", "name_ru": "Вьетнам", "name_uz": "Vyetnam"},
        {"slug": "yemen", "name_en": "Yemen", "name_ru": "Йемен", "name_uz": "Yaman"},
        {"slug": "zambia", "name_en": "Zambia", "name_ru": "Замбия", "name_uz": "Zambiya"},
        {"slug": "zimbabwe", "name_en": "Zimbabwe", "name_ru": "Зимбабве", "name_uz": "Zimbabve"},
    ]
    for country_data in countries_data:
        create_country_if_not_exists(**country_data)


@transaction.atomic
def add_cities():
    cities_data = [
        {"slug": "tashkent", "name": "Ташкент", "country_slug": "uzbekistan"},
        {"slug": "andijon", "name": "Андижанская область", "country_slug": "uzbekistan"},
        {"slug": "buxoro", "name": "Бухарская область", "country_slug": "uzbekistan"},
        {"slug": "fargona", "name": "Ферганская область", "country_slug": "uzbekistan"},
        {"slug": "jizzax", "name": "Джизакская область", "country_slug": "uzbekistan"},
        {"slug": "namangan", "name": "Наманганская область", "country_slug": "uzbekistan"},
        {"slug": "navoi", "name": "Навоийская область", "country_slug": "uzbekistan"},
        {"slug": "qashqadaryo", "name": "Кашкадарьинская область", "country_slug": "uzbekistan"},
        {"slug": "samarqand", "name": "Самаркандская область", "country_slug": "uzbekistan"},
        {"slug": "sirdaryo", "name": "Сырдарьинская область", "country_slug": "uzbekistan"},
        {"slug": "surxandaryo", "name": "Сурхандарьинская область", "country_slug": "uzbekistan"},
        {"slug": "toshkent-viloyati", "name": "Ташкентская область", "country_slug": "uzbekistan"},
        {"slug": "xorazm", "name": "Хорезмская область", "country_slug": "uzbekistan"},
        {"slug": "Qoraqalpogiston-respublikasi", "name": "Республика Каракалпакстан", "country_slug": "uzbekistan"}
    ]

    for city_info in cities_data:
        country_slug = city_info["country_slug"]
        country = Country.objects.get(slug=country_slug)
        City.objects.create(
            slug=city_info["slug"],
            country=country,
            name=city_info["name"]
        )
