#Pydroid run kivy

import math
import ast
import operator

from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup

Window.clearcolor = (0.015, 0.025, 0.055, 1)

CYAN = "#00E5FF"
BLUE = "#087BFF"
DARK = "#101A2D"
PANEL = "#14223A"
WHITE = "#EAF7FF"
MUTED = "#7893B5"
PURPLE = "#813CFF"
RED = "#A52F50"


class NeonButton(Button):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ""
        self.background_down = ""
        self.font_size = "16sp"
        self.bold = True
        self.color = get_color_from_hex(WHITE)


class Heltoness(App):

    def build(self):

        self.memory = 0
        self.answer = 0
        self.history = []
        self.degrees = True
        self.expression = ""

        root = BoxLayout(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(9)
        )

        # CABEÇALHO

        header = BoxLayout(
            size_hint_y=None,
            height=dp(55)
        )

        menu = NeonButton(
            text="☰",
            size_hint_x=None,
            width=dp(48),
            background_color=get_color_from_hex(DARK),
            color=get_color_from_hex(CYAN)
        )
        menu.bind(on_release=lambda x: self.show_menu())

        header.add_widget(menu)

        brand = BoxLayout(orientation="vertical")

        brand.add_widget(Label(
            text="[b]HELTONESS IA[/b]",
            markup=True,
            color=get_color_from_hex(CYAN),
            font_size="22sp"
        ))

        brand.add_widget(Label(
            text="ADVANCED SCIENTIFIC SYSTEM",
            color=get_color_from_hex(MUTED),
            font_size="9sp"
        ))

        header.add_widget(brand)

        self.mode_button = NeonButton(
            text="DEG",
            size_hint_x=None,
            width=dp(55),
            background_color=get_color_from_hex(PURPLE)
        )
        self.mode_button.bind(on_release=self.toggle_mode)

        header.add_widget(self.mode_button)
        root.add_widget(header)

        # VISOR

        screen = BoxLayout(
            orientation="vertical",
            padding=dp(13),
            spacing=dp(6),
            size_hint_y=None,
            height=dp(145)
        )

        screen.background_color = get_color_from_hex(PANEL)

        self.display = TextInput(
            text="",
            hint_text="0",
            multiline=False,
            halign="right",
            font_size="25sp",
            foreground_color=get_color_from_hex(WHITE),
            background_color=get_color_from_hex(PANEL),
            cursor_color=get_color_from_hex(CYAN),
            size_hint_y=None,
            height=dp(55)
        )

        screen.add_widget(self.display)

        self.result = Label(
            text="0",
            halign="right",
            font_size="30sp",
            bold=True,
            color=get_color_from_hex(CYAN)
        )

        screen.add_widget(self.result)
        root.add_widget(screen)

        # MEMÓRIA

        memory = GridLayout(
            cols=5,
            spacing=dp(5),
            size_hint_y=None,
            height=dp(42)
        )

        for name in ["MC", "MR", "M+", "M-", "ANS"]:
            b = NeonButton(
                text=name,
                font_size="12sp",
                background_color=get_color_from_hex(DARK),
                color=get_color_from_hex(CYAN)
            )
            b.bind(on_release=self.press)
            memory.add_widget(b)

        root.add_widget(memory)

        # TECLADO CIENTÍFICO

        scroll = ScrollView()

        grid = GridLayout(
            cols=5,
            spacing=dp(6),
            size_hint_y=None
        )

        grid.bind(minimum_height=grid.setter("height"))

        keys = [
            ["sin", "cos", "tan", "asin", "acos"],
            ["atan", "log", "ln", "√", "∛"],
            ["x²", "x³", "xʸ", "10ˣ", "1/x"],
            ["(", ")", "π", "e", "!"],
            ["7", "8", "9", "DEL", "AC"],
            ["4", "5", "6", "×", "÷"],
            ["1", "2", "3", "+", "−"],
            ["0", ".", "%", "HIST", "="]
        ]

        for row in keys:
            for key in row:

                color = DARK

                if key == "=":
                    color = BLUE
                elif key in ["AC", "DEL"]:
                    color = RED
                elif key in [
                    "sin", "cos", "tan", "asin",
                    "acos", "atan", "log", "ln",
                    "√", "∛", "x²", "x³", "xʸ",
                    "10ˣ", "1/x", "π", "e", "!"
                ]:
                    color = PURPLE
                elif key in ["+", "−", "×", "÷", "%"]:
                    color = "#075B75"

                b = NeonButton(
                    text=key,
                    size_hint_y=None,
                    height=dp(53),
                    background_color=get_color_from_hex(color)
                )

                b.bind(on_release=self.press)
                grid.add_widget(b)

        scroll.add_widget(grid)
        root.add_widget(scroll)

        footer = Label(
            text="HELTONESS TECHNOLOGY  •  VERSION 2.0",
            size_hint_y=None,
            height=dp(23),
            font_size="9sp",
            color=get_color_from_hex(MUTED)
        )

        root.add_widget(footer)

        return root

    def toggle_mode(self, *args):

        self.degrees = not self.degrees
        self.mode_button.text = "DEG" if self.degrees else "RAD"

    def press(self, instance):

        k = instance.text
        t = self.display.text

        if k == "AC":
            self.display.text = ""
            self.result.text = "0"

        elif k == "DEL":
            self.display.text = t[:-1]

        elif k == "=":
            self.calculate()

        elif k == "HIST":
            self.show_history()

        elif k == "ANS":
            self.display.text += str(self.answer)

        elif k == "MC":
            self.memory = 0

        elif k == "MR":
            self.display.text += str(self.memory)

        elif k == "M+":
            self.memory += self.answer

        elif k == "M-":
            self.memory -= self.answer

        elif k == "π":
            self.display.text += "pi"

        elif k == "e":
            self.display.text += "e"

        elif k in ["sin", "cos", "tan",
                   "asin", "acos", "atan",
                   "log", "ln"]:

            self.display.text += k + "("

        elif k in ["√", "∛"]:
            self.display.text += (
                "sqrt(" if k == "√" else "cbrt("
            )

        elif k == "x²":
            self.display.text += "**2"

        elif k == "x³":
            self.display.text += "**3"

        elif k == "xʸ":
            self.display.text += "**"

        elif k == "10ˣ":
            self.display.text += "10**"

        elif k == "1/x":
            self.display.text += "1/("

        elif k == "!":
            self.display.text += "!"

        elif k == "×":
            self.display.text += "*"

        elif k == "÷":
            self.display.text += "/"

        elif k == "−":
            self.display.text += "-"

        elif k == "%":
            self.display.text += "/100"

        else:
            self.display.text += k

    def calculate(self):

        try:
            expression = self.display.text.replace("^", "**")

            result = self.safe_calculate(expression)

            if not math.isfinite(result):
                raise ValueError("Resultado inválido")

            self.answer = result
            self.result.text = str(round(result, 12))

            self.history.append(
                expression + " = " + str(result)
            )

        except Exception:
            self.result.text = "EXPRESSÃO INVÁLIDA"

    def safe_calculate(self, expression):

        def factorial(x):
            if x < 0 or int(x) != x or x > 170:
                raise ValueError()
            return math.factorial(int(x))

        def angle(x):
            return math.radians(x) if self.degrees else x

        def inverse(x):
            return math.degrees(x) if self.degrees else x

        functions = {
            "sin": lambda x: math.sin(angle(x)),
            "cos": lambda x: math.cos(angle(x)),
            "tan": lambda x: math.tan(angle(x)),
            "asin": lambda x: inverse(math.asin(x)),
            "acos": lambda x: inverse(math.acos(x)),
            "atan": lambda x: inverse(math.atan(x)),
            "sqrt": math.sqrt,
            "cbrt": lambda x: math.copysign(abs(x)**(1/3), x),
            "log": math.log10,
            "ln": math.log,
            "factorial": factorial
        }

        names = {
            "pi": math.pi,
            "e": math.e
        }

        tree = ast.parse(expression, mode="eval")

        def evaluate(node):

            if isinstance(node, ast.Expression):
                return evaluate(node.body)

            if isinstance(node, ast.Constant):
                if isinstance(node.value, (int, float)):
                    return node.value
                raise ValueError()

            if isinstance(node, ast.BinOp):
                a = evaluate(node.left)
                b = evaluate(node.right)

                ops = {
                    ast.Add: operator.add,
                    ast.Sub: operator.sub,
                    ast.Mult: operator.mul,
                    ast.Div: operator.truediv,
                    ast.Pow: operator.pow,
                    ast.Mod: operator.mod
                }

                for op, func in ops.items():
                    if isinstance(node.op, op):
                        return func(a, b)

                raise ValueError()

            if isinstance(node, ast.UnaryOp):
                x = evaluate(node.operand)

                if isinstance(node.op, ast.USub):
                    return -x

                if isinstance(node.op, ast.UAdd):
                    return x

                raise ValueError()

            if isinstance(node, ast.Call):
                if not isinstance(node.func, ast.Name):
                    raise ValueError()

                name = node.func.id

                if name not in functions or len(node.args) != 1:
                    raise ValueError()

                return functions[name](evaluate(node.args[0]))

            if isinstance(node, ast.Name):
                if node.id in names:
                    return names[node.id]
                raise ValueError()

            raise ValueError()

        # Factorial: 5! becomes factorial(5)
        import re

        expression = re.sub(
            r'(\d+(?:\.\d+)?)!',
            r'factorial(\1)',
            expression
        )

        tree = ast.parse(expression, mode="eval")

        return evaluate(tree)

    def show_history(self):

        content = BoxLayout(orientation="vertical")

        text = "\n".join(self.history[-30:])

        if not text:
            text = "Nenhum cálculo realizado."

        label = Label(
            text=text,
            color=get_color_from_hex(WHITE)
        )

        content.add_widget(label)

        popup = Popup(
            title="HISTÓRICO HELTONESS",
            content=content,
            size_hint=(0.9, 0.7)
        )

        popup.open()

    def show_menu(self):

        content = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=10
        )

        popup = Popup(
            title="HELTONESS IA",
            content=content,
            size_hint=(0.85, 0.55)
        )

        options = [
            "Calculadora científica",
            "Histórico de cálculos",
            "Sobre HELTONESS IA"
        ]

        for option in options:

            b = NeonButton(
                text=option,
                background_color=get_color_from_hex(DARK)
            )

            def action(instance, value=option):
                popup.dismiss()

                if value == "Histórico de cálculos":
                    self.show_history()

                elif value == "Sobre HELTONESS IA":
                    self.about()

            b.bind(on_release=action)
            content.add_widget(b)

        popup.open()

    def about(self):

        Popup(
            title="SOBRE",
            content=Label(
                text="HELTONESS IA\nADVANCED SCIENTIFIC CALCULATOR\nVersion 2.0"
            ),
            size_hint=(0.85, 0.4)
        ).open()


Heltoness().run()
