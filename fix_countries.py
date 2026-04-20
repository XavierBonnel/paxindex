#!/usr/bin/env python3
"""
Script de correction des noms de pays dans countries.json.
Remplace les entrées avec name "Pays XXX" par des pays réels.
"""

import json
import re
import sys
from pathlib import Path

# Liste des pays réels (code ISO, nom français, drapeau, région)
# Régions : Europe, Asie, Amériques, Afrique, Océanie, Moyen-Orient
# On en définit quelques-uns pour l'exemple, mais il faudrait une liste complète.
REAL_COUNTRIES = [
    {"code": "AF", "name": "Afghanistan", "flag": "🇦🇫", "region": "Asie"},
    {"code": "ZA", "name": "Afrique du Sud", "flag": "🇿🇦", "region": "Afrique"},
    {"code": "AL", "name": "Albanie", "flag": "🇦🇱", "region": "Europe"},
    {"code": "DZ", "name": "Algérie", "flag": "🇩🇿", "region": "Afrique"},
    {"code": "DE", "name": "Allemagne", "flag": "🇩🇪", "region": "Europe"},
    {"code": "AD", "name": "Andorre", "flag": "🇦🇩", "region": "Europe"},
    {"code": "AO", "name": "Angola", "flag": "🇦🇴", "region": "Afrique"},
    {"code": "AG", "name": "Antigua-et-Barbuda", "flag": "🇦🇬", "region": "Amériques"},
    {"code": "SA", "name": "Arabie saoudite", "flag": "🇸🇦", "region": "Moyen-Orient"},
    {"code": "AR", "name": "Argentine", "flag": "🇦🇷", "region": "Amériques"},
    {"code": "AM", "name": "Arménie", "flag": "🇦🇲", "region": "Asie"},
    {"code": "AU", "name": "Australie", "flag": "🇦🇺", "region": "Océanie"},
    {"code": "AT", "name": "Autriche", "flag": "🇦🇹", "region": "Europe"},
    {"code": "AZ", "name": "Azerbaïdjan", "flag": "🇦🇿", "region": "Asie"},
    {"code": "BS", "name": "Bahamas", "flag": "🇧🇸", "region": "Amériques"},
    {"code": "BH", "name": "Bahreïn", "flag": "🇧🇭", "region": "Moyen-Orient"},
    {"code": "BD", "name": "Bangladesh", "flag": "🇧🇩", "region": "Asie"},
    {"code": "BB", "name": "Barbade", "flag": "🇧🇧", "region": "Amériques"},
    {"code": "BE", "name": "Belgique", "flag": "🇧🇪", "region": "Europe"},
    {"code": "BZ", "name": "Belize", "flag": "🇧🇿", "region": "Amériques"},
    {"code": "BJ", "name": "Bénin", "flag": "🇧🇯", "region": "Afrique"},
    {"code": "BT", "name": "Bhoutan", "flag": "🇧🇹", "region": "Asie"},
    {"code": "BY", "name": "Biélorussie", "flag": "🇧🇾", "region": "Europe"},
    {"code": "MM", "name": "Birmanie", "flag": "🇲🇲", "region": "Asie"},
    {"code": "BO", "name": "Bolivie", "flag": "🇧🇴", "region": "Amériques"},
    {"code": "BA", "name": "Bosnie-Herzégovine", "flag": "🇧🇦", "region": "Europe"},
    {"code": "BW", "name": "Botswana", "flag": "🇧🇼", "region": "Afrique"},
    {"code": "BR", "name": "Brésil", "flag": "🇧🇷", "region": "Amériques"},
    {"code": "BN", "name": "Brunéi", "flag": "🇧🇳", "region": "Asie"},
    {"code": "BG", "name": "Bulgarie", "flag": "🇧🇬", "region": "Europe"},
    {"code": "BF", "name": "Burkina Faso", "flag": "🇧🇫", "region": "Afrique"},
    {"code": "BI", "name": "Burundi", "flag": "🇧🇮", "region": "Afrique"},
    {"code": "KH", "name": "Cambodge", "flag": "🇰🇭", "region": "Asie"},
    {"code": "CM", "name": "Cameroun", "flag": "🇨🇲", "region": "Afrique"},
    {"code": "CA", "name": "Canada", "flag": "🇨🇦", "region": "Amériques"},
    {"code": "CV", "name": "Cap-Vert", "flag": "🇨🇻", "region": "Afrique"},
    {"code": "CF", "name": "République centrafricaine", "flag": "🇨🇫", "region": "Afrique"},
    {"code": "CL", "name": "Chili", "flag": "🇨🇱", "region": "Amériques"},
    {"code": "CN", "name": "Chine", "flag": "🇨🇳", "region": "Asie"},
    {"code": "CY", "name": "Chypre", "flag": "🇨🇾", "region": "Europe"},
    {"code": "CO", "name": "Colombie", "flag": "🇨🇴", "region": "Amériques"},
    {"code": "KM", "name": "Comores", "flag": "🇰🇲", "region": "Afrique"},
    {"code": "CG", "name": "République du Congo", "flag": "🇨🇬", "region": "Afrique"},
    {"code": "CD", "name": "République démocratique du Congo", "flag": "🇨🇩", "region": "Afrique"},
    {"code": "KP", "name": "Corée du Nord", "flag": "🇰🇵", "region": "Asie"},
    {"code": "KR", "name": "Corée du Sud", "flag": "🇰🇷", "region": "Asie"},
    {"code": "CR", "name": "Costa Rica", "flag": "🇨🇷", "region": "Amériques"},
    {"code": "CI", "name": "Côte d'Ivoire", "flag": "🇨🇮", "region": "Afrique"},
    {"code": "HR", "name": "Croatie", "flag": "🇭🇷", "region": "Europe"},
    {"code": "CU", "name": "Cuba", "flag": "🇨🇺", "region": "Amériques"},
    {"code": "DK", "name": "Danemark", "flag": "🇩🇰", "region": "Europe"},
    {"code": "DJ", "name": "Djibouti", "flag": "🇩🇯", "region": "Afrique"},
    {"code": "DM", "name": "Dominique", "flag": "🇩🇲", "region": "Amériques"},
    {"code": "EG", "name": "Égypte", "flag": "🇪🇬", "region": "Afrique"},
    {"code": "SV", "name": "Salvador", "flag": "🇸🇻", "region": "Amériques"},
    {"code": "AE", "name": "Émirats arabes unis", "flag": "🇦🇪", "region": "Moyen-Orient"},
    {"code": "EC", "name": "Équateur", "flag": "🇪🇨", "region": "Amériques"},
    {"code": "ER", "name": "Érythrée", "flag": "🇪🇷", "region": "Afrique"},
    {"code": "ES", "name": "Espagne", "flag": "🇪🇸", "region": "Europe"},
    {"code": "EE", "name": "Estonie", "flag": "🇪🇪", "region": "Europe"},
    {"code": "SZ", "name": "Eswatini", "flag": "🇸🇿", "region": "Afrique"},
    {"code": "US", "name": "États-Unis", "flag": "🇺🇸", "region": "Amériques"},
    {"code": "ET", "name": "Éthiopie", "flag": "🇪🇹", "region": "Afrique"},
    {"code": "FJ", "name": "Fidji", "flag": "🇫🇯", "region": "Océanie"},
    {"code": "FI", "name": "Finlande", "flag": "🇫🇮", "region": "Europe"},
    {"code": "FR", "name": "France", "flag": "🇫🇷", "region": "Europe"},
    {"code": "GA", "name": "Gabon", "flag": "🇬🇦", "region": "Afrique"},
    {"code": "GM", "name": "Gambie", "flag": "🇬🇲", "region": "Afrique"},
    {"code": "GE", "name": "Géorgie", "flag": "🇬🇪", "region": "Asie"},
    {"code": "GH", "name": "Ghana", "flag": "🇬🇭", "region": "Afrique"},
    {"code": "GR", "name": "Grèce", "flag": "🇬🇷", "region": "Europe"},
    {"code": "GD", "name": "Grenade", "flag": "🇬🇩", "region": "Amériques"},
    {"code": "GT", "name": "Guatemala", "flag": "🇬🇹", "region": "Amériques"},
    {"code": "GN", "name": "Guinée", "flag": "🇬🇳", "region": "Afrique"},
    {"code": "GW", "name": "Guinée-Bissau", "flag": "🇬🇼", "region": "Afrique"},
    {"code": "GQ", "name": "Guinée équatoriale", "flag": "🇬🇶", "region": "Afrique"},
    {"code": "GY", "name": "Guyana", "flag": "🇬🇾", "region": "Amériques"},
    {"code": "HT", "name": "Haïti", "flag": "🇭🇹", "region": "Amériques"},
    {"code": "HN", "name": "Honduras", "flag": "🇭🇳", "region": "Amériques"},
    {"code": "HU", "name": "Hongrie", "flag": "🇭🇺", "region": "Europe"},
    {"code": "IN", "name": "Inde", "flag": "🇮🇳", "region": "Asie"},
    {"code": "ID", "name": "Indonésie", "flag": "🇮🇩", "region": "Asie"},
    {"code": "IQ", "name": "Irak", "flag": "🇮🇶", "region": "Moyen-Orient"},
    {"code": "IR", "name": "Iran", "flag": "🇮🇷", "region": "Moyen-Orient"},
    {"code": "IE", "name": "Irlande", "flag": "🇮🇪", "region": "Europe"},
    {"code": "IS", "name": "Islande", "flag": "🇮🇸", "region": "Europe"},
    {"code": "IL", "name": "Israël", "flag": "🇮🇱", "region": "Moyen-Orient"},
    {"code": "IT", "name": "Italie", "flag": "🇮🇹", "region": "Europe"},
    {"code": "JM", "name": "Jamaïque", "flag": "🇯🇲", "region": "Amériques"},
    {"code": "JP", "name": "Japon", "flag": "🇯🇵", "region": "Asie"},
    {"code": "JO", "name": "Jordanie", "flag": "🇯🇴", "region": "Moyen-Orient"},
    {"code": "KZ", "name": "Kazakhstan", "flag": "🇰🇿", "region": "Asie"},
    {"code": "KE", "name": "Kenya", "flag": "🇰🇪", "region": "Afrique"},
    {"code": "KG", "name": "Kirghizistan", "flag": "🇰🇬", "region": "Asie"},
    {"code": "KI", "name": "Kiribati", "flag": "🇰🇮", "region": "Océanie"},
    {"code": "KW", "name": "Koweït", "flag": "🇰🇼", "region": "Moyen-Orient"},
    {"code": "LA", "name": "Laos", "flag": "🇱🇦", "region": "Asie"},
    {"code": "LS", "name": "Lesotho", "flag": "🇱🇸", "region": "Afrique"},
    {"code": "LV", "name": "Lettonie", "flag": "🇱🇻", "region": "Europe"},
    {"code": "LB", "name": "Liban", "flag": "🇱🇧", "region": "Moyen-Orient"},
    {"code": "LR", "name": "Libéria", "flag": "🇱🇷", "region": "Afrique"},
    {"code": "LY", "name": "Libye", "flag": "🇱🇾", "region": "Afrique"},
    {"code": "LI", "name": "Liechtenstein", "flag": "🇱🇮", "region": "Europe"},
    {"code": "LT", "name": "Lituanie", "flag": "🇱🇹", "region": "Europe"},
    {"code": "LU", "name": "Luxembourg", "flag": "🇱🇺", "region": "Europe"},
    {"code": "MK", "name": "Macédoine du Nord", "flag": "🇲🇰", "region": "Europe"},
    {"code": "MG", "name": "Madagascar", "flag": "🇲🇬", "region": "Afrique"},
    {"code": "MY", "name": "Malaisie", "flag": "🇲🇾", "region": "Asie"},
    {"code": "MW", "name": "Malawi", "flag": "🇲🇼", "region": "Afrique"},
    {"code": "MV", "name": "Maldives", "flag": "🇲🇻", "region": "Asie"},
    {"code": "ML", "name": "Mali", "flag": "🇲🇱", "region": "Afrique"},
    {"code": "MT", "name": "Malte", "flag": "🇲🇹", "region": "Europe"},
    {"code": "MA", "name": "Maroc", "flag": "🇲🇦", "region": "Afrique"},
    {"code": "MH", "name": "Îles Marshall", "flag": "🇲🇭", "region": "Océanie"},
    {"code": "MR", "name": "Mauritanie", "flag": "🇲🇷", "region": "Afrique"},
    {"code": "MU", "name": "Maurice", "flag": "🇲🇺", "region": "Afrique"},
    {"code": "MX", "name": "Mexique", "flag": "🇲🇽", "region": "Amériques"},
    {"code": "FM", "name": "Micronésie", "flag": "🇫🇲", "region": "Océanie"},
    {"code": "MD", "name": "Moldavie", "flag": "🇲🇩", "region": "Europe"},
    {"code": "MC", "name": "Monaco", "flag": "🇲🇨", "region": "Europe"},
    {"code": "MN", "name": "Mongolie", "flag": "🇲🇳", "region": "Asie"},
    {"code": "ME", "name": "Monténégro", "flag": "🇲🇪", "region": "Europe"},
    {"code": "MZ", "name": "Mozambique", "flag": "🇲🇿", "region": "Afrique"},
    {"code": "NA", "name": "Namibie", "flag": "🇳🇦", "region": "Afrique"},
    {"code": "NR", "name": "Nauru", "flag": "🇳🇷", "region": "Océanie"},
    {"code": "NP", "name": "Népal", "flag": "🇳🇵", "region": "Asie"},
    {"code": "NI", "name": "Nicaragua", "flag": "🇳🇮", "region": "Amériques"},
    {"code": "NE", "name": "Niger", "flag": "🇳🇪", "region": "Afrique"},
    {"code": "NG", "name": "Nigéria", "flag": "🇳🇬", "region": "Afrique"},
    {"code": "NO", "name": "Norvège", "flag": "🇳🇴", "region": "Europe"},
    {"code": "NZ", "name": "Nouvelle-Zélande", "flag": "🇳🇿", "region": "Océanie"},
    {"code": "OM", "name": "Oman", "flag": "🇴🇲", "region": "Moyen-Orient"},
    {"code": "UG", "name": "Ouganda", "flag": "🇺🇬", "region": "Afrique"},
    {"code": "UZ", "name": "Ouzbékistan", "flag": "🇺🇿", "region": "Asie"},
    {"code": "PK", "name": "Pakistan", "flag": "🇵🇰", "region": "Asie"},
    {"code": "PW", "name": "Palaos", "flag": "🇵🇼", "region": "Océanie"},
    {"code": "PA", "name": "Panama", "flag": "🇵🇦", "region": "Amériques"},
    {"code": "PG", "name": "Papouasie-Nouvelle-Guinée", "flag": "🇵🇬", "region": "Océanie"},
    {"code": "PY", "name": "Paraguay", "flag": "🇵🇾", "region": "Amériques"},
    {"code": "NL", "name": "Pays-Bas", "flag": "🇳🇱", "region": "Europe"},
    {"code": "PE", "name": "Pérou", "flag": "🇵🇪", "region": "Amériques"},
    {"code": "PH", "name": "Philippines", "flag": "🇵🇭", "region": "Asie"},
    {"code": "PL", "name": "Pologne", "flag": "🇵🇱", "region": "Europe"},
    {"code": "PT", "name": "Portugal", "flag": "🇵🇹", "region": "Europe"},
    {"code": "QA", "name": "Qatar", "flag": "🇶🇦", "region": "Moyen-Orient"},
    {"code": "RO", "name": "Roumanie", "flag": "🇷🇴", "region": "Europe"},
    {"code": "GB", "name": "Royaume-Uni", "flag": "🇬🇧", "region": "Europe"},
    {"code": "RU", "name": "Russie", "flag": "🇷🇺", "region": "Europe"},
    {"code": "RW", "name": "Rwanda", "flag": "🇷🇼", "region": "Afrique"},
    {"code": "KN", "name": "Saint-Christophe-et-Niévès", "flag": "🇰🇳", "region": "Amériques"},
    {"code": "SM", "name": "Saint-Marin", "flag": "🇸🇲", "region": "Europe"},
    {"code": "VC", "name": "Saint-Vincent-et-les-Grenadines", "flag": "🇻🇨", "region": "Amériques"},
    {"code": "LC", "name": "Sainte-Lucie", "flag": "🇱🇨", "region": "Amériques"},
    {"code": "SV", "name": "Salvador", "flag": "🇸🇻", "region": "Amériques"},
    {"code": "WS", "name": "Samoa", "flag": "🇼🇸", "region": "Océanie"},
    {"code": "ST", "name": "Sao Tomé-et-Principe", "flag": "🇸🇹", "region": "Afrique"},
    {"code": "SN", "name": "Sénégal", "flag": "🇸🇳", "region": "Afrique"},
    {"code": "RS", "name": "Serbie", "flag": "🇷🇸", "region": "Europe"},
    {"code": "SC", "name": "Seychelles", "flag": "🇸🇨", "region": "Afrique"},
    {"code": "SL", "name": "Sierra Leone", "flag": "🇸🇱", "region": "Afrique"},
    {"code": "SG", "name": "Singapour", "flag": "🇸🇬", "region": "Asie"},
    {"code": "SK", "name": "Slovaquie", "flag": "🇸🇰", "region": "Europe"},
    {"code": "SI", "name": "Slovénie", "flag": "🇸🇮", "region": "Europe"},
    {"code": "SO", "name": "Somalie", "flag": "🇸🇴", "region": "Afrique"},
    {"code": "SD", "name": "Soudan", "flag": "🇸🇩", "region": "Afrique"},
    {"code": "SS", "name": "Soudan du Sud", "flag": "🇸🇸", "region": "Afrique"},
    {"code": "LK", "name": "Sri Lanka", "flag": "🇱🇰", "region": "Asie"},
    {"code": "SE", "name": "Suède", "flag": "🇸🇪", "region": "Europe"},
    {"code": "CH", "name": "Suisse", "flag": "🇨🇭", "region": "Europe"},
    {"code": "SR", "name": "Suriname", "flag": "🇸🇷", "region": "Amériques"},
    {"code": "SY", "name": "Syrie", "flag": "🇸🇾", "region": "Moyen-Orient"},
    {"code": "TJ", "name": "Tadjikistan", "flag": "🇹🇯", "region": "Asie"},
    {"code": "TZ", "name": "Tanzanie", "flag": "🇹🇿", "region": "Afrique"},
    {"code": "TW", "name": "Taïwan", "flag": "🇹🇼", "region": "Asie"},
    {"code": "TD", "name": "Tchad", "flag": "🇹🇩", "region": "Afrique"},
    {"code": "CZ", "name": "Tchéquie", "flag": "🇨🇿", "region": "Europe"},
    {"code": "TH", "name": "Thaïlande", "flag": "🇹🇭", "region": "Asie"},
    {"code": "TL", "name": "Timor oriental", "flag": "🇹🇱", "region": "Asie"},
    {"code": "TG", "name": "Togo", "flag": "🇹🇬", "region": "Afrique"},
    {"code": "TO", "name": "Tonga", "flag": "🇹🇴", "region": "Océanie"},
    {"code": "TT", "name": "Trinité-et-Tobago", "flag": "🇹🇹", "region": "Amériques"},
    {"code": "TN", "name": "Tunisie", "flag": "🇹🇳", "region": "Afrique"},
    {"code": "TM", "name": "Turkménistan", "flag": "🇹🇲", "region": "Asie"},
    {"code": "TR", "name": "Turquie", "flag": "🇹🇷", "region": "Asie"},
    {"code": "TV", "name": "Tuvalu", "flag": "🇹🇻", "region": "Océanie"},
    {"code": "UA", "name": "Ukraine", "flag": "🇺🇦", "region": "Europe"},
    {"code": "UY", "name": "Uruguay", "flag": "🇺🇾", "region": "Amériques"},
    {"code": "VU", "name": "Vanuatu", "flag": "🇻🇺", "region": "Océanie"},
    {"code": "VA", "name": "Vatican", "flag": "🇻🇦", "region": "Europe"},
    {"code": "VE", "name": "Venezuela", "flag": "🇻🇪", "region": "Amériques"},
    {"code": "VN", "name": "Vietnam", "flag": "🇻🇳", "region": "Asie"},
    {"code": "YE", "name": "Yémen", "flag": "🇾🇪", "region": "Moyen-Orient"},
    {"code": "ZM", "name": "Zambie", "flag": "🇿🇲", "region": "Afrique"},
    {"code": "ZW", "name": "Zimbabwe", "flag": "🇿🇼", "region": "Afrique"},
]

def load_countries(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_countries(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def fix_countries(countries):
    # Identifier les entrées fictives (nom commence par "Pays" ou code commence par "P")
    fictive_indices = []
    for i, c in enumerate(countries):
        if c['name'].startswith('Pays') or c['code'].startswith('P'):
            fictive_indices.append(i)
    
    print(f"Found {len(fictive_indices)} fictive countries.")
    
    # Liste des pays réels déjà utilisés (par code)
    used_codes = {c['code'] for c in countries if not c['code'].startswith('P')}
    available_real = [rc for rc in REAL_COUNTRIES if rc['code'] not in used_codes]
    
    if len(available_real) < len(fictive_indices):
        print(f"Warning: Not enough real countries to replace all fictive ones. Need {len(fictive_indices)} have {len(available_real)}")
        # On tronque
        fictive_indices = fictive_indices[:len(available_real)]
    
    # Remplacer chaque entrée fictive par un pays réel disponible
    for idx, real in zip(fictive_indices, available_real):
        # Garder les autres champs (score, change, wars, trade, rank, gdelt_penalty)
        countries[idx]['code'] = real['code']
        countries[idx]['name'] = real['name']
        countries[idx]['flag'] = real['flag']
        countries[idx]['region'] = real['region']
        print(f"Replaced {countries[idx]['name']} ({countries[idx]['code']})")
    
    return countries

def main():
    filepath = Path('data/countries.json')
    if not filepath.exists():
        print(f"File {filepath} not found.")
        sys.exit(1)
    
    countries = load_countries(filepath)
    print(f"Loaded {len(countries)} countries.")
    
    fixed = fix_countries(countries)
    
    backup = filepath.with_suffix('.json.backup')
    import shutil
    shutil.copy2(filepath, backup)
    print(f"Backup saved to {backup}")
    
    save_countries(filepath, fixed)
    print(f"Fixed {len(countries)} countries saved to {filepath}")

if __name__ == '__main__':
    main()