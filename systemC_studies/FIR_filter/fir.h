#include <systemc.h>

SC_MODULE( fir ) {
  sc_in<bool>           clk;
  sc_in<bool>           rst;
  sc_in<sc_int<16>>     inp;
  sc_out<sc_int<16>>    out;

  // Handshake signals
  sc_in<bool>           inp_vld;
  sc_out<bool>          inp_rdy;
  sc_out<bool>          out_vld;
  sc_in<bool>           out_rdy;

  void fir_main();

  SC_CTOR( fir ) {
    SC_CTHREAD(fir_main, clk.pos());
    reset_signal_is(rst, true);
  }
};