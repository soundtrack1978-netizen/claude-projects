import tkinter as tk


class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("計算機")
        self.window.resizable(False, False)

        self.expression = ""
        self.display_var = tk.StringVar(value="0")

        self._build_display()
        self._build_buttons()
        self._bind_keys()

    def _build_display(self):
        display = tk.Entry(
            self.window,
            textvariable=self.display_var,
            font=("Helvetica", 28),
            justify="right",
            bd=0,
            bg="#1c1c1e",
            fg="white",
            readonlybackground="#1c1c1e",
            state="readonly",
        )
        display.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=(20, 10), ipady=20)

    def _build_buttons(self):
        buttons = [
            ("C", 1, 0, "#a5a5a5", "black"),
            ("±", 1, 1, "#a5a5a5", "black"),
            ("%", 1, 2, "#a5a5a5", "black"),
            ("÷", 1, 3, "#ff9f0a", "white"),
            ("7", 2, 0, "#333333", "white"),
            ("8", 2, 1, "#333333", "white"),
            ("9", 2, 2, "#333333", "white"),
            ("×", 2, 3, "#ff9f0a", "white"),
            ("4", 3, 0, "#333333", "white"),
            ("5", 3, 1, "#333333", "white"),
            ("6", 3, 2, "#333333", "white"),
            ("−", 3, 3, "#ff9f0a", "white"),
            ("1", 4, 0, "#333333", "white"),
            ("2", 4, 1, "#333333", "white"),
            ("3", 4, 2, "#333333", "white"),
            ("+", 4, 3, "#ff9f0a", "white"),
            ("0", 5, 0, "#333333", "white"),
            (".", 5, 2, "#333333", "white"),
            ("=", 5, 3, "#ff9f0a", "white"),
        ]

        for text, row, col, bg, fg in buttons:
            colspan = 2 if text == "0" else 1
            btn = tk.Button(
                self.window,
                text=text,
                font=("Helvetica", 20),
                bg=bg,
                fg=fg,
                activebackground=bg,
                activeforeground=fg,
                bd=0,
                width=4 if text != "0" else 9,
                height=2,
                command=lambda t=text: self._on_press(t),
            )
            btn.grid(row=row, column=col, columnspan=colspan, padx=2, pady=2, sticky="nsew")

        self.window.configure(bg="#000000")
        for i in range(6):
            self.window.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.window.grid_columnconfigure(i, weight=1)

    def _bind_keys(self):
        self.window.bind("<Key>", self._on_key)

    def _on_key(self, event):
        key_map = {
            "0": "0", "1": "1", "2": "2", "3": "3", "4": "4",
            "5": "5", "6": "6", "7": "7", "8": "8", "9": "9",
            ".": ".", "+": "+", "-": "−", "*": "×", "/": "÷",
            "Return": "=", "KP_Enter": "=", "Escape": "C",
            "percent": "%",
        }
        action = key_map.get(event.keysym)
        if action:
            self._on_press(action)

    def _on_press(self, text):
        ops = {"+", "−", "×", "÷"}

        if text == "C":
            self.expression = ""
            self.display_var.set("0")
        elif text == "±":
            if self.expression and self.expression[0] == "-":
                self.expression = self.expression[1:]
            elif self.expression:
                self.expression = "-" + self.expression
            self.display_var.set(self.expression or "0")
        elif text == "%":
            try:
                result = self._evaluate() / 100
                self.expression = self._format(result)
                self.display_var.set(self.expression)
            except Exception:
                self.expression = ""
                self.display_var.set("エラー")
        elif text == "=":
            try:
                result = self._evaluate()
                self.expression = self._format(result)
                self.display_var.set(self.expression)
            except Exception:
                self.expression = ""
                self.display_var.set("エラー")
        elif text in ops:
            if self.expression and self.expression[-1] in "+-*/":
                self.expression = self.expression[:-1]
            symbol_map = {"÷": "/", "×": "*", "−": "-", "+": "+"}
            self.expression += symbol_map[text]
            self.display_var.set(self.expression.translate(str.maketrans("/*-", "÷×−")))
        else:
            if self.expression == "0" and text != ".":
                self.expression = ""
            self.expression += text
            self.display_var.set(self.expression.translate(str.maketrans("/*-", "÷×−")))

    def _evaluate(self):
        return eval(self.expression)

    def _format(self, value):
        if isinstance(value, float) and value == int(value):
            return str(int(value))
        return str(value)

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    Calculator().run()
