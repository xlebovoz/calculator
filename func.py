
def button_click(current_text, number):
    if current_text == '0':
        return str(number)
    else:
        return current_text + str(number)  

def move(current_text, last_text, op):
    last_text = f"{current_text} {op}"
    return '0', last_text

def delite_f(current_text):
    if len(current_text) > 1:
        return current_text[:-1]
    else:
        return '0'

def clear(m, last_text):
    if m == 'ce':
        return '0', last_text
    elif m == 'c':
        return '0', ''
    
def negative(current_text):
    try:
        value = float(current_text)
        value *= -1
        if value.is_integer():
            return str(int(value))
        else:
            return str(value)
    except ValueError:
        return current_text

def comma(current_text):
    if '.' not in current_text:
        return current_text + '.'
    else:
        return current_text