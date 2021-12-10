# DomoticzLYWSD03MMC
Xiaomi Mijia Humidity and Temperature (LYWSD03MMC) for Domoticz
## Installation
Requis : Testé uniquement sur Domoticz version 2020.2, Python 3 doit être installé.
* Installer les packages pythons requis:
   - ```sudo apt-get install python3-pip libglib2.0-dev```
   - ```sudo pip3 install requests bluepy```
 
Pour récupérer la version de développement :
* En ligne de commande aller dans le répertoire plugin de Domoticz (domoticz/plugins)
* Lancer la commande: ```git clone https://github.com/ultrasuperpingu/DomoticzLYWSD03MMC.git```
* Redémarrer le service Domoticz en lancant la commande ```sudo service domoticz restart```

Vous pouvez aussi simplement copier le fichier plugin.py dans le répertoire ```domoticz/plugins/{NomDeRepertoireDeVotreChoix}``` et redémarrer domoticz.

Pour récupérer une release (quand il y en aura une), télécharger la version et décompresser l'archive dans le répertoire ```domoticz/plugins/{NomDeRepertoireDeVotreChoix}``` et redémarrer domoticz.

## Mise à Jour

Pour mettre à jour le plugin :

* En ligne de commande, aller dans le répertoire plugin de Domoticz (domoticz/plugins)
* Lancer la commande: ```git pull```
* Redémarrer le service Domoticz en lancant la commande ```sudo service domoticz restart```

Vous pouvez également mettre à jour le fichier plugin.py dans le répertoire ```domoticz/plugins/{NomDeRepertoireDeVotreChoix}``` et redémarrer domoticz.

## Configuration
 * Récupérer l'adresse MAC de votre capteur:
   - ```sudo hcitool lescan```
   - Chercher une ligne du type : ```A1:C2:E3:04:25:46 LYWSD03MMC```
 * Entrer l'adresse MAC dans le champ correspondant
