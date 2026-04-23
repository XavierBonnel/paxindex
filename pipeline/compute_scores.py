"""
compute_scores.py — Calcule le PaxScore™ pour chaque pays
à partir des données brutes GDELT + Wikidata.

Sortie : data/countries.json  (lu directement par l'app HTML via data.js)
         data/conflicts.json
         data/trade.json
         data/alerts.json
         data/stats.json
"""

import json
from pathlib import Path

DATA = Path(__file__).parent.parent / "data"

# Alpha-2 → Alpha-3 pour la correspondance GDELT (uniquement les pays couverts)
GDELT_A3 = {
    "IS": "ISL", "DK": "DNK", "CH": "CHE", "NZ": "NZL", "SG": "SGP",
    "NO": "NOR", "SE": "SWE", "FI": "FIN", "AT": "AUT", "PT": "PRT",
    "DE": "DEU", "FR": "FRA", "JP": "JPN", "CA": "CAN", "AU": "AUS",
    "BR": "BRA", "IN": "IND", "CN": "CHN", "GB": "GBR", "RU": "RUS",
    "US": "USA", "IR": "IRN", "IL": "ISR", "SA": "SAU", "ZA": "ZAF",
    "NG": "NGA", "ET": "ETH", "SD": "SDN", "SY": "SYR", "YE": "YEM",
}

# Clé : ISO 3166-1 alpha-2
COUNTRIES_BASE = {
    "AD": {"flag": "🇦🇩", "name": "Andorre",                         "region": "Europe"},
    "AE": {"flag": "🇦🇪", "name": "Émirats arabes unis",             "region": "Moyen-Orient"},
    "AF": {"flag": "🇦🇫", "name": "Afghanistan",                     "region": "Asie"},
    "AG": {"flag": "🇦🇬", "name": "Antigua-et-Barbuda",              "region": "Amériques"},
    "AL": {"flag": "🇦🇱", "name": "Albanie",                         "region": "Europe"},
    "AM": {"flag": "🇦🇲", "name": "Arménie",                         "region": "Asie"},
    "AO": {"flag": "🇦🇴", "name": "Angola",                          "region": "Afrique"},
    "AR": {"flag": "🇦🇷", "name": "Argentine",                       "region": "Amériques"},
    "AT": {"flag": "🇦🇹", "name": "Autriche",                        "region": "Europe"},
    "AU": {"flag": "🇦🇺", "name": "Australie",                       "region": "Océanie"},
    "AZ": {"flag": "🇦🇿", "name": "Azerbaïdjan",                     "region": "Asie"},
    "BA": {"flag": "🇧🇦", "name": "Bosnie-Herzégovine",              "region": "Europe"},
    "BB": {"flag": "🇧🇧", "name": "Barbade",                         "region": "Amériques"},
    "BD": {"flag": "🇧🇩", "name": "Bangladesh",                      "region": "Asie"},
    "BE": {"flag": "🇧🇪", "name": "Belgique",                        "region": "Europe"},
    "BF": {"flag": "🇧🇫", "name": "Burkina Faso",                    "region": "Afrique"},
    "BG": {"flag": "🇧🇬", "name": "Bulgarie",                        "region": "Europe"},
    "BH": {"flag": "🇧🇭", "name": "Bahreïn",                         "region": "Moyen-Orient"},
    "BI": {"flag": "🇧🇮", "name": "Burundi",                         "region": "Afrique"},
    "BJ": {"flag": "🇧🇯", "name": "Bénin",                           "region": "Afrique"},
    "BN": {"flag": "🇧🇳", "name": "Brunéi",                          "region": "Asie"},
    "BO": {"flag": "🇧🇴", "name": "Bolivie",                         "region": "Amériques"},
    "BR": {"flag": "🇧🇷", "name": "Brésil",                          "region": "Amériques"},
    "BS": {"flag": "🇧🇸", "name": "Bahamas",                         "region": "Amériques"},
    "BT": {"flag": "🇧🇹", "name": "Bhoutan",                         "region": "Asie"},
    "BW": {"flag": "🇧🇼", "name": "Botswana",                        "region": "Afrique"},
    "BY": {"flag": "🇧🇾", "name": "Biélorussie",                     "region": "Europe"},
    "BZ": {"flag": "🇧🇿", "name": "Belize",                          "region": "Amériques"},
    "CA": {"flag": "🇨🇦", "name": "Canada",                          "region": "Amériques"},
    "CD": {"flag": "🇨🇩", "name": "République démocratique du Congo","region": "Afrique"},
    "CF": {"flag": "🇨🇫", "name": "République centrafricaine",       "region": "Afrique"},
    "CG": {"flag": "🇨🇬", "name": "République du Congo",             "region": "Afrique"},
    "CH": {"flag": "🇨🇭", "name": "Suisse",                          "region": "Europe"},
    "CI": {"flag": "🇨🇮", "name": "Côte d'Ivoire",                   "region": "Afrique"},
    "CL": {"flag": "🇨🇱", "name": "Chili",                           "region": "Amériques"},
    "CM": {"flag": "🇨🇲", "name": "Cameroun",                        "region": "Afrique"},
    "CN": {"flag": "🇨🇳", "name": "Chine",                           "region": "Asie"},
    "CO": {"flag": "🇨🇴", "name": "Colombie",                        "region": "Amériques"},
    "CR": {"flag": "🇨🇷", "name": "Costa Rica",                      "region": "Amériques"},
    "CU": {"flag": "🇨🇺", "name": "Cuba",                            "region": "Amériques"},
    "CV": {"flag": "🇨🇻", "name": "Cap-Vert",                        "region": "Afrique"},
    "CY": {"flag": "🇨🇾", "name": "Chypre",                          "region": "Europe"},
    "CZ": {"flag": "🇨🇿", "name": "Tchéquie",                        "region": "Europe"},
    "DE": {"flag": "🇩🇪", "name": "Allemagne",                       "region": "Europe"},
    "DJ": {"flag": "🇩🇯", "name": "Djibouti",                        "region": "Afrique"},
    "DK": {"flag": "🇩🇰", "name": "Danemark",                        "region": "Europe"},
    "DM": {"flag": "🇩🇲", "name": "Dominique",                       "region": "Amériques"},
    "DZ": {"flag": "🇩🇿", "name": "Algérie",                         "region": "Afrique"},
    "EC": {"flag": "🇪🇨", "name": "Équateur",                        "region": "Amériques"},
    "EE": {"flag": "🇪🇪", "name": "Estonie",                         "region": "Europe"},
    "EG": {"flag": "🇪🇬", "name": "Égypte",                          "region": "Afrique"},
    "ER": {"flag": "🇪🇷", "name": "Érythrée",                        "region": "Afrique"},
    "ES": {"flag": "🇪🇸", "name": "Espagne",                         "region": "Europe"},
    "ET": {"flag": "🇪🇹", "name": "Éthiopie",                        "region": "Afrique"},
    "FI": {"flag": "🇫🇮", "name": "Finlande",                        "region": "Europe"},
    "FJ": {"flag": "🇫🇯", "name": "Fidji",                           "region": "Océanie"},
    "FM": {"flag": "🇫🇲", "name": "Micronésie",                      "region": "Océanie"},
    "FR": {"flag": "🇫🇷", "name": "France",                          "region": "Europe"},
    "GA": {"flag": "🇬🇦", "name": "Gabon",                           "region": "Afrique"},
    "GB": {"flag": "🇬🇧", "name": "Royaume-Uni",                     "region": "Europe"},
    "GD": {"flag": "🇬🇩", "name": "Grenade",                         "region": "Amériques"},
    "GE": {"flag": "🇬🇪", "name": "Géorgie",                         "region": "Asie"},
    "GH": {"flag": "🇬🇭", "name": "Ghana",                           "region": "Afrique"},
    "GM": {"flag": "🇬🇲", "name": "Gambie",                          "region": "Afrique"},
    "GN": {"flag": "🇬🇳", "name": "Guinée",                          "region": "Afrique"},
    "GQ": {"flag": "🇬🇶", "name": "Guinée équatoriale",              "region": "Afrique"},
    "GR": {"flag": "🇬🇷", "name": "Grèce",                           "region": "Europe"},
    "GT": {"flag": "🇬🇹", "name": "Guatemala",                       "region": "Amériques"},
    "GW": {"flag": "🇬🇼", "name": "Guinée-Bissau",                   "region": "Afrique"},
    "GY": {"flag": "🇬🇾", "name": "Guyana",                          "region": "Amériques"},
    "HN": {"flag": "🇭🇳", "name": "Honduras",                        "region": "Amériques"},
    "HR": {"flag": "🇭🇷", "name": "Croatie",                         "region": "Europe"},
    "HT": {"flag": "🇭🇹", "name": "Haïti",                           "region": "Amériques"},
    "HU": {"flag": "🇭🇺", "name": "Hongrie",                         "region": "Europe"},
    "ID": {"flag": "🇮🇩", "name": "Indonésie",                       "region": "Asie"},
    "IE": {"flag": "🇮🇪", "name": "Irlande",                         "region": "Europe"},
    "IL": {"flag": "🇮🇱", "name": "Israël",                          "region": "Moyen-Orient"},
    "IN": {"flag": "🇮🇳", "name": "Inde",                            "region": "Asie"},
    "IQ": {"flag": "🇮🇶", "name": "Irak",                            "region": "Moyen-Orient"},
    "IR": {"flag": "🇮🇷", "name": "Iran",                            "region": "Moyen-Orient"},
    "IS": {"flag": "🇮🇸", "name": "Islande",                         "region": "Europe"},
    "IT": {"flag": "🇮🇹", "name": "Italie",                          "region": "Europe"},
    "JM": {"flag": "🇯🇲", "name": "Jamaïque",                        "region": "Amériques"},
    "JO": {"flag": "🇯🇴", "name": "Jordanie",                        "region": "Moyen-Orient"},
    "JP": {"flag": "🇯🇵", "name": "Japon",                           "region": "Asie"},
    "KE": {"flag": "🇰🇪", "name": "Kenya",                           "region": "Afrique"},
    "KG": {"flag": "🇰🇬", "name": "Kirghizistan",                    "region": "Asie"},
    "KH": {"flag": "🇰🇭", "name": "Cambodge",                        "region": "Asie"},
    "KI": {"flag": "🇰🇮", "name": "Kiribati",                        "region": "Océanie"},
    "KM": {"flag": "🇰🇲", "name": "Comores",                         "region": "Afrique"},
    "KN": {"flag": "🇰🇳", "name": "Saint-Christophe-et-Niévès",     "region": "Amériques"},
    "KP": {"flag": "🇰🇵", "name": "Corée du Nord",                   "region": "Asie"},
    "KR": {"flag": "🇰🇷", "name": "Corée du Sud",                    "region": "Asie"},
    "KW": {"flag": "🇰🇼", "name": "Koweït",                          "region": "Moyen-Orient"},
    "KZ": {"flag": "🇰🇿", "name": "Kazakhstan",                      "region": "Asie"},
    "LA": {"flag": "🇱🇦", "name": "Laos",                            "region": "Asie"},
    "LB": {"flag": "🇱🇧", "name": "Liban",                           "region": "Moyen-Orient"},
    "LC": {"flag": "🇱🇨", "name": "Sainte-Lucie",                    "region": "Amériques"},
    "LI": {"flag": "🇱🇮", "name": "Liechtenstein",                   "region": "Europe"},
    "LK": {"flag": "🇱🇰", "name": "Sri Lanka",                       "region": "Asie"},
    "LR": {"flag": "🇱🇷", "name": "Libéria",                         "region": "Afrique"},
    "LS": {"flag": "🇱🇸", "name": "Lesotho",                         "region": "Afrique"},
    "LT": {"flag": "🇱🇹", "name": "Lituanie",                        "region": "Europe"},
    "LU": {"flag": "🇱🇺", "name": "Luxembourg",                      "region": "Europe"},
    "LV": {"flag": "🇱🇻", "name": "Lettonie",                        "region": "Europe"},
    "LY": {"flag": "🇱🇾", "name": "Libye",                           "region": "Afrique"},
    "MA": {"flag": "🇲🇦", "name": "Maroc",                           "region": "Afrique"},
    "MC": {"flag": "🇲🇨", "name": "Monaco",                          "region": "Europe"},
    "MD": {"flag": "🇲🇩", "name": "Moldavie",                        "region": "Europe"},
    "ME": {"flag": "🇲🇪", "name": "Monténégro",                      "region": "Europe"},
    "MG": {"flag": "🇲🇬", "name": "Madagascar",                      "region": "Afrique"},
    "MH": {"flag": "🇲🇭", "name": "Îles Marshall",                   "region": "Océanie"},
    "MK": {"flag": "🇲🇰", "name": "Macédoine du Nord",               "region": "Europe"},
    "ML": {"flag": "🇲🇱", "name": "Mali",                            "region": "Afrique"},
    "MM": {"flag": "🇲🇲", "name": "Birmanie",                        "region": "Asie"},
    "MN": {"flag": "🇲🇳", "name": "Mongolie",                        "region": "Asie"},
    "MR": {"flag": "🇲🇷", "name": "Mauritanie",                      "region": "Afrique"},
    "MT": {"flag": "🇲🇹", "name": "Malte",                           "region": "Europe"},
    "MU": {"flag": "🇲🇺", "name": "Maurice",                         "region": "Afrique"},
    "MV": {"flag": "🇲🇻", "name": "Maldives",                        "region": "Asie"},
    "MW": {"flag": "🇲🇼", "name": "Malawi",                          "region": "Afrique"},
    "MX": {"flag": "🇲🇽", "name": "Mexique",                         "region": "Amériques"},
    "MY": {"flag": "🇲🇾", "name": "Malaisie",                        "region": "Asie"},
    "MZ": {"flag": "🇲🇿", "name": "Mozambique",                      "region": "Afrique"},
    "NA": {"flag": "🇳🇦", "name": "Namibie",                         "region": "Afrique"},
    "NE": {"flag": "🇳🇪", "name": "Niger",                           "region": "Afrique"},
    "NG": {"flag": "🇳🇬", "name": "Nigeria",                         "region": "Afrique"},
    "NI": {"flag": "🇳🇮", "name": "Nicaragua",                       "region": "Amériques"},
    "NL": {"flag": "🇳🇱", "name": "Pays-Bas",                        "region": "Europe"},
    "NO": {"flag": "🇳🇴", "name": "Norvège",                         "region": "Europe"},
    "NP": {"flag": "🇳🇵", "name": "Népal",                           "region": "Asie"},
    "NR": {"flag": "🇳🇷", "name": "Nauru",                           "region": "Océanie"},
    "NZ": {"flag": "🇳🇿", "name": "Nouvelle-Zélande",                "region": "Océanie"},
    "OM": {"flag": "🇴🇲", "name": "Oman",                            "region": "Moyen-Orient"},
    "PA": {"flag": "🇵🇦", "name": "Panama",                          "region": "Amériques"},
    "PE": {"flag": "🇵🇪", "name": "Pérou",                           "region": "Amériques"},
    "PG": {"flag": "🇵🇬", "name": "Papouasie-Nouvelle-Guinée",       "region": "Océanie"},
    "PH": {"flag": "🇵🇭", "name": "Philippines",                     "region": "Asie"},
    "PK": {"flag": "🇵🇰", "name": "Pakistan",                        "region": "Asie"},
    "PL": {"flag": "🇵🇱", "name": "Pologne",                         "region": "Europe"},
    "PT": {"flag": "🇵🇹", "name": "Portugal",                        "region": "Europe"},
    "PW": {"flag": "🇵🇼", "name": "Palaos",                          "region": "Océanie"},
    "PY": {"flag": "🇵🇾", "name": "Paraguay",                        "region": "Amériques"},
    "QA": {"flag": "🇶🇦", "name": "Qatar",                           "region": "Moyen-Orient"},
    "RO": {"flag": "🇷🇴", "name": "Roumanie",                        "region": "Europe"},
    "RS": {"flag": "🇷🇸", "name": "Serbie",                          "region": "Europe"},
    "RU": {"flag": "🇷🇺", "name": "Russie",                          "region": "Europe"},
    "RW": {"flag": "🇷🇼", "name": "Rwanda",                          "region": "Afrique"},
    "SA": {"flag": "🇸🇦", "name": "Arabie Saoudite",                 "region": "Moyen-Orient"},
    "SC": {"flag": "🇸🇨", "name": "Seychelles",                      "region": "Afrique"},
    "SD": {"flag": "🇸🇩", "name": "Soudan",                          "region": "Afrique"},
    "SE": {"flag": "🇸🇪", "name": "Suède",                           "region": "Europe"},
    "SG": {"flag": "🇸🇬", "name": "Singapour",                       "region": "Asie"},
    "SI": {"flag": "🇸🇮", "name": "Slovénie",                        "region": "Europe"},
    "SK": {"flag": "🇸🇰", "name": "Slovaquie",                       "region": "Europe"},
    "SL": {"flag": "🇸🇱", "name": "Sierra Leone",                    "region": "Afrique"},
    "SM": {"flag": "🇸🇲", "name": "Saint-Marin",                     "region": "Europe"},
    "SN": {"flag": "🇸🇳", "name": "Sénégal",                         "region": "Afrique"},
    "SO": {"flag": "🇸🇴", "name": "Somalie",                         "region": "Afrique"},
    "SR": {"flag": "🇸🇷", "name": "Suriname",                        "region": "Amériques"},
    "SS": {"flag": "🇸🇸", "name": "Soudan du Sud",                   "region": "Afrique"},
    "ST": {"flag": "🇸🇹", "name": "Sao Tomé-et-Principe",            "region": "Afrique"},
    "SV": {"flag": "🇸🇻", "name": "Salvador",                        "region": "Amériques"},
    "SY": {"flag": "🇸🇾", "name": "Syrie",                           "region": "Moyen-Orient"},
    "SZ": {"flag": "🇸🇿", "name": "Eswatini",                        "region": "Afrique"},
    "TD": {"flag": "🇹🇩", "name": "Tchad",                           "region": "Afrique"},
    "TG": {"flag": "🇹🇬", "name": "Togo",                            "region": "Afrique"},
    "TH": {"flag": "🇹🇭", "name": "Thaïlande",                       "region": "Asie"},
    "TJ": {"flag": "🇹🇯", "name": "Tadjikistan",                     "region": "Asie"},
    "TL": {"flag": "🇹🇱", "name": "Timor oriental",                  "region": "Asie"},
    "TM": {"flag": "🇹🇲", "name": "Turkménistan",                    "region": "Asie"},
    "TN": {"flag": "🇹🇳", "name": "Tunisie",                         "region": "Afrique"},
    "TO": {"flag": "🇹🇴", "name": "Tonga",                           "region": "Océanie"},
    "TR": {"flag": "🇹🇷", "name": "Turquie",                         "region": "Asie"},
    "TT": {"flag": "🇹🇹", "name": "Trinité-et-Tobago",               "region": "Amériques"},
    "TV": {"flag": "🇹🇻", "name": "Tuvalu",                          "region": "Océanie"},
    "TW": {"flag": "🇹🇼", "name": "Taïwan",                          "region": "Asie"},
    "TZ": {"flag": "🇹🇿", "name": "Tanzanie",                        "region": "Afrique"},
    "UA": {"flag": "🇺🇦", "name": "Ukraine",                         "region": "Europe"},
    "UG": {"flag": "🇺🇬", "name": "Ouganda",                         "region": "Afrique"},
    "US": {"flag": "🇺🇸", "name": "États-Unis",                      "region": "Amériques"},
    "UY": {"flag": "🇺🇾", "name": "Uruguay",                         "region": "Amériques"},
    "UZ": {"flag": "🇺🇿", "name": "Ouzbékistan",                     "region": "Asie"},
    "VA": {"flag": "🇻🇦", "name": "Vatican",                         "region": "Europe"},
    "VC": {"flag": "🇻🇨", "name": "Saint-Vincent-et-les-Grenadines","region": "Amériques"},
    "VE": {"flag": "🇻🇪", "name": "Venezuela",                       "region": "Amériques"},
    "VN": {"flag": "🇻🇳", "name": "Vietnam",                         "region": "Asie"},
    "VU": {"flag": "🇻🇺", "name": "Vanuatu",                         "region": "Océanie"},
    "WS": {"flag": "🇼🇸", "name": "Samoa",                           "region": "Océanie"},
    "YE": {"flag": "🇾🇪", "name": "Yémen",                           "region": "Moyen-Orient"},
    "ZA": {"flag": "🇿🇦", "name": "Afrique du Sud",                  "region": "Afrique"},
    "ZM": {"flag": "🇿🇲", "name": "Zambie",                          "region": "Afrique"},
    "ZW": {"flag": "🇿🇼", "name": "Zimbabwe",                        "region": "Afrique"},
}

# Nombre d'accords commerciaux estimés (fallback si Wikidata indisponible)
TRADE_BASELINE = {
    "AD": 119, "AE": 109, "AF":  12, "AG": 145, "AL":  35, "AM": 140,
    "AO":  47, "AR":  18, "AT":  84, "AU":  80, "AZ": 137, "BA":  94,
    "BB": 129, "BD": 131, "BE": 127, "BF":  87, "BG":  87, "BH": 133,
    "BI": 138, "BJ": 112, "BN":  89, "BO":  95, "BR":  42, "BS": 135,
    "BT": 107, "BW": 140, "BY": 107, "BZ": 119, "CA":  88, "CD":  67,
    "CF":  77, "CG":  67, "CH": 110, "CI":  62, "CL": 121, "CM":  83,
    "CN": 130, "CO":  69, "CR": 114, "CU": 113, "CV": 128, "CY":  70,
    "CZ":  13, "DE": 120, "DJ":  61, "DK":  82, "DM":  61, "DZ":  15,
    "EC": 108, "EE":  56, "EG": 110, "ER":  58, "ES": 107, "ET":  22,
    "FI":  85, "FJ":  47, "FM":  52, "FR": 115, "GA":  98, "GB":  62,
    "GD": 140, "GE":  94, "GH":  92, "GM": 146, "GN":  90, "GQ":  90,
    "GR": 141, "GT":  40, "GW": 140, "GY":  37, "HN":  35, "HR": 112,
    "HT":  35, "HU": 133, "ID":  31, "IE": 127, "IL":  55, "IN":  54,
    "IQ": 130, "IR":  15, "IS":  68, "IT":  78, "JM":  77, "JO":  78,
    "JP":  96, "KE":  26, "KG": 126, "KH": 136, "KI": 124, "KM": 119,
    "KN":  61, "KP":  67, "KR":  68, "KW":  24, "KZ":  27, "LA":  73,
    "LB":  70, "LC":  50, "LI": 118, "LK":  32, "LR":  18, "LS": 122,
    "LT":  18, "LU":  66, "LV": 122, "LY": 118, "MA":  62, "MC":  96,
    "MD":  47, "ME": 144, "MG": 114, "MH":  60, "MK": 116, "ML": 112,
    "MM":  97, "MN":  95, "MR": 110, "MT": 113, "MU":  59, "MV":  62,
    "MW": 112, "MX": 106, "MY":  14, "MZ": 144, "NA":  94, "NE":  87,
    "NG":  30, "NI":  37, "NL":  76, "NO":  90, "NP":  91, "NR":  41,
    "NZ":  76, "OM":  86, "PA": 131, "PE":  75, "PG":  31, "PH":  22,
    "PK":  82, "PL":  16, "PT":  64, "PW":  80, "PY":  81, "QA":  14,
    "RO":  63, "RS":  43, "RU":  28, "RW":  12, "SA":  35, "SC":  41,
    "SD":   8, "SE":  88, "SG":  95, "SI":  89, "SK":  39, "SL":  40,
    "SM":  57, "SN":  44, "SO":  39, "SR": 124, "SS":  36, "ST":  44,
    "SV":  59, "SY":   5, "SZ":  48, "TD": 116, "TG":  40, "TH":  95,
    "TJ":  23, "TL": 141, "TM":  11, "TN":  12, "TO":  20, "TR":  59,
    "TT": 120, "TV": 108, "TW":  18, "TZ":  67, "UA":  46, "UG":  35,
    "US": 214, "UY":  95, "UZ":  83, "VA":  39, "VC": 102, "VE":  28,
    "VN":  74, "VU":  40, "WS":  45, "YE":   4, "ZA":  48, "ZM":  24,
    "ZW":  67,
}

# Guerres / conflits historiques connus (fallback)
WARS_BASELINE = {
    "AD":  0, "AE":  1, "AF":  8, "AG":  0, "AL":  0, "AM":  0,
    "AO":  0, "AR":  1, "AT":  0, "AU":  3, "AZ":  0, "BA":  0,
    "BB":  0, "BD":  0, "BE":  0, "BF":  0, "BG":  0, "BH":  0,
    "BI":  1, "BJ":  0, "BN":  0, "BO":  0, "BR":  2, "BS":  0,
    "BT":  0, "BW":  1, "BY":  0, "BZ":  0, "CA":  2, "CD":  0,
    "CF":  0, "CG":  0, "CH":  0, "CI":  0, "CL":  1, "CM":  0,
    "CN":  5, "CO":  0, "CR":  1, "CU":  1, "CV":  1, "CY":  0,
    "CZ":  2, "DE":  2, "DJ":  0, "DK":  0, "DM":  0, "DZ":  2,
    "EC":  1, "EE":  0, "EG":  1, "ER":  0, "ES":  1, "ET":  5,
    "FI":  1, "FJ":  0, "FM":  1, "FR":  6, "GA":  1, "GB": 14,
    "GD":  2, "GE":  1, "GH":  1, "GM":  2, "GN":  1, "GQ":  1,
    "GR":  2, "GT":  0, "GW":  2, "GY":  0, "HN":  0, "HR":  1,
    "HT":  0, "HU":  2, "ID":  0, "IE":  2, "IL":  7, "IN":  3,
    "IQ":  2, "IR":  8, "IS":  0, "IT":  1, "JM":  1, "JO":  1,
    "JP":  1, "KE":  0, "KG":  2, "KH":  1, "KI":  2, "KM":  1,
    "KN":  2, "KP":  0, "KR":  0, "KW":  0, "KZ":  0, "LA":  1,
    "LB":  1, "LC":  2, "LI":  2, "LK":  2, "LR":  0, "LS":  2,
    "LT":  0, "LU":  1, "LV":  2, "LY":  2, "MA":  1, "MC":  2,
    "MD":  1, "ME":  3, "MG":  2, "MH":  1, "MK":  2, "ML":  2,
    "MM":  0, "MN":  2, "MR":  2, "MT":  2, "MU":  1, "MV":  1,
    "MW":  2, "MX":  2, "MY":  0, "MZ":  3, "NA":  2, "NE":  2,
    "NG":  4, "NI":  1, "NL":  2, "NO":  0, "NP":  2, "NR":  1,
    "NZ":  1, "OM":  2, "PA":  3, "PE":  2, "PG":  1, "PH":  1,
    "PK":  2, "PL":  1, "PT":  2, "PW":  2, "PY":  2, "QA":  1,
    "RO":  2, "RS":  2, "RU": 12, "RW":  1, "SA":  5, "SC":  2,
    "SD":  6, "SE":  0, "SG":  0, "SI":  3, "SK":  2, "SL":  2,
    "SM":  2, "SN":  2, "SO":  2, "SR":  4, "SS":  2, "ST":  2,
    "SV":  0, "SY":  3, "SZ":  0, "TD":  4, "TG":  3, "TH":  4,
    "TJ":  2, "TL":  5, "TM":  3, "TN":  3, "TO":  3, "TR":  4,
    "TT":  5, "TV":  5, "TW":  2, "TZ":  3, "UA":  4, "UG":  1,
    "US": 42, "UY":  5, "UZ":  2, "VA":  4, "VC":  3, "VE":  4,
    "VN":  5, "VU":  4, "WS":  2, "YE":  3, "ZA":  2, "ZM":  4,
    "ZW":  5,
}


def load_json(path):
    if path.exists():
        return json.loads(path.read_text())
    return None


def gdelt_conflict_score(gdelt_data, alpha2):
    """Extrait le score de conflit GDELT pour un pays (alpha-2)."""
    if not gdelt_data:
        return 0.0
    iso3 = GDELT_A3.get(alpha2)
    if not iso3:
        return 0.0
    for c in gdelt_data.get("conflicts", []):
        if c["country_code"] == iso3:
            g = c["avg_goldstein"]
            event_penalty = min(50, c["event_count"] * 0.5)
            return abs(g) * 5 + event_penalty
    return 0.0


def wikidata_trade_count(wiki_data, country_name):
    """Compte les accords commerciaux Wikidata pour un pays."""
    if not wiki_data:
        return None
    count = 0
    for agr in wiki_data.get("trade_agreements", []):
        if country_name in agr.get("countries", []):
            count += 1
    return count if count > 0 else None


def wikidata_conflict_count(wiki_data, country_name):
    """Compte les conflits Wikidata pour un pays."""
    if not wiki_data:
        return None
    count = 0
    for c in wiki_data.get("conflicts", []):
        if country_name in c.get("countries", []):
            count += 1
    return count if count > 0 else None


def compute_pax_score(wars, trade, gdelt_penalty=0):
    """
    PaxScore™ :
    - Paix (40%)      : basé sur guerres initiées + pénalité GDELT
    - Commerce (25%)  : basé sur nb d'accords
    - Humanitaire (20%): estimé depuis paix × 0.85
    - Diplomatie (15%) : estimé depuis (paix + commerce) / 2
    """
    paix     = min(100, max(0, 100 - wars * 5 - gdelt_penalty))
    commerce = min(100, trade / 2.5)
    humanitaire = paix * 0.85
    diplomatie  = (paix + commerce) / 2
    score = (paix * 0.40 + commerce * 0.25 + humanitaire * 0.20 + diplomatie * 0.15)
    return round(score, 1)


def build_countries(gdelt_data, wiki_data):
    countries = []
    for alpha2, base in COUNTRIES_BASE.items():
        wars  = wikidata_conflict_count(wiki_data, base["name"]) or WARS_BASELINE.get(alpha2, 0)
        trade = wikidata_trade_count(wiki_data, base["name"])    or TRADE_BASELINE.get(alpha2, 20)
        gdelt = gdelt_conflict_score(gdelt_data, alpha2)

        score = compute_pax_score(wars, trade, gdelt)

        countries.append({
            "code":          alpha2,
            "flag":          base["flag"],
            "name":          base["name"],
            "region":        base["region"],
            "score":         score,
            "change":        0.0,
            "wars":          wars,
            "trade":         trade,
            "gdelt_penalty": round(gdelt, 1),
        })

    countries.sort(key=lambda c: c["score"], reverse=True)
    for i, c in enumerate(countries):
        c["rank"] = i + 1

    return countries


def build_conflicts(wiki_data):
    if not wiki_data:
        return []
    conflicts = []
    for c in wiki_data.get("conflicts", []):
        flags = []
        for cname in c.get("countries", [])[:3]:
            match = next((b["flag"] for b in COUNTRIES_BASE.values() if b["name"] == cname), "🏳️")
            flags.append(match)
        conflicts.append({
            "id":        c["id"],
            "name":      c["name"],
            "countries": flags,
            "type":      "guerre",
            "intensity": 70,
            "since":     c.get("since") or "inconnue",
            "region":    "Inconnu",
        })
    return conflicts[:20]


def build_trade(wiki_data):
    if not wiki_data:
        return []
    result = []
    for agr in wiki_data.get("trade_agreements", [])[:30]:
        result.append({
            "id":        agr["id"],
            "name":      agr["name"],
            "countries": agr.get("countries", [])[:3],
            "type":      "bilateral" if len(agr.get("countries", [])) <= 2 else "regional",
            "status":    agr.get("status", "actif"),
            "signed":    agr.get("in_force") or "inconnu",
        })
    return result


def build_alerts(rss_data):
    if not rss_data:
        return []
    result = []
    for item in rss_data.get("alerts", [])[:20]:
        result.append({
            "id":      hash(item["title"]) % 10000,
            "level":   item["level"],
            "country": "🌍",
            "text":    item["title"][:80],
            "source":  item["source"],
            "link":    item.get("link", ""),
            "time":    item.get("published", "")[:16],
        })
    return result


def build_stats(countries):
    return {
        "totalCountries":  len(countries),
        "peacefulCount":   sum(1 for c in countries if c["wars"] == 0),
        "activeConflicts": sum(c["wars"] for c in countries),
        "tradeAgreements": sum(c["trade"] for c in countries) // 2,
    }


def run():
    print("[Score] Chargement des données brutes...")
    gdelt = load_json(DATA / "conflicts_raw.json")
    wiki  = load_json(DATA / "trade_raw.json")
    rss   = load_json(DATA / "alerts_raw.json")

    print("[Score] Calcul des PaxScores...")
    countries = build_countries(gdelt, wiki)
    conflicts = build_conflicts(wiki)
    trade     = build_trade(wiki)
    alerts    = build_alerts(rss)
    stats     = build_stats(countries)

    outputs = {
        "countries.json": countries,
        "conflicts.json": conflicts,
        "trade.json":     trade,
        "alerts.json":    alerts,
        "stats.json":     stats,
    }

    for fname, data in outputs.items():
        path = DATA / fname
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False))
        count = len(data) if isinstance(data, list) else "ok"
        print(f"[Score] {fname} → {count}")

    print(f"\n✅ Pipeline terminé — {len(countries)} pays scorés")
    print(f"   Top 3 : {', '.join(c['name'] for c in countries[:3])}")
    print(f"   Bottom 3 : {', '.join(c['name'] for c in countries[-3:])}")


if __name__ == "__main__":
    run()
