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
Feature: next-appointment

  Scenario Outline: next appointment
    Given an english speaking user
    When the user says <when is my next appointment>
    Then "nextcloud-calendar" should reply with anything
    And the reply should contain "appointment"

    Examples: When is my next appointment
      | when is my next appointment |
      | what is my next appointment |
      | when's my next appointment |
      | what's my next appointment |
      | when will my next appointment take place |
``` 
Im "Scenario Outline" wird der allgemein Testfall beschrieben. Da unsere Implementierung nur die englische Sprache unterstützt,
ist immer ein englischsprachiger Benutzer gegeben. Der `When-Then` Test beschreibt, was passiert, wenn ein Nutzer eine gewisse
Phrase verwendet. Im obigen Beispiel gibt es zwei Mögliche Fälle: Es gibt ein geplantes Event in der Zukunft oder eben nicht.
Die Gemeinsamkeit der Sprachausgabe für beide Fälle ist hier nur das Wort "appointment", weshalb nur geprüft wird, ob der Skill
überhaupt etwas antwortet und die Antwort "appointment" enthält.

Basierend auf den Scenarios der Testfiles wurden anschließend die jeweiligen .dialog 
und .intent Dateien angelegt, ebenfalls mit Vorüberlegungen auf welche Weise der Benutzer
die Sätze jeweils anders formulieren könnte und dennoch eine Antwort erwartet. Hierbei gilt zu beachten:

1. .intent-Dateien: Diese Dateien bilden das ab, was der Nutzer an Mycroft richtet.
2. .dialog-Dateien: Diese Dateien bilden die Antwortmöglichkeiten von Mycroft ab.
3. Insgesamt:   
- Worte in `()` bilden eine Auswahlmöglichkeit mehrerer Worte ab, die mit einem `|` getrennt werden. Zudem ist
es möglich ein "leeres" Feld zur Auswahl zu lassen, falls es möglich sein soll, keine der Möglichkeiten benutzen zu müssen.  
- Bei Worten in `{}` handelt es sich um Variablen, die später im Code verwendet werden können.

## Implementierung
Nach dem Anlegen der Sprachein- bzw. -ausgabe-Dateien war es wichtig und notwendig eine Schnittstelle zwischen dem Nextcloud-
Kalender und dem Skill herzustellen. Hier wurde die Verwendung von Caldav bereits empfohlen. Die eigentliche Implementierung
der Schnittstelle und des Skills an sich wird unter den nachfolgenden Punkt beschrieben.

### cal_dav_interface
Für die Implemmentierung der Schnittstelle zum Nexcloud Kalender wurden folgende Libraries verwendet:
- [CalDav](https://pypi.org/project/caldav/)
- [iCalendar](https://pypi.org/project/icalendar/)

Um die Schnittstelle zum Kalender abzubilden, wurde die Klasse `CalDavInterface` erstellt. Um die Verbindung zum Nextcloud Kalender aufbauen
zu können, wird die CalDav-Url, ein Username und ein Passwort benötigt. Diese drei Parameter sind in der [settingsmeta.yaml](./settingsmeta.yaml)
aufgelistet, was bedeutet, dass der User sie auf home.mycroft.ai in den Skill Settings nach der Installation des Skills setzen kann.
Sobald die festgelegten Login Details automatisch mit dem Gerät synchronisiert wurden, kann der Skill auf die Credentials zugreifen und
beim Instanzieren der Klasse an diese übergeben.

Der Klasse wurden alle benötigten Funktionen hinzugefügt, um mit dem Nextcloud Calender zu interagieren. Die Daten, die man bei der
Abfrage des Kalenders erhält, sind im Format eines *.ical* Strings. Um leichter in Python arbeiten zu können, wird der
*ical* String für jedes Event mithilfe der [iCalendar](https://pypi.org/project/icalendar/) geparst und in ein
Python Dictionary geschrieben, das dann den Titel, die Startzeit und die Endzeit enthält. Außerdem wird in dem Dictionary eine URL gespeichert,
die einen späteren Zugriff auf das eigentliche Event im Kalender über die [CalDav](https://pypi.org/project/caldav/) ermöglicht.

Vom MyCroft Skill genutzte Methoden sind:
- *get_next_event* um das nächste Event abzufragen, falls eines existiert
- *get_events_for_date* um alle Events an einem bestimmten Tag abzufragen
- *get_events_with_title* um Events zu einem gegebenen Title zu finden 
(wird für das Umbenennen und Löschen von spezifischen Events benötigt)
- *create_new_event* um ein neues Event anzulegen (hier wird die [iCalendar](https://pypi.org/project/icalendar/) Library
verwendet, um die festgelegten Event Details in ein *ical* String umzuwandeln, der von der [CalDav](https://pypi.org/project/caldav/)
Library verarbeitet werden kann)
- *delete_event* um ein Event anhand seiner Event Url zu löschen
- *rename_event* um einem Event anhand seiner Event Url einen neuen Event Title zu geben

### \_\_init__.py
Beim Starten des Skills wird zunächst geprüft, ob die benötigen Credentials für die Nextcloud verfügbar sind. Wenn ja, wird eine Instanz
des CalDavInterface erstellt. Ansonsten wird der User über die Sprachausgabe über die fehlenden Credentials informiert und das
empfohlene Vorgehen erklärt.  
Die Klasse für den Skill enthält insgesamt sechs Intent Handler Methoden:
1. *handle_get_next_appointment* für die Abfrage des Kalenders nach dem nächsten geplanten Termin. Je nach gegebenen Event Details,
wird für die entsprechende Ausgabe der passende Name der .dialog Datei zusammengebaut und die vorhandenen Informationen übergeben.
2. *handle_get_appointment_date* für die Abfrage des Kalenders der Termine an einem bestimmten Tag. Sind Termine an dem Tag geplant
wird zunächst nur die Anzahl der geplanten Termine ausgegeben und der User anschließend gefragt, ob die Termine aufgelistet werden sollen.
3. *handle_delete_event* für das Löschen eines Termins aus dem Kalender. Zunächst wird basierend auf den vom User gegebenen
Informationen (Titel, Datum) nach einem übereinstimmenden Event gesucht. Gibt es mehrere Übereinstimmungen, wird der User nach einer
genauen Angabe des zu löschenden Events gefragt. Bevor das Event endgültig gelöscht wird, muss der User dies noch einmal bestätigen.
4. *handle_rename_event* für das Umbennen eines Termins im Kalender. Zunächst wird basierend auf den vom User gegebenen
Informationen (Titel, Datum) nach einem übereinstimmenden Event gesucht. Gibt es mehrere Übereinstimmungen, wird der User nach einer
genauen Angabe des umzubenennenden Events gefragt. Anschließend muss der User noch den gewünschten, neuen Titel des Termins angeben.
5. *handle_create_event* für das Anlegen eines neuen Termins. Je nach Umfang der Informationen in der initialen Intent Message,
wird der User nach mehr oder weniger weiteren Informationen gefragt. Benötigt werden Titel, Datum, Startzeit (bzw. ganztägig) und
Dauer, wovon Titel, Datum und Startzeit ggf. schon aus der initialen Intent Message herausgelesen werden können.
6. *handle_connect_to_calendar* für den Verbindungsaufbau zum Kalender, nachdem auf home.mycroft.ai die Credentials eingetragen
und auf das Gerät synchronisiert wurden.  
Zusätzlich enthält die Klasse unterschieldliche Hilfsmethoden, unter anderem um durch unterschiedliche Rückfragen die jeweils genauen Events
vom User zu erfragen.  
An mehreren Stellen werden Funktionen des [mycroft.util](https://mycroft-core.readthedocs.io/en/latest/source/mycroft.html#mycroft-util)
Packages verwendet:
- *nice_time* und *nice_date*, um *datetime* Objekte in ein besseres Output Formt zu bringen
- *extract_datetime* um aus den Nachrichten der Spracheingabe Datumsangaben in *datetime* Objekte zu parsen
- *extract_duration* um aus den Nachrichten der Spracheingabe *timedelta* Objekte zu erhalten
- *extract_number* um aus den Nachrichten der Spracheingabe *Integer* zu erhalten
- *default_timezone* um die Zeitzone des Users zu erfahren, damit die Zeitangaben der Termine korrekt ausgegebene werden können

### Code-Dokumentierung
Für die Aufgabe war die Code-Dokumentierung in Python Docstrings gemäß der Google-Styleguidelines gefordert.
Die Guidelines sind unter folgendem [Link](https://google.github.io/styleguide/pyguide.html) zu finden.

## Learnings
Insgesamt lässt sich bei den Learnings Folgendes festhalten:

### Positives:
1. Der allgemeine Umgang mit einem Raspberry sowie weiterer an den Pi verbundene Hardware und die daraus resultierenden 
Probleme mit Treibern und Einstellungen unter Linux konnten hier noch einmal sehr gut vertieft werden. 
2. Das Kennenlernen eines OpenSource Sprachassistententools (MyCroft) war sehr spannend.
3. Es war sehr interessant, die Schnittstelle Caldav und iCalendar und allem was dazugehört, zu benutzen und den Umgang 
damit zu üben. Bisher hatten wir beide noch keine Erfahrung damit.

### Negatives:
1. Beim Testen des eigenen Skills und dessen Funktionen kam es sehr häufig dazu, dass die Spracherkennung einzelne Worte
nicht richtig nachvollziehen konnte oder sie falsch verstanden hat. Gelegentlich kam es so zu Konflikten mit anderen Skills.
Aber insbesondere mit Eigennamen kam es doch auch häufiger zu Schwierigkeiten, was für einen Kalender Skill
denkbar schlecht ist. Gerade beim Anlegen eines neuen Kalendereintrags werden
doch häufiger Namen bzw. Eigennamen verwendet. Werden diese nicht richtig erkannt, führt das möglicherweise zur Frustration
bei Usern.
2. Bei den Vorüberlegungen ist bereits unser Testing beschrieben. Hier ist uns aufgefallen, dass bei den automatischen Tests
bei mehrmaligen Durchläufen unter denselben Bedingungen willkürliche Fehler auftreten, die bei manuellem Testing nicht
vorkommen oder sich nicht reproduzieren lassen. Nach kurzer Recherche sind wir auf folgenden [Blog-Artikel](https://community.mycroft.ai/t/voight-kampff-how-you-can-help-addatest/8690) in der 
Mycroft-Community aufmerksam geworden. Hier wird die Einführung der Tests angekündigt, im letzten Absatz ist aber auch die
Rede davon, dass sie durch diese Tests auch auf Fehler in ihren offiziellen Skills aufmerksam geworden sind, die sie sich
mitunter auch nicht erklären können. Unter folgendem [Link](https://github.com/search?q=org%3AMycroftAI+xfail&type=Code) sind alle derzeit bekannten fehlerhaften Tests von Marketplace
Skills hinterlegt. Da es sich um ein recht junges Feature handelt, scheint es noch nicht komplett fehlerfrei zu laufen.  
So ist uns beispielsweise aufgefallen, dass ein Test fehlschlägt, wenn eine Zahl ausgeschrieben wird, der gleiche Test aber
erfolgreich durchläuft, wenn die Zahl als tatsächliches Zahlsymbol eingefügt wird, ein Umstand der sich bei einer Spracherkennungssoftware
nicht ganz erklären lässt.

