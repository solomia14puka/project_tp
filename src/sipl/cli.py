import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(__file__))

from parser import parse_source
from interpreter import Interpreter

def main():
    # Налаштовуємо головний парсер аргументів
    parser = argparse.ArgumentParser(description="Транслятор та інтерпретатор мови SIPL")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Доступні команди")

    # Команда 'check' (лише перевірка синтаксису)
    check_parser = subparsers.add_parser("check", help="Перевірити синтаксис файлу .sipl")
    check_parser.add_argument("file", type=str, help="Шлях до файлу з кодом")

    # Команда 'run' (виконання програми)
    run_parser = subparsers.add_parser("run", help="Виконати програму .sipl")
    run_parser.add_argument("file", type=str, help="Шлях до файлу з кодом")
    run_parser.add_argument("--trace", action="store_true", help="Увімкнути покрокове трасування подій")

    args = parser.parse_args()

    # Спроба прочитати файл із кодом
    try:
        with open(args.file, 'r', encoding='utf-8') as f:
            code = f.read()
    except FileNotFoundError:
        print(f"Помилка: Файл '{args.file}' не знайдено.")
        sys.exit(1)

    # Обробка команди check
    if args.command == "check":
        try:
            parse_source(code)
            print(f"Синтаксис файлу '{args.file}' коректний. Помилок не знайдено.")
        except Exception as e:
            print(f"Помилка синтаксису у файлі '{args.file}':\n{e}")
            sys.exit(1)

    # Обробка команди run
    elif args.command == "run":
        try:
            ast_tree = parse_source(code)
        except Exception as e:
            print(f"Неможливо виконати програму, виправте синтаксис:\n{e}")
            sys.exit(1)

        print(f"Початок виконання '{args.file}'...")
        # Передаємо прапорець trace в інтерпретатор
        interp = Interpreter(trace=args.trace)
        
        try:
            final_env = interp.evaluate(ast_tree)
            print("\nВиконання успішно завершено. Фінальний стан пам'яті:")
            for var, val in final_env.items():
                print(f"  {var} = {val}")
        except Exception as e:
            print(f"\nПомилка під час виконання (Runtime Error):\n{e}")
            sys.exit(1)

if __name__ == "__main__":
    main()