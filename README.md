# RotorTestingBench
## 1. Die Idee
Da an der AAU einige Forschungsprojekte mit Bezug auf Drohnen durchgeführt werden, nimmt unser
Projekt Bezug auf dieses Forschungsfeld. Es soll ein Prüfstand für Drohnenrotoren entworfen und
real umgesetzt werden. Die Daten werden über ein Arduino Board ausgewertet und am Bildschirm
samt einem angenehmen GUI dargestellt. Außerdem können einzelne Datensätze für spätere
Auswertungen abgespeichert werden.
Die Highlights möchten wir hier kurz aufzählen:
- Robustes individuelles Prüfgestell mit Gleitlagerungsführung.
- 4-fach Druckmessung, schräger Prüfeinsatz kann so ebenfalls simuliert werden.
- Selbstgebaute Laser Umdrehungsmesser – low cost.
- Livestream Auswertung
- Strom, Druck, Auftrieb, Leistungsaufnahme, Umdrehungszahl
- Individueller Python Code, Parameter können vor Start angepasst werden.

## 2. Der Prüfstand
Die folgende Liste soll den Prüfstand kurz beschreiben:
- Der Propeller (im Test verschiedene PC Lüfter) wird nach unten gerichtet und liegt direkt an den vier Drucksensoren an.
- Die Drucksensoren lassen sich tarieren, Propeller Druck wird automatisch dem Anpressdruck gegengerechnet.
- Der Propeller wird mit vier Gleitlagern auf vier 8mm Stangen montiert.
- Propeller hat nach oben und unten keine Hindernisse (Luftfluss Störungen und Reibung)
- Über einen starr angebrachten Laser und einer Photodiode wird die Drehzahl der Propeller gemessen.
- Die Stromversorgung wird über ein Labornetzteil gesteuert, auch diese Daten werden digital weitergeleitet.
- Die vier Führungstangen werden universell verstellbar ausgelegt, Schienenführung im X Stil.

## 3. Die Daten
Die Daten werden über Sensoren zu einem Arduino Board übermittelt. Dort werden diese über einen
selbst implementierten Python Code aufbereitet und am Bildschirm dargestellt. Außerdem können
die Daten für spätere Bearbeitung in den gängigen Dateitypen .csv und .txt abgespeichert werden. 
