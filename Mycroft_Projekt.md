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

## Weiteres Vorgehen / Vorüberlegungen
Für die Einrichtung und das Starten von Mycroft haben wir hauptsächlich die Mycroft eigene Anleitung
verwendet. ([Anleitung](https://mycroft-ai.gitbook.io/docs/skill-development/introduction/your-first-skill))
Nach dieser haben wir auch unseren ersten eigenen Skill angelegt. Hierbei wird man mit dem Befehl mycroft-msk create` 
durch ein interatktives Skript geführt in dem man einige grundlegende Fragen zur Funktionalität beantowrten muss
und es wird ein allgemeines Skill Template erstellt. Folgende Fragen bzw. Abfragen waren zu beantworten.
1. Name: Der Name des Projektes sollte möglichst kurz und prägnant sein, von Mycroft selbst wird hier eine Länge
bis zu maximal 22 Zeichen vorgeschlagen. Desweiteren muss der Name einzigartig sein innerhalb des Mycroft Marketplaces.
2. Beispielsätze: Hier sollten Äußerungen eingetragen werden, die vom User erwartet werden und auf die der Skill dann 
reagieren soll.
3. Antwortdialog: Der Dialog oder die Dialoge mit denen der Skill antworten wird.
4. Kurze Erklärung: Ein Einzeiler zur Erklärung des Skills, der nach Mycroft unter 40 Zeichen lang sein sollte.
5. Lange Erklärung: Eine ausführliche Erklärung, die beliebig lang sein darf.
6. Author: Hier konnte bereits ein Authorenname eingetragen werden.
7. Kategorien: Kategorien, unter die der Skill fehlt, die dann im Marketplace benutzt werden. Wichtig um den Skill richtig
einzuordnen. Die erste ausgewählte Kategorie ist die Default-Kategorie.
8. Tags: Beliebig wählbare Tags, die es anderen Nutzern erleichtern soll, den Skill zu finden.

Anschließend an dieses Skript wird man gefragt, ob ein Github Repo angelegt werden soll, was Relevanz bekommt, so fern 
man den Skill im Marketplace veröffentlichen möchte.
 

Nach dem Anlegen des Skills, ging es weiter mit der Überlegung welche Grundfunktionen denn insgesamt 
möglich sein sollten und dazu wurden nach folgendem [Schema](https://mycroft-ai.gitbook.io/docs/skill-development/voight-kampff) Testfiles angelegt. 
Ein solches Testfile besteht aus den einzelnen Tests für die Funktionalitäten des Skills. Anhand folgenden Beispiels werden
die Optionen erklärt:   
 ```
 Feature: nextcloud-calendar 

 Scenario: number of appointments today  
    Given an english speaking user   
     When the user says <number of appointments today>                
     Then "nextcloud-calendar" should reply with dialog from "number.appointments.today.dialog" 

  Examples: How many appointments do I have today  
    | number of appointments today |  
    | how many appointments do I have today |
``` 
Im Scenario wird der allgemein Testfall beschrieben. Da unsere Implementierung nur die englische Sprache unterstützt,
ist immer ein englischsprachiger Benutzer gegeben. Der `When-Then` Test beschreibt, was passiert, wenn ein Nutzer eine gewisse
Phrase verwendet, im obigen Beispiel soll also die Zahl der Events für den heutigen Tag ausgegeben werden, wenn der 
Nutzer danach fragt.

Basierend auf diesen Testfiles wurden anschließend die jeweiligen .dialog 
und .intent Dateien angelegt, ebenfalls mit Vorüberlegungen auf welche Weise der Benutzer
die Sätze jeweils anders formulieren könnte und dennoch eine Antwort erwartet.

Da in unseren Vorüberlegungen bereits die Bonus-Aufgaben beinhaltet waren, haben wir für den Anfang die zugehörigen, nicht 
benötigten Dateien vorerst in einem separaten Branch ausgelagert.

## Implementierung

### cal_dav_interface

### ___init___


## Learnings





