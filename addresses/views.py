import requests
import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from .models import Address

logger = logging.getLogger(__name__)

class AddressView(APIView):

    def post(self, request):
        # Validation basique du payload
        q = request.data.get('q')
        if not q or not isinstance(q, str):
            return Response(
                {"error": "Le champ 'q' est requis et doit être une chaîne non vide."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # 1. Appel à l'API BAN
            ban_response = requests.get(
                "https://api-adresse.data.gouv.fr/search/",
                params={'q': q, 'limit': 1},
                timeout=5
            )
            ban_response.raise_for_status()
            ban_data = ban_response.json()

            # 2. Vérification des résultats (format 404)
            if not ban_data.get('features'):
                return Response(
                    {"error": "Adresse non trouvée. Aucun résultat ne correspond à votre recherche."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # 3. Extraction des données
            feature = ban_data['features'][0]
            properties = feature['properties']
            geometry = feature['geometry']

            # 4. Création de l'adresse
            address = Address.objects.create(
                label=properties['label'],
                housenumber=properties['housenumber'],
                street=properties['street'],
                postcode=properties['postcode'],
                citycode=properties['citycode'],
                latitude=geometry['coordinates'][1],
                longitude=geometry['coordinates'][0]
            )

            # 5. Réponse 200 avec format exact
            return Response({
                "id": address.id,
                "label": address.label,
                "housenumber": address.housenumber,
                "street": address.street,
                "postcode": address.postcode,
                "citycode": address.citycode,
                "latitude": address.latitude,
                "longitude": address.longitude
            }, status=status.HTTP_200_OK)

        except requests.RequestException:
            # Format d'erreur 500 exact
            return Response(
                {"error": "Erreur serveur : impossible de contacter l'API externe."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            logger.error(f"Erreur inattendue: {str(e)}")
            return Response(
                {"error": "Erreur serveur : impossible de contacter l'API externe."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AddressRiskView(APIView):

    def get(self, request, id):
        try:
            address = Address.objects.get(pk=id)
        except ObjectDoesNotExist:
            # Format d'erreur 404 exact
            return Response(
                {"error": "Adresse non trouvée."},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            # Appel à l'API Géorisques
            response = requests.get(
                "https://www.georisques.gouv.fr/api/v3/v1/resultats_rapport_risque",
                params={'latlon': f"{address.longitude},{address.latitude}"},
                timeout=5
            )
            response.raise_for_status()
            return Response(response.json(), status=status.HTTP_200_OK)

        except requests.RequestException:
            # Format d'erreur 500 exact
            return Response(
                {"error": "Erreur serveur : échec de la récupération des données de Géorisques."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            logger.error(f"Erreur inattendue: {str(e)}")
            return Response(
                {"error": "Erreur serveur : échec de la récupération des données de Géorisques."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )