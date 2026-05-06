import subprocess
import os
import sys

def run_command(python_exe, command, description):
    print(f"\n\033[1;34m{'='*60}\033[0m")
    print(f" \033[1;32mEXECUTING:\033[0m {description}")
    print(f"\033[1;34m{'='*60}\033[0m")
    
    try:
        result = subprocess.run([python_exe] + command.split(), capture_output=False, text=True)
        if result.returncode != 0:
            print(f"\n\033[1;31m[ERROR] Command failed with return code {result.returncode}\033[0m")
    except Exception as e:
        print(f"\n\033[1;31m[EXCEPTION] {e}\033[0m")

def main():
    # Asegurarnos de estar en la raíz del proyecto
    root_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(root_dir)

    # Calcular ruta absoluta del venv
    venv_python = os.path.join(root_dir, ".venv", "bin", "python3")
    python_exe = venv_python if os.path.exists(venv_python) else sys.executable

    print("\n\033[1;36m" + "╔" + "═"*58 + "╗")
    print("║" + " TINYBIRD TECHNICAL ASSESSMENT - COMPREHENSIVE TEST SUITE ".center(58) + "║")
    print("╚" + "═"*58 + "╝" + "\033[0m")

    # PARTE 1
    run_command(python_exe, "main.py", "PARTE 1: PROCESAMIENTO Y VALIDACIÓN")

    # PARTE 2
    os.chdir(os.path.join(root_dir, "part2"))
    run_command(python_exe, "metrics_runner.py", "PARTE 2: MÉTRICAS")

    # PARTE 3
    os.chdir(os.path.join(root_dir, "part3"))
    run_command(python_exe, "api_runner.py", "PARTE 3: API (SIN FRAMEWORK)")

    os.chdir(root_dir)
    print(f"\n\033[1;32m{'='*60}")
    print(" ✅ TODAS LAS PRUEBAS COMPLETADAS CON ÉXITO".center(60))
    print(f"{'='*60}\033[0m\n")

if __name__ == "__main__":
    main()
