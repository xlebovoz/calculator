from PyQt5.QtCore import Qt, QSize, QPoint
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QGraphicsDropShadowEffect, QScrollArea, QListWidgetItem, QListWidget
from PyQt5.QtGui import QFont, QIcon
from consts import *
import func


app = QApplication([])
main_win = QWidget()
main_win.setWindowTitle('calculator')
ICON = QIcon('img/img-title.png')
main_win.setWindowIcon(ICON)
main_win.setFixedSize(W, H)


with open('main.qss', 'r', encoding='utf-8') as f:
    style_sheet = f.read()

app.setStyleSheet(style_sheet)

main_txt = QLabel('0')
last_txt = QLabel('')

font1 = QFont()
font2 = QFont()
font1.setPointSize(main_font)
font2.setPointSize(last_font)
main_txt.setFont(font1)
last_txt.setFont(font2)

btn1 = QPushButton('1')
btn1.setFixedSize(B_W, B_H)
btn2 = QPushButton('2')
btn2.setFixedSize(B_W, B_H)
btn3 = QPushButton('3')
btn3.setFixedSize(B_W, B_H)
btn4 = QPushButton('4')
btn4.setFixedSize(B_W, B_H)
btn5 = QPushButton('5')
btn5.setFixedSize(B_W, B_H)
btn6 = QPushButton('6')
btn6.setFixedSize(B_W, B_H)
btn7 = QPushButton('7')
btn7.setFixedSize(B_W, B_H)
btn8 = QPushButton('8')
btn8.setFixedSize(B_W, B_H)
btn9 = QPushButton('9')
btn9.setFixedSize(B_W, B_H)
btn0 = QPushButton('0')
btn0.setFixedSize(B_W, B_H)

plus = QPushButton('+')
plus.setFixedSize(B_W, B_H)
minus = QPushButton('-')
minus.setFixedSize(B_W, B_H)
mult = QPushButton('*')
mult.setFixedSize(B_W, B_H)
divide = QPushButton('/')
divide.setFixedSize(B_W, B_H)

equals = QPushButton('=')
equals.setFixedSize(B_W, B_H)
equals.setObjectName("myButton")


delite = QPushButton('←')
delite.setFixedSize(B_W, B_H)
c_button = QPushButton('C')
c_button.setFixedSize(B_W, B_H)
ce_button = QPushButton('CE')
ce_button.setFixedSize(B_W, B_H)

btn_comma = QPushButton('.')
btn_comma.setFixedSize(B_W, B_H)
btn_negative = QPushButton('⁺/₋')
btn_negative.setFixedSize(B_W, B_H)

btn_menu = QPushButton('')
menu_icon = QIcon('img/menu.png')
btn_menu.setIcon(menu_icon)
btn_menu.setIconSize(QSize(40, 40))
btn_menu.setObjectName("MenuBtn")

menu_type = 'Ordinary'

menu_label = QLabel(menu_type)
menu_label.setObjectName('MenuLabel')


history_b = QPushButton('')
history_icon = QIcon('img/history.png')
history_b.setIcon(history_icon)
history_b.setIconSize(QSize(40, 40))
history_b.setObjectName("HistoryBtn")



class ScrollableMenu(QWidget):
    def __init__(self, width=300, height=400):
        super().__init__()
        self.setWindowFlags(Qt.Popup)
        self.setFixedSize(width, height)
        self.setStyleSheet("border: none;")

        list_widget = QListWidget()
        list_widget.setObjectName('list_widget')

        calc_item = QListWidgetItem("Calculator")
        conv_item = QListWidgetItem("Converter")
        calc_item.setFlags(calc_item.flags() & ~Qt.ItemIsEnabled)
        list_widget.addItem(calc_item)

        actions = ['Ordinary']
        for action_text in actions:
            item = QListWidgetItem(action_text)
            list_widget.addItem(item)

        conv_item.setFlags(conv_item.flags() & ~Qt.ItemIsEnabled)
        list_widget.addItem(conv_item)
        list_widget.setFocusPolicy(Qt.NoFocus)


        def on_selection_changed():
            global menu_type, menu_label
            selected_items = list_widget.selectedItems()
            if selected_items:
                for item in selected_items:
                    print("Выбранный элемент:", item.text())
                    menu_type = item.text()
                    menu_label.setText(menu_type)
            else:
                print("Нет выбранных элементов")

        list_widget.itemSelectionChanged.connect(on_selection_changed)


        # Настраиваем скроллбар
        list_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        list_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(list_widget)

        self.adjustSize()

        
menu = ScrollableMenu(450, main_win.height() - 80)




buttons = [
    btn0, btn1, btn2, btn3,
    btn4, btn5, btn6,
    btn7, btn8, btn9,
    plus, minus,
    mult,
    divide,
    equals,
    delite,
    c_button,
    ce_button,
    btn_comma,
    btn_negative
]

for button in buttons:
    shadow_effect = QGraphicsDropShadowEffect()
    shadow_effect.setBlurRadius(3)
    shadow_effect.setXOffset(1)
    shadow_effect.setYOffset(1)
    shadow_effect.setColor(Qt.black)
    button.setGraphicsEffect(shadow_effect)

def on_number_click(n):
    global max_len, min_text_size, main_font, max_text_size

    cur_text = main_txt.text()
    if len(cur_text) >= max_len:
        return
    if len(cur_text) > 12:
        if main_font > min_text_size:
            main_font -= 2
            font1.setPointSize(main_font)
            main_txt.setFont(font1)
    else:
        main_font = max_text_size
        font1.setPointSize(main_font)
        main_txt.setFont(font1)

    new_text = func.button_click(cur_text, n)
    main_txt.setText(new_text)

def op_click(op):
    current_text = main_txt.text()
    last_cur_state = func.move(current_text, last_txt.text(), op)
    main_txt.setText(last_cur_state[0])
    last_txt.setText(last_cur_state[1])

def calculate():
    expression = last_txt.text() + ' ' + main_txt.text()
    try:
        result = eval(expression)
        if isinstance(result,float) and result.is_integer():
            result=int(result)
        result_str=str(result)

        if len(result_str) >17:
            scientific_str="{:.10e}".format(result) 
            if len(scientific_str)<=17:
                result_str=scientific_str
            else:
                precision=5
                scientific_str="{:.{}e}".format(result , precision )
                if len(scientific_str)<=17:
                    result_str=scientific_str
                else:
                    result_str=scientific_str

        main_txt.setText(result_str)
        last_txt.setText('')  
    except Exception:
        main_txt.setText('Error')
        last_txt .setText('')

def on_delite():
    
     global main_font,max_text_size,min_text_size,max_text_size
    
     cur_text=main_txt.text()
     new_text=func.delite_f(cur_text) 
     main_txt .setText(new_text) 
     
     if main_font<max_text_size:
         main_font+=2 
         if main_font>max_text_size:
             main_font=max_text_size 
         font1 .setPointSize(main_font) 
         main_txt .setFont(font1) 

def on_clear(m,last_text):
    
     global main_font 
     
     cur_text=main_txt.text() 
     if len(cur_text)<max_len+1:
         main_font=max_text_size 
         font1 .setPointSize(main_font) 
         main_txt .setFont(font1) 

     new_main_txt,new_last_txt=func.clear(m,last_text) 
     main_txt .setText(new_main_txt) 
     last_txt .setText(new_last_txt) 

def on_negative():
    
     current_text=main_txt.text() 
     new_value=func.negative(current_text) 
     main_txt .setText(new_value) 

def on_comma():
    
     global max_len,min_text_size ,main_font,max_text_size
    
     cur_text=main_txt.text() 
    
     if len(cur_text)>=max_len:
         return
    
     if len(cur_text)>12:
         if main_font>min_text_size :
             main_font-=2 
             font1 .setPointSize(main_font) 
             main_txt .setFont(font1) 
    
     else :
         
         main_font=max_text_size 
         
         font1 .setPointSize(main_font) 
    
         main_txt .setFont(font1) 


btn1.clicked.connect(lambda: on_number_click(1))
btn2.clicked.connect(lambda: on_number_click(2))
btn3.clicked.connect(lambda: on_number_click(3))
btn4.clicked.connect(lambda: on_number_click(4))
btn5.clicked.connect(lambda: on_number_click(5))
btn6.clicked.connect(lambda: on_number_click(6))
btn7.clicked.connect(lambda: on_number_click(7))
btn8.clicked.connect(lambda: on_number_click(8))
btn9.clicked.connect(lambda: on_number_click(9))
btn0.clicked.connect(lambda: on_number_click(0))

mult.clicked.connect(lambda: op_click('*'))
divide.clicked.connect(lambda: op_click('/'))
plus.clicked.connect(lambda: op_click('+'))
minus.clicked.connect(lambda: op_click('-'))

equals.clicked.connect(calculate)

delite.clicked.connect(on_delite)

c_button.clicked.connect(lambda: on_clear('c', last_txt.text()))
ce_button.clicked.connect(lambda: on_clear('ce', last_txt.text()))

btn_negative.clicked.connect(on_negative)
btn_comma.clicked.connect(on_comma)

open = False
def show_menu():
    btn_pos = btn_menu.mapToGlobal(btn_menu.rect().bottomLeft())
    window_pos = main_win.mapToGlobal(main_win.rect().topLeft())
    x = window_pos.x()
    y = btn_pos.y() + 15

    menu.move(QPoint(x, y))
    if open:
        menu.hide()
    else:
        menu.show()

btn_menu.clicked.connect(show_menu)


main_layout = QVBoxLayout()
menu_layout = QHBoxLayout()
layouth_0 = QHBoxLayout()
layouth_1 = QHBoxLayout()
layouth_2 = QHBoxLayout()
layouth_3 = QHBoxLayout()
layouth_4 = QHBoxLayout()
layouth_5 = QHBoxLayout()
layouth_6 = QHBoxLayout()


menu_layout.addWidget(btn_menu)
menu_layout.addWidget(menu_label)
menu_layout.addStretch()
menu_layout.addWidget(history_b)

layouth_0.addWidget(last_txt, alignment=Qt.AlignRight)
layouth_1.addWidget(main_txt, alignment=Qt.AlignRight)

layouth_2.addWidget(delite)
layouth_2.addWidget(ce_button)
layouth_2.addWidget(c_button)
layouth_2.addWidget(divide)

layouth_3.addWidget(btn7)
layouth_3.addWidget(btn8)
layouth_3.addWidget(btn9)
layouth_3.addWidget(mult)

layouth_4.addWidget(btn4)
layouth_4.addWidget(btn5)
layouth_4.addWidget(btn6)
layouth_4.addWidget(minus)

layouth_5.addWidget(btn1)
layouth_5.addWidget(btn2)
layouth_5.addWidget(btn3)
layouth_5.addWidget(plus)

layouth_6.addWidget(btn_negative)
layouth_6.addWidget(btn0)
layouth_6.addWidget(btn_comma)
layouth_6.addWidget(equals)

main_layout.addLayout(menu_layout)
main_layout.addStretch()
main_layout.addLayout(layouth_0)
main_layout.addLayout(layouth_1)
main_layout.addLayout(layouth_2)
main_layout.addLayout(layouth_3)
main_layout.addLayout(layouth_4)
main_layout.addLayout(layouth_5)
main_layout.addLayout(layouth_6)

main_win.setLayout(main_layout)


main_win.show()

app.exec()