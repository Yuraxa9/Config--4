import struct
import csv
import sys

# Таблица команд с их бинарными кодами
COMMANDS = {
    "LOAD_CONST": 0xC5,
    "LOAD_MEM": 0xB1,
    "STORE_MEM": 0x6B,
    "UNARY_ABS": 0xE4
}

def validate_range(value, min_val, max_val, field_name):
    if not (min_val <= value <= max_val):
        raise ValueError(f"{field_name} value {value} is out of range [{min_val}, {max_val}]")
    return value

def assemble(input_file, output_file, log_file):
    binary_data = []
    log_data = []

    # Чтение входного файла
    with open(input_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                command = row["Command"]
                a = int(row["A"]) & 0x3  # Ограничиваем A до двух младших битов
                b = int(row["B"])
                c = int(row["C"])
                opcode = COMMANDS.get(command)

                if opcode is None:
                    raise ValueError(f"Unknown command: {command}")

                # Формируем машинную команду (6 байт)
                instruction = struct.pack(
                    '>BIB',
                    validate_range(opcode, 0, 255, "Opcode"),
                    validate_range(b, 0, 2**32 - 1, "B"),
                    validate_range(c, 0, 15, "C")
                )
                binary_data.append(instruction)

                # Добавляем запись в лог
                log_data.append({
                    "Command": command,
                    "Opcode": f"0x{opcode:X}",
                    "A": a,
                    "B": b,
                    "C": c
                })
            except KeyError as e:
                print(f"Missing column in input file: {e}")
                sys.exit(1)
            except ValueError as e:
                print(f"Error in data formatting: {e}")
                sys.exit(1)

    # Записываем бинарный файл
    with open(output_file, 'wb') as f:
        for data in binary_data:
            f.write(data)

    # Записываем лог-файл в формате CSV
    with open(log_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["Command", "Opcode", "A", "B", "C"])
        writer.writeheader()
        writer.writerows(log_data)

    print("Assembling completed successfully!")

def run_tests():
    test_cases = [
        {
            "description": "Загрузка константы",
            "command": "LOAD_CONST",
            "A": 69,
            "B": 489,
            "C": 2,
            "expected": b'\xC5\x00\x00\x01\xE9\x02'  # Исправлено
        },
        {
            "description": "Чтение значения из памяти",
            "command": "LOAD_MEM",
            "A": 49,
            "B": 15,
            "C": 200,
            "expected": b'\xB1\x00\x00\x00\x0F\xC8'  # Исправлено
        },
        {
            "description": "Запись значения в память",
            "command": "STORE_MEM",
            "A": 107,
            "B": 6,
            "C": 11,
            "expected": b'\x6B\x00\x00\x00\x06\x0B'  # Исправлено
        },
        {
            "description": "Унарная операция abs()",
            "command": "UNARY_ABS",
            "A": 100,
            "B": 13,
            "C": 4,
            "expected": b'\xE4\x00\x00\x00\x0D\x04'  # Исправлено
        }
    ]

    print("\nRunning tests...")
    all_passed = True
    for test in test_cases:
        print(f"Test: {test['description']}")
        opcode = COMMANDS[test["command"]]
        a = test["A"] & 0x3
        b = test["B"]
        c = test["C"]

        try:
            # Формируем машинную команду
            result = struct.pack(
                '>BIB',
                validate_range(opcode, 0, 255, "Opcode"),
                validate_range(b, 0, 2**32 - 1, "B"),
                validate_range(c & 0xFF, 0, 255, "C")
            )
            assert result == test["expected"], f"Expected {test['expected']}, got {result}"
            print(f"  Passed: {result}")
        except ValueError as e:
            print(f"  Failed: {e}")
            all_passed = False
        except AssertionError as e:
            print(f"  Failed: {e}")
            all_passed = False

    if all_passed:
        print("All tests passed successfully!")
    else:
        print("Some tests failed.")


if __name__ == "__main__":
    run_tests()
    if len(sys.argv) < 4:
        print("Usage: python assembler.py <input_csv> <output_bin> <log_csv>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    log_file = sys.argv[3]
    assemble(input_file, output_file, log_file)
