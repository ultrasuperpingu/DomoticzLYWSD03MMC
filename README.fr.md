# DomoticzLYWSD03MMC
Plugin Xiaomi Mijia Humidity and Temperature (LYWSD03MMC) pour Domoticz.

Ce plugin NE FONCTIONNE PAS correctement (plus d'information sur le bug tracker). Je ne recommande PAS son utilisation.

## Installation
Requis : Testé uniquement sur Domoticz version 2020.2, Python 3 doit être installé.
* Installer les packages pythons requis:
   - ```sudo apt-get install python3-pip libglib2.0-dev```
   - ```sudo apt-get install --no-install-recommends bluetooth```
   - ```sudo pip3 install gatt```
   - ```sudo apt-get install python3-dbus```
 
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
 * Récupérer l'adresse MAC de votre capteur :
   - ```sudo hcitool lescan```
   - Chercher une ligne du type : ```A1:C2:E3:04:25:46 LYWSD03MMC```
 * Dans le formulaire d'ajout de Materiel dans Domoticz, choisir 'Xiaomi Mijia Humidity and Temperature (LYWSD03MMC)'
 * Entrer l'adresse MAC dans le champ 'Mac Address'
 * Entrer le nom de l'adaptateur Bluetooth (par défaut: hci0)
