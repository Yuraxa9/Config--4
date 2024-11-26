import argparse
import csv

def log_operation(log_path, operation_code, *args):
    """Запись операции в лог файл."""
    if log_path is not None:
        with open(log_path, "a", encoding="utf-8") as log_file:
            log_file.write(f"A={operation_code},B={args[0]},C={args[1]}\n")

def serializer(cmd, fields, size):
    """Преобразование команды в бинарный формат."""
    bits = 0
    bits |= cmd
    for value, offset in fields:
        bits |= (value << offset)
    return bits.to_bytes(size, "little")

def assembler(instructions, log_path=None):
    """Перевод инструкций в бинарный формат."""
    byte_code = []
    for instruction in instructions:
        operation = instruction[0]
        args = instruction[1:]

        if operation == "load":
            B, C = args
            byte_code += serializer(69, [(B, 7), (C, 39)], 6)
            log_operation(log_path, 69, B, C)

        elif operation == "read":
            B, C = args
            byte_code += serializer(49, [(B, 7), (C, 11)], 6)
            log_operation(log_path, 49, B, C)

        elif operation == "write":
            B, C = args
            byte_code += serializer(107, [(B, 7), (C, 11)], 6)
            log_operation(log_path, 107, B, C)

        elif operation == "abs":
            B, C = args
            byte_code += serializer(100, [(B, 7), (C, 11)], 6)
            log_operation(log_path, 100, B, C)

    return byte_code

def assemble(instructions_path: str, log_path=None):
    """Чтение инструкций из CSV файла и их ассемблирование."""
    instructions = []
    with open(instructions_path, newline='', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Пропуск заголовка
        for row in reader:
            operation = row[0].strip()
            B = int(row[1].strip())
            C = int(row[2].strip())
            instructions.append([operation, B, C])
    return assembler(instructions, log_path)

def save_to_bin(assembled_instructions, binary_path):
    """Сохранение ассемблированных инструкций в бинарный файл."""
    with open(binary_path, "wb") as binary_file:
        binary_file.write(bytes(assembled_instructions))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Assemble instructions to bytecode.")
    parser.add_argument("instructions_path", help="Path to the instructions CSV file")
    parser.add_argument("binary_path", help="Path to the binary file (bin)")
    parser.add_argument("log_path", help="Path to the log file (csv)")
    args = parser.parse_args()

    # Запись заголовка в лог файл
    with open(args.log_path, "w", encoding="utf-8") as log_file:
        log_file.write("Operation code,B,Address\n")

    # Ассемблирование
    result = assemble(args.instructions_path, args.log_path)
    save_to_bin(result, args.binary_path)
