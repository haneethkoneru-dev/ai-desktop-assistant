# 🤖 AI Desktop Automation Assistant

A robust, modular desktop automation assistant built in Python using **Object-Oriented Programming (OOP)** principles, a custom **Natural Language Processing (NLP)** intent parser, and a decoupled execution architecture.

## 🚀 Key Features

* **Custom NLP Intent Parser:** Tokenizes, normalizes, and evaluates natural language user directives using regular expression pattern matching and keyword scoring.
* **Modular OOP Architecture:** Implements abstract base command handlers (`BaseCommand`) to cleanly decouple command execution logic from user input interfaces.
* **Dynamic Module Loading:** Allows seamless runtime registration of new capabilities (`register_module()`) without modifying core execution handlers.
* **Multi-Domain Automation:** Supports web searches, browser navigation, system time/date queries, application launching, and live arithmetic expression evaluation.

## 🛠️ Tech Stack & Concepts
* **Language:** Python 3.x
* **Core Paradigms:** Object-Oriented Programming (OOP), Abstract Base Classes (ABC), Modular Design Patterns
* **Libraries Used:** `re`, `datetime`, `webbrowser`, `subprocess`, `sys`

## 📦 Getting Started

Clone the repository and run the assistant interactively via your terminal:

```bash
git clone [https://github.com/your-username/ai-desktop-assistant.git](https://github.com/your-username/ai-desktop-assistant.git)
cd ai-desktop-assistant
python ai_assistant_math.py
