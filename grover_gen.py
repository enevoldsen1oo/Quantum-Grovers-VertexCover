import argparse
from math import sqrt, pi

def gen_grov(num_qub: int, target_bit: str):
    # Header text for QASM file
    file_str = f'OPENQASM 3.0;\ninclude "stdgates.inc";\n'
    
    # Init qubits
    qubit_str = f'qubit[{num_qub}] q;\nbit[{num_qub-1}] c;\n'

    # Construct oracle function from target_bit
    oracle_init_str = f'gate oracle {", ".join(f"q{i}" for i in range(num_qub))}' + '{\n'
    ctrl_bits = []
    other_bits = []
    for i, bit in enumerate(target_bit):
        if bit == "1":
            ctrl_bits.append(i)
        else:
            other_bits.append(i)
    oracle_ctrl_bits = f'  {" ".join("ctrl @" for _ in ctrl_bits)} x{"".join(f' q{i},' for i in ctrl_bits)}'
    oracle_other_bits = f'{"".join(oracle_ctrl_bits + f'q{i};\n' for i in other_bits)}'
    oracle_kick_back = f'  {" ".join('ctrl @' for _ in range(num_qub-1))} z {",".join(f'q{i}' for i in range(num_qub))};\n'

    oracle_str = oracle_init_str + oracle_other_bits + oracle_kick_back + oracle_other_bits + '}\n'

    # Construct diffusion operator
    diff_init_str = f'gate diffusion {", ".join(f"q{i}" for i in range(num_qub))}' + '{\n'
    diff_h_str = f'  {"".join(f' h q{i};' for i in range(num_qub))}\n'
    diff_x_str = f'  {"".join(f' x q{i};' for i in range(num_qub))}\n'
    diff_ctrl_str = f'  {"".join(f' ctrl @' for i in range(num_qub-1))} x {",".join(f' q{i}' for i in range(num_qub))};\n'
    diffusion_str = diff_init_str + diff_h_str + diff_x_str + diff_ctrl_str + diff_x_str + diff_h_str + '}\n'
    
    # Init circuit
    init_ancilla_str = f'x q[{num_qub-1}];\nh q[0:{num_qub-1}];\n'
    reset_ancilla_str = f'h q[{num_qub-1}];\nx q[{num_qub-1}];\n'

    # Oracle and Diffusion gates
    use_ora_str = f'oracle {",".join(f'q[{i}]' for i in range(num_qub))};\n'
    use_dif_str = f'diffusion {",".join(f'q[{i}]' for i in range(num_qub))};\n'

    use_str = use_ora_str + use_dif_str

    # Measure qubits except helper qubit
    measure_str = f'c[0:{num_qub-2}] = measure q[0:{num_qub-2}];'

    # Combine beginning of file
    file_str += qubit_str + oracle_str + diffusion_str + init_ancilla_str
    
    # Insert sqrt(n) number of diffusion operators
    iterations = round(pi / 4 * sqrt(2 ** (num_qub - 1)))
    for _ in range(iterations):
        file_str += use_str
    file_str += reset_ancilla_str + measure_str

    # Write to file
    with open("grov_gen.qasm", "w") as f:
        f.write(file_str)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="My script")
    
    parser.add_argument("--num_qub", type=int, default=3, help="How many qubits")
    parser.add_argument("--target", type=str, help="Target Bit string")

    args = parser.parse_args()
    assert args.num_qub == len(args.target)
    gen_grov(args.num_qub + 1, args.target)