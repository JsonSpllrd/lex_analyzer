from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import re

# Check if character is delimiter
def is_delimiter(char):
    return char in {',', ';', '(', ')', '[', ']', '{', '}'}

# Check if character is operator
def is_operator(char):
    return char in {'+', '-', '*', '/', '%', '>', '<', '='}

# Get operator name
def get_operator_name(char):
    operators = {
        '+': 'plus_op', '-': 'minus_op', '*': 'multiply_op',
        '/': 'divide_op', '>': 'greater_than', '<': 'less_than',
        '=': 'equal_sign', '%': 'modulus_op'
    }
    return operators.get(char)

# Get delimiter name
def get_delimiter_name(char):
    delimiters = {
        ',': 'comma', ';': 'semicolon', '(': 'open_parenthesis',
        ')': 'close_parenthesis', '[': 'open_bracket', ']': 'close_bracket',
        '{': 'open_brace', '}': 'close_brace'
    }
    return delimiters.get(char)

# Check if identifier is valid
def is_valid_identifier(string):
    return bool(re.match(r'^[^\d\W]\w*\Z', string))

# Check if the string is a keyword or datatype
def get_keyword_or_datatype_name(string):
    keywords = {"break", "case", "continue", "default", "do", "else", "enum",
                "extern", "for", "goto", "if", "return", "sizeof", "static",
                "struct", "switch", "typedef", "union", "while"}
    datatypes = {"auto", "char", "const", "double", "float", "int", "long",
                 "register", "short", "signed", "unsigned", "void", "volatile"}

    if string in keywords:
        return "keyword"
    elif string in datatypes:
        return "datatype"
    return None

# Check if the string is an integer
def is_integer(string):
    return string.isdigit()

# Main lexical analyzer function
def lexical_analyzer(input_text):
    tokens = []
    length = len(input_text)
    left = 0

    while left < length:
        if input_text[left] == '"':
            right = left + 1
            while right < length and input_text[right] != '"':
                right += 1
            if right < length:
                lexeme = input_text[left + 1:right]
                tokens.append((lexeme, "string_literal"))
            left = right + 1
            continue

        right = left
        while right < length and not is_delimiter(input_text[right]) and not is_operator(input_text[right]) and input_text[right] != ' ':
            right += 1

        if left != right:
            lexeme = input_text[left:right]
            if (token := get_keyword_or_datatype_name(lexeme)):
                tokens.append((lexeme, token))
            elif is_integer(lexeme):
                tokens.append((lexeme, "int_literal"))
            elif is_valid_identifier(lexeme):
                tokens.append((lexeme, "identifier"))
            else:
                tokens.append((lexeme, "unidentified"))
            left = right
        else:
            if is_delimiter(input_text[left]):
                tokens.append((input_text[left], get_delimiter_name(input_text[left])))
            elif is_operator(input_text[left]):
                tokens.append((input_text[left], get_operator_name(input_text[left])))
            left += 1

        if left < length and input_text[left] == ' ':
            left += 1

    return tokens

# Generate PDF report
def generate_pdf(tokens, input_text, output_filename="lexical_analysis.pdf"):
    c = canvas.Canvas(output_filename, pagesize=letter)
    width, height = letter

    # Add title
    c.drawString(30, height - 30, "Lexical Analysis Report")
    c.drawString(30, height - 50, "=====================================")

    # Add user input at the top
    c.drawString(30, height - 80, "Input Expression:")
    c.drawString(30, height - 100, input_text)  # This prints the user's input expression
    c.drawString(30, height - 120, "=====================================")

    # Add space for tokens below
    y = height - 150
    c.drawString(30, y, "Lexemes")
    c.drawString(200, y, "Tokens")
    c.drawString(30, height - 160, "=====================================")
    y -= 30

    # Check if tokens exist
    if not tokens:
        c.drawString(30, y, "No tokens generated.")
    else:
        for lexeme, token in tokens:
            c.drawString(30, y, str(lexeme))
            c.drawString(200, y, str(token))
            y -= 20
            if y < 40:  # Create a new page if there isn't enough space
                c.showPage()
                y = height - 40

    c.save()
    print(f"PDF generated: {output_filename}")

# Main function to get input and run lexical analyzer
def main():
    input_text = input("Enter an expression: ")
    tokens = lexical_analyzer(input_text)
    print("Lexical Analysis Results:")
    for lexeme, token in tokens:
        print(f"Lexeme: {lexeme}, Token: {token}")
    generate_pdf(tokens, input_text)  # Pass the input text here

if __name__ == "__main__":
    main()
