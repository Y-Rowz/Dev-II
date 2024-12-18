## Processus d'installation du script personnel

### 1. Cloner le dépôt
Clonez le dépôt depuis GitHub en utilisant la commande suivante :

```bash
git clone <votre-lien-depot>
```
### 2. Installer les dépendances
Installez les dépendances nécessaires au projet, à savoir pandas, matplotlib et FPDF, avec la commande suivante :
```bash
pip install pandas matplotlib FPDF
```
### 3. Lancer le programme
Une fois les dépendances installées, vous pouvez lancer le programme avec la commande suivante :
```bash
python main.py
```
### 4. Lancer les tests unitaires avec coverage
Pour exécuter les tests unitaires avec coverage et obtenir un rapport détaillé sur la couverture de code, utilisez la commande suivante :
```bash
coverage run -m unittest discover
```
Puis, pour afficher le rapport de couverture, utilisez :
```bash
coverage report
```
Vous pouvez avoir un retour html avec la commande suivante :
```bash
coverage html
```
### 5. installation du linter :
```bash
pip install flake8
```
Test centralisé :
```bash
flake8 mon_script.py
```
Test général :
```bash
flake8 .
```
