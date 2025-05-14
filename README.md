# C to Promela Code Converter (`c2promela`)

This project provides a tool to convert a subset of **C code** into **Promela**, the modeling language used by the **SPIN model checker**. The purpose is to assist in the **formal verification** of C programs by enabling their analysis with SPIN.

![image](https://github.com/user-attachments/assets/0b1436e8-62f4-4e62-bdce-781d9884b0af)

---

## 🔧 Features

- Parses C code and generates equivalent Promela code.
- Supports a subset of the C language:
  - Variable declarations (`int`, `byte`, `bool`)
  - `if`, `else`, `switch`, `while`, `for`, and `do...while` control structures
  - Functions (converted to Promela inline or proctype)
  - Arrays and structs (mapped to Promela equivalents)
  - Simple pointer-like behavior (limited)
- Ensures **scope-safe variable naming** to avoid Promela redeclaration issues.
- Generates **commented Promela code** for better traceability to original C lines.

---

## Installation

```bash
git clone https://github.com/yourusername/c2promela.git
cd c2promela
pip install -r requirements.txt
```

## Running c2promela
### Through CLI
- Run the following command on terminal
```bash
cd c2promela
.\run_pipeline
```
### Through GUI
- Run `app1.py` using the following command
```bash
python app1.py
```
