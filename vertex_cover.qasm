OPENQASM 3.0;
include "stdgates.inc";

// -- Vertex Cover --
// The following is a circuit that will find the solution to a graph.
// The graph is G = (V, E)
// V = {v1, v2, v3}
// E = {e1, e2, e3}
// e1: v2 - v3
// e2: v1 - v3
// e3: v1 - v2
// Since the graph is bidirectional, the edge e1: v2 - v3 implies that there is an edge which can
// go both from v2 -> v3 and also v3 -> v2.

// Additionally, in the vertex cover problem, a value N is provided, which is the number
// of nodes to check for in the vertex cover.
// So if N = 1, then 1 node should have an edge to all other nodes in the graph.
// If N = 2, then the combined edges of those to nodes should hit all nodes in the graph.
// etc.


// The following circuit will find the solution to the graph G as defined above and N = 2.

// The qubits are ordered as follows
// q0 = ancilla.
// q1 - q3 = Counter qubits
// q4 - q6 = Vertex qubits
// q7 - q9 = Edge qubits
// q10 = Solution qubit (phase kickback qubit).

qubit[11] q;
bit[3] c;
gate oracle aux, c1, c2, c3, v1, v2, v3, e1, e2, e3, s {

    // Counter pattern for v1
    cx v1, aux;
    ctrl @ ctrl @ ctrl @ x aux, c1, c2, c3;
    ccx aux, c1, c2;
    cx aux, c1;
    cx v1, aux;
    cx c3, aux;
    cx aux, c1;
    ccx aux, c1, c2;
    ctrl @ ctrl @ ctrl @ x aux, c1, c2, c3;
    reset aux;    

    // Counter pattern for v2
    cx v2, aux;
    ctrl @ ctrl @ ctrl @ x aux, c1, c2, c3;
    ccx aux, c1, c2;
    cx aux, c1;
    cx v2, aux;
    cx c3, aux;
    cx aux, c1;
    ccx aux, c1, c2;
    ctrl @ ctrl @ ctrl @ x aux, c1, c2, c3;
    reset aux;   

    // Counter pattern for v3
    cx v3, aux;
    ctrl @ ctrl @ ctrl @ x aux, c1, c2, c3;
    ccx aux, c1, c2;
    cx aux, c1;
    cx v3, aux;
    cx c3, aux;
    cx aux, c1;
    ccx aux, c1, c2;
    ctrl @ ctrl @ ctrl @ x aux, c1, c2, c3;
    reset aux;  

    // Affected vertexes from e1
    x v2; x v3;
    ccx v2, v3, e1;
    x e1;
    x v2; x v3;

    // Affected vertexes from e2
    x v1; x v3;
    ccx v1, v3, e2;
    x e2;
    x v1; x v3;

    // Affected vertexes from e3
    x v1; x v2;
    ccx v1, v2, e3;
    x e3;
    x v1; x v2;
    
    // Phase Kickback on s, which is |-> state.
    x c1;
    ctrl @ ctrl @ ctrl @ ctrl @ ctrl @ x c1, c2, e1, e2, e3, s;
    x c1;

    // Reverse circuit to reset oracle.
    x v1; x v2;
    x e3;
    ccx v1, v2, e3;
    x v1; x v2;

    x v1; x v3;
    x e2;
    ccx v1, v3, e2;
    x v1; x v3;

    x v2; x v3;
    x e1;
    ccx v2, v3, e1;
    x v2; x v3;

    reset aux;
    ctrl @ ctrl @ ctrl @ x aux, c1, c2, c3;
    ccx aux, c1, c2;
    cx aux, c1;
    cx c3, aux;
    cx v3, aux;
    cx aux, c1;
    ccx aux, c1, c2;
    ctrl @ ctrl @ ctrl @ x aux, c1, c2, c3;
    cx v3, aux;

    reset aux;
    ctrl @ ctrl @ ctrl @ x aux, c1, c2, c3;
    ccx aux, c1, c2;
    cx aux, c1;
    cx c3, aux;
    cx v2, aux;
    cx aux, c1;
    ccx aux, c1, c2;
    ctrl @ ctrl @ ctrl @ x aux, c1, c2, c3;
    cx v2, aux;

    reset aux;
    ctrl @ ctrl @ ctrl @ x aux, c1, c2, c3;
    ccx aux, c1, c2;
    cx aux, c1;
    cx c3, aux;
    cx v1, aux;
    cx aux, c1;
    ccx aux, c1, c2;
    ctrl @ ctrl @ ctrl @ x aux, c1, c2, c3;
    cx v1, aux;

}

gate diffusion q0, q1, q2 {
    h q0; h q1; h q2;
    x q0; x q1; x q2;
    ctrl @ ctrl @ z q0, q1, q2;
    x q0; x q1; x q2;
    h q0; h q1; h q2;
}

// Prepare phase-kickback qubit in |->
x q[10];
h q[10];

// Uniform superposition over the 3 vertexes
h q[4]; h q[5]; h q[6];

// Grover iterations: optimal k = 4 for N=32, M=1  (success prob ~99.9%)
oracle q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10];
diffusion q[4], q[5], q[6];
oracle q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10];
diffusion q[0], q[1], q[2];
oracle q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10];
diffusion q[0], q[1], q[2];


// Restore phase qubit
h q[10];
x q[10];

// Measure edge qubits -> expect |11011> (e1,e2,e4,e5 = Hamiltonian cycle)
c[0] = measure q[4];
c[1] = measure q[5];
c[2] = measure q[6];