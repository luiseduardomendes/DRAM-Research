#include <systemc.h>
#include "fir.h"
#include "tb_fir.h"

SC_MODULE( SYSTEM ) {
  // Module declarations
  tb_fir    *tb_fir0;
  fir       *fir0;
  
  // Local Signal declarations
  sc_signal<sc_int<16>> input_signal;
  sc_signal<sc_int<16>> output_signal;
  sc_signal<bool> reset_signal;

  sc_signal<bool>       inp_vld;
  sc_signal<bool>       inp_rdy;
  sc_signal<bool>       out_vld;
  sc_signal<bool>       out_rdy;

  sc_clock  clock_signal;

  SC_CTOR ( SYSTEM ) : clock_signal ("clk_sig", 10, SC_NS) // 10 nanoseconds period 
  {
    tb_fir0 = new tb_fir("tb_fir0");
    tb_fir0->clk( clock_signal );
    tb_fir0->rst( reset_signal );
    tb_fir0->inp( input_signal );
    tb_fir0->out( output_signal );

    tb_fir0->inp_vld(inp_vld);
    tb_fir0->inp_rdy(inp_rdy);
    tb_fir0->out_vld(out_vld);
    tb_fir0->out_rdy(out_rdy);

    fir0 = new fir("fir0");
    fir0->clk( clock_signal );
    fir0->rst( reset_signal );
    fir0->inp( input_signal );
    fir0->out( output_signal );
    
    fir0->inp_vld(inp_vld);
    fir0->inp_rdy(inp_rdy);
    fir0->out_vld(out_vld);
    fir0->out_rdy(out_rdy);

  }

  // Destructor
  ~SYSTEM() {
    delete tb_fir0;
    delete fir0;
  }
};

SYSTEM *top = NULL;

int sc_main(int argc, char* argv[]) {
  if (argc < 3) {
    std::cerr << "Usage: " << argv[0] << " <input_file> <output_file>\n";
    return 1;
  }
  
  top = new SYSTEM("top");
  top->tb_fir0->set_input_file(argv[1]);
  top->tb_fir0->set_output_file(argv[2]);

  sc_start();

  return 0;
}