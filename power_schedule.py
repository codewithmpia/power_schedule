#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import datetime
import os

# Heures d'arrêt et de réveil par défaut
DEFAULT_SHUTDOWN_TIME = "9:30"
DEFAULT_WAKEUP_TIME = "18:00"

# Heures d'arrêt et de réveil spécifiques pour le mercredi
WEDNESDAY_SHUTDOWN_TIME = "13:50"
WEDNESDAY_WAKEUP_TIME = "18:00"

# Fichier de log (personnaliser le chemin si nécessaire)
LOG_FILE = "path_to_save_log_files/shutdown_and_wakeup.log"
# Fichier de suivi de l'exécution quotidienne
LAST_RUN_FILE = "path_to_save_log_file/last_run_day.txt"


def log_message(message):
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"{datetime.datetime.now()} - {message}\n")


def was_last_run_on_sunday():
    if not os.path.exists(LAST_RUN_FILE):
        return False
    with open(LAST_RUN_FILE, "r") as file:
        last_run_day = file.read().strip()
    return last_run_day == "6"  # 6 représente le dimanche


def update_last_run_day():
    current_day = datetime.datetime.now().weekday()
    with open(LAST_RUN_FILE, "w") as file:
        file.write(str(current_day))


def calculate_seconds_until_wakeup(wakeup_time):
    # Obtenir l'heure actuelle
    current_time = datetime.datetime.now()
    # Créer un objet datetime pour l'heure de réveil
    wakeup_datetime = current_time.replace(
        hour=int(wakeup_time.split(":")[0]),
        minute=int(wakeup_time.split(":")[1]),
        second=0,
        microsecond=0
    )

    # Si l'heure de réveil est déjà passée aujourd'hui, ajouter un jour
    if wakeup_datetime < current_time:
        wakeup_datetime += datetime.timedelta(days=1)

    # Calculer le nombre de secondes jusqu'à l'heure de réveil
    return (wakeup_datetime - current_time).total_seconds()


def shutdown_and_wakeup(shutdown_time, wakeup_time):
    # Calculer le nombre de secondes jusqu'à l'heure de réveil
    seconds_until_wakeup = calculate_seconds_until_wakeup(wakeup_time)

    # Programmer le réveil avec rtcwake
    subprocess.run(["sudo", "rtcwake", "-m", "no", "-s", str(int(seconds_until_wakeup))])
    log_message(f"rtcwake programmé pour {wakeup_time}")

    # Obtenir l'heure actuelle
    current_time = datetime.datetime.now()
    # Créer un objet datetime pour l'heure d'arrêt
    shutdown_datetime = current_time.replace(
        hour=int(shutdown_time.split(":")[0]),
        minute=int(shutdown_time.split(":")[1]),
        second=0,
        microsecond=0
    )
    # Si l'heure d'arrêt est déjà passée aujourd'hui, ajouter un jour
    if shutdown_datetime < current_time:
        shutdown_datetime += datetime.timedelta(days=1)

    # Calculer le nombre de secondes jusqu'à l'heure d'arrêt
    seconds_until_shutdown = (shutdown_datetime - current_time).total_seconds()

    # Programmer l'arrêt du système
    subprocess.run(["sudo", "shutdown", "-h", "+{}".format(int(seconds_until_shutdown) // 60)])
    log_message(f"shutdown programmé pour {shutdown_time}")


if __name__ == "__main__":
    # Obtenir le jour de la semaine actuel (0 = lundi, 6 = dimanche)
    current_day = datetime.datetime.now().weekday()

    # Vérifie si c'est lundi et que le dernier run était un dimanche
    if current_day == 0 and was_last_run_on_sunday():
        log_message("Reprise du script après le dimanche")

    # Définir les heures d'arrêt et de réveil en fonction du jour de la semaine
    if current_day == 2:  # Mercredi
        shutdown_time = WEDNESDAY_SHUTDOWN_TIME
        wakeup_time = WEDNESDAY_WAKEUP_TIME
    elif current_day == 6:  # Dimanche
        # Ne rien faire le dimanche
        log_message("Pas d'arrêt le dimanche")
        update_last_run_day()
        exit(0)
    else:
        shutdown_time = DEFAULT_SHUTDOWN_TIME
        wakeup_time = DEFAULT_WAKEUP_TIME

    # Exécuter la fonction principale avec les heures définies
    shutdown_and_wakeup(shutdown_time, wakeup_time)

    # Mise à jour du dernier jour d'exécution
    update_last_run_day()
