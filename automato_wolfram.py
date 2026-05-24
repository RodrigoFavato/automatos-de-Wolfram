import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox

# =========================
# Funções do autômato
# =========================
def regra_para_binario(rule):
    return np.array([int(x) for x in np.binary_repr(rule, width=8)])

def evoluir(estado, rule_bin):
    novo = np.zeros_like(estado)
    for i in range(len(estado)):
        esquerda = estado[(i-1) % len(estado)]
        centro = estado[i]
        direita = estado[(i+1) % len(estado)]
        idx = 7 - (4*esquerda + 2*centro + direita)
        novo[i] = rule_bin[idx]
    return novo

def gerar_inicial(tamanho, modo, densidade, distribuicao):
    estado = np.zeros(tamanho, dtype=int)

    if modo == "Um sítio":
        estado[tamanho // 2] = 1
    else:
        if distribuicao == "Espalhado":
            estado = np.random.choice([0,1], size=tamanho, p=[1-densidade, densidade])
        else:
            n = int(tamanho * densidade)
            inicio = np.random.randint(0, max(1, tamanho-n))
            estado[inicio:inicio+n] = 1

    return estado

def classificar(historico):
    variancia = np.var(historico)
    if variancia < 0.01:
        return "Classe I (Homogêneo)"
    elif variancia < 0.05:
        return "Classe II (Periódico)"
    elif variancia > 0.2:
        return "Classe III (Caótico)"
    else:
        return "Classe IV (Complexo)"

def grafico_densidade(historico):
    densidade = np.mean(historico, axis=1)
    plt.figure()
    plt.plot(densidade)
    plt.title("Densidade ao longo do tempo")
    plt.xlabel("Tempo")
    plt.ylabel("Densidade")
    plt.show()

# =========================
# Animação
# =========================
def animar(rule, tamanho, passos, modo, densidade, distribuicao, delay):
    rule_bin = regra_para_binario(rule)
    estado = gerar_inicial(tamanho, modo, densidade, distribuicao)

    historico = [estado.copy()]

    plt.ion()
    fig, ax = plt.subplots()
    img = ax.imshow([estado], cmap='binary', aspect='auto')

    for t in range(passos):
        estado = evoluir(estado, rule_bin)
        historico.append(estado.copy())

        img.set_data(historico)
        ax.set_title(f"Tempo: {t}")
        plt.pause(delay)

    plt.ioff()
    plt.show()

    historico = np.array(historico)

    classe = classificar(historico)
    messagebox.showinfo("Classificação", classe)

    grafico_densidade(historico)

# =========================
# Interface gráfica
# =========================
def ajuda(texto):
    messagebox.showinfo("Ajuda", texto)

def executar():
    try:
        rule = int(entry_regra.get())
        tamanho = int(entry_tamanho.get())
        passos = int(entry_passos.get())
        modo = var_modo.get()
        densidade = float(entry_densidade.get())
        distribuicao = var_dist.get()
        delay = float(entry_delay.get())

        animar(rule, tamanho, passos, modo, densidade, distribuicao, delay)

    except Exception as e:
        messagebox.showerror("Erro", str(e))

root = tk.Tk()
root.title("Autômatos de Wolfram (Animado)")

# ===== REGRA =====
tk.Label(root, text="Regra (0-255)").grid(row=0, column=0)
entry_regra = tk.Entry(root)
entry_regra.grid(row=0, column=1)
tk.Button(root, text="❓", command=lambda: ajuda(
    "Número de 0 a 255.\nEx: 30 (caótico), 110 (complexo)"
)).grid(row=0, column=2)

# ===== TAMANHO =====
tk.Label(root, text="Tamanho").grid(row=1, column=0)
entry_tamanho = tk.Entry(root)
entry_tamanho.grid(row=1, column=1)
tk.Button(root, text="❓", command=lambda: ajuda(
    "Número de células.\nEx: 100"
)).grid(row=1, column=2)

# ===== PASSOS =====
tk.Label(root, text="Passos").grid(row=2, column=0)
entry_passos = tk.Entry(root)
entry_passos.grid(row=2, column=1)
tk.Button(root, text="❓", command=lambda: ajuda(
    "Número de iterações.\nEx: 100"
)).grid(row=2, column=2)

# ===== DELAY =====
tk.Label(root, text="Velocidade (delay)").grid(row=3, column=0)
entry_delay = tk.Entry(root)
entry_delay.insert(0, "0.05")
entry_delay.grid(row=3, column=1)
tk.Button(root, text="❓", command=lambda: ajuda(
    "Tempo entre passos.\nMenor = mais rápido\nEx: 0.05"
)).grid(row=3, column=2)

# ===== MODO =====
tk.Label(root, text="Estado Inicial").grid(row=4, column=0)
var_modo = tk.StringVar(value="Um sítio")
tk.OptionMenu(root, var_modo, "Um sítio", "Aleatório").grid(row=4, column=1)
tk.Button(root, text="❓", command=lambda: ajuda(
    "Um sítio: padrão clássico\nAleatório: distribuição inicial"
)).grid(row=4, column=2)

# ===== DENSIDADE =====
tk.Label(root, text="Densidade").grid(row=5, column=0)
entry_densidade = tk.Entry(root)
entry_densidade.insert(0, "0.5")
entry_densidade.grid(row=5, column=1)
tk.Button(root, text="❓", command=lambda: ajuda(
    "Valor entre 0 e 1\nEx: 0.5"
)).grid(row=5, column=2)

# ===== DISTRIBUIÇÃO =====
tk.Label(root, text="Distribuição").grid(row=6, column=0)
var_dist = tk.StringVar(value="Espalhado")
tk.OptionMenu(root, var_dist, "Espalhado", "Agrupado").grid(row=6, column=1)
tk.Button(root, text="❓", command=lambda: ajuda(
    "Espalhado ou agrupado"
)).grid(row=6, column=2)

# ===== EXECUTAR =====
tk.Button(root, text="Executar", command=executar, bg="green", fg="white").grid(row=7, column=0, columnspan=3)

root.mainloop()