
# 🕹️ Mundo do Wumpus

Um jogo clássico de raciocínio lógico e sobrevivência! Explore a caverna, evite os perigos, colete o ouro e volte vivo!

## 📦 Requisitos

- Python 3.8+
- Pygame

### Instalar o Pygame:
```bash
pip install pygame
```

---

## 🚀 Como Jogar

1. **Execute o jogo:**
   ```bash
   python index.py ou
   python -X utf8 index.py
   ```

2. **Escolha o tamanho do mapa.**
   - Você verá uma tela com botões (por exemplo: 4x4, 5x5, 6x6).
   - Clique com o mouse no tamanho desejado para iniciar a aventura.

3. **Movimente o agente (explorador):**
   - **Setas do teclado (↑ ↓ ← →)** para mover o agente pela caverna.

4. **Objetivo:**
   - Pegue o ouro (ícone dourado `G`) e volte para a posição inicial `[1,1]` para vencer.
   - Evite:
     - O **Wumpus** (`W`) – um monstro mortal!
     - Os **abismos** (`P`) – quedas fatais!

---

## 🧠 Percepções do agente

- 💨 **Brisa**: Há um abismo em uma sala adjacente.
- 🤢 **Cheiro**: O Wumpus está próximo.
- ✨ **Brilho**: O ouro está na sala atual.
- 🪦 **"VOCÊ MORREU"**: Você entrou em uma sala com Wumpus ou abismo.

---

## 🎮 Controles

| Tecla | Ação                |
|-------|---------------------|
| ↑     | Move para cima      |
| ↓     | Move para baixo     |
| ←     | Move para esquerda  |
| →     | Move para direita   |
| Esc   | Sai do jogo         |

---

## 🔁 Reiniciar

Após morrer ou vencer, clique no botão **"Reiniciar"** para jogar novamente!

---

