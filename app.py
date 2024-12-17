import os
from flask import Flask, request, render_template
from google.cloud import storage, vision

app = Flask(__name__)

# Configuration du bucket
BUCKET_NAME = "analyseur-images-bucket"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        # Étape 1 : Upload du fichier dans Cloud Storage
        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(file.filename)
        blob.upload_from_file(file)

        # Générer l'URL publique
        public_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{file.filename}"

        # Étape 2 : Analyse avec Cloud Vision API
        vision_client = vision.ImageAnnotatorClient()
        image = vision.Image()
        image.source.image_uri = public_url
        response = vision_client.label_detection(image=image)

        # Récupérer les étiquettes détectées
        labels = [label.description for label in response.label_annotations]
        labels_text = ", ".join(labels)

        return f"""
        <h1>Analyse réussie !</h1>
        <p>URL de l'image : <a href="{public_url}">{public_url}</a></p>
        <p>Étiquettes détectées : {labels_text}</p>
        """
    return "Aucun fichier sélectionné.", 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Par défaut 8080
    app.run(host="0.0.0.0", port=port)
