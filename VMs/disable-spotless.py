def find_forward(lines, text, start=0):
    for index, line in enumerate(lines[start:]):
        if text in line:
            return index + start
    raise ValueError(f"no line matches {text!r}")

def find_reversed(lines, text):
    for index, line in reversed(list(enumerate(lines))):
        if text in line:
            return index
    raise ValueError(f"no line matches {text!r}")

def main(filename="pom.xml"):
    lines = open(filename).readlines()
    index = find_forward(lines, "spotless")
    start_index = find_reversed(lines[:index], "<plugin>")
    limit_index = find_forward(lines, "</plugin>", index) + 1
    lines[start_index:limit_index] = []
    open(filename, "w").writelines(lines)


if __name__ == "__main__":
    main()
