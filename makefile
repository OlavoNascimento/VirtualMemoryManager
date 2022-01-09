# Nome do executável
EXECUTABLE = vmm.py
BIN_DIR = bin
SCRIPTS_DIR = scripts
GENERATOR_BIN = $(BIN_DIR)/generate
TESTER_BIN = $(BIN_DIR)/test

ADDRESSES_FILE = addresses.txt

# Flags de compilação
CFLAGS = -fstack-protector-all -std=c99 -O2

all: executar

executar: gerar
	python3 ./$(EXECUTABLE) $(ADDRESSES_FILE)

gerar: compilar_gerador
	@echo "Gerando arquivo teste.dat..."
	@rm -f teste.dat
	./$(GENERATOR_BIN)

compilar_gerador: $(SCRIPTS_DIR)/geradorBS_C_v2.c
# $^ representa a dependência atual (geradorBS_C_v2.c)
	@echo "Compilando $^..."
	@mkdir -p $(BIN_DIR)
	gcc $(CFLAGS) -o $(GENERATOR_BIN) $^

consultar: compilar_consulta
	@echo "Consultando arquivo teste.dat..."
	./$(TESTER_BIN)

compilar_consulta: $(SCRIPTS_DIR)/consultarBS_C_v2.c
# $^ representa a dependência atual (consultarBS_C_v2.c)
	@echo "Compilando $^..."
	@mkdir -p $(BIN_DIR)
	gcc $(CFLAGS) -o $(TESTER_BIN) $^

clean:
	rm -f $(GENERATOR_BIN) $(TESTER_BIN) output.txt *.o

