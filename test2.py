from python_interpreter import PythonInterpreter, run_interpreter


filename="code.py"
code = 'print("bye world")'
interpreter_code_output = run_interpreter(code)
print("Python code output:\n", interpreter_code_output)
