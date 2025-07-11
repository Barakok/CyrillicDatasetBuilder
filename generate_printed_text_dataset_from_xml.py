import xml.etree.ElementTree as ET

# Путь к входному XML-файлу
input_file = "dict.opcorpora.xml"
# Путь к выходному текстовому файлу
output_file = "printed_words.txt"

# Разбор XML-файла
tree = ET.parse(input_file)
root = tree.getroot()

# Соберем все слова
words = set()

# Найдём все леммы
for lemma in root.find("lemmata").findall("lemma"):
    # Добавим основную лемму
    l_elem = lemma.find("l")
    if l_elem is not None and "t" in l_elem.attrib:
        words.add(l_elem.attrib["t"])

    # Добавим все словоформы
    for f_elem in lemma.findall("f"):
        if "t" in f_elem.attrib:
            words.add(f_elem.attrib["t"])

# Запишем в текстовый файл
with open(output_file, "w", encoding="utf-8") as f:
    for word in sorted(words):
        f.write(word + "\n")

print(f"Извлечено {len(words)} слов. Сохранено в {output_file}.")
