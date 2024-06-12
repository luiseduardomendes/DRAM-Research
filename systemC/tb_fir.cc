#include "tb_fir.h"

void tb_fir::source() {
  // reset
  inp.write(0);
  inp_vld.write(0);
  rst.write(1);
  wait();

  rst.write(0);
  wait();

  sc_int<16> tmp;

  // Send stimilus to FIR
  for(int i = 0; i < 64; i ++){
    if (i > 23 && i < 29){
      tmp = 256;
    } else {
      tmp = 0;
    }
    inp_vld.write(1);
    inp.write( tmp );
    
    do {
      wait();
    } while (!inp_rdy.read());

    inp_vld.write(0);
  }
}

FILE* outf;
void tb_fir::sink() {
  sc_int<16> indata;

  char output_file[256];
  sprintf(output_file, "./output.dat");
  outf = fopen(output_file, "wb");
  if (outf == NULL){
    printf("Couldnt open output.dat for writing\n");
    exit(0);
  }

  out_rdy.write(0);

  for (int i = 0; i < 64; i ++){
    out_rdy.write(1);
    do {
      wait();
    } while (!out_vld.read());
    indata = out.read();
    out_rdy.write(0);

    
    fprintf(outf, "%g\n", indata.to_double());
    cout << i << " :\t" << indata.to_double() << endl;
  }

  fclose(outf);
  sc_stop();
}