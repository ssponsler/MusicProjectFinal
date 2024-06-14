import matplotlib.pyplot as plt
import librosa.display

y, sr = librosa.load("songs/wheninrome.wav")
#y, sr = librosa.load(librosa.ex('nutcracker'), duration=10, offset=10)
y = librosa.effects.harmonic(y)

tonnetz = librosa.feature.tonnetz(y=y, sr=sr)

fig, ax = plt.subplots(nrows=2, sharex=True)
img1 = librosa.display.specshow(tonnetz, y_axis='tonnetz', x_axis='time', ax=ax[0])
ax[0].set(title='Tonal Centroids (Tonnetz)')
ax[0].label_outer()
img2 = librosa.display.specshow(librosa.feature.chroma_cqt(y=y, sr=sr), y_axis='chroma', x_axis='time', ax=ax[1])
ax[1].set(title='Chroma')
fig.colorbar(img1, ax=[ax[0]])
fig.colorbar(img2, ax=[ax[1]])