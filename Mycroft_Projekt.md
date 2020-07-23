# Mycroft Projekt 

## Projektgruppe
Jannik Schlemmer (js329@hdm-stuttgart.de)
Jan Ziemann (jz043@hdm-stuttgart.de)

## Organisatorisches
Uns stand beiden jeweils ein eigener Raspberry Pi 4, sowie der MiFa Lautsprecher zur Wiedergabe
und die Logitech c270 Webcam als Mikrofon zur Verfügung. Die Hardware haben wir bei dem
gemeinsamen Vor-Ort-Termin an der HdM erhalten. Das Einrichten des Pi hat dort auch schon
funktioniert, bei uns bestand lediglich die selbe Problematik wie bei nahezu allen anderen,
dass die Wiedergabe- bzw. Aufnahmegeräte nicht korrekt verwendet wurden.

Für das weitere Vorgehen und das Hinzufügen eines eigenen Skills stand uns jeweils ein eigener Account
auf der nextcloud-Instanz (https://next.social-robot.info/nc) zur Verfügung.

Über einen eigenen github-Account verfügten wir bereits.

## Aufgabenstellung
Ziel ist es einen eigenen Skill zu entwickeln, der die nächsten Eintragungen in einem nextcloud-Kalender
verkünden soll. Folgende Bonusaufgaben sind optional:
- Kalendereintrag machen
- bestimmten Tag abfragen
- Event löschen
- Event umbenennen

## Problemlösung Audiogeräte
Folgender Link war hierfür sehr hilfreich: https://elinux.org/R-Pi_Troubleshooting#Sound

### 1. Löschen von pulseaudio
`sudo apt-get --purge remove pulseaudio`

### 2. Installation von alsamixer
`sudo apt-get update`
`sudo apt-get upgrade`
`sudo apt-get install alsa-utils`
`sudo modprobe snd_bcm2835`

### 3. Output auswählen
 `amixer cset numid=X <n>` 

0 = auto, 1 = Kopfhörer, 2= HDM)

### 4. Testen
`speaker-test -t sine -f 440 -c 2 -s 1`

### 5. Neuinstallation pulseaudio
`sudo apt-get install gstreamer1.0-pulseaudio`

Durch diesen Workaround hat dann unser Setup auch jeweils funktioniert.

## Weiteres Vorgehen/Vorüberlegungen
Für die Einrichtung und das Starten von Mycroft haben wir hauptsächlich die Mycroft eigene Anleitung
verwendet. (https://github.com/MycroftAI/mycroft-core/blob/dev/README.md)
Nach dieser haben wir auch unseren ersten eigenen Skill angelegt. Als dieser dann angelegt war,
wurden die Testfiles angelegt, mit den Vorüberlegungen welche Grundfunktionen denn prinzipiell
möglich sein sollten. Basierend auf diesen Testfiles wurden anschließend die jeweiligen .dialog 
und .intent Dateien angelegt, ebenfalls mit Vorüberlegungen auf welche Weise der Benutzer
die Sätze jeweils anders formulieren könnte und dennoch eine Antwort erwartet.

## Implementierung





