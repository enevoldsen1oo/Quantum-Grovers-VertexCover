OPENQASM 3.0;
include "stdgates.inc";

// Hamiltonian Cycle via Grover's Algorithm
//
// Graph: 4 nodes (n1-n4), 5 undirected edges
//   e1: n1-n2   e2: n2-n3   e3: n1-n3   e4: n3-n4   e5: n4-n1
//
// Qubits:
//   q[0]-q[4]  : edge variables (e1-e5), the search register
//   q[5]-q[8]  : node-degree ancillas (n1-n4), 1 iff node has degree == 2
//   q[9]       : reusable ancilla for parity computation
//   q[10]      : reusable ancilla for majority computation
//   q[11]      : phase-kickback qubit (prepared in |->)
//
// Oracle strategy: a subset of edges is a Hamiltonian cycle on 4 nodes
// iff every node has exactly degree 2.
//
//   Node incidences:
//     n1 -> e1(q0), e3(q2), e5(q4)   : exactly 2 of 3
//     n2 -> e1(q0), e2(q1)           : both must be 1
//     n3 -> e2(q1), e3(q2), e4(q3)   : exactly 2 of 3
//     n4 -> e4(q3), e5(q4)           : both must be 1
//
// "Exactly 2 of 3" is computed as: majority(a,b,c) AND NOT parity(a,b,c)
//   parity  = a XOR b XOR c           (via 3 CX gates)
//   majority = ab XOR ac XOR bc       (via 3 CCX gates)

qubit[12] q;
bit[5] c;
gate oracle e1, e2, e3, e4, e5, a_n1, a_n2, a_n3, a_n4, par, maj, ph {

    // ===== Compute node constraints =====

    // n2 (edges e1, e2): degree 2 requires both selected
    ccx e1, e2, a_n2;

    // n4 (edges e4, e5): degree 2 requires both selected
    ccx e4, e5, a_n4;

    // n1 (edges e1, e3, e5): exactly 2 of 3
    //   compute parity into par
    cx e1, par;
    cx e3, par;
    cx e5, par;
    //   compute majority into maj
    ccx e1, e3, maj;
    ccx e1, e5, maj;
    ccx e3, e5, maj;
    //   a_n1 = maj AND NOT(par)
    x par;
    ccx maj, par, a_n1;
    x par;
    //   uncompute maj
    ccx e3, e5, maj;
    ccx e1, e5, maj;
    ccx e1, e3, maj;
    //   uncompute par
    cx e5, par;
    cx e3, par;
    cx e1, par;

    // n3 (edges e2, e3, e4): exactly 2 of 3
    cx e2, par;
    cx e3, par;
    cx e4, par;
    ccx e2, e3, maj;
    ccx e2, e4, maj;
    ccx e3, e4, maj;
    x par;
    ccx maj, par, a_n3;
    x par;
    ccx e3, e4, maj;
    ccx e2, e4, maj;
    ccx e2, e3, maj;
    cx e4, par;
    cx e3, par;
    cx e2, par;

    // ===== Phase flip if ALL constraints satisfied =====
    ctrl @ ctrl @ ctrl @ ctrl @ x a_n1, a_n2, a_n3, a_n4, ph;
    // ===== Uncompute node constraints (reverse order) =====

    // un-n3
    cx e2, par;
    cx e3, par;
    cx e4, par;
    ccx e2, e3, maj;
    ccx e2, e4, maj;
    ccx e3, e4, maj;
    x par;
    ccx maj, par, a_n3;
    x par;
    ccx e3, e4, maj;
    ccx e2, e4, maj;
    ccx e2, e3, maj;
    cx e4, par;
    cx e3, par;
    cx e2, par;

    // un-n1
    cx e1, par;
    cx e3, par;
    cx e5, par;
    ccx e1, e3, maj;
    ccx e1, e5, maj;
    ccx e3, e5, maj;
    x par;
    ccx maj, par, a_n1;
    x par;
    ccx e3, e5, maj;
    ccx e1, e5, maj;
    ccx e1, e3, maj;
    cx e5, par;
    cx e3, par;
    cx e1, par;

    // un-n4
    ccx e4, e5, a_n4;

    // un-n2
    ccx e1, e2, a_n2;
}
gate diffusion q0, q1, q2, q3, q4 {
    h q0; h q1; h q2; h q3; h q4;
    x q0; x q1; x q2; x q3; x q4;
    ctrl @ ctrl @ ctrl @ ctrl @ z q0, q1, q2, q3, q4;
    x q0; x q1; x q2; x q3; x q4;
    h q0; h q1; h q2; h q3; h q4;
}

// Prepare phase-kickback qubit in |->
x q[11];
h q[11];

// Uniform superposition over all 2^5 edge subsets
h q[0]; h q[1]; h q[2]; h q[3]; h q[4];

// Grover iterations: optimal k = 4 for N=32, M=1  (success prob ~99.9%)
oracle q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11];
diffusion q[0], q[1], q[2], q[3], q[4];
oracle q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11];
diffusion q[0], q[1], q[2], q[3], q[4];
oracle q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11];
diffusion q[0], q[1], q[2], q[3], q[4];


// Restore phase qubit
h q[11];
x q[11];

// Measure edge qubits -> expect |11011> (e1,e2,e4,e5 = Hamiltonian cycle)
c[0] = measure q[0];
c[1] = measure q[1];
c[2] = measure q[2];
c[3] = measure q[3];
c[4] = measure q[4];