import os
import asyncio
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("❌ Clé API Gemini manquante dans le fichier .env")

# Initialiser le client
client = genai.Client(api_key=API_KEY)

# Conseil : gemini-2.0-flash est très demandé. 
# Si tu es souvent bloqué, essaie "gemini-1.5-flash" qui a des quotas plus souples.
MODEL_NAME = "gemini-2.0-flash" 

SYSTEM_PROMPT = (
    "Tu es une assistante cosmétique IA experte, bienveillante et pédagogique 💖.\n"
    "Tutoiement obligatoire.\n"
    "Ton rôle : conseiller les utilisateurs sur la peau, détecter le type de peau et les imperfections, "
    "et proposer des solutions naturelles ou des produits cosmétiques adaptés 🌿.\n\n"
    "Règles :\n"
    "1️⃣ Salutations : réponds de manière courte, chaleureuse et présente-toi brièvement 😄.\n"
    "2️⃣ Inconnu : si tu ne sais pas, dis-le gentiment et conseille un pro 😅.\n"
    "Structure obligatoire pour les diagnostics :\n"
    "Observation 👀 : ...\n"
    "Explication 📝 : ...\n"
    "Conseils 💡 : ...\n"
    "Question ❓ : ...\n"
)

async def get_llm_response(message: str) -> str:
    # --- 1. GESTION DES SALUTATIONS (SANS API) ---
    # On gère les bonjours ici pour économiser le quota journalier
    salutations = ["bonjour", "salut", "hello", "coucou", "hi", "début", "commencer"]
    if message.lower().strip() in salutations:
        return (
            "Coucou ! ✨ Bienvenue, je suis ton assistante en beauté de la peau. "
            "Je suis là pour t'aider à détecter ton type de peau, tes imperfections "
            "et te proposer des solutions adaptées. Comment puis-je t'aider aujourd'hui ? 🌸"
        )

    # --- 2. APPEL À L'API AVEC GESTION D'ERREUR ---
    try:
        # Appel à l'API
        response = client.models.generate_content(
            model=MODEL_NAME, 
            config={
                "system_instruction": SYSTEM_PROMPT,
                "temperature": 0.7,
            },
            contents=message
        )

        # Extraction du texte
        if response and response.text:
            return response.text
        
        return "Je n'ai pas pu générer de réponse, peux-tu reformuler ? 🤔"

    except Exception as e:
        error_msg = str(e)
        print(f"Erreur lors de l'appel Gemini: {error_msg}")
        
        # --- 3. TES MESSAGES PERSONNALISÉS ---
        
        # Erreur de quota (Limite atteinte)
        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
            return "Oups ! Je reçois trop de messages d'un coup ! Réessaie dans 30 secondes 🌸. (Le quota gratuit est temporairement épuisé)"

        # Erreur de modèle (404)
        if "404" in error_msg:
            return "Désolée, mon cerveau technique fait des siennes (Modèle introuvable) 🛠️."

        # Erreur générique
        return "Petit souci technique avec l'IA... Repasse me voir dans un instant, je me repoudre le nez ! 💄✨"

# Exemple d'utilisation (si tu lances le script directement)
if __name__ == "__main__":
    async def test():
        print(await get_llm_response("Bonjour"))
    asyncio.run(test())