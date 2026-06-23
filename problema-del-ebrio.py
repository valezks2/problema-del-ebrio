import random
import tkinter as tk

def caminar(pasos):
    x, y = 0, 0
    for _ in range(pasos):
        direccion = random.choice(['N', 'S', 'E', 'O'])
        if direccion == 'N':
            y += 1
        elif direccion == 'S':
            y -= 1
        elif direccion == 'E':
            x += 1
        elif direccion == 'O':
            x -= 1
    return (x, y)

def simulacion(num_simulaciones, pasos):
    exitos = 0
    posiciones = []

    for _ in range(num_simulaciones):
        posicion_final = caminar(pasos)
        posiciones.append(posicion_final)
        if abs(posicion_final[0]) + abs(posicion_final[1]) == 2:
            exitos += 1

    probabilidad = (exitos / num_simulaciones) * 100
    return probabilidad, posiciones

def dibujar_cuadricula(canvas):
    for i in range(0, 501, 20):
        canvas.create_line(i, 0, i, 400, fill="lightgrey")
        canvas.create_line(0, i, 500, i, fill="lightgrey")

def mostrar_recorrido(posiciones, canvas, index=0):
    if index < len(posiciones):
        canvas.delete("punto")

        canvas.create_oval(255, 195, 265, 205, fill="blue", tags="punto")

        pos = posiciones[index]
        x = pos[0] * 20 + 255
        y = -pos[1] * 20 + 195

        if -250 <= x <= 500 and -250 <= y <= 500:
            canvas.create_oval(x, y, x + 10, y + 10, fill="red", tags="punto")

        global after_id
        after_id = canvas.after(1000, mostrar_recorrido, posiciones, canvas, index + 1)

def mostrar_resultado(event=None):
    global after_id
    if 'after_id' in globals():
        canvas.after_cancel(after_id)

    try:
        num_simulaciones = int(entrada.get())
        if num_simulaciones <= 0:
            raise ValueError
        probabilidad, posiciones = simulacion(num_simulaciones, 10)
        texto_label.config(text=f"La probabilidad de que termine a dos calles es de: {probabilidad:.2f}%", fg="black")
        mostrar_recorrido(posiciones, canvas)
    except ValueError:
        texto_label.config(text="Por favor, ingrese un número válido.", fg="red")

ventana = tk.Tk()
ventana.title("Problema del Ebrio")
ventana.resizable(False, False)

frame_controles = tk.Frame(ventana)
frame_controles.pack(side=tk.BOTTOM)

entrada = tk.Entry(frame_controles)
entrada.pack(side=tk.TOP)

boton = tk.Button(frame_controles, text="Iniciar", command=mostrar_resultado)
boton.pack(side=tk.TOP, pady=5)

texto_label = tk.Label(ventana, text="Ingrese el número de simulaciones.")
texto_label.pack()

canvas = tk.Canvas(ventana, width=500, height=400, bg="white")
canvas.pack()

dibujar_cuadricula(canvas)

entrada.bind('<Return>', mostrar_resultado)

ventana.eval('tk::PlaceWindow . center')
ventana.mainloop()