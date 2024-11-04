# Power Schedule Script

**Power Schedule Script**

Est un programme Python permettant de programmer l'arrêt et le réveil automatique d'un système à des heures spécifiques.
Il est conçu pour automatiser ces tâches en fonction des jours de la semaine, avec des configurations spéciales pour le mercredi et le dimanche.

## Fonctionnalités

- **Arrêt automatique** à 9h30 et **réveil** à 18h00 par défaut.
- **Programmation spéciale** pour le mercredi : arrêt à 13h50 et réveil à 18h00.
- **Pas d'arrêt le dimanche** : le script reste inactif ce jour-là.
- **Reprise automatique le lundi** après une inactivité le dimanche, grâce à un suivi de la dernière exécution.
- Gestion des logs d'événements pour suivre les actions du script.

## Installation

### Prérequis

- **Python 3** doit être installé sur le système.
- **Permissions sudo** pour exécuter `shutdown` et `rtcwake`.

### Étapes d'installation

1. Clonez le dépôt sur votre machine locale :

    ```bash
    git clone https://github.com/codewithmpia/power_schedule.git
    cd power_schedule
    ```

2. Assurez-vous que le script est exécutable :

    ```bash
    chmod +x power_schedule.py
    ```

3. Installez les fichiers `service` et `timer` dans le répertoire systemd :

    ```bash
    sudo cp power_schedule.service /etc/systemd/system/
    sudo cp power_schedule.timer /etc/systemd/system/
    ```

4. Rechargez systemd et démarrez le timer :

    ```bash
    sudo systemctl daemon-reload
    sudo systemctl enable power_schedule.service
    sudo systemctl enable power_schedule.timer
    sudo systemctl start power_schedule.service
    sudo systemctl start power_schedule.timer
    ```

## Configuration

Le script est configuré avec les heures d'arrêt et de réveil par défaut suivantes :

- **Par défaut** : arrêt à `9:30`, réveil à `18:00`.
- **Mercredi** : arrêt à `13:50`, réveil à `18:00`.
- **Dimanche** : aucune action.

### Personnalisation

Les heures d'arrêt et de réveil peuvent être modifiées directement dans le script en éditant les variables suivantes :

```python
DEFAULT_SHUTDOWN_TIME = "9:30"
DEFAULT_WAKEUP_TIME = "18:00"
WEDNESDAY_SHUTDOWN_TIME = "13:50"
WEDNESDAY_WAKEUP_TIME = "18:00"
```

## Utilisation

Une fois le timer activé, le script s'exécutera automatiquement tous les jours à une heure fixe pour programmer les arrêts et réveils :

- Les logs d'événements seront sauvegardés dans le fichier spécifié (`/path_to_save_log_files/shutdown_and_wakeup.log` par défaut).
- Le script ne fera rien le dimanche et reprendra son fonctionnement normalement le lundi.

## Fichiers

- `power_schedule.py` : script principal gérant les horaires d'arrêt et de réveil.
- `power_schedule.service` : fichier de configuration du service systemd.
- `power_schedule.timer` : fichier timer systemd pour lancer le script quotidiennement.
- `shutdown_and_wakeup.log` : fichier de log où sont consignées les actions du script.
- `last_run_day.txt` : fichier pour suivre le dernier jour d'exécution.

## Exemple de Log

Exemple de lignes de log dans `shutdown_and_wakeup.log` :

```
2023-10-02 09:30:00 - rtcwake programmé pour 18:00
2023-10-02 09:31:00 - shutdown programmé pour 9:30
2023-10-08 09:30:00 - Pas d'arrêt le dimanche
```

## Contributions

Les contributions sont les bienvenues. N'hésitez pas à créer une *issue* ou une *pull request* pour toute amélioration.

## Licence

Ce projet est sous licence MIT. Consultez le fichier [LICENSE](LICENSE) pour plus de détails.
