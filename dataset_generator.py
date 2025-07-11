from image_creator import image_creator
from data_provider import data_provider
from utils.morphy_generator import WordMorphy
import random
from itertools import product
from datetime import datetime


class DatasetGenerator:
    def __init__(self):
        self.background_color = (255, 255, 255)  # белый
        self.blue_color = (0, 0, 255)  # синий
        self.red_color = (255, 0, 0)  # красный
        self.green_color = (0, 255, 0)  # зеленый
        self.pen_colors = [self.blue_color, self.red_color, self.green_color]
        self.font_size_array = [18, 22, 26, 30]
        self.margin = 3
        self.fonts = [
            # "cyrillic Cancellaresca Script LET.ttf",
            # "cyrillic_Kobzar KS.ttf",
            # "cyrillic_Larisa script.ttf",
            # "cyrillic_Script Thin Pen.ttf",
            # "cyrillic_propisi.ttf",
            "ofont.ru_Spell.ttf"
        ]
        self.config = {
            "file_path": "text.txt",
            "fields": [
                "firstName",
                "lastName",
                "surname",
            ],
        }
        self.russian_upper_alphabet = [
            "А",
            "Б",
            "В",
            "Г",
            "Д",
            "Е",
            "Ё",
            "Ж",
            "З",
            "И",
            "Й",
            "К",
            "Л",
            "М",
            "Н",
            "О",
            "П",
            "Р",
            "С",
            "Т",
            "У",
            "Ф",
            "Х",
            "Ц",
            "Ч",
            "Ш",
            "Щ",
            "Э",
            "Ю",
            "Я",
        ]
        self.russian_months = [
            "января",
            "февраля",
            "марта",
            "апреля",
            "мая",
            "июня",
            "июля",
            "августа",
            "сентября",
            "октября",
            "ноября",
            "декабря",
        ]
        self.train_folder = "3_data_plast/train/images"
        self.test_folder = "3_data_plast/test/images"
        self.word_morphy = WordMorphy()
        self.fonts_combinations = {}
        self.fonts_generate()
        self.image_creator_instance = image_creator(
            self.background_color,
            self.margin,
        )
        self.image_creator_instance.set_fonts(self.fonts_combinations)

    def fonts_generate(self):
        font_index = 0
        for font in self.fonts:
            for size in self.font_size_array:
                self.fonts_combinations[font_index] = {"font": font, "size": size}
                font_index = font_index + 1

    def save_label(self, folder, image_path, text):
        with open(f"{folder}/labels.txt", "a", encoding="utf-8") as file:
            file.write(f"{image_path}\t{text}" + "\n")

    def getPattern(self, mode, combination):
        pattern = ""

        if mode == "initials":
            word, n, s = combination
            pattern = f"{word.capitalize()} {n}. {s}."

        if mode == "initial":
            word, n = combination
            pattern = f"{word.capitalize()} {n}."

        if mode == "date":
            d, m, y, fmt = combination
            m_int = int(m)
            pattern = fmt.format(d=d, m=m, y=y, m_name=self.russian_months[m_int - 1])

        if mode == "default":
            pattern = combination[0]

        return pattern

    def save_combinations(self, combinations, folder, iterator, mode):
        for font, color, *combination in combinations:
            pattern = self.getPattern(mode, combination)
            image_path, text = self.image_creator_instance.create_image(
                pattern,
                color,
                font,
                iterator,
                folder,
            )
            self.save_label(folder, image_path, text)
            iterator = iterator + 1

        return iterator

    def generate(self):
        train_iterator, test_iterator = 0, 0

        steps = [
            self.generate_fio_alt,
            self.generate_lastName_with_initials,
            self.generate_lastName_with_initial,
            self.generate_dates,
            self.generate_passport_numbers,
            self.generate_doc_numbers,
            self.generate_address,
            self.generate_random_words,
        ]

        for step in steps:
            train_iterator, test_iterator = step(train_iterator, test_iterator)

    def generate_random_words(self, train_iterator, test_iterator):
        neutral_vocab = [
            # Частотные слова
            "заявка",
            "документ",
            "данные",
            "код",
            "форма",
            "система",
            "режим",
            "запись",
            "отчет",
            "таблица",
            "пункт",
            "вход",
            "пользователь",
            "сервер",
            "папка",
            "поиск",
            "архив",
            "шаблон",
            # Термины
            "печать",
            "отдел",
            "номер",
            "файл",
            "логин",
            "сертификат",
            "лицензия",
            "сайт",
            "отчетность",
            # Аббревиатуры
            "ФНС",
            "ФССП",
            "РЖД",
            "ГИС",
            "ФМС",
            "ОГРН",
            "ИНН",
            "КПП",
            "ПФР",
            "СНИЛС",
            "ТК",
            "ТЦ",
            "ФОИВ",
            # Бессмысленные строки
            "abc123",
            "qwe_rty",
            "zzz999",
            "text_001",
            "xxx777",
            "test_mode",
            "doc_x9",
            # Геометрические и ИТ-слова
            "строка",
            "заголовок",
            "сетка",
            "рамка",
            "цвет",
            "размер",
            "иконка",
            "ссылка",
        ]

        # 1-сложные и 2-сложные комбинации
        one_word = neutral_vocab
        two_word = [" ".join(pair) for pair in product(neutral_vocab, repeat=2)]
        three_word = [" ".join(triple) for triple in product(neutral_vocab, repeat=3)]

        # Объединяем
        all_combinations = one_word + two_word + three_word

        # Удалим дубликаты и shuffle
        unique_combinations = list(set(all_combinations))

        unique_combinations_len = len(unique_combinations)
        split_index = int(unique_combinations_len * 0.8)

        combinations = list(
            product(
                range(len(self.fonts_combinations)),
                self.pen_colors,
                unique_combinations[:split_index],
            )
        )

        random.shuffle(combinations)

        n = 10000
        train_n_samples = int(n * 0.8)

        train_samples = train_n_samples
        test_samples = n - train_n_samples

        if len(combinations) < train_samples:
            train_samples = len(combinations)

        # Ограничим количество (например, 30k)
        combinations = combinations[:train_samples]

        train_iterator = self.save_combinations(
            combinations, self.train_folder, train_iterator, "default"
        )

        combinations = list(
            product(
                range(len(self.fonts_combinations)),
                self.pen_colors,
                unique_combinations[split_index:],
            )
        )

        random.shuffle(combinations)

        if len(combinations) < test_samples:
            test_samples = len(combinations)

        # Ограничим количество (например, 30k)
        combinations = combinations[:test_samples]

        test_iterator = self.save_combinations(
            combinations, self.test_folder, test_iterator, "default"
        )

        return train_iterator, test_iterator

    def generate_address(self, train_iterator, test_iterator):
        config = {"file_path": "./textData/unique_addresses_30k.csv"}
        train_data, test_data = data_provider("csv", config)

        n = 10000
        train_n_samples = int(n * 0.8)
        test_n_samples = n - train_n_samples

        combinations = list(
            product(
                range(len(self.fonts_combinations)),
                self.pen_colors,
                train_data,
            )
        )

        random.shuffle(combinations)
        # Обрезаем до нужного количества
        combinations = combinations[:train_n_samples]

        train_iterator = self.save_combinations(
            combinations, self.train_folder, train_iterator, "default"
        )

        combinations = list(
            product(
                range(len(self.fonts_combinations)),
                self.pen_colors,
                test_data,
            )
        )

        random.shuffle(combinations)
        # Обрезаем до нужного количества
        combinations = combinations[:test_n_samples]

        test_iterator = self.save_combinations(
            combinations, self.test_folder, test_iterator, "default"
        )

        return train_iterator, test_iterator

    def generate_doc_numbers(self, train_iterator, test_iterator):
        random.seed(42)
        formats = [
            lambda: f"ДОГ-{random.randint(2000, 2025)}/{random.randint(1, 99999):05}",
            lambda: f"№ {random.randint(1, 99)}-{random.randint(1, 12):02}/{random.randint(100, 999)}",
            lambda: f"ДОК№{random.randint(1, 999):03}-ИП/{random.randint(2000, 2025)}",
            lambda: f"ПР-{random.randint(100, 999)}-{random.randint(10, 99)}",
            lambda: f"{random.randint(1,999):03}/АБ-{random.randint(2000,2025)}",
        ]

        train_n_samples = 10000
        split_index = int(train_n_samples * 0.8)

        codes = []
        for _ in range(train_n_samples):
            fmt = random.choice(formats)
            codes.append(fmt())

            # Все возможные комбинации: серия + номер
        combinations = list(
            product(
                range(len(self.fonts_combinations)),
                self.pen_colors,
                codes,
            )
        )
        random.shuffle(combinations)
        # Обрезаем до нужного количества
        combinations = combinations[:train_n_samples]

        train_combinations = combinations[:split_index]
        test_combinations = combinations[split_index:]

        train_iterator = self.save_combinations(
            train_combinations, self.train_folder, train_iterator, "default"
        )

        test_iterator = self.save_combinations(
            test_combinations, self.test_folder, test_iterator, "default"
        )

        return train_iterator, test_iterator

    def generate_passport_numbers(self, train_iterator, test_iterator):
        train_n_samples = 10000

        split_index = int(train_n_samples * 0.8)
        passport_list = []

        formats = [
            "{region_code}{department_code} {number}",
            "{region_code} {department_code} {number}",
            "{region_code}{department_code}-{number}",
        ]

        for _ in range(train_n_samples):
            region_code = random.randint(1, 99)
            department_code = random.randint(1, 99)
            r_code = f"{region_code:02}"
            d_code = f"{department_code:02}"
            number = f"{random.randint(0, 999999):06}"
            fmt = random.choice(formats)
            formatted = fmt.format(
                region_code=r_code, department_code=d_code, number=number
            )
            passport_list.append(formatted)

        # Все возможные комбинации: серия + номер
        combinations = list(
            product(
                range(len(self.fonts_combinations)),
                self.pen_colors,
                passport_list,
            )
        )

        random.shuffle(combinations)

        # Обрезаем до нужного количества
        combinations = combinations[:train_n_samples]

        train_combinations = combinations[:split_index]
        test_combinations = combinations[split_index:]

        random.shuffle(train_combinations)
        random.shuffle(test_combinations)

        train_iterator = self.save_combinations(
            train_combinations, self.train_folder, train_iterator, "default"
        )

        test_iterator = self.save_combinations(
            test_combinations, self.test_folder, test_iterator, "default"
        )

        return train_iterator, test_iterator

    def generate_dates(self, train_iterator, test_iterator):
        random.seed(42)

        days = [f"{d:02}" for d in range(1, 32)]
        months = [f"{m:02}" for m in range(1, 13)]
        years = [str(y) for y in range(1930, 2026)]

        formats = [
            "{d}.{m}.{y}",
            "{d}-{m}-{y}",
            "{d}/{m}/{y}",
            "{d} {m_name} {y} г.",
            "{y}-{m}-{d}",
        ]

        train_n_samples = 10000

        split_index = int(train_n_samples * 0.8)

        combinations = list(
            product(
                range(len(self.fonts_combinations)),
                self.pen_colors,
                days,
                months,
                years,
                formats,
            )
        )

        random.shuffle(combinations)
        combinations = combinations[:train_n_samples]

        train_combinations = combinations[:split_index]
        test_combinations = combinations[split_index:]

        train_iterator = self.save_combinations(
            train_combinations, self.train_folder, train_iterator, "date"
        )

        test_iterator = self.save_combinations(
            test_combinations, self.test_folder, test_iterator, "date"
        )

        return train_iterator, test_iterator

    def generate_lastName_with_initial(self, train_iterator, test_iterator):
        config = {"file_path": "./textData/lastName.txt"}
        train_data, test_data = data_provider("file", config)

        train_data_word_cases = []
        test_data_word_cases = []

        n = 10000
        train_n_samples = int(n * 0.8)
        test_n_samples = n - train_n_samples

        for word in train_data:
            # падеж
            word_cases = self.word_morphy.get_words_morphy(word)
            train_data_word_cases.extend(word_cases)

        combinations = list(
            product(
                range(len(self.fonts_combinations)),
                self.pen_colors,
                train_data_word_cases,
                self.russian_upper_alphabet,
            )
        )

        random.shuffle(combinations)
        combinations = combinations[:train_n_samples]

        train_iterator = self.save_combinations(
            combinations, self.train_folder, train_iterator, "initial"
        )

        for word in test_data:
            # падеж
            word_cases = self.word_morphy.get_words_morphy(word)
            test_data_word_cases.extend(word_cases)

        combinations = list(
            product(
                range(len(self.fonts_combinations)),
                self.pen_colors,
                test_data_word_cases,
                self.russian_upper_alphabet,
            )
        )

        random.shuffle(combinations)
        combinations = combinations[:test_n_samples]

        test_iterator = self.save_combinations(
            combinations, self.test_folder, test_iterator, "initial"
        )

        return train_iterator, test_iterator

    def generate_lastName_with_initials(self, train_iterator, test_iterator):
        config = {"file_path": "./textData/lastName.txt"}
        train_data, test_data = data_provider("file", config)
        train_data_word_cases = []
        test_data_word_cases = []

        n = 10000
        train_n_samples = int(n * 0.8)
        test_n_samples = n - train_n_samples

        for word in train_data:
            # падеж
            word_cases = self.word_morphy.get_words_morphy(word)
            train_data_word_cases.extend(word_cases)

        combinations = list(
            product(
                range(len(self.fonts_combinations)),
                self.pen_colors,
                train_data_word_cases,
                self.russian_upper_alphabet,
                self.russian_upper_alphabet,
            )
        )

        random.shuffle(combinations)
        combinations = combinations[:train_n_samples]

        train_iterator = self.save_combinations(
            combinations, self.train_folder, train_iterator, "initials"
        )

        for word in test_data:
            # падеж
            word_cases = self.word_morphy.get_words_morphy(word)
            test_data_word_cases.extend(word_cases)

        combinations = list(
            product(
                range(len(self.fonts_combinations)),
                self.pen_colors,
                test_data_word_cases,
                self.russian_upper_alphabet,
                self.russian_upper_alphabet,
            )
        )

        random.shuffle(combinations)
        combinations = combinations[:test_n_samples]

        test_iterator = self.save_combinations(
            combinations, self.test_folder, test_iterator, "initials"
        )

        return train_iterator, test_iterator

    def generate_fio_alt(self, train_iterator, test_iterator):
        train_data, test_data = data_provider("files", self.config)

        n = 30000
        train_n_samples = int(n * 0.8)
        test_n_samples = n - train_n_samples

        train_data_word_cases = []
        test_data_word_cases = []

        for word in train_data:
            # падеж
            word_cases = self.word_morphy.get_words_morphy(word)
            train_data_word_cases.extend(word_cases)

        combinations = list(
            product(
                range(len(self.fonts_combinations)),
                self.pen_colors,
                train_data_word_cases,
            )
        )

        random.shuffle(combinations)
        combinations = combinations[:train_n_samples]

        for font, color, word in combinations:
            image_path, text = self.image_creator_instance.create_image(
                word.capitalize(),
                color,
                font,
                train_iterator,
                self.train_folder,
            )
            self.save_label(self.train_folder, image_path, text)
            train_iterator = train_iterator + 1

        for word in test_data:
            # падеж
            word_cases = self.word_morphy.get_words_morphy(word)
            test_data_word_cases.extend(word_cases)

        combinations = list(
            product(
                range(len(self.fonts_combinations)),
                self.pen_colors,
                test_data_word_cases,
            )
        )
        random.shuffle(combinations)
        combinations = combinations[:test_n_samples]

        for font, color, word in combinations:
            image_path, text = self.image_creator_instance.create_image(
                word.capitalize(),
                color,
                font,
                test_iterator,
                self.test_folder,
            )
            self.save_label(self.test_folder, image_path, text)
            test_iterator = test_iterator + 1

        return train_iterator, test_iterator

    def generate_all_fio(self, train_iterator, test_iterator):
        # 1) размер

        train_data, test_data = data_provider("files", self.config)
        # 3) шрифт
        for font in self.fonts:
            # 5) Размер шрифта
            for font_size in self.font_size_array:
                self.image_creator_instance.load_font(font, font_size)
                # 4) цвет ручки
                for color in self.pen_colors:
                    # 5) часть фио
                    for word in train_data:
                        # 6) падеж
                        word_cases = self.word_morphy.get_words_morphy(word)
                        for word_case in word_cases:
                            print("word_case", word_case)
                            image_path, text = self.image_creator_instance.create_image(
                                word_case.capitalize(),
                                color,
                                train_iterator,
                                self.train_folder,
                            )
                            print("text", text)
                            self.save_label(self.train_folder, image_path, text)
                            train_iterator = train_iterator + 1
                    # 5) часть фио
                    for word in test_data:
                        # 6) падеж
                        word_cases = self.word_morphy.get_words_morphy(word)
                        for word_case in word_cases:
                            image_path, text = self.image_creator_instance.create_image(
                                word_case.capitalize(),
                                color,
                                test_iterator,
                                self.test_folder,
                            )

                            self.save_label(self.test_folder, image_path, text)
                            test_iterator = test_iterator + 1

        return train_iterator, test_iterator


dataset_generator = DatasetGenerator()
dataset_generator.generate()
