"""
AI Desktop Automation Assistant (with Arithmetic Extension)
----------------------------------------------------------
A robust, modular desktop automation assistant built in Python using 
Object-Oriented Programming (OOP) principles, a custom Natural Language Processing (NLP) 
intent parser, an automated module-loading engine, and a secure arithmetic solver.

Author: Haneeth Koneru
Period: Jan 2026 – Mar 2026
"""

import os
import sys
import re
import datetime
import webbrowser
import subprocess
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Callable


# ==========================================
# 1. Intent Parsing & NLP Engine
# ==========================================

class Intent:
    """Represents a parsed user intent with extracted parameters."""
    def __init__(self, name: str, confidence: float, entities: Dict[str, Any]):
        self.name = name
        self.confidence = confidence
        self.entities = entities

    def __repr__(self) -> str:
        return f"Intent(name='{self.name}', confidence={self.confidence}, entities={self.entities})"


class NLPIntentParser:
    """
    Custom Natural Language Processing engine that tokenizes, normalizes, 
    and evaluates user commands using regular expression pattern matching and keyword scoring.
    """
    def __init__(self):
        # Mapping intent names to regex patterns and keyword lists
        self.patterns = {
            "open_browser": {
                "regex": [r"\bopen\s+(?:the\s+)?browser\b", r"\blaunch\s+browser\b", r"\bopen\s+chrome\b"],
                "keywords": ["browser", "chrome", "surf"]
            },
            "open_url": {
                "regex": [r"\bopen\s+(https?://[^\s]+)", r"\bgo\s+to\s+([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})"],
                "keywords": ["http", "www", "website", "url"]
            },
            "search_web": {
                "regex": [r"\bsearch\s+(?:for\s+)?(.+)", r"\bgoogle\s+(.+)"],
                "keywords": ["search", "google", "look up"]
            },
            "system_time": {
                "regex": [r"\bwhat(?:'s|\s+is)\s+the\s+time\b", r"\bcurrent\s+time\b", r"\btime\s+now\b"],
                "keywords": ["time", "clock"]
            },
            "system_date": {
                "regex": [r"\bwhat(?:'s|\s+is)\s+the\s+date\b", r"\btoday['s]*\s+date\b", r"\bdate\s+today\b"],
                "keywords": ["date", "day", "calendar"]
            },
            "open_application": {
                "regex": [r"\bopen\s+app(?:lication)?\s+([a-zA-Z0-9_]+)", r"\blaunch\s+([a-zA-Z0-9_]+)"],
                "keywords": ["launch", "open app"]
            },
            "solve_arithmetic": {
                "regex": [r"\b(?:calculate|solve|compute|what(?:'s|\s+is))\s+([\d\+\-\*\/\.\(\)\s]+)\b"],
                "keywords": ["calculate", "solve", "compute", "plus", "minus"]
            },
            "exit_assistant": {
                "regex": [r"\bexit\b", r"\bquit\b", r"\bbye\b", r"\bshutdown\b"],
                "keywords": ["exit", "quit", "stop", "bye"]
            }
        }

    def preprocess(self, text: str) -> str:
        """Normalizes raw text input by lowering case and stripping whitespace."""
        return text.strip().lower()

    def parse(self, raw_text: str) -> Intent:
        """
        Parses raw text to identify the highest-confidence intent and extract associated entities.
        """
        text = self.preprocess(raw_text)
        best_intent = "unknown"
        max_score = 0.0
        extracted_entities: Dict[str, Any] = {}

        for intent_name, config in self.patterns.items():
            score = 0.0
            # Check regex patterns
            for pattern in config["regex"]:
                match = re.search(pattern, text)
                if match:
                    score += 0.8
                    # Extract captured groups if any
                    groups = match.groups()
                    if groups:
                        if intent_name == "open_url":
                            extracted_entities["url"] = groups[0] if groups[0].startswith("http") else f"https://{groups[0]}"
                        elif intent_name == "search_web":
                            extracted_entities["query"] = groups[0]
                        elif intent_name == "open_application":
                            extracted_entities["app_name"] = groups[0]
                        elif intent_name == "solve_arithmetic":
                            extracted_entities["expression"] = groups[0].strip()

            # Check keyword presence
            for kw in config["keywords"]:
                if kw in text:
                    score += 0.3

            if score > max_score:
                max_score = min(score, 1.0)
                best_intent = intent_name

        # Fallback entity extraction if regex didn't capture specific groups
        if best_intent == "search_web" and "query" not in extracted_entities:
            query = re.sub(r"\b(search for|search|google|look up)\b", "", text).strip()
            extracted_entities["query"] = query if query else text
            
        elif best_intent == "solve_arithmetic" and "expression" not in extracted_entities:
            # Fallback for expression matching if regex didn't catch the exact capture group
            expr = re.sub(r"\b(calculate|solve|compute|what's|what is)\b", "", text).strip()
            extracted_entities["expression"] = expr if expr else text

        return Intent(name=best_intent, confidence=max_score, entities=extracted_entities)


# ==========================================
# 2. Modular Command Handlers (OOP Design)
# ==========================================

class BaseCommand(ABC):
    """Abstract base class for all execution handlers."""
    @abstractmethod
    def execute(self, entities: Dict[str, Any]) -> str:
        pass


class BrowserCommand(BaseCommand):
    def execute(self, entities: Dict[str, Any]) -> str:
        url = entities.get("url", "https://www.google.com")
        webbrowser.open(url)
        return f"Opening browser to: {url}"


class SearchCommand(BaseCommand):
    def execute(self, entities: Dict[str, Any]) -> str:
        query = entities.get("query", "python programming")
        encoded_query = query.replace(" ", "+")
        url = f"https://www.google.com/search?q={encoded_query}"
        webbrowser.open(url)
        return f"Searching the web for: '{query}'"


class SystemTimeCommand(BaseCommand):
    def execute(self, entities: Dict[str, Any]) -> str:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}."


class SystemDateCommand(BaseCommand):
    def execute(self, entities: Dict[str, Any]) -> str:
        current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        return f"Today's date is {current_date}."


class AppLaunchCommand(BaseCommand):
    def execute(self, entities: Dict[str, Any]) -> str:
        app_name = entities.get("app_name", "")
        if not app_name:
            return "Error: No application name specified."
        try:
            if sys.platform == "darwin":       # macOS
                subprocess.run(["open", "-a", app_name], check=True)
            elif sys.platform == "win32":      # Windows
                subprocess.run(["start", app_name], shell=True, check=True)
            else:                              # Linux
                subprocess.run([app_name], check=True)
            return f"Successfully launched application: {app_name}"
        except Exception as e:
            return f"Failed to launch '{app_name}'. Error: {str(e)}"


class ArithmeticCommand(BaseCommand):
    """Secure arithmetic command handler for basic math calculations."""
    def execute(self, entities: Dict[str, Any]) -> str:
        expression = entities.get("expression", "")
        if not expression:
            return "Error: No arithmetic expression provided."
        try:
            # Basic security check to allow only numbers and math operators
            if not re.match(r'^[\d\+\-\*\/\.\(\)\s]+$', expression):
                return "Error: Expression contains invalid characters."
            
            # Evaluate the safe math expression
            result = eval(expression)
            return f"The result of {expression} is {result}"
        except Exception as e:
            return f"Could not evaluate expression '{expression}'. Error: {str(e)}"


# ==========================================
# 3. Automated Module-Loading Engine & Assistant Core
# ==========================================

class AutomationAssistant:
    """
    Core AI Assistant engine implementing an automated module-loading architecture
    to decouple processing logic from user input interfaces.
    """
    def __init__(self, name: str = "Aura"):
        self.name = name
        self.parser = NLPIntentParser()
        self.registry: Dict[str, BaseCommand] = {}
        self._register_default_modules()

    def register_module(self, intent_name: str, command_handler: BaseCommand) -> None:
        """Seamlessly registers new functionality without modifying core execution handlers."""
        self.registry[intent_name] = command_handler

    def _register_default_modules(self) -> None:
        self.register_module("open_browser", BrowserCommand())
        self.register_module("open_url", BrowserCommand())
        self.register_module("search_web", SearchCommand())
        self.register_module("system_time", SystemTimeCommand())
        self.register_module("system_date", SystemDateCommand())
        self.register_module("open_application", AppLaunchCommand())
        self.register_module("solve_arithmetic", ArithmeticCommand())

    def process_command(self, raw_input: str) -> str:
        """Parses natural language input and routes it to the appropriate modular handler."""
        intent = self.parser.parse(raw_input)
        
        if intent.name == "exit_assistant":
            return "EXIT"
        
        if intent.name == "unknown" or intent.confidence < 0.3:
            return f"I'm sorry, I didn't quite understand that directive. (Confidence: {intent.confidence:.2f})"
        
        handler = self.registry.get(intent.name)
        if handler:
            return handler.execute(intent.entities)
        else:
            return f"No execution handler registered for intent: '{intent.name}'"

    def run_interactive(self) -> None:
        """Runs the interactive CLI loop for the desktop automation assistant."""
        print(f"==================================================")
        print(f"🤖 {self.name} - AI Desktop Automation Assistant")
        print(f"==================================================")
        print("Type your commands (e.g., 'Calculate 45 * 12 + 150', 'What is the time?', 'Exit').\n")

        while True:
            try:
                user_input = input("You > ")
                if not user_input.strip():
                    continue
                
                response = self.process_command(user_input)
                if response == "EXIT":
                    print(f"[{self.name}] Shutting down automation engine. Goodbye!")
                    break
                
                print(f"[{self.name}] {response}\n")
            except KeyboardInterrupt:
                print(f"\n[{self.name}] Session interrupted. Exiting gracefully.")
                break


# ==========================================
# 4. Main Entry Point
# ==========================================
if __name__ == "__main__":
    assistant = AutomationAssistant(name="Aura")
    assistant.run_interactive()