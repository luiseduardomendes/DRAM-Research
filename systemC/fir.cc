#include "fir.h"

const sc_uint<8> coef[5] = {
  18,
  77,
  107,
  77,
  18
};

void fir::fir_main(void) {
  sc_int<16> taps[5];

  // initialize handshake
  inp_rdy.write(0);
  out_vld.write(0);
  out.write(0);
  wait();

  while (true) {
    sc_int<16> in_val;
    sc_int<16> out_val;

    inp_rdy.write(1);
    do {
      wait();
    } while(!inp_vld.read());
    in_val = inp.read();
    inp_rdy.write(0);

    for (int i = 5-1; i > 0; i --) {
      taps[i] = taps[i-1];
    }
    taps[0] = in_val;

    out_val = 0;
    for (int i = 0; i < 5; i ++) {
      out_val += coef[i] * taps[i];
    }

    out_vld.write(1);
    out.write(out_val);
    do{
      wait();
    } while(!out_rdy.read());
    out_vld.write(0);
  }
}