robCarIntro = ["så...","då var vi här","bilfabriken",
"(hör bankande ljud)", "Shit,","Det blav just högsta prio att du bygger en bil",
"det dröjer nog inte så värst länge tills att de river den där dörren ska du se",
"...","men du har nog tid att bygga en bil från grunden","du är nog snabb...",
"hoppas jag...","uhm, men om du inte är det vill jag påminna dig om att de inte var särkiljt glada med vad vi gjorde i förra delen av spelet",
"du vet vilken jag talar om"]

#En dialogbit består av flera ordböcker. 
#Godtagbara nycklar är:
#"text"      {string} Det som sägs
#"source"    {string} Vad som säger ljudet, pekar mot en bild. Om ingen så blir det ingen bild
#"duration"     {int} Hur långsamt texten sägs
#"color"      {tuple} Färgen på texten, om ingen så är texten vit.
#"special"   {string} om något ska hända, typ robs ansiktsuttryck
class DL:
    def __init__(self, text, source = "rob", duration = 2, color = (255, 255, 255), special = []):
        self.text = text
        self.source = source
        self.duration = duration
        self.color = color
        self.special = special
    
robCarDialog = [
    DL("Ja-sås… vi verkar ha tagit oss till en… uhm", special=["rob neutral"]),
    DL("Bilfabrik? kanske?"),
    DL("Aja, det får agera gömställe"),
    DL("Och med lite tur så kanske de inte hittar oss."),
    DL("…"),
    DL("Vet du vad, jag tror vi faktiskt skakade av oss dem."),
    DL("BANK BANK BANK (osv)", source="base",special=["rob worry"]),
    DL("Vi vet ni gömmer er där inne!", source="base"),
    DL("Rackarns! De vet att vi gömmer oss här inne!"),
    DL("Kom ut med händerna över huvudet, så behöver ingen komma till skada", source="base"),
    DL("Jag kan inte återvända till robotfängelset!"),
    DL("Vi måste fly här ifrån!"),
    DL("Men hur ska vi göra det??", special = ["rob neutral"]),
    DL("Hmmm…. VÄNTA!"),
    DL("Vi är ju i en bilfabrik"),
    DL("Vi kan bygga en bil och köra iväg med den."),
    DL("Jag drar och letar bitar i den där skräphögen där borta, Så pysslar du ihop bilen med dina bara händer…"),
    DL("JASSÅ NI VÄLJER DEN SVÅRA VÄGEN?", source="base"),
    DL("DÅ BRYTER VI NER DÖRREN", source="base"),
    DL("-KLONK-", source="base"),
    DL("…(aj fan, min fot)", source="base"),
    DL("VÄNTA NI BARA!", source="base"),
    DL("..."),
    DL("Bygg fort, innan han upptäcker dörrhandtaget"),
]

 #jag vet att dialog egentligen bara är två personer som talar, men lite får ni tåla
