# Configuration des credentials Google Earth Engine

Ce dossier est destiné à stocker les credentials de votre compte de service Google Earth Engine.

## Étapes pour obtenir et configurer les credentials

1. **Créez un compte Google Earth Engine**
   - Visitez [https://earthengine.google.com/](https://earthengine.google.com/)
   - Inscrivez-vous ou connectez-vous avec votre compte Google
   - Acceptez les conditions d'utilisation

2. **Créez un projet dans Google Cloud Console**
   - Allez sur [https://console.cloud.google.com/](https://console.cloud.google.com/)
   - Créez un nouveau projet ou sélectionnez un projet existant
   - Notez l'ID de votre projet

3. **Activez l'API Earth Engine**
   - Dans la console Google Cloud, allez dans "APIs & Services" > "Library"
   - Recherchez "Earth Engine" et activez l'API "Google Earth Engine"

4. **Créez un compte de service**
   - Dans la console Google Cloud, allez dans "IAM & Admin" > "Service Accounts"
   - Cliquez sur "Create Service Account"
   - Donnez un nom et une description au compte de service
   - Attribuez le rôle "Earth Engine Resource Viewer" (ou plus si nécessaire)
   - Cliquez sur "Done"

5. **Créez une clé pour le compte de service**
   - Dans la liste des comptes de service, cliquez sur le compte que vous venez de créer
   - Allez dans l'onglet "Keys"
   - Cliquez sur "Add Key" > "Create new key"
   - Sélectionnez le format JSON
   - Téléchargez le fichier de clé

6. **Enregistrez le compte de service dans Earth Engine**
   - Allez sur [https://developers.google.com/earth-engine/guides/service_account](https://developers.google.com/earth-engine/guides/service_account)
   - Suivez les instructions pour enregistrer l'adresse e-mail de votre compte de service

7. **Placez le fichier de credentials dans ce dossier**
   - Renommez le fichier téléchargé en `gee-credentials.json`
   - Placez-le dans ce dossier (`credentials/`)

## Structure du fichier credentials

Le fichier `gee-credentials.json` doit avoir une structure similaire à celle-ci:

```json
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "your-service-account@your-project-id.iam.gserviceaccount.com",
  "client_id": "...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project-id.iam.gserviceaccount.com"
}
```

⚠️ **ATTENTION**: Ne partagez jamais ce fichier et ne le committez pas dans un dépôt Git. Il contient des informations sensibles qui pourraient être utilisées pour accéder à votre compte Google Cloud.

## Authentification automatique

Cette application est configurée pour utiliser automatiquement les credentials stockés dans ce dossier. Le fichier `gee-credentials.json` est utilisé pour initialiser Google Earth Engine au démarrage de l'application.

## Dépannage

Si vous rencontrez des problèmes d'authentification:

1. Vérifiez que le fichier est correctement nommé (`gee-credentials.json`)
2. Assurez-vous que le compte de service est bien enregistré dans Earth Engine
3. Vérifiez que les permissions du fichier sont correctes (lisible par l'application)
4. Redémarrez l'application après avoir ajouté ou modifié le fichier de credentials

## Ressources supplémentaires

- [Guide d'authentification Google Earth Engine](https://developers.google.com/earth-engine/guides/authentication)
- [Documentation des comptes de service](https://cloud.google.com/iam/docs/service-accounts)
- [FAQ Earth Engine](https://developers.google.com/earth-engine/faq)

Si vous avez des questions ou des problèmes, consultez la documentation officielle de Google Earth Engine ou contactez l'assistance Google Cloud.
