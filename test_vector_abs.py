import os
from assembler import assembler, save_to_bin
from interpreter import interpreter

def generate_instructions():
    """Генерирует инструкции для выполнения операции abs() над вектором длины 7."""
    instructions = []
    vector = [-12, 15, -20, 25, -30, 35, -40]  # Вектор длины 7 с положительными и отрицательными значениями

    # Загрузка элементов вектора в память
    for i, value in enumerate(vector):
        instructions.append(("write_mem", i, value))  # Записываем сразу в память (без загрузки в регистры)

    # Выполнение операции abs для каждого элемента вектора
    for i in range(7):
        instructions.append(("abs", i, i))  # Применяем abs() к каждому элементу и сохраняем в том же месте

    return instructions

def write_csv_instructions(instructions, file_path):
    """Сохраняет инструкции в CSV файл."""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("operation,B,C\n")
        for instruction in instructions:
            print(f"Writing instruction: {instruction}")  # Добавим вывод инструкций
            f.write(",".join(map(str, instruction)) + "\n")

def main():
    # Параметры файлов
    instructions_file = "test_instructions.csv"
    binary_file = "test_binary.bin"
    result_file = "test_result.csv"  # Файл для записи результата
    log_file = "test_log.csv"

    # Генерация инструкций
    instructions = generate_instructions()
    write_csv_instructions(instructions, instructions_file)

    # Запуск ассемблера
    print("Сборка программы...")
    assembled_instructions = assembler(instructions, log_file)
    save_to_bin(assembled_instructions, binary_file)
    print(f"Программа собрана, бинарный файл: {binary_file}")

    # Запуск интерпретатора
    print("Запуск интерпретатора...")
    interpreter(binary_file, result_file, (0, 50))  # Убедимся, что обрабатываем всю память
    print(f"Результат интерпретации сохранён в файл: {result_file}")

if __name__ == "__main__":
    main()
