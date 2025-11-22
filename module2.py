import tkinter as tk
from tkinter import ttk, messagebox


def _create_dialog(parent_window):
    """Приватна функція створення діалогового вікна"""
    result = {"value": None}
    
    dialog = tk.Toplevel(parent_window)
    dialog.title("Введення тексту")
    dialog.geometry("500x350")
    dialog.resizable(False, False)
    dialog.transient(parent_window)
    dialog.grab_set()
    
    # Центрування вікна
    dialog.update_idletasks()
    x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
    y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
    dialog.geometry(f"+{x}+{y}")
    
    # Заголовок
    header = ttk.Label(
        dialog,
        text="Введіть текст:",
        font=("Segoe UI", 12, "bold"),
        foreground="#0078D4"
    )
    header.pack(pady=(20, 10))
    
    # Підзаголовок
    instruction = ttk.Label(
        dialog,
        text="Введіть будь-який текст у поле нижче",
        font=("Segoe UI", 9),
        foreground="gray"
    )
    instruction.pack(pady=(0, 15))
    
    # Frame для текстового поля
    text_frame = ttk.LabelFrame(dialog, text="Текст", padding=10)
    text_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
    
    # Scrollbar
    scrollbar = ttk.Scrollbar(text_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Текстове поле (Edit Control)
    text_widget = tk.Text(
        text_frame,
        font=("Consolas", 10),
        yscrollcommand=scrollbar.set,
        wrap=tk.WORD,
        height=8,
        width=50,
        bg='white',
        relief=tk.SUNKEN,
        borderwidth=2
    )
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.config(command=text_widget.yview)
    
    # Placeholder
    placeholder = "Введіть ваш текст тут..."
    text_widget.insert("1.0", placeholder)
    text_widget.config(foreground="gray")
    
    # Лічильник символів
    char_count_var = tk.StringVar()
    char_count_var.set("Символів: 0 / 1000")
    
    char_info_frame = ttk.Frame(dialog)
    char_info_frame.pack(fill=tk.X, padx=20, pady=(5, 10))
    
    char_count_label = ttk.Label(
        char_info_frame,
        textvariable=char_count_var,
        font=("Segoe UI", 9)
    )
    char_count_label.pack(side=tk.LEFT)
    
    status_label = ttk.Label(
        char_info_frame,
        text="✓ Готово до введення",
        font=("Segoe UI", 9),
        foreground="green"
    )
    status_label.pack(side=tk.RIGHT)
    
    # Callback-функції
    def _on_focus_in(event):
        current_text = text_widget.get("1.0", "end-1c")
        if current_text == placeholder:
            text_widget.delete("1.0", tk.END)
            text_widget.config(foreground="black")
            status_label.config(text="✏ Введення...", foreground="blue")
    
    def _on_focus_out(event):
        current_text = text_widget.get("1.0", "end-1c").strip()
        if not current_text:
            text_widget.insert("1.0", placeholder)
            text_widget.config(foreground="gray")
            char_count_var.set("Символів: 0 / 1000")
            status_label.config(text="⚠ Поле порожнє", foreground="orange")
    
    def _on_text_change(event):
        current_text = text_widget.get("1.0", "end-1c")
        if current_text == placeholder:
            char_count_var.set("Символів: 0 / 1000")
            return
        
        char_count = len(current_text)
        char_count_var.set(f"Символів: {char_count} / 1000")
        
        if char_count > 1000:
            text_widget.delete("1.1001", tk.END)
            char_count_var.set("Символів: 1000 / 1000 (максимум)")
            status_label.config(text="⚠ Досягнуто ліміт", foreground="red")
        else:
            if char_count > 0:
                status_label.config(text="✓ Готово", foreground="green")
            else:
                status_label.config(text="⚠ Поле порожнє", foreground="orange")
    
    def _on_ok():
        content = text_widget.get("1.0", "end-1c").strip()
        if not content or content == placeholder:
            messagebox.showwarning(
                "Увага",
                "Будь ласка, введіть текст!\n\nПоле не може бути порожнім.",
                parent=dialog
            )
            text_widget.focus_set()
        else:
            result["value"] = content
            dialog.destroy()
    
    def _on_cancel():
        content = text_widget.get("1.0", "end-1c").strip()
        if content and content != placeholder and len(content) > 50:
            confirm = messagebox.askyesno(
                "Підтвердження",
                "Ви ввели текст. Дійсно скасувати?\n\nВведений текст буде втрачено.",
                parent=dialog
            )
            if not confirm:
                return
        result["value"] = None
        dialog.destroy()
    
    def _on_ctrl_enter(event):
        _on_ok()
        return "break"
    
    # Прив'язка подій
    text_widget.bind("<FocusIn>", _on_focus_in)
    text_widget.bind("<FocusOut>", _on_focus_out)
    text_widget.bind("<KeyRelease>", _on_text_change)
    text_widget.bind("<Control-Return>", _on_ctrl_enter)
    
    # Кнопки
    button_frame = ttk.Frame(dialog)
    button_frame.pack(pady=20)
    
    btn_ok = ttk.Button(button_frame, text="Так", command=_on_ok, width=15)
    btn_ok.pack(side=tk.LEFT, padx=10)
    
    btn_cancel = ttk.Button(button_frame, text="Відміна", command=_on_cancel, width=15)
    btn_cancel.pack(side=tk.LEFT, padx=10)
    
    # Підказка
    hint = ttk.Label(dialog, text="Підказка: Ctrl+Enter = Так", 
                     font=("Segoe UI", 8), foreground="gray")
    hint.pack(pady=(0, 10))
    
    dialog.protocol("WM_DELETE_WINDOW", _on_cancel)
    text_widget.focus_set()
    parent_window.wait_window(dialog)
    
    return result["value"]


def Func_MOD2(parent_window):
    """
    Інтерфейсна функція модуля 2
    
    Аргументи:
        parent_window: handle головного вікна
    
    Повертає:
        0 - якщо користувач скасував
        str - введений текст
    """
    entered_text = _create_dialog(parent_window)
    
    if entered_text is None:
        return 0
    else:
        return entered_text


if __name__ == "__main__":
    print("=" * 60)
    print("ТЕСТУВАННЯ MODULE2.PY")
    print("=" * 60)
    
    root = tk.Tk()
    root.withdraw()
    
    print("\n[INFO] Відкриття діалогу введення тексту...")
    result = Func_MOD2(root)
    
    print("\n" + "=" * 60)
    if result != 0:
        print("✓ УСПІХ: Текст введено")
        print(f"  Довжина: {len(result)} символів")
        print(f"  Текст:")
        print("-" * 60)
        print(result)
        print("-" * 60)
    else:
        print("✗ СКАСОВАНО: Користувач відмінив введення")
    print("=" * 60)
    
    root.destroy()
