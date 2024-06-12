#include <systemc.h>

SC_MODULE (tb_fir) {
  sc_in<bool>           clk;
  sc_out<bool>          rst;
  sc_out<sc_int<16>>    inp;
  sc_in<sc_int<16>>     out;

  // Handshake pins
  sc_out<bool>          inp_vld;
  sc_in<bool>           inp_rdy;
  sc_in<bool>           out_vld;
  sc_out<bool>          out_rdy;

  void source();
  void sink();

  SC_CTOR ( tb_fir ) {
    SC_CTHREAD( source, clk.pos() );
    SC_CTHREAD( sink, clk.pos() );
  }
};
