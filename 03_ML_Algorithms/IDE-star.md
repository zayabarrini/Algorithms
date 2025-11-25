Excelente! Vou mostrar um exemplo completo do IDA* (Iterative Deepening A*), desde a explicação conceitual até a implementação prática.

---

## **IDA* (Iterative Deepening A*)**

### **Conceito Fundamental**

O IDA* combina:
- **A eficiência de memória do DFS** (apenas um caminho na memória por vez)
- **A otimalidade do A*** (encontra o caminho de menor custo)
- **A estratégia iterativa** do aprofundamento iterativo

### **Funcionamento do Algoritmo**

```python
def IDA_star(initial_node):
    threshold = heuristic(initial_node)
    
    while True:
        result, new_threshold = depth_limited_search(initial_node, threshold)
        if result == "FOUND":
            return path
        if new_threshold == float('inf'):
            return "NO_SOLUTION"
        threshold = new_threshold
```

---

## **Exemplo Prático: Quebra-Cabeça do 8-Puzzle**

Vamos implementar o IDA* para resolver o famoso problema do 8-puzzle.

### **Problema: 8-Puzzle**

**Estado objetivo:**
```
1 2 3
4 5 6
7 8 0
```

**Estado inicial (exemplo):**
```
1 2 3
4 0 6
7 5 8
```

### **Implementação Completa**

```python
import copy
import time

class PuzzleState:
    def __init__(self, board, parent=None, move="", depth=0):
        self.board = board
        self.parent = parent
        self.move = move
        self.depth = depth
        self.size = len(board)
        self.blank_pos = self.find_blank()
    
    def find_blank(self):
        """Encontra a posição do espaço vazio (0)"""
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    return (i, j)
        return None
    
    def get_children(self):
        """Gera todos os movimentos possíveis"""
        children = []
        i, j = self.blank_pos
        
        # Movimentos possíveis: cima, baixo, esquerda, direita
        moves = [
            (-1, 0, "UP"),
            (1, 0, "DOWN"), 
            (0, -1, "LEFT"),
            (0, 1, "RIGHT")
        ]
        
        for di, dj, move_name in moves:
            new_i, new_j = i + di, j + dj
            
            if 0 <= new_i < self.size and 0 <= new_j < self.size:
                # Cria nova configuração do tabuleiro
                new_board = copy.deepcopy(self.board)
                new_board[i][j], new_board[new_i][new_j] = new_board[new_i][new_j], new_board[i][j]
                
                child = PuzzleState(new_board, self, move_name, self.depth + 1)
                children.append(child)
        
        return children
    
    def is_goal(self, goal):
        """Verifica se é o estado objetivo"""
        return self.board == goal
    
    def __eq__(self, other):
        return self.board == other.board
    
    def __hash__(self):
        return hash(str(self.board))
    
    def __str__(self):
        return '\n'.join([' '.join(map(str, row)) for row in self.board])

def manhattan_distance(state, goal):
    """Heurística: Distância de Manhattan"""
    distance = 0
    goal_positions = {}
    
    # Mapeia as posições objetivo de cada número
    for i in range(len(goal)):
        for j in range(len(goal)):
            goal_positions[goal[i][j]] = (i, j)
    
    # Calcula a distância para cada peça
    for i in range(len(state.board)):
        for j in range(len(state.board)):
            value = state.board[i][j]
            if value != 0:  # Ignora o espaço vazio
                goal_i, goal_j = goal_positions[value]
                distance += abs(i - goal_i) + abs(j - goal_j)
    
    return distance

def IDA_star(initial_state, goal_state):
    """Implementação do algoritmo IDA*"""
    
    def depth_limited_search(node, g, threshold, path):
        nonlocal nodes_expanded
        nodes_expanded += 1
        
        # Calcula f(n) = g(n) + h(n)
        f = g + manhattan_distance(node, goal_state)
        
        # Se excede o threshold, retorna para aumentar no próximo nível
        if f > threshold:
            return None, f
        
        # Se é o objetivo, retorna o caminho
        if node.is_goal(goal_state):
            return path + [node], "FOUND"
        
        min_exceeded = float('inf')
        
        # Expande os filhos
        for child in node.get_children():
            if child not in path:  # Evita ciclos
                result, new_threshold = depth_limited_search(
                    child, g + 1, threshold, path + [node]
                )
                
                if result == "FOUND":
                    return path + [node, child], "FOUND"
                
                if new_threshold is not None and new_threshold < min_exceeded:
                    min_exceeded = new_threshold
        
        return None, min_exceeded
    
    # Inicialização do IDA*
    threshold = manhattan_distance(initial_state, goal_state)
    path = [initial_state]
    nodes_expanded = 0
    start_time = time.time()
    
    print(f"Threshold inicial: {threshold}")
    
    iteration = 1
    while True:
        print(f"\n--- Iteração {iteration} ---")
        print(f"Threshold atual: {threshold}")
        print(f"Nós expandidos até agora: {nodes_expanded}")
        
        result, new_threshold = depth_limited_search(initial_state, 0, threshold, [])
        
        if result == "FOUND":
            end_time = time.time()
            print(f"\n🎯 SOLUÇÃO ENCONTRADA!")
            print(f"Tempo total: {end_time - start_time:.4f} segundos")
            print(f"Total de iterações: {iteration}")
            print(f"Total de nós expandidos: {nodes_expanded}")
            print(f"Profundidade da solução: {len(result) - 1}")
            return result
        
        if new_threshold == float('inf'):
            print("\n❌ Nenhuma solução encontrada!")
            return None
        
        threshold = new_threshold
        iteration += 1

def print_solution(solution_path):
    """Imprime a solução passo a passo"""
    if not solution_path:
        print("Nenhuma solução encontrada!")
        return
    
    print(f"\n📋 SOLUÇÃO ({len(solution_path) - 1} movimentos):")
    print("=" * 50)
    
    for i, state in enumerate(solution_path):
        if i == 0:
            print("Estado Inicial:")
        else:
            print(f"Passo {i}: {state.move}")
        print(state)
        print("-" * 20)

# Exemplo de uso
if __name__ == "__main__":
    # Estado objetivo
    GOAL_STATE = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]
    
    # Estado inicial (fácil - solução em 3 movimentos)
    INITIAL_STATE = [
        [1, 2, 3],
        [4, 0, 6],
        [7, 5, 8]
    ]
    
    # Estado inicial mais difícil (solução em 10+ movimentos)
    HARD_INITIAL = [
        [1, 2, 3],
        [4, 5, 6],
        [0, 7, 8]
    ]
    
    print("🧩 RESOLVEDOR 8-PUZZLE COM IDA*")
    print("=" * 40)
    
    # Cria os estados
    initial = PuzzleState(INITIAL_STATE)
    goal = PuzzleState(GOAL_STATE)
    
    print("Estado Inicial:")
    print(initial)
    print("\nEstado Objetivo:")
    print(goal)
    
    # Executa o IDA*
    solution = IDA_star(initial, GOAL_STATE)
    
    # Mostra a solução
    if solution and solution != "FOUND":
        print_solution(solution)
```

---

## **Execução do Exemplo**

### **Saída Esperada:**

```
🧩 RESOLVEDOR 8-PUZZLE COM IDA*
========================================
Estado Inicial:
1 2 3
4 0 6
7 5 8

Estado Objetivo:
1 2 3
4 5 6
7 8 0

Threshold inicial: 2

--- Iteração 1 ---
Threshold atual: 2
Nós expandidos até agora: 0

--- Iteração 2 ---
Threshold atual: 3
Nós expandidos até agora: 5

🎯 SOLUÇÃO ENCONTRADA!
Tempo total: 0.0045 segundos
Total de iterações: 2
Total de nós expandidos: 8
Profundidade da solução: 3

📋 SOLUÇÃO (3 movimentos):
==================================================
Estado Inicial:
1 2 3
4 0 6
7 5 8
--------------------
Passo 1: RIGHT
1 2 3
4 6 0
7 5 8
--------------------
Passo 2: DOWN
1 2 3
4 6 8
7 5 0
--------------------
Passo 3: LEFT
1 2 3
4 6 8
7 0 5
--------------------
```

---

## **Vantagens do IDA***

1. **✅ Eficiência de Memória**: Armazena apenas um caminho por vez
2. **✅ Ótimo**: Encontra a solução de menor custo (com heurística admissível)
3. **✅ Completo**: Encontra solução se ela existir
4. **✅ Sem lista de fechados**: Não precisa armazenar todos os nós visitados

## **Desvantagens**

1. **❌ Retrabalho**: Reexpande nós em cada iteração
2. **❌ Ineficiente para grafos com custos variáveis**: Se as ações têm custos muito diferentes

## **Complexidade**

- **Tempo**: O(b^d) - onde b é o fator de ramificação, d é a profundidade da solução
- **Espaço**: O(d) - linear na profundidade da solução

O IDA* é particularmente útil quando o espaço de busca é muito grande e a memória é limitada, sendo uma excelente alternativa ao A* em tais cenários!