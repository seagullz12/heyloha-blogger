from email_sender import send_email

test_html = """
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html lang="nl">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Heyloha Blog</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    <style type="text/css">
        body { font-family: 'Roboto', sans-serif; color: #333333; background-color: #FFFCF3; line-height: 1.6; margin: 0; padding: 0; }
        .blog-container { max-width: 800px; margin: 20px auto; padding: 25px; background-color: #FFFFFF; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.05); }
        h1, h2, h3 { font-family: 'Roboto', sans-serif; color: #4AAB9A; margin-top: 1.5em; margin-bottom: 0.8em; line-height: 1.2; }
        h1 { font-size: 2.2em; }
        h2 { font-size: 1.8em; }
        h3 { font-size: 1.4em; }
        p { font-family: 'Roboto', sans-serif; color: #333333; margin-bottom: 1em; }
        a { font-family: 'Roboto', sans-serif; color: #EF7D62; text-decoration: none; font-weight: bold; }
        ul { font-family: 'Roboto', sans-serif; color: #333333; list-style-type: none; padding-left: 0; margin-bottom: 1em; }
        li { font-family: 'Roboto', sans-serif; color: #333333; }
        strong { font-weight: bold; }
        em { font-style: italic; }
    </style>
</head>
<body style="font-family: 'Roboto', sans-serif; color: #333333; background-color: #FFFCF3; line-height: 1.6; margin: 0; padding: 0;">
    <div class="blog-container" style="max-width: 800px; margin: 20px auto; padding: 25px; background-color: #FFFFFF; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.05);">
        <div style="text-align: center; margin-bottom: 20px;">
            <img src="https://www.heyloha.ai/wp-content/uploads/2025/05/Heyloha-3.png" alt="Heyloha Logo" style="max-width: 200px; height: auto;">
        </div>
        <h1 style="font-family: 'Roboto', sans-serif; color: #4AAB9A; margin-top: 1.5em; margin-bottom: 0.8em; line-height: 1.2;font-size: 2.2em;">Slimmer Klantcontact met AI: De Toekomst van Klantenservice</h1>
        <p style="font-family: 'Roboto', sans-serif; color: #333333; margin-bottom: 1em;">In de wereld van klantenservice zien we een opvallende trend. Bedrijven omarmen steeds vaker de kracht van Artificial Intelligence (AI) om hun klantcontact te verbeteren. Een recent artikel van Tech Today benadrukt hoe nieuwe AI-tools bedrijven helpen om klantvragen sneller te beantwoorden. Dit is niet alleen een technologische doorbraak, maar ook een kans om de klantbeleving aanzienlijk te verbeteren.</p>
        <h2 style="font-family: 'Roboto', sans-serif; color: #4AAB9A; margin-top: 1.5em; margin-bottom: 0.8em; line-height: 1.2;font-size: 1.8em;">Wat zijn AI-tools en hoe werken ze?</h2>
        <p style="font-family: 'Roboto', sans-serif; color: #333333; margin-bottom: 1em;">AI-tools maken gebruik van geavanceerde algoritmes die klantfeedback en vragen analyseren. Door deze technologie kunnen bedrijven veel sneller inspelen op de behoeften van hun klanten. In plaats van dat een medewerker handmatig elke vraag moet verwerken, kan AI deze taken automatiseren. Dit leidt tot een snellere responstijd en een efficiënter werkproces.</p>
        <p style="font-family: 'Roboto', sans-serif; color: #333333; margin-bottom: 1em;">Stel je voor dat je als klant een vraag hebt. In plaats van lange wachttijden aan de telefoon of eindeloos zoeken op een website, krijg je binnen enkele seconden een antwoord dat specifiek op jouw vraag is afgestemd. Dit is de toekomst van klantcontact, en bedrijven die deze technologie omarmen, zullen een streepje voor hebben.</p>
        <h2 style="font-family: 'Roboto', sans-serif; color: #4AAB9A; margin-top: 1.5em; margin-bottom: 0.8em; line-height: 1.2;font-size: 1.8em;">Heyloha en de voordelen van AI</h2>
        <p style="font-family: 'Roboto', sans-serif; color: #333333; margin-bottom: 1em;">Bij Heyloha begrijpen we dat klantcontact niet alleen om snelheid draait, maar ook om kwaliteit. Onze slimme oplossingen zijn ontworpen om bedrijven te helpen bij het efficiënt beheren van klantvragen. Door gebruik te maken van AI kunnen we de werkdruk van medewerkers verminderen en tegelijkertijd de klanttevredenheid verhogen. Dit sluit perfect aan bij de trends die in het artikel worden besproken.</p>
        <p style="font-family: 'Roboto', sans-serif; color: #333333; margin-bottom: 1em;">Met Heyloha kunnen bedrijven profiteren van een geautomatiseerde klantenservice die niet alleen de snelheid verbetert, maar ook de consistentie en relevantie van de antwoorden. Dit zorgt ervoor dat klanten zich gehoord en gewaardeerd voelen, wat cruciaal is voor hun loyaliteit.</p>
        <h2 style="font-family: 'Roboto', sans-serif; color: #4AAB9A; margin-top: 1.5em; margin-bottom: 0.8em; line-height: 1.2;font-size: 1.8em;">De toekomst van klantenservice</h2>
        <p style="font-family: 'Roboto', sans-serif; color: #333333; margin-bottom: 1em;">De integratie van AI in klantcontact is meer dan een tijdelijke trend; het is de toekomst. Bedrijven die nu investeren in deze technologie zullen niet alleen de tevredenheid van hun klanten verhogen, maar ook de efficiëntie van hun medewerkers verbeteren. Dit is een win-winsituatie die leidt tot een hogere productiviteit en betere service.</p>
        <p style="font-family: 'Roboto', sans-serif; color: #333333; margin-bottom: 1em;">Het artikel van Tech Today biedt een inspirerende kijk op hoe AI-tools kunnen bijdragen aan een beter klantcontact. En met innovaties zoals die van Heyloha wordt deze toekomst al werkelijkheid. Wil je meer weten over hoe wij bedrijven helpen bij het optimaliseren van klantcontact? Neem dan een kijkje op <a href="https://heyloha.ai" style="font-family: 'Roboto', sans-serif; color: #EF7D62; text-decoration: none; font-weight: bold;">heyloha.ai</a>.</p>
        <h2 style="font-family: 'Roboto', sans-serif; color: #4AAB9A; margin-top: 1.5em; margin-bottom: 0.8em; line-height: 1.2;font-size: 1.8em;">Bron</h2>
        <p style="font-family: 'Roboto', sans-serif; color: #333333; margin-bottom: 1em;">Dit artikel is geïnspireerd door het artikel "AI verbetert klantcontact: Nieuwe AI-tools helpen bedrijven klantvragen sneller te beantwoorden" van Tech Today. Je kunt het volledige artikel hier lezen: <a href="https://techtoday.com/ai-verbeterd-klantcontact" style="font-family: 'Roboto', sans-serif; color: #EF7D62; text-decoration: none; font-weight: bold;">Tech Today</a>.</p>
    </div>
</body>
</html>
"""

send_email(test_html)