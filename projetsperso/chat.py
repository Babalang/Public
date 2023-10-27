import openai
#Tentative de création d'un chat avec chatgpt.
# Définir votre clé d'API d'OpenAI
openai.api_key = "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"

# Fonction pour envoyer une requête à ChatGPT
def envoyer_requete(texte):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=texte,
        max_tokens=50,
        temperature=0.7,
        top_p=1.0,
        n=1,
        stop=None,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    return response.choices[0].text.strip()

# Boucle de conversation
print("Bienvenue ! Vous pouvez commencer à discuter avec moi.")
while True:
    utilisateur_saisie = input("Utilisateur: ")
    if utilisateur_saisie.lower() == 'bye':
        print("ChatGPT: Au revoir !")
        break

    reponse = envoyer_requete(utilisateur_saisie + '\nChatGPT:')
    print("ChatGPT:", reponse)
