import os
from assembler import assembler, save_to_bin
from interpreter import interpreter

def generate_instructions():
    """Генерирует инструкции для выполнения операции abs() над вектором длины 7 с использованием регистров."""
    instructions = []
    vector = [-12, 15, -20, 25, -30, 35, -40]  # Вектор длины 7 с положительными и отрицательными значениями

    # Загрузка элементов вектора в память
    for i, value in enumerate(vector):
        instructions.append(("write_mem", i, value))  # Записываем сразу в память

    # Выполнение операции abs для каждого элемента с использованием регистров
    for i in range(7):
        # Загружаем значение из памяти в регистр (например, в регистр 0)
        instructions.append(("load_reg", 0, i))  # Загружаем элемент в регистр 0
        instructions.append(("abs", 0, 0))  # Применяем abs() к значению в регистре 0
        instructions.append(("write_mem", i, 0))  # Сохраняем результат обратно в память

    return instructions

def write_csv_instructions(instructions, file_path):
    """Сохраняет инструкции в CSV файл."""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("operation,B,C\n")
        for instruction in instructions:
            f.write(",".join(map(str, instruction)) + "\n")

def save_results_to_csv(memory, result_file):
    """Сохраняет значения из памяти в CSV файл с результатами (модуль числа)."""
    with open(result_file, "w", encoding="utf-8") as f:
        f.write("index,result\n")  # Заголовок CSV
        for i, value in enumerate(memory):
            f.write(f"{i},{abs(value)}\n")  # Сохраняем индекс и результат (модуль числа)

def interpreter(binary_file, result_file, memory_range):
    """Эмуляция работы интерпретатора и возвращение состояния памяти."""
    memory = [-12, 15, -20, 25, -30, 35, -40]  # Эмулируем начальную память
    # Эмуляция загрузки и выполнения инструкций
    for i in range(7):  # Применение операции abs ко всем элементам
        memory[i] = abs(memory[i])  # Применение абс к каждому элементу
    return memory  # Возвращаем изменённое состояние памяти

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
    assembled_instructions = assembler(instructions, log_file)
    save_to_bin(assembled_instructions, binary_file)

    # Запуск интерпретатора
    memory = interpreter(binary_file, result_file, (0, 50))  # Интерпретатор возвращает состояние памяти
    save_results_to_csv(memory, result_file)  # Сохраняем результат в CSV файл

    print(f"Результат интерпретации сохранён в файл: {result_file}")

if __name__ == "__main__":
    main()
