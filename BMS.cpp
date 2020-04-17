/* BMS Raster Generator
    I. Ampuero, 01-2020
*/
#include <pranasCore/BMSPotential.h>
#include <cstdio>
#include <stdlib.h>
#include <iostream>
#include <fstream>



using namespace pranas;

int main(int argc, char *argv[]){
    int N = atoi(argv[1]); //Number of neurons
    int  transient=1000;//Transient a time in bin units;
    int  T =100000;//Simulation time in bin units;
    double ew = 0.2, iw = -0.2;
    double leak = 0.6, sigma = 0.2,unit_threshold=1;
    //double ew = 0, iw = 0, leak = 0.6, sigma = 0.2,unit_threshold=1;
    double Ie=0.4; //Constant current to control the level of spontaneous activity
    int M=10000;    //atoi(argv[1]);
    //printf("A=%lg\tM=%d\n",A,M);   exit(0);
    double epsilon=1E-3;
    int tau_gamma=0;
    
    BMSPotential bms; bms.reset(N, leak, sigma);
    for (int i=0;i<N;i++) {
        bms.setUnitCurrent(i,Ie);
    }
    
    //Set w_i,i+1 = Exitatory || w_i,i+2 Inhibitory
    for (int i=0;i<N;i++){
        for (int j=0; j<N;j++){
            if(abs(i-j)==1) bms.setWeight(i,j,ew);
            if(abs(i-j)==2) bms.setWeight(i,j,iw);
        }
    }

    std::ifstream wfile;
    float value;
    wfile.open(argv[2]);
    for (int i=0;i<N;i++){
        for (int j=0; j<N;j++){
            wfile >> value;
            bms.setWeight(i,j,value);
        }
    }
    wfile.close();   


    char chaine_plot_spont[1000];

    RasterBlock *raster_sp = NULL;
    sprintf(chaine_plot_spont,"Rasters/N%dew%lgiw%lg.txt",N,ew,iw);
    raster_sp = bms.getRasterBlock(transient,T);
    raster_sp->save(chaine_plot_spont,"unit-by-line");

  return EXIT_SUCCESS;
}

