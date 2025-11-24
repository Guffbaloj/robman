#En dialogbit består av flera ordböcker. 
#Godtagbara nycklar är:
#"text"      {string} Det som sägs
#"source"    {string} Vad som säger ljudet, pekar mot en bild. Om ingen så blir det ingen bild
#"duration"     {int} Hur långsamt texten sägs
#"color"      {tuple} Färgen på texten, om ingen så är texten vit.
#"special"   {string} om något ska hända, typ robs ansiktsuttryck
class DL:
    def __init__(self, text, source = "rob", duration = 2, color = (255, 255, 255), special = [], profile = "rob neutral"):
        self.text = text
        self.source = source
        self.profile = profile
        self.duration = duration
        self.color = color
        self.special = special
   
robCarDialog = [
    DL("Ja-sås… vi verkar ha tagit oss till en… uhm", special=["neutral"]),
    DL("Bilfabrik? kanske?", profile="rob huh1"),
    DL("Aja, det får agera gömställe", profile="rob worry2"),
    DL("Och med lite tur så kanske de inte hittar oss."),
    DL("…"),
    DL("Vet du vad, jag tror vi faktiskt skakade av oss dem.", profile="rob yay"),
    DL("BANK BANK BANK (osv)", profile="none", source = "none", special=["worry1"]),
    DL("Vi vet ni gömmer er där inne!", profile="none"),
    DL("Rackarns! De vet att vi gömmer oss här inne!", special=["worry2"]),
    DL("Kom ut med händerna över huvudet, så behöver ingen komma till skada", profile="none", source = "none"),
    DL("Jag kan inte återvända till robotfängelset!", profile="rob aah"),
    DL("Vi måste fly här ifrån!", profile="rob worry1"),
    DL("Men hur ska vi göra det??", special = ["neutral"], profile="rob worry1"),
    DL("Hmmm…. VÄNTA!"),
    DL("Vi är ju i en bilfabrik"),
    DL("Vi kan bygga en bil och köra iväg med den.", profile="rob yay"),
    DL("Jag drar och letar bitar i den där skräphögen där borta, Så pysslar du ihop bilen med dina bara händer…"),
    DL("JASSÅ NI VÄLJER DEN SVÅRA VÄGEN?", profile="none", source = "none"),
    DL("DÅ BRYTER VI NER DÖRREN", profile="none", source = "none"),
    DL("-KLONK-", profile="none", source = "none"),
    DL("…(aj fan, min fot)", profile="none", source = "none"),
    DL("VÄNTA NI BARA!", profile="none", source = "none"),
    DL("...", profile= "rob huh2"),
    DL("Bygg fort, innan han upptäcker dörrhandtaget", profile= "rob huh3"),
]
askrob0 = [DL("Jadu, denna skräphög verkar vara en hög med skräp."),
           DL("Något motorliknande borde det väll finnas?"),
           DL("Ahaa!")]

askRob1 = [DL("Sitter motorn?"),
           DL("Fler bitar säger du? Vadå fler bitar? Behövs det fler bitar till en bil än en motor."),
           DL("vänta! Här är några du kan använda!")]

askRob2 = [DL("Vad du ska skifta ämne hela tiden"),
           DL("")]
 #jag vet att dialog egentligen bara är två personer som talar, men lite får ni tåla
