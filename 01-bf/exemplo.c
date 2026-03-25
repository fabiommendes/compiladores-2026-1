#include<stdio.h>

void main() {
    char tape[10000];
    for (int i = 0; i < 10000; i++) {
        tape[i] = 0;
    }
    int pos = 0;

    tape[pos]++;
    tape[pos]++;
    tape[pos]++;
    tape[pos]++;
    tape[pos]++;

    tape[pos]++;
    tape[pos]++;
    tape[pos]++;
    tape[pos]++;
    tape[pos]++;

    printf("%c", tape[pos]);

    while (tape[pos] != 0) {
        // >+<-
        pos++;
        tape[pos]++;
        pos--;
        tape[pos]--;
    }

    pos++;
    printf("%c", tape[pos]);

}