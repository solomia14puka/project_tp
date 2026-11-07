import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from sipl.parser import parse_source
from sipl.interpreter import Interpreter

def run_test():
    # Обчислення факторіала
    code = """
    begin
        N := 5;
        R := 1;
        while N > 0 do
        begin
            R := R * N;
            N := N - 1
        end
    end
    """
    
    print("--- Запуск програми на SIPL ---")
    print(code)
    
    # 1. Розбираємо код на AST
    ast_tree = parse_source(code)
    
    # 2. Виконуємо дерево через інтерпретатор
    interp = Interpreter()
    final_env = interp.evaluate(ast_tree)
    
    # 3. Виводимо результат
    print("--- Результат виконання ---")
    for var, val in final_env.items():
        print(f"Змінна {var} = {val}")
        
    # Перевірка правильності (5! має дорівнювати 120, а N має стати 0)
    assert final_env['R'] == 120, f"Помилка обчислення: очікувалось R=120, отримано {final_env['R']}"
    assert final_env['N'] == 0, f"Помилка логіки циклу: очікувалось N=0, отримано {final_env['N']}"

if __name__ == "__main__":
    run_test()