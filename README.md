# AVA Public — version 0.1 expérimentale

Créée pour Oreo / Jordan Pradel. Projet Windows à ouvrir dans VS Code.

## Installation rapide

1. Installer Node.js LTS (https://nodejs.org) puis extraire **tout** le ZIP.
2. Ouvrir ce dossier dans VS Code. Double-cliquer INSTALLER.bat, puis DEMARRER.bat.
3. Créer un profil avec un nom et un code personnel de 6 à 12 chiffres. Ouvrir ce profil.
4. Ajouter une clé personnelle depuis https://platform.openai.com/api-keys. Une facturation API active est nécessaire ; ChatGPT Plus ne finance pas ces appels.
5. Accepter l'écoute puis cliquer « Parler avec AVA ». La voix par défaut est marin, modifiable avant la connexion.
6. Pour la caméra, cliquer « Activer / couper ». L'aperçu reste local tant que le partage d'images n'est pas coché.
7. Pour obtenir l'installateur Windows : CONSTRUIRE_EXE.bat. Le résultat sera dans dist/.

Le ZIP contient les sources et la recette de compilation, **pas un EXE précompilé**. La compilation Windows n'a pas été exécutée sur Windows dans cet environnement.

## Ce qui est implémenté

- Conversation vocale OpenAI Realtime via WebRTC ; détection de parole et interruption automatique de la réponse.
- Choix des voix marin, coral, shimmer, sage. Ce sont des voix API : aucune garantie qu'elles soient identiques à la voix sélectionnée dans ChatGPT.
- Aperçu webcam local et partage optionnel d'une image toutes les 15 secondes : pas un flux vidéo continu.
- Profils séparés, code personnel, souvenirs saisis volontairement, oubli et suppression.
- Clé API dans le processus principal, chiffrée via Electron safeStorage quand Windows le permet. Jamais intégrée aux fichiers distribués.
- Reconnaissance locale expérimentale du visage et de la voix, si les dépendances Python sont installées.
- Mode verrouillé : visage ET voix vérifiés avant de connecter le microphone ; visage revérifié toutes les 3 secondes et déconnexion en cas d'absence ou d'erreur.
- Micro arrêté au verrouillage, à l'arrêt et à la fermeture. Session limitée localement à 20 minutes pour éviter une écoute payante oubliée.

## Biométrie optionnelle

Installer Python 3.11 ou 3.12 depuis https://www.python.org, avec « Add Python to PATH », puis lancer INSTALLER_BIOMETRIE.bat. PyTorch et le modèle de voix peuvent entraîner un téléchargement important au premier usage. Le visage utilise OpenCV LBPH ; la voix utilise les embeddings Resemblyzer.

Activer la caméra, se placer seul devant, enregistrer le visage. Enregistrer la voix en parlant 5 secondes, puis activer le mode verrouillé. Un casque réduit les échos. Les seuils (visage 65 / voix 0.78) sont des valeurs de départ non calibrées : faux positifs et faux négatifs possibles. Pas de détection anti-photo ni anti-enregistrement. Ne pas utiliser comme authentification forte.

**Limite majeure : la voix n'est vérifiée qu'avant la session. Une autre personne peut ensuite être entendue et obtenir une réponse. L'exclusivité continue visage + voix demandée n'est donc pas terminée.** La vérification continue du locuteur nécessiterait de retenir l'audio localement avant envoi, avec une latence supplémentaire et des tests réels. AVA ne prétend pas savoir qui parle grâce à l'API.

## Apprentissage, confidentialité et créateur

La mémoire est une liste de souvenirs édités par l'utilisateur, réinjectés au début d'une nouvelle session. Le modèle n'est pas réentraîné. Pas d'apprentissage partagé entre amis : leurs confidences restent séparées. Les conversations sont affichées temporairement mais ne sont pas sauvegardées par le programme. Les empreintes biométriques et souvenirs sont stockés localement dans le dossier de données Electron, sous Windows généralement %APPDATA%/ava-public. Souvenirs et empreintes ne sont pas chiffrés par cette version ; les permissions Windows protègent seulement leur accès ordinaire.

Le nom du créateur et les limites de permissions sont fixés dans les instructions applicatives. Le premier profil porte un indicateur owner, mais ce prototype ne fournit pas d'administration distante ni de console propriétaire. Aucun profil ne peut lire les souvenirs d'un autre via l'interface. **Une copie du code peut être modifiée : aucune promesse de loyauté absolue ou d'impossibilité de détournement.** AVA n'a aucun outil pour exécuter du code, surveiller Discord, envoyer des alertes ou contrôler le PC. « Protéger » signifie aider et conseiller, pas surveiller les dangers ou remplacer un dispositif d'urgence.

## Donner AVA à tes amis

Distribuer l'installateur généré ou ce ZIP sans clé API. Dans cette version, chaque ami utilise sa propre clé, ses propres profils et sa facturation sur son PC. Ne jamais partager ta clé dans l'EXE. Pour payer toi-même pour tous et piloter AVA à distance, il faudra un serveur authentifié avec invitations, quotas et secrets côté serveur : cette infrastructure n'est pas incluse.

L'application reste à l'écoute tant que la session est ouverte, le PC éveillé et la connexion active, pour un maximum de 20 minutes. Elle ne démarre pas seule avec Windows et ne fonctionne pas PC éteint. Une déconnexion réseau demande de relancer la session. L'audio et les images partagées quittent le PC vers OpenAI ; la biométrie reste locale.

## Dépannage

- Erreur 401 : vérifier la clé. 429 : vérifier crédit, quotas et limites API.
- Erreur de modèle : changer la variable d'environnement AVA_MODEL si ton compte n'a pas accès à gpt-realtime-2.1.
- Caméra/micro : vérifier les autorisations Windows, fermer les autres applications qui utilisent la webcam.
- Python absent : installer Python dans PATH ou définir AVA_PYTHON sur son chemin absolu.
- Casque conseillé pour éviter qu'AVA entende sa propre sortie.
- Ne pas lancer dans WSL pour tester caméra et microphone Windows : utiliser un terminal Windows.

## Validation et limites de livraison

Tests du code personnel et du format d'instructions, vérification syntaxique JavaScript et Python. Aucun appel API payant testé faute de clé ; aucune validation réelle du micro, de la caméra, de la qualité vocale, des seuils biométriques ou de l'installateur Windows. Cette version est un point de départ utilisable à configurer et tester sur ton PC, pas une application finalisée garantissant toutes les demandes.

## Documentation utilisée

https://developers.openai.com/api/docs/guides/voice-webrtc
https://developers.openai.com/api/docs/guides/realtime-conversations
