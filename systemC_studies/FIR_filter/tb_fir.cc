#include "tb_fir.h"

void tb_fir::source() {
  // reset
  inp.write(0);
  inp_vld.write(0);
  rst.write(1);
  wait();

  rst.write(0);
  wait();

  // Open the input file
  std::ifstream infile(input_file.c_str());
  if (!infile.is_open()) {
    std::cerr << "Could not open " << input_file << " for reading\n";
    sc_stop();
    return;
  }

  sc_int<16> tmp;
  int i = 0;

  // inp_vld.write(0);

  while (i < 64) {
    infile >> tmp;
    inp_vld.write(1);
    inp.write( tmp );

    do {
      wait();
    } while (!inp_rdy.read());

    inp_vld.write(0);
    i++;
  }

  infile.close();
}

FILE* outf;
void tb_fir::sink() {
  sc_int<16> indata;
  // cout << output_file << endl;
  outf = fopen(output_file.c_str(), "wb");
  if (outf == NULL){
    cout << "Couldnt open \"" << output_file << "\" for writing\n";
    sc_stop();
    exit(0);
  }

  out_rdy.write(0);

  for (int i = 0; i < 64; i ++){
    out_rdy.write(1);
    do {
      wait();
      // cout << "output valid: " << out_vld << endl;
    } while (!out_vld.read());
    indata = out.read();
    out_rdy.write(0);

    
    fprintf(outf, "%g\n", indata.to_double());
    cout << i << " :\t" << indata.to_double() << endl;
  }

  fclose(outf);
  sc_stop();
}

  // Send stimilus to FIR
  /*
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
  }*/