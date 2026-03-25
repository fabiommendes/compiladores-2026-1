import sys


def main():
    file_name = sys.argv[-1]

    with open(file_name) as f:
        source = f.read()

    interpret(source)


def interpret(src: str):
    tape = [0] * 10
    pos = 0
    ip = 0
    ip_stack = []
    i = 0

    while ip < len(src):
        instr = src[ip]
        if instr not in "+-[]><.":
            ip += 1
            continue

        # # i += 1
        # # if i > 20:
        # #     break
        # print(f"{instr}: pos = {pos}, tape = {tape}, ip = {ip}")

        match instr:
            case "+":
                tape[pos] = (tape[pos] + 1) % 256
            case "-":
                tape[pos] = (tape[pos] - 1) % 256
            case "<":
                pos -= 1
            case ">":
                pos += 1
            case ".":
                print(chr(tape[pos]), end="", flush=True)
            case ",":
                raise NotImplementedError
            case "[":
                if tape[pos] == 0:
                    ip = find_loop_end(src, ip) + 1
                    continue
                else:
                    ip_stack.append(ip)
            case "]":
                ip = ip_stack.pop()
                continue

        ip += 1


def find_loop_end(src, ip):
    assert src[ip] == "["

    ip += 1
    n_open = 1

    while ip < len(src):
        match src[ip]:
            case "[":
                n_open += 1
            case "]":
                n_open -= 1
                if n_open == 0:
                    return ip
        ip += 1

    raise ValueError("Colchetes nao pareados")


if __name__ == "__main__":
    main()
