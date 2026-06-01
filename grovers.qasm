OPENQASM 3.0;
include "stdgates.inc";

qubit[4] q;
bit[4] c;

gate oracle q0, q1, q2, q3 {
    ccx q0, q2, q1;
    ctrl @ ctrl @ ctrl @ x q0, q1, q2, q3;
    ccx q0, q2, q1;
}

gate diffusion q0, q1, q2, q3 {
    h q0; h q1; h q2;
    x q0; x q1; x q2;
    ctrl @ ctrl @ ctrl @ x q0, q1, q2, q3;
    x q0; x q1; x q2;
    h q0; h q1; h q2;
}

x q[3];
h q[0:3];

oracle q[0], q[1], q[2], q[3];
diffusion q[0], q[1], q[2], q[3];

oracle q[0], q[1], q[2], q[3];
diffusion q[0], q[1], q[2], q[3];

h q[3];
x q[3];

c[0:3] = measure q[0:3];
