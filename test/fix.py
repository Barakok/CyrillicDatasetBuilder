input_filename = "labels.txt"  # Имя входного файла
output_filename = "labels-fix.txt"  # Имя выходного файла

with open(input_filename, "r", encoding="utf-8") as infile, open(
    output_filename, "w", encoding="utf-8"
) as outfile:
    for line in infile:
        # Разбиваем строку на слова по пробелам (любой длины)
        words = line.strip().split()
        # Объединяем слова через табуляцию
        new_line = "\t".join(words)
        outfile.write(new_line + "\n")
