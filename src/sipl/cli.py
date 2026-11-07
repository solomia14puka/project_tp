import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(__file__))

from parser import parse_source
from interpreter import Interpreter

def main():
    parser = argparse.ArgumentParser(description="Транслятор та інтерпретатор мови SIPL")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Доступні команди")

    # Команда 'check'
    check_parser = subparsers.add_parser("check", help="Перевірити синтаксис файлу .sipl")
    check_parser.add_argument("file", type=str, help="Шлях до файлу з кодом")
    check_parser.add_argument("--visualize", action="store_true", help="Згенерувати дерево AST (DOT та PNG)")

    # Команда 'run'
    run_parser = subparsers.add_parser("run", help="Виконати програму .sipl")
    run_parser.add_argument("file", type=str, help="Шлях до файлу з кодом")
    run_parser.add_argument("--trace", action="store_true", help="Увімкнути покрокове трасування подій")
    run_parser.add_argument("--visualize", action="store_true", help="Згенерувати дерево AST (DOT та PNG)")

    args = parser.parse_args()

    # Зчитуємо файл
    try:
        with open(args.file, 'r', encoding='utf-8') as f:
            code = f.read()
    except FileNotFoundError:
        print(f"Помилка: Файл '{args.file}' не знайдено.")
        sys.exit(1)

    try:
        ast_tree = parse_source(code)
    except Exception as e:
        print(f"Помилка синтаксису у файлі '{args.file}':\n{e}")
        sys.exit(1)

    if args.command == "check":
        print(f"Синтаксис файлу '{args.file}' коректний. Помилок не знайдено.")

    # Візуалізація
    if getattr(args, 'visualize', False):
        from visualizer import ASTVisualizer
        vis = ASTVisualizer()
        dot_source = vis.generate_dot(ast_tree)
        
        with open("ast.dot", "w", encoding="utf-8") as f:
            f.write(dot_source)
        print("Згенеровано файл графа: ast.dot")
        
        if os.system("dot -Tpng ast.dot -o ast.png") == 0:
            print("Згенеровано зображення: ast.png")
        else:
            print("Помилка генерації PNG. Перевірте, чи встановлено graphviz.")

    # Виконання програми (тільки для команди run)
    if args.command == "run":
        print(f"Початок виконання '{args.file}'...")
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