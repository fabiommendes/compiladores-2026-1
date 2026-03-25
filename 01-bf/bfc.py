import sys

C_TEMPLATE = """
#include<stdio.h>

void main() {
    char tape[10000];
    for (int i = 0; i < 10000; i++) {
        tape[i] = 0;
    }
    int pos = 0;

    ...

}
"""


def main():
    file_name = sys.argv[-1]

    with open(file_name) as f:
        source = f.read()

    c_source = bf_compile(source)
    print(C_TEMPLATE.replace("...", c_source))


def bf_compile(src: str) -> str:
    lines = []

    for c in src:
        match c:
            case "+":
                lines.append("tape[pos]++;")
            case "-":
                lines.append("tape[pos]--;")
            case "<":
                lines.append("pos--;")
            case ">":
                lines.append("pos++;")
            case ".":
                lines.append("putchar(tape[pos]);")
            case ",":
                lines.append("tape[pos] = getchar();")
            case "[":
                lines.append("while (tape[pos] != 0) {")
            case "]":
                lines.append("}")

    return "\n".join(lines)

if __name__ == "__main__":
    main()