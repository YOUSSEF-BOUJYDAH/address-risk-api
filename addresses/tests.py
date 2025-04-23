from django.urls import reverse
from rest_framework.test import APITestCase
from unittest.mock import patch, MagicMock
from .models import Address

class AddressAPITests(APITestCase):
    def setUp(self):
        self.test_address = Address.objects.create(
            id=1,
            label="8 bd du Port, 56170 Sarzeau",
            housenumber="8",
            street="bd du Port",
            postcode="56170",
            citycode="56242",
            latitude=47.58234,
            longitude=-2.73745
        )

    def test_empty_query_returns_400(self):
        """Test 1: Requête vide retourne 400"""
        response = self.client.post(
            reverse('address-create'),
            {'q': ''},
            format='json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            "error": "Le champ 'q' est requis et doit être une chaîne non vide."
        })

    @patch('requests.get')
    def test_address_not_found_returns_404(self, mock_get):
        """Test 2: Adresse introuvable retourne 404"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'features': []}
        mock_get.return_value = mock_response

        response = self.client.post(
            reverse('address-create'),
            {'q': 'adresse inexistante'},
            format='json'
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {
            "error": "Adresse non trouvée. Aucun résultat ne correspond à votre recherche."
        })

    def test_get_risks_nonexistent_address_returns_404(self):
        """Test 3: Récupération risques sur adresse inexistante retourne 404"""
        response = self.client.get(
            reverse('address-risks', kwargs={'id': 999})
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {
            "error": "Adresse non trouvée."
        })