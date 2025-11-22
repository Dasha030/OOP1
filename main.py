
import tkinter as tk
from tkinter import ttk

# Імпорт модулів (тільки інтерфейсні функції)
from module1 import Func_MOD1
from module2 import Func_MOD2


class MainWindow:
    """Головне вікно програми"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Lab2 - Модульна структура")
        self.root.geometry("600x400")
        
        # Результати роботи модулів
        self.result_text = tk.StringVar()
        self.result_text.set("Оберіть пункт меню для початку роботи")
        
        # Створення меню
        self._create_menu()
        
        # Створення області відображення результатів
        self._create_display_area()
    
    def _create_menu(self):
        """Створення головного меню"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Меню "Файл"
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Вихід", command=self.root.quit)
        
        # Меню "Робота"
        work_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Робота", menu=work_menu)
        work_menu.add_command(label="Робота1", command=self.on_work1)
        work_menu.add_command(label="Робота2", command=self.on_work2)
        work_menu.add_separator()
        work_menu.add_command(label="Очистити", command=self.clear_display)
    
    def _create_display_area(self):
        """Створення області для відображення результатів"""
        # Рамка для результатів
        frame = ttk.LabelFrame(self.root, text="Результати роботи", padding=20)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Мітка для відображення результату
        label = ttk.Label(
            frame,
            textvariable=self.result_text,
            font=("Segoe UI", 14),
            foreground="#0078D4",
            wraplength=500,
            justify=tk.CENTER
        )
        label.pack(expand=True)
    
    def on_work1(self):
        """
        Обробник меню "Робота1"
        Викликає функцію з module1
        """
        # Викликаємо функцію модуля 1
        result = Func_MOD1(self.root)
        
        # Якщо користувач натиснув OK (result != 0)
        if result != 0:
            self.result_text.set(f"Робота1 виконана:\n{result}")
        else:
            self.result_text.set("Робота1 скасована користувачем")
    
    def on_work2(self):
        """
        Обробник меню "Робота2"
        Викликає функцію з module2
        """
        # Викликаємо функцію модуля 2
        result = Func_MOD2(self.root)
        
        # Якщо користувач натиснув OK (result != 0)
        if result != 0:
            self.result_text.set(f"Робота2 виконана:\n{result}")
        else:
            self.result_text.set("Робота2 скасована користувачем")
    
    def clear_display(self):
        """Очищення області відображення"""
        self.result_text.set("Оберіть пункт меню для початку роботи")


def main():
    """Головна функція програми"""
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
