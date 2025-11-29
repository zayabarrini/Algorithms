Let's create an IA Agent 
It Should receive an Algorithm and folder path then

- generate .md file with the Algorithm name, generic prompts, folder structure contents
.md Content: 
- execute a list of prompts
E,g: Prompt 1 and 2
- Prompt execution, File generation + Analysis
Prompt 1 should generate project files
Prompt 2 should generate tests

Prompt 1:

```
Explanation, Implementation (python) and analysis
Time Complexity (The "How Fast")
- Best Case (Ω - Omega) - Average Case (Θ - Theta) - Worst Case (O - Omicron) - In Practice 
Space Complexity (The "How Much Memory")
- Auxiliary Space - Total Space - Common Pitfall 
Correctness & Assumptions
- Input Constraints - Preconditions - Postconditions - Edge Cases 
Practical Considerations
- Constant Factors - Cache Performance - Real-world Data Patterns
```

Prompt 2:

```
Number of essentials tests
List of Tests:
Inputs, Outputs, Time to finish, space used
List of problematic cases for each Algorithm
List of difficult problems that can be solved with the Algorithm
```

Current Project:
/home/zaya/Downloads/Zayas/Zayas-Algorithms/01_Digital_Circuits/FPGA_Implementations/LUT.md
pwd: /home/zaya/Downloads/Zayas/Zayas-Algorithms

5 Algorithms for each = 120 Algorithms

```
SystemVerilog/AI_Accelerators/
SystemVerilog/Security_Modules/
SystemVerilog/Quantum_Interfaces/
TCL_Scripts/EDA_Automation/
TCL_Scripts/Verification_Flows/
TCL_Scripts/Physical_Design/
FPGA_Implementations/
MultiScale_Framework/Quantum_Scale/
MultiScale_Framework/Atomic_Scale/
MultiScale_Framework/Mesoscale/
MultiScale_Framework/System_Scale/
Nuclear_Applications/
Materials_Science/
Optimization/
Computer_Vision/
NLP/
Reinforcement_Learning/
Pathfinding/
Optimization/
Game_Theory/
Quantum_Classical_Hybrid/
Sensor_Networks/
Edge_Computing/
Outdoor_Applications/
```

tree
```
.
├── 01_Digital_Circuits
│   ├── FPGA_Implementations
│   │   ├── LUT.md
│   │   └── README.md
│   ├── README.md
│   ├── SystemVerilog
│   │   ├── AI_Accelerators
│   │   ├── Quantum_Interfaces
│   │   ├── README.md
│   │   └── Security_Modules
│   └── TCL_Scripts
│       ├── EDA_Automation
│       ├── Physical_Design
│       ├── README.md
│       └── Verification_Flows
├── 02_Physics_Simulations
│   ├── Materials_Science
│   │   └── README.md
│   ├── MultiScale_Framework
│   │   ├── Atomic_Scale
│   │   ├── Mesoscale
│   │   ├── Quantum_Scale
│   │   ├── README.md
│   │   └── System_Scale
│   ├── Nuclear_Applications
│   │   └── README.md
│   └── README.md
├── 03_ML_Algorithms
│   ├── Computer_Vision
│   │   ├── Convolutional-Neural-Networks.md
│   │   └── README.md
│   ├── IDE-star.md
│   ├── IDE-star.py
│   ├── NLP
│   │   └── README.md
│   ├── Optimization
│   │   └── README.md
│   ├── README.md
│   └── Reinforcement_Learning
│       └── README.md
├── 04_Advanced_Problems
│   ├── Game_Theory
│   │   └── README.md
│   ├── Optimization
│   │   └── README.md
│   ├── Pathfinding
│   │   └── README.md
│   ├── Quantum_Classical_Hybrid
│   │   └── README.md
│   └── README.md
├── 05_Field_Integration
│   ├── Edge_Computing
│   │   └── README.md
│   ├── Outdoor_Applications
│   │   └── README.md
│   ├── README.md
│   └── Sensor_Networks
│       └── README.md
```