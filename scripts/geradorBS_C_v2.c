#include <stdio.h>
#include <stdlib.h>

void GerarArquivo();

void main() {
    GerarArquivo();  // para manter o mesmo aquivo, executar uma unica vez a geração do arquivo
}

void GerarArquivo() {
    FILE* arq;

    if ((arq = fopen("teste.dat", "wb")) == NULL) {
        printf("Error! opening file");
        exit(1);
    }
    int i;
    unsigned char num;
    int numint;

    for (i = 0; i < 65536; i++) {
        numint = rand();

        num = (char) (numint % 256);

        fwrite(&num, sizeof(num), 1, arq);
    }
    fclose(arq);
}
