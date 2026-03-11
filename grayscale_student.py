"""
Aufgabe: Farbbild nach Graustufen konvertieren (Rec. 709)
=========================================================
Gegeben ist ein JPG-Bild. Deine Aufgabe:
  1. Lies das Bild als NumPy-Array ein.
  2. Konvertiere es nach Graustufen mit den Rec.-709-Gewichten:
       Y = 0.2126 * R  +  0.7152 * G  +  0.0722 * B
  3. Zeige Original und Graustufen nebeneinander an.
"""

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# --- Bild einlesen ---
img      = np.array(Image.open("bild.jpg"))        # Shape: (H, W, 3), dtype uint8
r, g, b  = img[:, :, 0], img[:, :, 1], img[:, :, 2]

# --- Rec.-709-Konvertierung ---
gray = 0.2126 * r + 0.7152 * g + 0.0722 * b       ______  # Hinweis: Rec.-709-Formel: Y = 0.2126*R + 0.7152*G + 0.0722*B
gray = gray.astype(np.uint8)                        ______  # Hinweis: Ergebnis in uint8 umwandeln, damit Werte 0–255 bleiben

# --- Anzeige ---
fig, axes = plt.subplots(1, 2, figsize=(10, 4))    ______  # Hinweis: 1 Zeile, 2 Spalten nebeneinander

axes[0].imshow(img)                                 ______
axes[0].set_title("Original (RGB)")                 ______

axes[1].imshow(gray, cmap="gray")                   ______  # Hinweis: cmap="gray" für Graustufendarstellung
axes[1].set_title("Graustufen (Rec. 709)")          ______

plt.tight_layout()
plt.show()
