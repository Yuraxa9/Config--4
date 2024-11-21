import struct
import csv
import sys

# Таблица команд с их бинарными кодами
COMMANDS = {
    0xC5: "LOAD_CONST",
    0xB1: "LOAD_MEM",
    0x6B: "STORE_MEM",
    0xE4: "UNARY_ABS"
}

class VirtualMachine:
    def __init__(self, memory_size=1024):
        self.registers = [0] * 16  # 16 регистров
        self.memory = [0] * memory_size  # Память размером 1024 слова

    def load_const(self, b, c):
        """Загрузка константы в регистр"""
        if not (0 <= c < len(self.registers)):
            raise IndexError(f"Register index out of range: C={c}")
        print(f"Loading constant {b} into register {c}")
        self.registers[c] = b


    def load_mem(self, b, c):
        """Чтение значения из памяти"""
        if not (0 <= c < len(self.registers)):
            raise IndexError(f"Register index out of range: C={c}")
        address = self.registers[c]
        if not (0 <= address < len(self.memory)):
            raise IndexError(f"Memory access out of range: {address}")
        print(f"Loading value from memory address {address} into register {b}")
        self.registers[b] = self.memory[address]

    def store_mem(self, b, c):
        """Запись значения в память"""
        if not (0 <= b < len(self.registers)):
            raise IndexError(f"Register index out of range: B={b}")
        if not (0 <= c < len(self.registers)):
            raise IndexError(f"Register index out of range: C={c}")
        address = self.registers[b]
        if not (0 <= address < len(self.memory)):
            raise IndexError(f"Memory access out of range: {address}")
        print(f"Storing value {self.registers[c]} at memory address {address}")
        self.memory[address] = self.registers[c]


    def unary_abs(self, b, c):
        """Унарная операция abs()"""
        if not (0 <= c < len(self.registers)):
            raise IndexError(f"Register index out of range: C={c}")
        address = self.registers[c]
        if not (0 <= address < len(self.memory)):
            raise IndexError(f"Memory access out of range: {address}")
        self.registers[b] = abs(self.memory[address])

    def execute(self, instruction):
        """Выполнение одной инструкции"""
        opcode = instruction[0]
        b = struct.unpack(">I", instruction[1:5])[0]
        c = instruction[5]

        print(f"Executing opcode: {opcode}, B: {b}, C: {c}")
        print(f"Registers before execution: {self.registers}")

        if opcode == 0xC5:
            self.load_const(b, c)
        elif opcode == 0xB1:
            self.load_mem(b, c)
        elif opcode == 0x6B:
            self.store_mem(b, c)
        elif opcode == 0xE4:
            self.unary_abs(b, c)
        else:
            print(f"Warning: Unknown opcode {opcode}. Skipping.")

        print(f"Registers after execution: {self.registers}")
        print(f"Memory after execution: {self.memory[:20]}")  # Вывод первых 20 значений памяти

def interpret(binary_file, result_file, memory_range):
    vm = VirtualMachine()
    with open(binary_file, 'rb') as f:
        binary_data = f.read()

    print("Binary file content (hex):", binary_data.hex())

    for i in range(0, len(binary_data), 6):
        instruction = binary_data[i:i + 6]
        vm.execute(instruction)

    start, end = memory_range
    with open(result_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Address", "Value"])
        for addr in range(start, end + 1):
            writer.writerow([addr, vm.memory[addr]])

    print(f"Execution completed. Memory saved to {result_file}")

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python interpreter.py <binary_file> <result_file> <memory_start> <memory_end>")
        sys.exit(1)

    binary_file = sys.argv[1]
    result_file = sys.argv[2]
    memory_start = int(sys.argv[3])
    memory_end = int(sys.argv[4])

    interpret(binary_file, result_file, (memory_start, memory_end))
