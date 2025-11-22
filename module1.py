
import tkinter as tk
from tkinter import ttk, messagebox


# ============================================================================
# ПРИВАТНІ ФУНКЦІЇ МОДУЛЯ (не експортуються)
# ============================================================================

def _create_dialog(parent_window):
    """
    Приватна функція створення діалогового вікна з List Box
    Еквівалент static функції в C++
    
    Повертає:
        None - якщо користувач скасував
        str - текст обраної групи
    """
    # Результат вибору
    result = {"value": None}
    
    # Створення модального діалогу
    dialog = tk.Toplevel(parent_window)
    dialog.title("Вибір групи факультету")
    dialog.geometry("450x400")
    dialog.resizable(False, False)
    
    # Робимо діалог модальним (блокує батьківське вікно)
    dialog.transient(parent_window)
    dialog.grab_set()
    
    # Центрування вікна на екрані
    dialog.update_idletasks()
    x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
    y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
    dialog.geometry(f"+{x}+{y}")
    
    # ---- Інтерфейс діалогу ----
    
    # Заголовок
    header = ttk.Label(
        dialog,
        text="Оберіть групу факультету:",
        font=("Segoe UI", 12, "bold"),
        foreground="#0078D4"
    )
    header.pack(pady=(20, 15))
    
    # Frame для List Box та Scrollbar
    list_frame = ttk.Frame(dialog)
    list_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
    
    # Scrollbar
    scrollbar = ttk.Scrollbar(list_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # List Box з групами
    listbox = tk.Listbox(
        list_frame,
        font=("Segoe UI", 10),
        yscrollcommand=scrollbar.set,
        selectmode=tk.SINGLE,
        activestyle='dotbox',
        height=12,
        bg='white',
        selectbackground='#0078D4',
        selectforeground='white'
    )
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.config(command=listbox.yview)
    
    # ---- РЕСУРСИ МОДУЛЯ: Список груп факультету ----
    groups = [
        "ІМ-41 (Інженерія програмного забезпечення)",
        "ІМ-42 (Інженерія програмного забезпечення)",
        "ІМ-43 (Інженерія програмного забезпечення)",
        "ІМ-44 (Інженерія програмного забезпечення)",
        "ІП-41 (Інженерія програмного забезпечення)",
        "ІП-42 (Інженерія програмного забезпечення)",
        "ІП-43 (Інженерія програмного забезпечення)",
        "ІП-44 (Інженерія програмного забезпечення)",
    
    # Заповнення List Box групами
    for group in groups:
        listbox.insert(tk.END, group)
    
    # Вибір першого елемента за замовчуванням
    listbox.selection_set(0)
    listbox.activate(0)
    listbox.see(0)  # Прокрутка до вибраного елемента
    
    # Підказка
    hint_label = ttk.Label(
        dialog,
        text="Подвійний клік на групі = вибір",
        font=("Segoe UI", 9),
        foreground="gray"
    )
    hint_label.pack(pady=(5, 10))
    
    # ---- CALLBACK-ФУНКЦІЇ (приватні, не експортуються) ----
    
    def _on_ok():
        """
        Обробник кнопки [Так]
        Перевіряє чи обрано елемент та повертає його текст
        """
        selection = listbox.curselection()
        if selection:
            index = selection[0]
            result["value"] = listbox.get(index)
            dialog.destroy()
        else:
            messagebox.showwarning(
                "Увага",
                "Будь ласка, оберіть групу зі списку!",
                parent=dialog
            )
    
    def _on_cancel():
        """
        Обробник кнопки [Відміна]
        Закриває діалог без збереження результату
        """
        result["value"] = None
        dialog.destroy()
    
    def _on_double_click(event):
        """
        Обробник подвійного кліку на елементі списку
        Еквівалент натискання кнопки [Так]
        """
        _on_ok()
    
    def _on_enter_key(event):
        """
        Обробник клавіші Enter
        Еквівалент натискання кнопки [Так]
        """
        _on_ok()
    
    # Прив'язка подій
    listbox.bind('<Double-Button-1>', _on_double_click)
    listbox.bind('<Return>', _on_enter_key)
    
    # ---- Кнопки ----
    
    button_frame = ttk.Frame(dialog)
    button_frame.pack(pady=20)
    
    btn_ok = ttk.Button(
        button_frame,
        text="Так",
        command=_on_ok,
        width=15
    )
    btn_ok.pack(side=tk.LEFT, padx=10)
    
    btn_cancel = ttk.Button(
        button_frame,
        text="Відміна",
        command=_on_cancel,
        width=15
    )
    btn_cancel.pack(side=tk.LEFT, padx=10)
    
    # Обробка закриття вікна через [×]
    dialog.protocol("WM_DELETE_WINDOW", _on_cancel)
    
    # Встановлення фокусу на List Box
    listbox.focus_set()
    
    # Очікування закриття діалогу
    parent_window.wait_window(dialog)
    
    return result["value"]


# ============================================================================
# ПУБЛІЧНИЙ ІНТЕРФЕЙС МОДУЛЯ (експортується)
# ============================================================================

def Func_MOD1(parent_window):
    """
    Інтерфейсна функція модуля 1
    
    Відкриває діалогове вікно з List Box для вибору групи факультету.
    Якщо користувач обирає групу і натискає [Так], повертає текст групи.
    Якщо натискає [Відміна] або закриває вікно - повертає 0.
    
    Аргументи:
        parent_window: tkinter.Tk або tkinter.Toplevel
                      Handle головного вікна програми
    
    Повертає:
        0 (int) - якщо користувач натиснув [Відміна] або закрив вікно
        str - текст обраної групи, якщо користувач натиснув [Так]
    
    Приклад використання:
        result = Func_MOD1(root)
        if result != 0:
            print(f"Обрана група: {result}")
        else:
            print("Вибір скасовано користувачем")
    """
    # Викликаємо приватну функцію створення діалогу
    selected_group = _create_dialog(parent_window)
    
    # Повертаємо результат відповідно до вимог
    if selected_group is None:
        return 0  # Користувач скасував вибір
    else:
        return selected_group  # Повертаємо текст обраної групи


# ============================================================================
# ТЕСТУВАННЯ МОДУЛЯ
# ============================================================================

if __name__ == "__main__":
    """
    Блок тестування модуля
    Виконується тільки при прямому запуску: python module1.py
    Не виконується при імпорті модуля
    """
    print("=" * 60)
    print("ТЕСТУВАННЯ MODULE1.PY")
    print("=" * 60)
    
    # Створення тестового вікна
    root = tk.Tk()
    root.withdraw()  # Ховаємо головне вікно для тесту
    
    print("\n[INFO] Відкриття діалогу вибору групи...")
    
    # Виклик функції модуля
    result = Func_MOD1(root)
    
    # Аналіз результату
    print("\n" + "=" * 60)
    if result != 0:
        print("✓ УСПІХ: Група обрана")
        print(f"  Обрана група: {result}")
    else:
        print("✗ СКАСОВАНО: Користувач відмінив вибір")
    print("=" * 60)
    
    root.destroy()
