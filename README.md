précision : 1/4000s (pour une raison obscure, en python ça se transforme en 1/1000)


[TimingPoints]
255,4000,4,1,0,100,1,0
offset,bpm,nombre de temps,je sais pas


bpm : 
respecte le fonction f(x) telle que :
    f(15)=4000 (bpm de 15 -> 4000 dans le fichier)
    f(30)=2000 (bpm de 30 -> 2000 dans le fichier)
    f(60)=1000 (bpm de 60 -> 1000 dans le fichier)
    f(120)=500 (bpm de 120 -> 500 dans le fichier)
donc f(x)=60000/x
en gros la différence de timing entre deux graduations (noire - 1/1)
