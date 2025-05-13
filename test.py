import requests

# Paramètres de la requête
url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
params = {
    "location": "40.477797,-80.102807",  # Coordonnées (lat,lng) Latitude: 5.4247309, Longitude: -4.0003111
    "radius": 2000,                      # Rayon en mètres
    "type": "restaurant",                # Type de lieu
    "key": "AIzaSyDjV8aSDctyyV6xcWKPJS1C77AjyI9H7pg"  # Clé API (à remplacer si nécessaire)
}

# Exécution de la requête
response = requests.get(url, params=params)
data = response.json()  # Conversion de la réponse en JSON

# Affichage des résultats (simplifié)
print("Statut de la réponse:", data.get("status"))
print("Nombre de résultats:", len(data.get("results", [])))
# print(data.get("results", [])[:3])

# Détails des premiers résultats (exemple)
# for i, place in enumerate(data.get("results", [])[:3]):  # Affiche les 3 premiers
#     print(f"\nRésultat {i + 1}:")
#     print("Nom:", place.get("name"))
#     print("Adresse:", place.get("vicinity"))
#     print("Note:", place.get("rating", "Non disponible"))
#     print("ID:", place.get("place_id"))


# Détails des premiers résultats avec commentaires
for i, place in enumerate(data.get("results", [])[:10]):  # Affiche les 3 premiers
    print(f"\nRésultat {i + 1}:")
    print("Nom:", place.get("name"))
    print("Adresse:", place.get("vicinity"))
    print("Note moyenne:", place.get("rating", "Non disponible"))
    print("ID:", place.get("place_id"))
    
    # Afficher les commentaires et évaluations individuelles
    reviews = place.get("reviews", [])
    if reviews:
        print("\nAvis des utilisateurs:")
        for j, review in enumerate(reviews[:5]):  # Affiche les 5 premiers commentaires
            print(f"\n  Avis {j + 1}:")
            print("  Auteur:", review.get("author_name", "Anonyme"))
            print("  Note:", review.get("rating", "Non disponible"))
            print("  Texte:", review.get("text", "Pas de commentaire"))
            print("  Date:", review.get("relative_time_description", "Date inconnue"))
    else:
        print("\nAucun avis utilisateur disponible.")