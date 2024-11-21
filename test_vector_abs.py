import os
from assembler import assemble
from interpreter import interpret

def process_csv(input_csv, output_csv):
    """Обрабатывает CSV файл, преобразуя отрицательные значения."""
    with open(input_csv, 'r') as infile, open(output_csv, 'w') as outfile:
        lines = infile.readlines()
        outfile.write(lines[0])  # Копируем заголовок
        for line in lines[1:]:
            parts = line.strip().split(',')
            if len(parts) < 4:
                print(f"Error: Malformed line in {input_csv}: {line.strip()}")
                continue
            if parts[0] == "LOAD_CONST" and int(parts[2]) < 0:
                parts[2] = str((1 << 32) + int(parts[2]))  # Преобразование в 2-комплементарный вид
            outfile.write(','.join(parts) + '\n')

def test_vector_abs():
    """Основная тестовая программа."""
    # Пути к файлам
    input_csv = "vector_abs.csv"       # Предполагается, что этот файл уже существует
    processed_csv = "processed_vector_abs.csv"
    binary_file = "vector_abs.bin"    # Бинарный файл, который будет сгенерирован
    log_file = "vector_abs.log.csv"   # Лог-файл после сборки
    result_file = "result_abs.csv"        # Файл с результатами выполнения
    
    # Проверяем существование файла vector_abs.csv
    if not os.path.exists(input_csv):
        print(f"Error: Input file {input_csv} does not exist.")
        return

    # Преобразование отрицательных значений в input_csv
    print(f"Processing negative values in {input_csv}...")
    process_csv(input_csv, processed_csv)

    # Сборка программы в бинарный файл
    print(f"Assembling program from {processed_csv}...")
    assemble(processed_csv, binary_file, log_file)
    print(f"Binary file created: {binary_file}")
    
    # Выполнение программы
    print(f"Running program {binary_file}...")
    interpret(binary_file, result_file, (0, 7))
    
    # Проверка результата
    if os.path.exists(result_file):
        print(f"Contents of {result_file}:")
        with open(result_file, 'r') as f:
            print(f.read())
    else:
        print(f"Error: Result file {result_file} was not created.")
    
    # Удаление временных файлов (если необходимо)
    cleanup = input("Do you want to delete temporary files? (y/n): ").strip().lower()
    if cleanup == 'y':
        for file in [binary_file, log_file, result_file, processed_csv]:
            if os.path.exists(file):
                os.remove(file)
        print("Temporary files deleted.")
    else:
        print("Temporary files retained.")

if __name__ == "__main__":
    test_vector_abs()
