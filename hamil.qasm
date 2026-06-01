OPENQASM 3.0;
include "stdgates.inc";
qubit[16] q;
bit[7] c;

gate oracle q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, q15, q16{
    ctrl @ ctrl @ ctrl @ x q10, q1, q2, q3;
    ctrl @ ctrl @ x q10, q1, q2;
    ctrl @ x q10, q1;
    ctrl @ ctrl @ x q10, q4, q9;
    ctrl @ x q10, q4;
    ctrl @ x q10, q5;

    ctrl @ ctrl @ ctrl @ x q11, q1, q2, q3;
    ctrl @ ctrl @ x q11, q1, q2;
    ctrl @ x q11, q1;
    ctrl @ ctrl @ x q11, q4, q9;
    ctrl @ x q11, q4;
    ctrl @ x q11, q6;

    ctrl @ ctrl @ ctrl @ x q12, q1, q2, q3;
    ctrl @ ctrl @ x q12, q1, q2;
    ctrl @ x q12, q1;
    ctrl @ x q12, q5;
    ctrl @ x q12, q6;
    
    ctrl @ ctrl @ ctrl @ x q13, q1, q2, q3;
    ctrl @ ctrl @ x q13, q1, q2;
    ctrl @ x q13, q1;
    ctrl @ x q13, q6;
    ctrl @ x q13, q7;

    ctrl @ ctrl @ ctrl @ x q14, q1, q2, q3;
    ctrl @ ctrl @ x q14, q1, q2;
    ctrl @ x q14, q1;
    ctrl @ x q14, q7;
    ctrl @ x q14, q8;

    ctrl @ ctrl @ ctrl @ x q15, q1, q2, q3;
    ctrl @ ctrl @ x q15, q1, q2;
    ctrl @ x q15, q1;
    ctrl @ ctrl @ x q15, q4, q9;
    ctrl @ x q15, q4;
    ctrl @ x q15, q8;

    x q3; x q4;
    ctrl @ ctrl @ ctrl @ ctrl @ ctrl @ ctrl @ ctrl @ ctrl @ ctrl @ z
    q1, q2, q3, q4, q5, q6, q7, q8, q9, q16;
    x q3; x q4;

    // Reverse circuit
    ctrl @ x q15, q8;
    ctrl @ x q15, q4;
    ctrl @ ctrl @ x q15, q4, q9;
    ctrl @ x q15, q1;
    ctrl @ ctrl @ x q15, q1, q2;
    ctrl @ ctrl @ ctrl @ x q15, q1, q2, q3;

    ctrl @ x q14, q8;
    ctrl @ x q14, q7;
    ctrl @ x q14, q1;
    ctrl @ ctrl @ x q14, q1, q2;
    ctrl @ ctrl @ ctrl @ x q14, q1, q2, q3;

    ctrl @ x q13, q7;
    ctrl @ x q13, q6;
    ctrl @ x q13, q1;
    ctrl @ ctrl @ x q13, q1, q2;
    ctrl @ ctrl @ ctrl @ x q13, q1, q2, q3;

    ctrl @ x q12, q6;
    ctrl @ x q12, q5;
    ctrl @ x q12, q1;
    ctrl @ ctrl @ x q12, q1, q2;
    ctrl @ ctrl @ ctrl @ x q12, q1, q2, q3;

    ctrl @ x q11, q6;
    ctrl @ x q11, q4;
    ctrl @ ctrl @ x q11, q4, q9;
    ctrl @ x q11, q1;
    ctrl @ ctrl @ x q11, q1, q2;
    ctrl @ ctrl @ ctrl @ x q11, q1, q2, q3;

    ctrl @ x q10, q5;
    ctrl @ x q10, q4;
    ctrl @ ctrl @ x q10, q4, q9;
    ctrl @ x q10, q1;
    ctrl @ ctrl @ x q10, q1, q2;
    ctrl @ ctrl @ ctrl @ x q10, q1, q2, q3;
}
gate diffusion q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, q15, q16{
   h q1; h q2; h q3; h q4; h q5; h q6; h q7; h q8; h q9; h q10; h q11; h q12; h q13; h q14; h q15;
   x q1; x q2; x q3; x q4; x q5; x q6; x q7; x q8; x q9; x q10; x q11; x q12; x q13; x q14; x q15;
   ctrl @ ctrl @ ctrl @ ctrl @ ctrl @ ctrl @ ctrl @ ctrl @ ctrl @ ctrl @ ctrl @ ctrl @ ctrl @ ctrl @ ctrl @ x  q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, q15, q16;
   x q1; x q2; x q3; x q4; x q5; x q6; x q7; x q8; x q9; x q10; x q11; x q12; x q13; x q14; x q15;
   h q1; h q2; h q3; h q4; h q5; h q6; h q7; h q8; h q9; h q10; h q11; h q12; h q13; h q14; h q15;
}
x q[15];
h q[9:15];

oracle q[0], q[1],q[2],q[3],q[4], q[5],q[6],q[7],q[8], q[9],q[10],q[11],q[12], q[13], q[14], q[15];
diffusion q[0], q[1],q[2],q[3],q[4], q[5],q[6],q[7],q[8], q[9],q[10],q[11],q[12], q[13], q[14], q[15];
oracle q[0], q[1],q[2],q[3],q[4], q[5],q[6],q[7],q[8],q[9], q[10],q[11],q[12],q[13], q[14], q[15];
diffusion q[0], q[1],q[2],q[3],q[4], q[5],q[6],q[7],q[8], q[9],q[10],q[11],q[12], q[13], q[14], q[15];
oracle q[0], q[1],q[2],q[3],q[4], q[5],q[6],q[7],q[8],q[9], q[10],q[11],q[12],q[13], q[14], q[15];
diffusion q[0], q[1],q[2],q[3],q[4], q[5],q[6],q[7],q[8], q[9],q[10],q[11],q[12], q[13], q[14], q[15];
oracle q[0], q[1],q[2],q[3],q[4], q[5],q[6],q[7],q[8],q[9], q[10],q[11],q[12],q[13], q[14], q[15];
diffusion q[0], q[1],q[2],q[3],q[4], q[5],q[6],q[7],q[8], q[9],q[10],q[11],q[12], q[13], q[14], q[15];


h q[15];
x q[15];
c[0:6] = measure q[9:15];