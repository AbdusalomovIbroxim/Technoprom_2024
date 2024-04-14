from films.models import Categories, SubCategories, SubCategoryCategory
from django.core.exceptions import ObjectDoesNotExist


def create_category_if_not_exists(slug, name_en, name_ru, name_uz):
    if not Categories.objects.filter(slug=slug).exists():
        category = Categories.objects.create(
            slug=slug,
            name_en=name_en,
            name_ru=name_ru,
            name_uz=name_uz
        )
        return category
    else:
        return None


def create_subcategory_if_not_exists(slug, name_en, name_ru, name_uz):
    if not SubCategories.objects.filter(slug=slug).exists():
        subcategory = SubCategories.objects.create(
            slug=slug,
            name_en=name_en,
            name_ru=name_ru,
            name_uz=name_uz
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


from films.models import Tag, TagCategory, TagSubcategory


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
        {"slug": "C1", "name_en": "C1", "name_ru": "C1", "name_uz": "C1"},
        {"slug": "C2", "name_en": "C2", "name_ru": "C2", "name_uz": "C2"},
        {"slug": "C3", "name_en": "C3", "name_ru": "C3", "name_uz": "C3"},
        {"slug": "C4", "name_en": "C4", "name_ru": "C4", "name_uz": "C4"},
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
        {"slug": "textile", "name_en": "Textile", "name_ru": "Текстиль", "name_uz": "Tekstil"},
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
