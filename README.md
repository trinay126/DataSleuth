# 🔍 DataSleuth – Pure Python Data Profiler

A small project I built to strengthen my Python fundamentals by implementing a basic data profiling tool from scratch. Instead of relying on libraries like Pandas, I wanted to understand how common data profiling operations work internally using only core Python concepts.

---

## Features

- Parse CSV-formatted string data
- Detect basic column data types
- Generate descriptive statistics for numeric columns
- Generate summary statistics for text columns
- Perform basic data quality checks
  - Null values
  - Duplicate values
  - Whitespace detection
  - Type consistency
  - Email validation
  - Range validation
- Calculate Pearson correlation for numeric columns
- Generate a formatted text-based data quality report

---

## Why I Built This

I built this project to better understand Python fundamentals by implementing common data profiling operations from scratch.

The objective was not to replace existing libraries, but to practice problem-solving, modular programming, and understand the logic behind statistical calculations and data quality checks using only core Python.

---

## Project Structure

```text
datasleuth/
├── main.py
├── reader.py
├── stats.py
├── quality.py
├── profiler.py
├── reporter.py
├── utils.py
└── requirements.txt
└── output.txt
```

---

## Technologies Used

- Python
- Standard Library (`math`)
- No external libraries

---

## What I Learned

- Organizing a Python project into multiple modules
- Writing reusable utility functions
- Implementing statistical calculations manually
- Performing basic data quality checks
- Separating business logic from presentation
- Building a complete project using only core Python

---
