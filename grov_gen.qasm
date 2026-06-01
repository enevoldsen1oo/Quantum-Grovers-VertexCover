OPENQASM 3.0;
include "stdgates.inc";
qubit[5] q;
bit[4] c;
gate oracle q0, q1, q2, q3, q4{
  ctrl @ x q2,q0;
  ctrl @ x q2,q1;
  ctrl @ x q2,q3;
  ctrl @ ctrl @ ctrl @ ctrl @ z q0,q1,q2,q3,q4;
  ctrl @ x q2,q0;
  ctrl @ x q2,q1;
  ctrl @ x q2,q3;
}
gate diffusion q0, q1, q2, q3, q4{
   h q0; h q1; h q2; h q3; h q4;
   x q0; x q1; x q2; x q3; x q4;
   ctrl @ ctrl @ ctrl @ ctrl @ x  q0, q1, q2, q3, q4;
   x q0; x q1; x q2; x q3; x q4;
   h q0; h q1; h q2; h q3; h q4;
}
x q[4];
h q[0:4];
oracle q[0],q[1],q[2],q[3],q[4];
diffusion q[0],q[1],q[2],q[3],q[4];
oracle q[0],q[1],q[2],q[3],q[4];
diffusion q[0],q[1],q[2],q[3],q[4];
oracle q[0],q[1],q[2],q[3],q[4];
diffusion q[0],q[1],q[2],q[3],q[4];
h q[4];
x q[4];
c[0:3] = measure q[0:3];