robCarIntro = ["så...","då var vi här","bilfabriken",
"(hör bankande ljud)", "Shit,","Det blav just högsta prio att du bygger en bil",
"det dröjer nog inte så värst länge tills att de river den där dörren ska du se",
"...","men du har nog tid att bygga en bil från grunden","du är nog snabb...",
"hoppas jag...","uhm, men om du inte är det vill jag påminna dig om att de inte var särkiljt glada med vad vi gjorde i förra delen av spelet",
"du vet vilken jag talar om"]

#En dialogbit består av flera ordböcker. 
#Godtagbara nycklar är:
#"text"     {string} Det som sägs
#"source"   {string} Vad som säger ljudet, pekar mot en bild. Om ingen så blir det ingen bild
#"duration"    {int} Hur långsamt texten sägs
#"color"     {tuple} Färgen på texten, om ingen så är texten vit.
robCarDialog = [{"text":"hej", "source":"rob", "duration": 2}, {"text":"hoj", "source":"rob", "duration": 2}] #jag vet att dialog egentligen bara är två personer som talar, men lite får ni tåla
