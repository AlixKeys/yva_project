from django.shortcuts import render
from transformers import pipeline
import random

# --- Initialisation du modèle IA local ---
generator = pipeline("text-generation", model="gpt2")


# --- Page d'accueil ---
def home(request):
    return render(request, 'yva/home.html')


# --- Orientation Scolaire & Pro ---
def orientation_test(request):
    if request.method == 'POST':
        reponses = request.POST
        interet = reponses.get('interet')
        if interet == 'science':
            resultat = "Tu pourrais t’orienter vers les sciences ou l’ingénierie."
        elif interet == 'art':
            resultat = "Les arts, la communication ou le design semblent faits pour toi."
        elif interet == 'social':
            resultat = "Tu es peut-être destiné(e) aux métiers du social, de la santé ou de l’éducation."
        else:
            resultat = "On te conseille d'explorer plusieurs domaines via des mini-formations."

        return render(request, 'yva/orientation_result.html', {'resultat': resultat})
    
    return render(request, 'yva/orientation_form.html')


# --- Génération IA de mini-formation ---
def ia_formation(theme):
    prompt = (
        f"Donne une mini-formation claire et concise sur le thème : '{theme}', "
        "adaptée à la jeunesse togolaise (18-25 ans), avec des exemples locaux et des conseils pratiques. "
        "Sois motivant et concret, et donne des pistes d'action qu’un jeune au Togo pourrait suivre avec peu de moyens."
    )
    result = generator(prompt, max_length=200, num_return_sequences=1)
    texte = result[0]["generated_text"]
    return texte

def mini_formation(request):
    if request.method == 'POST':
        theme = request.POST.get('theme')
        formation = ia_formation(theme)
        return render(request, 'yva/formation_result.html', {'theme': theme, 'formation': formation})
    return render(request, 'yva/formation_form.html')


# --- Générateur IA de documents (CV ou lettre) ---
def generate_document(data, type_doc):
    prompt = f"""
    Génère un(e) {type_doc} professionnel(le) pour un jeune togolais :
    Nom : {data.get('nom')}
    Formation : {data.get('formation')}
    Expérience : {data.get('experience')}
    Objectif professionnel : {data.get('objectif')}
    Le ton doit être inspirant, structuré et adapté au marché de l’emploi local.
    """
    result = generator(prompt, max_length=300, num_return_sequences=1)
    return result[0]['generated_text']

def generate_doc(request):
    if request.method == 'POST':
        type_doc = request.POST.get('type_doc')  # 'cv' ou 'lettre'
        doc = generate_document(request.POST, type_doc)
        return render(request, 'yva/doc_result.html', {'doc': doc})
    return render(request, 'yva/doc_form.html')


# --- Coach IA : Réponse motivante personnalisée ---
def ia_conseiller(message):
    prompt = (
        f"Tu es un coach bienveillant. Donne une réponse motivante à ce message reçu d’un jeune togolais : '{message}'. "
        "Sois sincère, empathique et encourageant. Reste simple, mais puissant."
    )
    result = generator(prompt, max_length=150, num_return_sequences=1)
    return result[0]['generated_text']

def conseiller_virtuel(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        reponse = ia_conseiller(message)
        return render(request, 'yva/conseiller_result.html', {'message': message, 'reponse': reponse})
    return render(request, 'yva/conseiller_form.html')
