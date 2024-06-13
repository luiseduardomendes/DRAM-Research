# Variáveis de compilador e flags
CXX = g++
SYSTEMC_HOME = /home/luismendes/systemc-2.3.3
CXXFLAGS = -I$(SYSTEMC_HOME)/include -L$(SYSTEMC_HOME)/lib-linux64 -lsystemc -lm -Wno-deprecated

# Diretórios
BINDIR = bin
GOLDEN_DIR = golden
RESULT_DIR = result

# Arquivos fonte e objeto
SRCS = main.cc fir.cc tb_fir.cc
OBJS = $(SRCS:%.cc=$(BINDIR)/%.o)
EXEC = $(BINDIR)/simulation

# Regras principais
all: $(BINDIR) $(EXEC)

$(BINDIR):
	mkdir -p $(BINDIR)

$(EXEC): $(OBJS)
	$(CXX) $(OBJS) -o $(EXEC) $(CXXFLAGS)

$(BINDIR)/%.o: %.cc
	$(CXX) -c $(CXXFLAGS) $< -o $@

# Regra para executar a simulação
run: $(EXEC)
	./$(EXEC) $(INPUT_FILE) $(RESULT_DIR)/$(OUTPUT_FILE)

# Regra para comparar os resultados com os esperados
compare: run
	@if diff -q $(RESULT_DIR)/$(OUTPUT_FILE) $(GOLDEN_DIR)/$(OUTPUT_FILE); then \
		echo "Outputs match"; \
	else \
		echo "Outputs do not match"; \
	fi

# Limpeza dos arquivos objeto e executável
clean:
	rm -f $(OBJS) $(EXEC) $(OUTPUT_FILE)
	rm -rf $(BINDIR)

.PHONY: all clean run compare
