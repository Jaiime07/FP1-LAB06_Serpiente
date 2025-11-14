import tkinter as tk
from collections import deque
import serpiente_utiles as serpiente_utiles
import platform

FILAS = 30
COLUMNAS = 40
RETRASO_MS = 100  # A menor valor, mayor velocidad
PAREDES = [
    [(15,15), (16,15), (17,15), (18,15)],
    [(25,10), (25,11), (25,12), (25,13), (25,14), (25,15)],
    [(10,25), (11,25), (12,25), (13,25), (14,25)],
    [(30,20), (31,20), (32,20), (33,20), (34,20), (35,20)],
    [(20,5), (20,6), (20,7), (20,8)],
    [(8,5), (8,6), (8,7), (8,8)]
]

class SerpienteGUI(tk.Canvas):
    def __init__(self, filas=FILAS, columnas=COLUMNAS, tam_bloque=20):
        self.filas = filas
        self.columnas = columnas
        self.tam_bloque = tam_bloque
        self.ancho = columnas * tam_bloque
        self.alto = filas * tam_bloque
        self.retraso_ms = RETRASO_MS   
        self.plataforma = platform.system()
        self.juego_iniciado = False

        super().__init__(width=self.ancho, height=self.alto, background="white", highlightthickness=0)
        self.master.resizable(False, False)

        self.serpiente = [(5, 2), (4, 2), (3, 2)]              
        self.paredes = PAREDES

        self.comida = serpiente_utiles.genera_comida_aleatoria(self.serpiente, self.paredes, self.filas, self.columnas)
        self.puntuacion = 0
        self.direccion = "Right"
        self.ultima_direccion = self.direccion  
        self.cola_direcciones = deque()  # Lo usamos para guardar pulsaciones más rápidas que el retardo

        self.bind_all("<Key>", self.al_pulsar_tecla)
        self.carga_imagenes()
        self.muestra_pantalla_inicial()

    def muestra_pantalla_inicial(self):
        self.create_text(
            self.ancho / 2,
            self.alto / 2 - 40,
            text="JUEGO DE LA SERPIENTE",
            fill="black",
            font=('TkDefaultFont', 24, 'bold'),
            tag="inicio"
        )
        self.create_text(
            self.ancho / 2,
            self.alto / 2 + 20,
            text="Controles: ← ↑ → ↓",
            fill="black",
            font=('TkDefaultFont', 16),
            tag="inicio"
        )
        self.create_text(
            self.ancho / 2,
            self.alto / 2 + 60,
            text="Pulsa cualquier tecla para comenzar",
            fill="gray",
            font=('TkDefaultFont', 12),
            tag="inicio"
        )

    def iniciar_juego(self):
        self.delete("inicio")
        self.crea_objetos()
        self.juego_iniciado = True
        self.after(100, self.bucle_juego)

    def convierte_a_pixeles(self, posicion):
        return posicion[0] * self.tam_bloque + self.tam_bloque/2, posicion[1] * self.tam_bloque + self.tam_bloque/2

    def carga_imagenes(self):
        self.imagenes_serpiente = [
            tk.PhotoImage(file="assets/piel_serpiente1.png"), 
            tk.PhotoImage(file="assets/piel_serpiente2.png"), 
            tk.PhotoImage(file="assets/piel_serpiente3.png")]

        self.imagen_comida = tk.PhotoImage(file="assets/comida.png")
        self.imagen_pared = tk.PhotoImage(file="assets/pared.png")
        
    def crea_objetos(self):
        self.create_text(
            65, 12, text=f"Puntuación: {self.puntuacion}", tag="score", fill="black", font=10
        )
        for i, posicion in enumerate(self.serpiente):
            x, y = self.convierte_a_pixeles(posicion)
            self.create_image(x, y, image=self.imagenes_serpiente[i % len(self.imagenes_serpiente)], tag="snake")
            if i == 0:
                half = self.tam_bloque / 2
                self.create_rectangle(
                    x - half, y - half, x + half, y + half,
                    outline="red", width=2, fill="", tag="snake_head_box"
                )
        self.create_image(*self.convierte_a_pixeles(self.comida), image=self.imagen_comida, tag="food")
        self.crea_objetos_paredes()
    
    def crea_objetos_paredes(self):
        for pared in self.paredes:
            for posicion in pared:
                x, y = self.convierte_a_pixeles(posicion)
                self.create_image(x, y, image=self.imagen_pared, tag="wall")
        
    def mueve_serpiente(self):
        while self.cola_direcciones:
            siguiente_direccion = self.cola_direcciones.popleft()
            if (self.ultima_direccion == "Left" and siguiente_direccion != "Right") or \
               (self.ultima_direccion == "Right" and siguiente_direccion != "Left") or \
               (self.ultima_direccion == "Up" and siguiente_direccion != "Down") or \
               (self.ultima_direccion == "Down" and siguiente_direccion != "Up"):
                self.direccion = siguiente_direccion
                break

        serpiente_utiles.mueve_serpiente(self.serpiente, self.direccion, self.filas, self.columnas)

        for segmento, posicion in zip(self.find_withtag("snake"), self.serpiente):
            self.coords(segmento, self.convierte_a_pixeles(posicion))

        # Mueve el recuadro rojo de la cabeza
        x, y = self.convierte_a_pixeles(self.serpiente[0])
        half = self.tam_bloque / 2
        self.coords(self.find_withtag("snake_head_box"), x - half, y - half, x + half, y + half)
            
        self.ultima_direccion = self.direccion

    def bucle_juego(self):
        self.mueve_serpiente()

        if serpiente_utiles.comprueba_choque(self.serpiente, self.paredes):
            self.game_over()
            return

        self.comprueba_serpiente_come_crece()
        self.after(self.retraso_ms, self.bucle_juego)

    def game_over(self):
        self.delete(tk.ALL)
        self.create_text(
            self.winfo_width() / 2,
            self.winfo_height() / 2,
            text=f"Game over! Puntuación: {self.puntuacion}",
            fill="black",
            font=('TkDefaultFont', 24)
        )

    def al_pulsar_tecla(self, e):
        if not self.juego_iniciado:
            self.iniciar_juego()
            return
            
        if e.keysym in {"Left", "Right", "Up", "Down"}:
            self.cola_direcciones.append(e.keysym)


    def comprueba_serpiente_come_crece(self):
        if serpiente_utiles.ha_comido_serpiente(self.serpiente, self.comida):
            self.puntuacion += 1
            serpiente_utiles.crece_serpiente(self.serpiente)
            if self.retraso_ms > 50:
                self.retraso_ms -= 1 # Cuanto más come, más rápido se moverá

            self.create_image(*self.convierte_a_pixeles(self.serpiente[-1]), image=self.imagenes_serpiente[(len(self.serpiente)-1)%2], tag="snake")
            
            self.comida = serpiente_utiles.genera_comida_aleatoria(self.serpiente, self.paredes, self.filas, self.columnas)
            self.coords(self.find_withtag("food"), self.convierte_a_pixeles(self.comida))
            
            score = self.find_withtag("score")
            self.itemconfigure(score, text=f"Puntuación: {self.puntuacion}")

               

root = tk.Tk()
root.title("Juego Serpiente")

board = SerpienteGUI()
board.pack()

root.mainloop()
