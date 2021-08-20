

Noms: 
Louis Jardinet
Mathieu Surquin

Matricules:
195030
195199


Pour lancer le client : (dans le bon dossier)

$ python client-abalone port pseudo

Nous avons codé une IA pour jouer à Abalone pour notre cours de Programmation de l'Ecam. D'abord, l'IA calcule les coups possibles.

Ensuite, si l'occasion d'éliminer une boule se présente et que l'adversaire ne gagnera pas la partie ce faisant, l'IA éliminera cette boule.

Sinon, elle tentera de protéger les boules exposées en les déplaçant. Si aucune boule n'est exposée, le coup suivant sera ne mettra pas de boule alliée en danger et se dirigera vers l'extérieur du plateau si possible, autrement elle ramènera la boule au centre. 

Si l'IA ne trouve pas le meilleur coup, elle lançera un coup aléatoire et si aucun coup n'est possible, elle abandonnera. 


Bibliothèques:

1. time : calculer le temps que prends la recherche d'un coup
2. random : créer une liste de coups aléatoires
3. copy : copier une variable globale et pouvoir l'utiliser en local dans une fonction
4. socket : communication serveur-client
5. JSON : sérialiser / déserialiser des requêtes en json
6. sys : arguments dans la partie client, un port et/ou nom