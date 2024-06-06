import random, re, json

class Obfuscator:
    def __init__(self):
        self.var_mapping = {}

    def obfuscate_var_names(self, code):
        var_pattern = re.compile(r'\b(\w+)\b')
        vars_found = set(re.findall(var_pattern, code))
        obfuscated_code = code
        for var in vars_found:
            obfuscated_var = ''.join(random.choice('0O1l') for _ in range(6))
            self.var_mapping[obfuscated_var] = var
            obfuscated_code = re.sub(r'\b' + var + r'\b', obfuscated_var, obfuscated_code)
        return obfuscated_code

    def replace_indentations(self, code):
        lines = code.split('\n')
        for i in range(len(lines)):
            indentation = len(lines[i]) - len(lines[i].lstrip())
            lines[i] = '◬' + str(indentation) + ' ' + lines[i].lstrip()
        return '\n'.join(lines)

class Deobfuscator:
    def __init__(self, var_mapping):
        self.var_mapping = var_mapping

    def deobfuscate_var_names(self, code):
        deobfuscated_code = code
        for obfuscated_var, original_var in self.var_mapping.items():
            deobfuscated_code = deobfuscated_code.replace(obfuscated_var, original_var)
        return deobfuscated_code

    def replace_indentations_back(self, code):
        lines = code.split('\n')
        for i in range(len(lines)):
            if lines[i].startswith('◬'):
                indentation = int(lines[i][1:lines[i].index(' ')])
                lines[i] = ' ' * indentation + lines[i][lines[i].index(' ') + 1:]
        return '\n'.join(lines)

def main():
    choice = input("Enter 'obf' to obfuscate or 'deobf' to deobfuscate: ")
    if choice == 'obf':
        ifile = input("Enter file name: ")
        obfuscator = Obfuscator()
        with open(ifile, 'r') as file:
            code = file.read()
        obfuscated_code = obfuscator.obfuscate_var_names(code)
        final_code = obfuscator.replace_indentations(obfuscated_code)
        with open('obfuscated.txt', 'w', encoding='utf-8') as file:
            file.write(final_code)
        with open('key.txt', 'w') as file:
            file.write(json.dumps(obfuscator.var_mapping))
        print("Variable mapping saved to 'key.txt'.")
    elif choice == 'deobf':
        with open('key.txt', 'r') as file:
            var_mapping = json.loads(file.read())
        deobfuscator = Deobfuscator(var_mapping)
        with open('obfuscated.txt', 'r', encoding='utf-8') as file:
            code = file.read()
        deobfuscated_code = deobfuscator.deobfuscate_var_names(code)
        final_code = deobfuscator.replace_indentations_back(deobfuscated_code)
        with open('deobfuscated.txt', 'w', encoding='utf-8') as file:
            file.write(final_code)
    else:
        print("Invalid choice. Please enter 'obf' or 'deobf'.")

if __name__ == "__main__":
    main()