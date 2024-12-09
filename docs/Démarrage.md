Vous pouvez utiliser le **"./start.bat"** pour démarrer Elyon :
### **Arguments** :
Tout les arguments sauf une exceptions sont de se format ci-contre : '--{clé} {valeur}'
Listes des arguments existant :

| clé        | valeur attendu                              | fonction                                                                                                                           |
| ---------- | ------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| dev        | Aucune (cas spécial)                        | Permet de passer entre le mode "prod" ou "dev"<br>Et d'afficher ou non certaine logs/débogage                                      |
| type       | client/server/local                         | Permet de choisir quel partie du projet doit être lancer (local lance les deux en même et modifie les configuration pour les lier) |
| config     | valeur au choix<br>(ne peut pas être "all") | Permet de passer outre le système de config de base entre prod et dev (cela permet d'avoir une troisième config pour des test)     |
| clear-data | client/server/all                           | Permet de supprimer les donnée d'une ou l'autre parti selon la valeur (all supprimer les deux)<br>                                 |
| data-path  | valeur de vôtre choix                       | Permet de changer le dossiers pour stocker les données                                                                             |
