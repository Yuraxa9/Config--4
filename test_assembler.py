import tempfile
import os
from assembler import assembler, serializer, log_operation

# Тестирование функции assembler для загрузки константы
def test_load():
    # Тест (A=69, B=489, C=2)
    bytes = assembler([("load", 489, 2)])
    assert bytes == [0xC5, 0xF4, 0x00, 0x00, 0x00, 0x01], "Test failed for load"

# Тестирование функции assembler для чтения значения из памяти
def test_read():
    # Тест (A=49, B=15, C=960)
    bytes = assembler([("read", 15, 960)])
    assert bytes == [0xB1, 0x07, 0x1E, 0x00, 0x00, 0x00], "Test failed for read"

# Тестирование функции assembler для записи значения в память
def test_write():
    # Тест (A=107, B=6, C=11)
    bytes = assembler([("write", 6, 11)])
    assert bytes == [0x6B, 0x5B, 0x00, 0x00, 0x00, 0x00], "Test failed for write"

# Тестирование функции assembler для унарной операции abs()
def test_abs():
    # Тест (A=100, B=13, C=4)
    bytes = assembler([("abs", 13, 4)])
    assert bytes == [0xE4, 0x26, 0x00, 0x00, 0x00, 0x00], "Test failed for abs"

# Тестирование функции serializer для команды загрузки константы
def test_serializer_load():
    # Пример для команды load (69) с полями B=489, C=2
    cmd = 69
    fields = ((489, 7), (2, 39))
    size = 6
    bytes = serializer(cmd, fields, size)
    assert bytes == b'\xC5\xF4\x00\x00\x00\x01', "Test failed for serializer load"

# Тестирование функции serializer для команды чтения значения
def test_serializer_read():
    # Пример для команды read (49) с полями B=15, C=960
    cmd = 49
    fields = ((15, 7), (960, 11))
    size = 6
    bytes = serializer(cmd, fields, size)
    assert bytes == b'\xB1\x07\x1E\x00\x00\x00', "Test failed for serializer read"

# Тестирование функции serializer для команды записи значения
def test_serializer_write():
    # Пример для команды write (107) с полями B=6, C=11
    cmd = 107
    fields = ((6, 7), (11, 11))
    size = 6
    bytes = serializer(cmd, fields, size)
    assert bytes == b'\x6B\x5B\x00\x00\x00\x00', "Test failed for serializer write"

# Тестирование функции serializer для унарной операции abs()
def test_serializer_abs():
    # Пример для команды abs (100) с полями B=13, C=4
    cmd = 100
    fields = ((13, 7), (4, 11))
    size = 6
    bytes = serializer(cmd, fields, size)
    assert bytes == b'\xE4\x26\x00\x00\x00\x00', "Test failed for serializer abs"

# Тестирование логирования операций
def test_log_operation():
    # Создаем временный файл для проверки
    with tempfile.NamedTemporaryFile(delete=False) as log_file:
        log_file_path = log_file.name  # Получаем путь к файлу
        log_operation(log_file_path, 69, 489, 2)

    # Проверка содержимого файла
    with open(log_file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        assert lines[-1] == "A=69,B=489,C=2\n", "Test failed for log operation"

    # Удаляем временный файл
    os.remove(log_file_path)

# Тестирование комбинации инструкций
def test_multiple_instructions():
    instructions = [
        ("load", 489, 2),  # (A=69, B=489, C=2)
        ("write", 6, 11),  # (A=107, B=6, C=11)
        ("read", 15, 960), # (A=49, B=15, C=960)
        ("abs", 13, 4)     # (A=100, B=13, C=4)
    ]
    bytes = assembler(instructions)
    expected_bytes = [
        0xC5, 0xF4, 0x00, 0x00, 0x00, 0x01,  # load 489 2
        0x6B, 0x5B, 0x00, 0x00, 0x00, 0x00,  # write 6 11
        0xB1, 0x07, 0x1E, 0x00, 0x00, 0x00,  # read 15 960
        0xE4, 0x26, 0x00, 0x00, 0x00, 0x00   # abs 13 4
    ]
    assert bytes == expected_bytes, "Test failed for multiple instructions"

def run_tests():
    tests = [
        test_load,
        test_read,
        test_write,
        test_abs,
        test_serializer_load,
        test_serializer_read,
        test_serializer_write,
        test_serializer_abs,
        test_log_operation,
        test_multiple_instructions
    ]
    
    passed = 0
    for test in tests:
        try:
            test()
            print(f"{test.__name__} PASSED")
            passed += 1
        except AssertionError as e:
            print(f"{test.__name__} FAILED: {e}")

    print(f"\nTotal tests passed: {passed}/{len(tests)}")

if __name__ == "__main__":
    run_tests()
