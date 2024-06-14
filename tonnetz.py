import librosa.display
import matplotlib.pyplot as plt

y, sr = librosa.load("songs/wheninrome.wav")
y = librosa.effects.harmonic(y)

tonnetz = librosa.feature.tonnetz(y=y, sr=sr)

plt.figure(figsize=(10, 5))
librosa.display.specshow(tonnetz, y_axis='tonnetz')
plt.colorbar()
plt.show()

