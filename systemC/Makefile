# Variáveis de compilador e flags
CXX = g++
SYSTEMC_HOME = /home/luismendes/systemc-2.3.3
CXXFLAGS = -I$(SYSTEMC_HOME)/include -L$(SYSTEMC_HOME)/lib-linux64 -lsystemc -lm -Wno-deprecated

# Diretórios
BINDIR = bin

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

# Limpeza dos arquivos objeto e executável
clean:
	rm -f $(OBJS)

.PHONY: all clean
