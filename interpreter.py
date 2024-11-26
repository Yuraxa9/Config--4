import argparse
import csv

def abs_operation(value):
    """Выполнение операции abs на числе."""
    return abs(value)

# Интерпретатор
def interpreter(binary_path, result_path, memory_range):
    memory = [0] * 128  # 128 ячеек памяти (или больше, если необходимо)
    registers = [0] * 32  # 32 регистра

    with open(binary_path, "rb") as binary_file:
        byte_code = binary_file.read()

    # Декодирование и исполнение команд
    i = 0
    while i < len(byte_code):
        # Декодируем команду
        command = byte_code[i] & 0x7F  # Биты 0-6 для команды
        B = (byte_code[i+1] >> 3) & 0x1F  # Биты 3-7 для B
        C = ((byte_code[i+1] & 0x07) << 2) | ((byte_code[i+2] >> 6) & 0x03)  # Биты 0-5 для C
        
        if command == 69:  # load (Загрузка константы)
            registers[C] = B
        elif command == 49:  # read (Чтение из памяти)
            registers[B] = memory[registers[C]]
        elif command == 107:  # write (Запись в память)
            memory[B] = registers[C]
        elif command == 100:  # abs (Операция abs)
            registers[B] = abs_operation(memory[registers[C]])
        
        i += 6  # Каждая команда занимает 6 байт

    # Запись результата в CSV
    with open(result_path, "w", newline='', encoding="utf-8") as result_file:
        csv_writer = csv.writer(result_file)
        csv_writer.writerow(["Address", "Value"])
        # Добавим проверку, чтобы избежать выхода за пределы памяти
        for address in range(memory_range[0], memory_range[1] + 1):
            if address < len(memory):
                csv_writer.writerow([address, memory[address]])
            else:
                # Если память не инициализирована, записываем 0
                csv_writer.writerow([address, 0])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Interpreter for UVM (execute commands from binary file).")
    parser.add_argument("binary_path", help="Path to the binary file (bin)")
    parser.add_argument("result_path", help="Path to the result file (csv)")
    parser.add_argument("first_index", help="The first index of the displayed memory")
    parser.add_argument("last_index", help="The last index of the displayed memory")
    args = parser.parse_args()

    interpreter(args.binary_path, args.result_path, (int(args.first_index), int(args.last_index)))
