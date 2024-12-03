Vous pouvez utiliser deux "**.bat**" différent pour démarrer Elyon :
- ./start.bat
Démarrer l'application en vérifiant les dépendance enregistrer dans le fichier "dependances.txt"
- ./dev.bat
Démarrer tout simplement l'application.

Si vous vous avoir la commande complet pour installer les dépendances vous pouvez effecter ./start.bat --dependances-cmd
### **Arguments** :
Tout les arguments sauf une exceptions sont de se format ci-contre : '--{clé} {valeur}'
Listes des arguments existant :

| clé    | valeur attendu                              | fonction                                                                                                                           |
| ------ | ------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| dev    | Aucune (cas spécial)                        | Permet de passer entre le mode "prod" ou "dev"<br>Et d'afficher ou non certaine logs/débogage                                      |
| mode   | client/server/local                         | Permet de choisir quel partie du projet doit être lancer (local lance les deux en même et modifie les configuration pour les lier) |
| config | valeur au choix<br>(ne peut pas être "all") | Permet de passer outre le système de config de base entre prod et dev (cela permet d'avoir une troisième config pour des test)     |
