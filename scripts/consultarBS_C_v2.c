#include <stdio.h>
#include <stdlib.h>

void ConsultarArquivo();

void main() {
    ConsultarArquivo();
}

void ConsultarArquivo() {
    FILE* arq;
    int i, j;
    unsigned char num;
    int numint;
    long offset = 0;
    if ((arq = fopen("teste.dat", "rb")) == NULL) {
        printf("Error! opening file");
        // Program exits if the file pointer returns NULL.
        exit(1);
    }

    for (i = 0; i < 65536; i++) {
        fread(&num, sizeof(num), 1, arq);
        printf(">>>Endereço: %d >>> conteúdo: %d\n", i, num);
    }

    fclose(arq);
}
