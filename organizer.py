class Organizer:
    def __init__(self, filename : str):
        self.filename = filename
        self.open_file = open(filename)
        self.includes = []
        self.types = ["int", "float", "double", "char", "void", "bool", "string"]
        self.main_file = open("main.cpp", "w")

    def parse_includes(self, line : str):
        self.includes.append(line.split()[1])
        self.types.append(line.split()[1][1:-2])

    def parse_functions(self, line : str):
        while True:
            line = self.open_file.readline()
            if not line:
                break
            if line.startswith("}"):
                break

    def parse_classes(self, class_dict : dict) -> None:
        
        class_name, methods, variables, method_implementation = class_dict['class_name'], class_dict['methods'], class_dict['variables'], class_dict['method_implementation']

        #create .hpp and .cpp files
        header_file = open(f"{class_name}.hpp", "w")
        cpp_file = open(f"{class_name}.cpp", "w")

        for include in self.includes:
            header_file.write(f"#include {include}\n")
            cpp_file.write(f"#include {include}\n")

        #write includes
        header_file.write(f"#ifndef {class_name.upper()}_HPP\n")
        header_file.write(f"#define {class_name.upper()}_HPP\n")

        #write class definition
        header_file.write(f"class {class_name} {{ \n")

        for variable in variables:
            header_file.write(f"\t{variable}\n")

        header_file.write("public:\n")
        for method in methods:
            header_file.write(f"\t{method};\n")

        for method in method_implementation:
            
            cpp_file.write(f"{method} {{\n")
            for line in method_implementation[method]:
                cpp_file.write(line)
            #cpp_file.write("}\n")

        header_file.write("};\n")
        header_file.write(f"#endif {class_name.upper()}_HPP\n")

        header_file.close()
        cpp_file.close()

    def parse_class(self, line : str) -> dict:
        class_lines = []
        class_lines.append(line)

        while True:
            line = self.open_file.readline()
            class_lines.append(line)
            if line.strip() == '};':
                break

        class_name = None
        methods = []
        variables = []
        method_implementation = dict()

        for ind in range(len(class_lines)):
            line = class_lines[ind]
            stripped_line = line.strip()

            if stripped_line.startswith('class '):
                class_name = stripped_line.split()[1]

            elif any(x in stripped_line for x in self.types) and ';' in stripped_line:
                variables.append(stripped_line)

            elif any(x in stripped_line for x in self.types) and '(' in stripped_line and ')' in stripped_line:
                if stripped_line.endswith('{'):
                    stripped_line = stripped_line[:-1]
                methods.append(stripped_line)

                #constructor
                if stripped_line.endswith("{}"):
                    method_implementation[stripped_line] = []
                    continue

                method_definition = []
                while True:
                    ind += 1
                    if ind >= len(class_lines):
                        break
                    line = class_lines[ind]
                    method_definition.append(line)
                    if line.strip() == '}' or line.strip() == "{}":
                        break

                #print(f"adding method {stripped_line} to method_implementation for {method_definition}")

                method_implementation[stripped_line] = method_definition

        return {
            'class_name': class_name,
            'methods': methods,
            'variables': variables,
            'method_implementation': method_implementation
        }
    

    def log_dict(self, d : dict) -> None:
        for key in d:
            print(key, d[key])



    def process_line(self, line : str):
        if line.startswith("//"):
            pass

        if line == "\n":
            self.main_file.write(line)

        elif line.startswith("#include"):
            self.parse_includes(line)
            self.main_file.write(line)

        elif any(x in line for x in self.types) and ")" in line and "(" in line:
            #self.parse_functions(line)
            self.main_file.write(line)
        
        elif line.startswith("class"):
            #self.parse_classes(line)
            parsed_class = self.parse_class(line)
            self.parse_classes(parsed_class)
            #self.log_dict(parsed_class)

        else:
            self.main_file.write(line)
            #raise Exception(f"Unknown line type {line}")

    def process_file(self):
        while True:
            line = self.open_file.readline()
            if not line:
                break
            self.process_line(line)

        self.close_file()

    def close_file(self):
        self.open_file.close()
        self.main_file.close()


if __name__ == "__main__":
    organizer = Organizer("test1.cpp")
    organizer.process_file()