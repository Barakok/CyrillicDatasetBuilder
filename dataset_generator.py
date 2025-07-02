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
            "cyrillic Cancellaresca Script LET.ttf",
            "cyrillic_Kobzar KS.ttf",
            "cyrillic_Larisa script.ttf",
            "cyrillic_Script Thin Pen.ttf",
            "cyrillic_propisi.ttf",
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
        self.train_folder = "second_data_plast/train/images"
        self.test_folder = "second_data_plast/test/images"
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

    def save_combinations_with_initials(self, combinations, folder, iterator):
        for font, color, word, n, s in combinations:
            image_path, text = self.image_creator_instance.create_image(
                f"{word.capitalize()} {n}. {s}.",
                color,
                font,
                iterator,
                folder,
            )
            self.save_label(folder, image_path, text)
            iterator = iterator + 1

        return iterator

    def save_combinations_with_initial(self, combinations, folder, iterator):
        for font, color, word, n in combinations:
            image_path, text = self.image_creator_instance.create_image(
                f"{word.capitalize()} {n}.",
                color,
                font,
                iterator,
                folder,
            )
            self.save_label(folder, image_path, text)
            iterator = iterator + 1

        return iterator

    def save_combinations_with_date(self, combinations, folder, iterator):
        for d, m, y, fmt, font, color in combinations:
            # Валидация даты
            dt = datetime.strptime(f"{d}.{m}.{y}", "%d.%m.%Y")
            m_int = int(m)
            formatted = fmt.format(d=d, m=m, y=y, m_name=self.russian_months[m_int - 1])
            image_path, text = self.image_creator_instance.create_image(
                formatted,
                color,
                font,
                iterator,
                folder,
            )
            self.save_label(folder, image_path, text)
            iterator = iterator + 1

        return iterator

    def save_combinations_with_pass_number(self, combinations, folder, iterator):
        for p, font, color in combinations:
            # Валидация даты
            image_path, text = self.image_creator_instance.create_image(
                p,
                color,
                font,
                iterator,
                folder,
            )
            self.save_label(folder, image_path, text)
            iterator = iterator + 1

        return iterator

    def save_combinations_with_pass_number(self, combinations, folder, iterator):
        for number, font, color in combinations:
            # Валидация даты
            image_path, text = self.image_creator_instance.create_image(
                number,
                color,
                font,
                iterator,
                folder,
            )
            self.save_label(folder, image_path, text)
            iterator = iterator + 1

        return iterator

    def generate(self):

        train_iterator = 0
        test_iterator = 0

        # new_train_iterator, new_test_iterator = self.generate_fio_alt(
        #     train_iterator, test_iterator
        # )

        # new_1_train_iterator, new_1_test_iterator = (
        #     self.generate_lastName_with_initials(new_train_iterator, new_test_iterator)
        # )

        # new_2_train_iterator, new_2_test_iterator = self.generate_lastName_with_initial(
        #     new_1_train_iterator, new_1_test_iterator
        # )

        # new_3_train_iterator, new_3_test_iterator = self.generate_dates(
        #     train_iterator, test_iterator
        # )

        # new_3_train_iterator, new_3_test_iterator = self.generate_passport_numbers(
        #     train_iterator, test_iterator
        # )

        # new_3_train_iterator, new_3_test_iterator = self.generate_doc_numbers(
        #     train_iterator, test_iterator
        # )

        new_3_train_iterator, new_3_test_iterator = self.generate_address(
            train_iterator, test_iterator
        )

        # print("new_train_iterator", new_train_iterator)
        # print("new_1_train_iterator", new_1_train_iterator)
        # print("new_2_train_iterator", new_2_train_iterator)
        print("new_3_train_iterator", new_3_train_iterator)

    def generate_address(self, train_iterator, test_iterator):
        pass

    def generate_doc_numbers(self, train_iterator, test_iterator):
        random.seed(42)
        formats = [
            lambda: f"ДОГ-{random.randint(2000, 2025)}/{random.randint(1, 99999):05}",
            lambda: f"№ {random.randint(1, 99)}-{random.randint(1, 12):02}/{random.randint(100, 999)}",
            lambda: f"ДОК№{random.randint(1, 999):03}-ИП/{random.randint(2000, 2025)}",
            lambda: f"ПР-{random.randint(100, 999)}-{random.randint(10, 99)}",
            lambda: f"{random.randint(1,999):03}/АБ-{random.randint(2000,2025)}",
        ]

        train_n_samples = 20000
        split_index = int(train_n_samples * 0.8)

        codes = []
        for _ in range(train_n_samples):
            fmt = random.choice(formats)
            codes.append(fmt())

            # Все возможные комбинации: серия + номер
        combinations = list(
            product(
                codes,
                range(len(self.fonts_combinations)),
                self.pen_colors,
            )
        )
        random.shuffle(combinations)
        # Обрезаем до нужного количества
        combinations = combinations[:train_n_samples]

        train_combinations = combinations[:split_index]
        test_combinations = combinations[split_index:]

        train_iterator = self.save_combinations_with_pass_number(
            train_combinations, self.train_folder, train_iterator
        )

        test_iterator = self.save_combinations_with_pass_number(
            test_combinations, self.test_folder, test_iterator
        )

        return train_iterator, test_iterator

    def generate_passport_numbers(self, train_iterator, test_iterator):
        train_n_samples = 20000

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
                passport_list,
                range(len(self.fonts_combinations)),
                self.pen_colors,
            )
        )
        random.shuffle(combinations)
        # Обрезаем до нужного количества
        combinations = combinations[:train_n_samples]

        train_combinations = combinations[:split_index]
        test_combinations = combinations[split_index:]

        train_iterator = self.save_combinations_with_pass_number(
            train_combinations, self.train_folder, train_iterator
        )

        test_iterator = self.save_combinations_with_pass_number(
            test_combinations, self.test_folder, test_iterator
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

        train_n_samples = 30000

        split_index = int(train_n_samples * 0.8)

        combinations = list(
            product(
                days,
                months,
                years,
                formats,
                range(len(self.fonts_combinations)),
                self.pen_colors,
            )
        )

        random.shuffle(combinations)
        combinations = combinations[:train_n_samples]

        train_combinations = combinations[:split_index]
        test_combinations = combinations[split_index:]

        train_iterator = self.save_combinations_with_date(
            train_combinations, self.train_folder, train_iterator
        )

        test_iterator = self.save_combinations_with_date(
            test_combinations, self.test_folder, test_iterator
        )

        return train_iterator, test_iterator

    def generate_lastName_with_initial(self, train_iterator, test_iterator):
        config = {"file_path": "./textData/lastName.txt"}
        train_data, test_data = data_provider("file", config)

        train_data_word_cases = []
        test_data_word_cases = []
        train_n_samples = 8000
        test_n_samples = 2000

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

        train_iterator = self.save_combinations_with_initial(
            combinations, self.train_folder, train_iterator
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

        test_iterator = self.save_combinations_with_initial(
            combinations, self.test_folder, test_iterator
        )

        return train_iterator, test_iterator

    def generate_lastName_with_initials(self, train_iterator, test_iterator):
        config = {"file_path": "./textData/lastName.txt"}
        train_data, test_data = data_provider("file", config)
        train_data_word_cases = []
        test_data_word_cases = []
        train_n_samples = 16000
        test_n_samples = 4000

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

        train_iterator = self.save_combinations_with_initials(
            combinations, self.train_folder, train_iterator
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

        test_iterator = self.save_combinations_with_initials(
            combinations, self.test_folder, test_iterator
        )

        return train_iterator, test_iterator

    def generate_fio_alt(self, train_iterator, test_iterator):
        train_data, test_data = data_provider("files", self.config)
        n_samples = 100000
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
        combinations = combinations[:n_samples]

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
        combinations = combinations[:n_samples]

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
