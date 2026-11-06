from lark.exceptions import LarkError
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from sipl.parser import parse_source

# 10+ позитивних тестів
valid_programs = [
    "begin skip end",
    "begin X := 5 end",
    "begin X := 5; Y := X + 2 end",
    "begin while X > 0 do X := X - 1 end",
    "begin if X = 0 then Y := 1 else Y := 2 end",
    "begin R := 1; while Y > 0 do begin R := R * 5; Y := Y - 1 end end",
    "begin A := (B + C) * 2 end",
    "begin while not (X = 0) do skip end",
    "begin X := 10 div 2 end",
    "begin begin skip end end",
    "begin A:=1; B:=2; C:=3 end"
]

# 10+ негативних тестів
invalid_programs = [
    "begin skip",            
    "X := 5",            
    "begin X := 5; end",       
    "begin while X > 0 X := 1 end",
    "begin if X = 0 then skip end",
    "begin 5 := X end",
    "begin X := * 5 end",
    "begin while X => 0 do skip end",
    "begin X := X + Y Z end",
    "begin R = 1 end",
    "begin not X > 0 do skip end"
]

def run_tests():
    passed = 0
    
    print("--- Перевірка коректних програм ---")
    for i, code in enumerate(valid_programs, 1):
        try:
            parse_source(code)
            passed += 1
        except LarkError as e:
            print(f"Помилка в позитивному тесті {i}: {code}\n{e}")
            
    print("\n--- Перевірка некоректних програм ---")
    for i, code in enumerate(invalid_programs, 1):
        try:
            parse_source(code)
            print(f"Помилка! Парсер прийняв некоректний код {i}: {code}")
        except LarkError:
            passed += 1 # Помилка очікувана, тест пройдено
            
    total = len(valid_programs) + len(invalid_programs)
    print(f"\nРезультат: пройдено {passed} з {total} тестів.")

if __name__ == "__main__":
    run_tests()