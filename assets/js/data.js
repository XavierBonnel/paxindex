/* ── PAXINDEX — COUCHE DONNÉES ── */
/* Phase 1 : JSON statiques générés par le pipeline Python (pipeline/run_pipeline.py) */
/* Phase 2 : remplacer DATA_BASE par une URL API distante                             */

const DATA_BASE = "./data"; // JSON locaux générés par le pipeline

const COUNTRIES = [
  { code: 'AD', flag: '🇦🇩', name: 'Andorre', score: 81.9, change: +0.6, wars: 0, trade: 119, rank: 1, region: 'Europe', gdelt_penalty: 0.0 },
  { code: 'AF', flag: '🇦🇫', name: 'Afghanistan', score: 81.8, change: +2.1, wars: 0, trade: 148, rank: 2, region: 'Asie', gdelt_penalty: 0.0 },
  { code: 'AG', flag: '🇦🇬', name: 'Antigua-et-Barbuda', score: 81.6, change: -1.7, wars: 0, trade: 145, rank: 3, region: 'Amériques', gdelt_penalty: 0.0 },
  { code: 'AM', flag: '🇦🇲', name: 'Arménie', score: 81.2, change: +1.9, wars: 0, trade: 140, rank: 4, region: 'Asie', gdelt_penalty: 0.0 },
  { code: 'AZ', flag: '🇦🇿', name: 'Azerbaïdjan', score: 81.0, change: -0.1, wars: 0, trade: 137, rank: 5, region: 'Asie', gdelt_penalty: 0.0 },
  { code: 'BS', flag: '🇧🇸', name: 'Bahamas', score: 80.8, change: +1.2, wars: 0, trade: 135, rank: 6, region: 'Amériques', gdelt_penalty: 0.0 },
  { code: 'BH', flag: '🇧🇭', name: 'Bahreïn', score: 80.6, change: -1.0, wars: 0, trade: 133, rank: 7, region: 'Moyen-Orient', gdelt_penalty: 0.0 },
  { code: 'BD', flag: '🇧🇩', name: 'Bangladesh', score: 80.5, change: +0.1, wars: 0, trade: 131, rank: 8, region: 'Asie', gdelt_penalty: 0.0 },
  { code: 'BB', flag: '🇧🇧', name: 'Barbade', score: 80.3, change: -0.2, wars: 0, trade: 129, rank: 9, region: 'Amériques', gdelt_penalty: 0.0 },
  { code: 'BE', flag: '🇧🇪', name: 'Belgique', score: 80.2, change: -1.7, wars: 0, trade: 127, rank: 10, region: 'Europe', gdelt_penalty: 0.0 },
  { code: 'BZ', flag: '🇧🇿', name: 'Belize', score: 79.5, change: -0.4, wars: 0, trade: 119, rank: 11, region: 'Amériques', gdelt_penalty: 0.0 },
  { code: 'BJ', flag: '🇧🇯', name: 'Bénin', score: 79.0, change: -2.4, wars: 0, trade: 112, rank: 12, region: 'Afrique', gdelt_penalty: 0.0 },
  { code: 'CH', flag: '🇨🇭', name: 'Suisse', score: 78.8, change: 0.0, wars: 0, trade: 110, rank: 13, region: 'Europe', gdelt_penalty: 0.0 },
  { code: 'BT', flag: '🇧🇹', name: 'Bhoutan', score: 78.6, change: -0.7, wars: 0, trade: 107, rank: 14, region: 'Asie', gdelt_penalty: 0.0 },
  { code: 'BY', flag: '🇧🇾', name: 'Biélorussie', score: 78.6, change: -2.4, wars: 0, trade: 107, rank: 15, region: 'Europe', gdelt_penalty: 0.0 },
  { code: 'MM', flag: '🇲🇲', name: 'Birmanie', score: 77.8, change: +1.6, wars: 0, trade: 97, rank: 16, region: 'Asie', gdelt_penalty: 0.0 },
  { code: 'BO', flag: '🇧🇴', name: 'Bolivie', score: 77.6, change: -2.2, wars: 0, trade: 95, rank: 17, region: 'Amériques', gdelt_penalty: 0.0 },
  { code: 'BA', flag: '🇧🇦', name: 'Bosnie-Herzégovine', score: 77.5, change: +2.4, wars: 0, trade: 94, rank: 18, region: 'Europe', gdelt_penalty: 0.0 },
  { code: 'BW', flag: '🇧🇼', name: 'Botswana', score: 77.2, change: -1.1, wars: 1, trade: 140, rank: 19, region: 'Afrique', gdelt_penalty: 13.0 },
  { code: 'BN', flag: '🇧🇳', name: 'Brunéi', score: 77.1, change: -1.9, wars: 0, trade: 89, rank: 20, region: 'Asie', gdelt_penalty: 0.0 },
  { code: 'BG', flag: '🇧🇬', name: 'Bulgarie', score: 77.0, change: -2.0, wars: 0, trade: 87, rank: 21, region: 'Europe', gdelt_penalty: 0.0 },
  { code: 'BF', flag: '🇧🇫', name: 'Burkina Faso', score: 77.0, change: +0.2, wars: 0, trade: 87, rank: 22, region: 'Afrique', gdelt_penalty: 0.0 },
  { code: 'BI', flag: '🇧🇮', name: 'Burundi', score: 77.0, change: -2.3, wars: 1, trade: 138, rank: 23, region: 'Afrique', gdelt_penalty: 22.8 },
  { code: 'SG', flag: '🇸🇬', name: 'Singapour', score: 76.9, change: +1.0, wars: 0, trade: 95, rank: 24, region: 'Asie', gdelt_penalty: 0.0 },
  { code: 'KH', flag: '🇰🇭', name: 'Cambodge', score: 76.9, change: +0.6, wars: 1, trade: 136, rank: 25, region: 'Asie', gdelt_penalty: 22.9 },
  { code: 'CM', flag: '🇨🇲', name: 'Cameroun', score: 76.6, change: -1.7, wars: 0, trade: 83, rank: 26, region: 'Afrique', gdelt_penalty: 0.0 },
  { code: 'NO', flag: '🇳🇴', name: 'Norvège', score: 76.2, change: +0.5, wars: 0, trade: 90, rank: 27, region: 'Europe', gdelt_penalty: 0.0 },
  { code: 'CV', flag: '🇨🇻', name: 'Cap-Vert', score: 76.2, change: +0.2, wars: 1, trade: 128, rank: 28, region: 'Afrique', gdelt_penalty: 4.8 },
  { code: 'CF', flag: '🇨🇫', name: 'République centrafricaine', score: 76.2, change: -2.4, wars: 0, trade: 77, rank: 29, region: 'Afrique', gdelt_penalty: 0.0 },
  { code: 'SE', flag: '🇸🇪', name: 'Suède', score: 75.9, change: +0.3, wars: 0, trade: 88, rank: 30, region: 'Europe', gdelt_penalty: 0.0 },
  { code: 'CL', flag: '🇨🇱', name: 'Chili', score: 75.7, change: +1.4, wars: 1, trade: 121, rank: 31, region: 'Amériques', gdelt_penalty: 5.8 },
  { code: 'CY', flag: '🇨🇾', name: 'Chypre', score: 75.6, change: +1.2, wars: 0, trade: 70, rank: 32, region: 'Europe', gdelt_penalty: 0.0 },
  { code: 'CO', flag: '🇨🇴', name: 'Colombie', score: 75.5, change: +0.5, wars: 0, trade: 69, rank: 33, region: 'Amériques', gdelt_penalty: 0.0 },
  { code: 'KM', flag: '🇰🇲', name: 'Comores', score: 75.5, change: +0.7, wars: 1, trade: 119, rank: 34, region: 'Afrique', gdelt_penalty: 17.2 },
  { code: 'AT', flag: '🇦🇹', name: 'Autriche', score: 75.4, change: 0.0, wars: 0, trade: 84, rank: 35, region: 'Europe', gdelt_penalty: 0.0 },
  { code: 'CG', flag: '🇨🇬', name: 'République du Congo', score: 75.4, change: -1.0, wars: 0, trade: 67, rank: 36, region: 'Afrique', gdelt_penalty: 0.0 },
  { code: 'CD', flag: '🇨🇩', name: 'République démocratique du Congo', score: 75.4, change: -1.0, wars: 0, trade: 67, rank: 37, region: 'Afrique', gdelt_penalty: 0.0 },
  { code: 'KP', flag: '🇰🇵', name: 'Corée du Nord', score: 75.4, change: +0.9, wars: 0, trade: 67, rank: 38, region: 'Asie', gdelt_penalty: 0.0 },
  { code: 'KR', flag: '🇰🇷', name: 'Corée du Sud', score: 75.4, change: +1.2, wars: 0, trade: 68, rank: 39, region: 'Asie', gdelt_penalty: 0.0 },
  { code: 'DK', flag: '🇩🇰', name: 'Danemark', score: 75.2, change: +1.0, wars: 0, trade: 82, rank: 40, region: 'Europe', gdelt_penalty: 0.0 },
  { code: 'CR', flag: '🇨🇷', name: 'Costa Rica', score: 75.1, change: +1.2, wars: 1, trade: 114, rank: 41, region: 'Amériques', gdelt_penalty: 4.0 },
  { code: 'CI', flag: '🇨🇮', name: 'Côte d\'Ivoire', score: 75.0, change: -0.4, wars: 0, trade: 62, rank: 42, region: 'Afrique', gdelt_penalty: 0.0 },
  { code: 'HR', flag: '🇭🇷', name: 'Croatie', score: 75.0, change: -1.5, wars: 1, trade: 112, rank: 43, region: 'Europe', gdelt_penalty: 4.4 },
  { code: 'CU', flag: '🇨🇺', name: 'Cuba', score: 75.0, change: +1.9, wars: 1, trade: 113, rank: 44, region: 'Amériques', gdelt_penalty: 7.9 },
  { code: 'DJ', flag: '🇩🇯', name: 'Djibouti', score: 74.9, change: -1.9, wars: 0, trade: 61, rank: 45, region: 'Afrique', gdelt_penalty: 0.0 },
  { code: 'DM', flag: '🇩🇲', name: 'Dominique', score: 74.9, change: +0.5, wars: 0, trade: 61, rank: 46, region: 'Amériques', gdelt_penalty: 0.0 },
  { code: 'EG', flag: '🇪🇬', name: 'Égypte', score: 74.8, change: -1.6, wars: 1, trade: 110, rank: 47, region: 'Afrique', gdelt_penalty: 1.1 },
  { code: 'AO', flag: '🇦🇴', name: 'Angola', score: 74.7, change: -0.6, wars: 0, trade: 47, rank: 48, region: 'Afrique', gdelt_penalty: 0.0 },
  { code: 'SV', flag: '🇸🇻', name: 'Salvador', score: 74.7, change: +1.4, wars: 0, trade: 59, rank: 49, region: 'Amériques', gdelt_penalty: 0.0 },
  { code: 'AE', flag: '🇦🇪', name: 'Émirats arabes unis', score: 74.7, change: -1.8, wars: 1, trade: 109, rank: 50, region: 'Moyen-Orient', gdelt_penalty: 23.5 },
  { code: 'EC', flag: '🇪🇨', name: 'Équateur', score: 74.6, change: +1.3, wars: 1, trade: 108, rank: 51, region: 'Amériques', gdelt_penalty: 17.7 },
  { code: 'ER', flag: '🇪🇷', name: 'Érythrée', score: 74.6, change: -1.8, wars: 0, trade: 58, rank: 52, region: 'Afrique', gdelt_penalty: 0.0 },
  { code: 'ES', flag: '🇪🇸', name: 'Espagne', score: 74.6, change: -1.3, wars: 1, trade: 107, rank: 53, region: 'Europe', gdelt_penalty: 14.5 },
  { code: 'EE', flag: '🇪🇪', name: 'Estonie', score: 74.5, change: -2.4, wars: 0, trade: 56, rank: 54, region: 'Europe', gdelt_penalty: 0.0 },
  { code: 'JP', flag: '🇯🇵', name: 'Japon', score: 73.8, change: +0.5, wars: 1, trade: 96, rank: 55, region: 'Asie', gdelt_penalty: 0.0 },
  { code: 'SZ', flag: '🇸🇿', name: 'Eswatini', score: 73.8, change: -0.1, wars: 0, trade: 48, rank: 56, region: 'Afrique', gdelt_penalty: 0.0 },
  { code: 'FJ', flag: '🇫🇯', name: 'Fidji', score: 73.8, change: +0.6, wars: 0, trade: 47, rank: 57, region: 'Océanie', gdelt_penalty: 0.0 },
  { code: 'GA', flag: '🇬🇦', name: 'Gabon', score: 73.8, change: +2.0, wars: 1, trade: 98, rank: 58, region: 'Afrique', gdelt_penalty: 10.6 },
  { code: 'DE', flag: '🇩🇪', name: 'Allemagne', score: 73.7, change: +0.2, wars: 2, trade: 120, rank: 59, region: 'Europe', gdelt_penalty: 0.0 },
  { code: 'GM', flag: '🇬🇲', name: 'Gambie', score: 73.7, change: +0.9, wars: 2, trade: 146, rank: 60, region: 'Afrique', gdelt_penalty: 15.4 },
  { code: 'AL', flag: '🇦🇱', name: 'Albanie', score: 73.5, change: +0.6, wars: 0, trade: 35, rank: 61, region: 'Europe', gdelt_penalty: 0.0 },
  { code: 'GE', flag: '🇬🇪', name: 'Géorgie', score: 73.5, change: -2.5, wars: 1, trade: 94, rank: 62, region: 'Asie', gdelt_penalty: 9.3 },
  { code: 'GH', flag: '🇬🇭', name: 'Ghana', score: 73.4, change: +2.3, wars: 1, trade: 92, rank: 63, region: 'Afrique', gdelt_penalty: 22.7 },
  { code: 'IS', flag: '🇮🇸', name: 'Islande', score: 73.3, change: +2.0, wars: 0, trade: 68, rank: 64, region: 'Europe', gdelt_penalty: 0.0 },
  { code: 'GR', flag: '🇬🇷', name: 'Grèce', score: 73.3, change: +1.2, wars: 2, trade: 141, rank: 65, region: 'Europe', gdelt_penalty: 15.7 },
  { code: 'GD', flag: '🇬🇩', name: 'Grenade', score: 73.2, change: -0.0, wars: 2, trade: 140, rank: 66, region: 'Amériques', gdelt_penalty: 2.1 },
  { code: 'GT', flag: '🇬🇹', name: 'Guatemala', score: 73.2, change: +2.4, wars: 0, trade: 40, rank: 67, region: 'Amériques', gdelt_penalty: 0.0 },
  { code: 'GN', flag: '🇬🇳', name: 'Guinée', score: 73.2, change: +0.4, wars: 1, trade: 90, rank: 68, region: 'Afrique', gdelt_penalty: 8.1 },
  { code: 'GW', flag: '🇬🇼', name: 'Guinée-Bissau', score: 73.2, change: -2.0, wars: 2, trade: 140, rank: 69, region: 'Afrique', gdelt_penalty: 6.8 },
  { code: 'GQ', flag: '🇬🇶', name: 'Guinée équatoriale', score: 73.2, change: +1.3, wars: 1, trade: 90, rank: 70, region: 'Afrique', gdelt_penalty: 3.3 },
  { code: 'GY', flag: '🇬🇾', name: 'Guyana', score: 73.0, change: +0.7, wars: 0, trade: 37, rank: 71, region: 'Amériques', gdelt_penalty: 0.0 },
  { code: 'HT', flag: '🇭🇹', name: 'Haïti', score: 72.8, change: -0.5, wars: 0, trade: 35, rank: 72, region: 'Amériques', gdelt_penalty: 0.0 },
  { code: 'HN', flag: '🇭🇳', name: 'Honduras', score: 72.8, change: +1.3, wars: 0, trade: 35, rank: 73, region: 'Amériques', gdelt_penalty: 0.0 },
  { code: 'HU', flag: '🇭🇺', name: 'Hongrie', score: 72.6, change: +0.7, wars: 2, trade: 133, rank: 74, region: 'Europe', gdelt_penalty: 18.6 },
  { code: 'ID', flag: '🇮🇩', name: 'Indonésie', score: 72.5, change: -1.6, wars: 0, trade: 31, rank: 75, region: 'Asie', gdelt_penalty: 0.0 },
  { code: 'IQ', flag: '🇮🇶', name: 'Irak', score: 72.4, change: +0.4, wars: 2, trade: 130, rank: 76, region: 'Moyen-Orient', gdelt_penalty: 13.6 },
  { code: 'FI', flag: '🇫🇮', name: 'Finlande', score: 72.3, change: 0.0, wars: 1, trade: 85, rank: 77, region: 'Europe', gdelt_penalty: 0.0 },
  { code: 'IE', flag: '🇮🇪', name: 'Irlande', score: 72.2, change: -0.7, wars: 2, trade: 127, rank: 78, region: 'Europe', gdelt_penalty: 3.6 },
  { code: 'IT', flag: '🇮🇹', name: 'Italie', score: 72.2, change: +0.1, wars: 1, trade: 78, rank: 79, region: 'Europe', gdelt_penalty: 4.7 },
  { code: 'JM', flag: '🇯🇲', name: 'Jamaïque', score: 72.2, change: +2.0, wars: 1, trade: 77, rank: 80, region: 'Amériques', gdelt_penalty: 3.3 },
  { code: 'JO', flag: '🇯🇴', name: 'Jordanie', score: 72.2, change: -0.4, wars: 1, trade: 78, rank: 81, region: 'Moyen-Orient', gdelt_penalty: 20.8 },
  { code: 'KZ', flag: '🇰🇿', name: 'Kazakhstan', score: 72.2, change: -1.9, wars: 0, trade: 27, rank: 82, region: 'Asie', gdelt_penalty: 0.0 },
  { code: 'KE', flag: '🇰🇪', name: 'Kenya', score: 72.1, change: -0.4, wars: 0, trade: 26, rank: 83, region: 'Afrique', gdelt_penalty: 0.0 },
  { code: 'KG', flag: '🇰🇬', name: 'Kirghizistan', score: 72.1, change: +1.7, wars: 2, trade: 126, rank: 84, region: 'Asie', gdelt_penalty: 2.1 },
  { code: 'KI', flag: '🇰🇮', name: 'Kiribati', score: 71.9, change: +0.8, wars: 2, trade: 124, rank: 85, region: 'Océanie', gdelt_penalty: 23.7 },
  { code: 'KW', flag: '🇰🇼', name: 'Koweït', score: 71.9, change: +0.4, wars: 0, trade: 24, rank: 86, region: 'Moyen-Orient', gdelt_penalty: 0.0 },
  { code: 'LA', flag: '🇱🇦', name: 'Laos', score: 71.8, change: +0.2, wars: 1, trade: 73, rank: 87, region: 'Asie', gdelt_penalty: 20.1 },
  { code: 'LS', flag: '🇱🇸', name: 'Lesotho', score: 71.8, change: -1.0, wars: 2, trade: 122, rank: 88, region: 'Afrique', gdelt_penalty: 10.5 },
  { code: 'LV', flag: '🇱🇻', name: 'Lettonie', score: 71.8, change: +1.1, wars: 2, trade: 122, rank: 89, region: 'Europe', gdelt_penalty: 7.6 },
  { code: 'LB', flag: '🇱🇧', name: 'Liban', score: 71.6, change: -2.0, wars: 1, trade: 70, rank: 90, region: 'Moyen-Orient', gdelt_penalty: 4.8 },
  { code: 'LR', flag: '🇱🇷', name: 'Libéria', score: 71.4, change: -2.4, wars: 0, trade: 18, rank: 91, region: 'Afrique', gdelt_penalty: 0.0 },
  { code: 'LY', flag: '🇱🇾', name: 'Libye', score: 71.4, change: +0.8, wars: 2, trade: 118, rank: 92, region: 'Afrique', gdelt_penalty: 22.2 },
  { code: 'LI', flag: '🇱🇮', name: 'Liechtenstein', score: 71.4, change: +2.4, wars: 2, trade: 118, rank: 93, region: 'Europe', gdelt_penalty: 12.9 },
  { code: 'LT', flag: '🇱🇹', name: 'Lituanie', score: 71.4, change: +1.0, wars: 0, trade: 18, rank: 94, region: 'Europe', gdelt_penalty: 0.0 },
  { code: 'LU', flag: '🇱🇺', name: 'Luxembourg', score: 71.3, change: -0.4, wars: 1, trade: 66, rank: 95, region: 'Europe', gdelt_penalty: 8.1 },
  { code: 'MK', flag: '🇲🇰', name: 'Macédoine du Nord', score: 71.3, change: -0.1, wars: 2, trade: 116, rank: 96, region: 'Europe', gdelt_penalty: 11.0 },
  { code: 'NZ', flag: '🇳🇿', name: 'Nouvelle-Zélande', score: 71.2, change: +3.0, wars: 1, trade: 76, rank: 97, region: 'Océanie', gdelt_penalty: 0.0 },
  { code: 'MG', flag: '🇲🇬', name: 'Madagascar', score: 71.1, change: +1.8, wars: 2, trade: 114, rank: 98, region: 'Afrique', gdelt_penalty: 11.5 },
  { code: 'MY', flag: '🇲🇾', name: 'Malaisie', score: 71.1, change: +0.6, wars: 0, trade: 14, rank: 99, region: 'Asie', gdelt_penalty: 0.0 },
  { code: 'MW', flag: '🇲🇼', name: 'Malawi', score: 71.0, change: -2.4, wars: 2, trade: 112, rank: 100, region: 'Afrique', gdelt_penalty: 0.2 },
  { code: 'MV', flag: '🇲🇻', name: 'Maldives', score: 71.0, change: -1.1, wars: 1, trade: 62, rank: 101, region: 'Asie', gdelt_penalty: 12.0 },
  { code: 'ML', flag: '🇲🇱', name: 'Mali', score: 71.0, change: +1.0, wars: 2, trade: 112, rank: 102, region: 'Afrique', gdelt_penalty: 11.3 },
  { code: 'MT', flag: '🇲🇹', name: 'Malte', score: 71.0, change: +1.8, wars: 2, trade: 113, rank: 103, region: 'Europe', gdelt_penalty: 18.3 },
  { code: 'MA', flag: '🇲🇦', name: 'Maroc', score: 71.0, change: +2.1, wars: 1, trade: 62, rank: 104, region: 'Afrique', gdelt_penalty: 11.5 },
  { code: 'MH', flag: '🇲🇭', name: 'Îles Marshall', score: 70.8, change: -0.8, wars: 1, trade: 60, rank: 105, region: 'Océanie', gdelt_penalty: 16.5 },
  { code: 'MR', flag: '🇲🇷', name: 'Mauritanie', score: 70.8, change: +2.1, wars: 2, trade: 110, rank: 106, region: 'Afrique', gdelt_penalty: 24.8 },
  { code: 'MU', flag: '🇲🇺', name: 'Maurice', score: 70.7, change: -2.1, wars: 1, trade: 59, rank: 107, region: 'Afrique', gdelt_penalty: 19.8 },
  { code: 'MX', flag: '🇲🇽', name: 'Mexique', score: 70.5, change: -0.8, wars: 2, trade: 106, rank: 108, region: 'Amériques', gdelt_penalty: 18.5 },
  { code: 'FM', flag: '🇫🇲', name: 'Micronésie', score: 70.2, change: +0.5, wars: 1, trade: 52, rank: 109, region: 'Océanie', gdelt_penalty: 6.6 },
  { code: 'MD', flag: '🇲🇩', name: 'Moldavie', score: 69.8, change: +2.1, wars: 1, trade: 47, rank: 110, region: 'Europe', gdelt_penalty: 22.2 },
  { code: 'MC', flag: '🇲🇨', name: 'Monaco', score: 69.7, change: +0.4, wars: 2, trade: 96, rank: 111, region: 'Europe', gdelt_penalty: 18.2 },
  { code: 'MN', flag: '🇲🇳', name: 'Mongolie', score: 69.6, change: -0.6, wars: 2, trade: 95, rank: 112, region: 'Asie', gdelt_penalty: 7.0 },
  { code: 'CA', flag: '🇨🇦', name: 'Canada', score: 69.5, change: +0.3, wars: 2, trade: 88, rank: 113, region: 'Amériques', gdelt_penalty: 0.0 },
  { code: 'ME', flag: '🇲🇪', name: 'Monténégro', score: 69.5, change: +1.3, wars: 3, trade: 144, rank: 114, region: 'Europe', gdelt_penalty: 19.4 },
  { code: 'MZ', flag: '🇲🇿', name: 'Mozambique', score: 69.5, change: -0.2, wars: 3, trade: 144, rank: 115, region: 'Afrique', gdelt_penalty: 1.0 },
  { code: 'NA', flag: '🇳🇦', name: 'Namibie', score: 69.5, change: -1.6, wars: 2, trade: 94, rank: 116, region: 'Afrique', gdelt_penalty: 3.2 },
  { code: 'NR', flag: '🇳🇷', name: 'Nauru', score: 69.3, change: -1.6, wars: 1, trade: 41, rank: 117, region: 'Océanie', gdelt_penalty: 13.6 },
  { code: 'NP', flag: '🇳🇵', name: 'Népal', score: 69.3, change: -0.4, wars: 2, trade: 91, rank: 118, region: 'Asie', gdelt_penalty: 1.4 },
  { code: 'NI', flag: '🇳🇮', name: 'Nicaragua', score: 69.0, change: -2.3, wars: 1, trade: 37, rank: 119, region: 'Amériques', gdelt_penalty: 19.9 },
  { code: 'NE', flag: '🇳🇪', name: 'Niger', score: 69.0, change: -0.8, wars: 2, trade: 87, rank: 120, region: 'Afrique', gdelt_penalty: 22.0 },
  { code: 'OM', flag: '🇴🇲', name: 'Oman', score: 68.9, change: -0.2, wars: 2, trade: 86, rank: 121, region: 'Moyen-Orient', gdelt_penalty: 8.2 },
  { code: 'UG', flag: '🇺🇬', name: 'Ouganda', score: 68.8, change: +2.0, wars: 1, trade: 35, rank: 122, region: 'Afrique', gdelt_penalty: 9.1 },
  { code: 'UZ', flag: '🇺🇿', name: 'Ouzbékistan', score: 68.6, change: -1.4, wars: 2, trade: 83, rank: 123, region: 'Asie', gdelt_penalty: 4.0 },
  { code: 'PK', flag: '🇵🇰', name: 'Pakistan', score: 68.6, change: -0.3, wars: 2, trade: 82, rank: 124, region: 'Asie', gdelt_penalty: 21.0 },
  { code: 'PW', flag: '🇵🇼', name: 'Palaos', score: 68.5, change: +0.8, wars: 2, trade: 80, rank: 125, region: 'Océanie', gdelt_penalty: 0.0 },
  { code: 'PA', flag: '🇵🇦', name: 'Panama', score: 68.5, change: -0.3, wars: 3, trade: 131, rank: 126, region: 'Amériques', gdelt_penalty: 23.3 },
  { code: 'PG', flag: '🇵🇬', name: 'Papouasie-Nouvelle-Guinée', score: 68.5, change: +1.5, wars: 1, trade: 31, rank: 127, region: 'Océanie', gdelt_penalty: 22.1 },
  { code: 'PY', flag: '🇵🇾', name: 'Paraguay', score: 68.5, change: +2.0, wars: 2, trade: 81, rank: 128, region: 'Amériques', gdelt_penalty: 10.9 },
  { code: 'NL', flag: '🇳🇱', name: 'Pays-Bas', score: 68.1, change: +1.3, wars: 2, trade: 76, rank: 129, region: 'Europe', gdelt_penalty: 11.5 },
  { code: 'PE', flag: '🇵🇪', name: 'Pérou', score: 68.0, change: +2.4, wars: 2, trade: 75, rank: 130, region: 'Amériques', gdelt_penalty: 16.9 },
  { code: 'PH', flag: '🇵🇭', name: 'Philippines', score: 67.8, change: -1.4, wars: 1, trade: 22, rank: 131, region: 'Asie', gdelt_penalty: 8.8 },
  { code: 'PL', flag: '🇵🇱', name: 'Pologne', score: 67.3, change: +2.4, wars: 1, trade: 16, rank: 132, region: 'Europe', gdelt_penalty: 0.4 },
  { code: 'PT', flag: '🇵🇹', name: 'Portugal', score: 67.1, change: -2.0, wars: 2, trade: 64, rank: 133, region: 'Europe', gdelt_penalty: 17.5 },
  { code: 'QA', flag: '🇶🇦', name: 'Qatar', score: 67.1, change: -0.1, wars: 1, trade: 14, rank: 134, region: 'Moyen-Orient', gdelt_penalty: 3.6 },
  { code: 'RO', flag: '🇷🇴', name: 'Roumanie', score: 67.0, change: -1.4, wars: 2, trade: 63, rank: 135, region: 'Europe', gdelt_penalty: 10.2 },
  { code: 'RW', flag: '🇷🇼', name: 'Rwanda', score: 67.0, change: +1.8, wars: 1, trade: 12, rank: 136, region: 'Afrique', gdelt_penalty: 15.6 },
  { code: 'KN', flag: '🇰🇳', name: 'Saint-Christophe-et-Niévès', score: 66.9, change: +1.6, wars: 2, trade: 61, rank: 137, region: 'Amériques', gdelt_penalty: 10.9 },
  { code: 'AR', flag: '🇦🇷', name: 'Argentine', score: 66.8, change: -0.4, wars: 1, trade: 18, rank: 138, region: 'Amériques', gdelt_penalty: 8.8 },
  { code: 'SM', flag: '🇸🇲', name: 'Saint-Marin', score: 66.6, change: +2.3, wars: 2, trade: 57, rank: 139, region: 'Europe', gdelt_penalty: 5.1 },
  { code: 'VC', flag: '🇻🇨', name: 'Saint-Vincent-et-les-Grenadines', score: 66.2, change: +1.7, wars: 3, trade: 102, rank: 140, region: 'Amériques', gdelt_penalty: 5.3 },
  { code: 'LC', flag: '🇱🇨', name: 'Sainte-Lucie', score: 66.0, change: +2.1, wars: 2, trade: 50, rank: 141, region: 'Amériques', gdelt_penalty: 7.5 },
  { code: 'SV', flag: '🇸🇻', name: 'Salvador', score: 65.8, change: +2.3, wars: 2, trade: 47, rank: 142, region: 'Amériques', gdelt_penalty: 13.4 },
  { code: 'WS', flag: '🇼🇸', name: 'Samoa', score: 65.6, change: +1.6, wars: 2, trade: 45, rank: 143, region: 'Océanie', gdelt_penalty: 17.6 },
  { code: 'ST', flag: '🇸🇹', name: 'Sao Tomé-et-Principe', score: 65.5, change: -0.4, wars: 2, trade: 44, rank: 144, region: 'Afrique', gdelt_penalty: 16.8 },
  { code: 'SN', flag: '🇸🇳', name: 'Sénégal', score: 65.5, change: +1.2, wars: 2, trade: 44, rank: 145, region: 'Afrique', gdelt_penalty: 16.2 },
  { code: 'RS', flag: '🇷🇸', name: 'Serbie', score: 65.4, change: -2.4, wars: 2, trade: 43, rank: 146, region: 'Europe', gdelt_penalty: 15.5 },
  { code: 'CN', flag: '🇨🇳', name: 'Chine', score: 65.3, change: -1.0, wars: 5, trade: 130, rank: 147, region: 'Asie', gdelt_penalty: 0.0 },
  { code: 'SC', flag: '🇸🇨', name: 'Seychelles', score: 65.3, change: +1.5, wars: 2, trade: 41, rank: 148, region: 'Afrique', gdelt_penalty: 12.4 },
  { code: 'AU', flag: '🇦🇺', name: 'Australie', score: 65.2, change: -0.5, wars: 3, trade: 80, rank: 149, region: 'Océanie', gdelt_penalty: 0.0 },
  { code: 'SL', flag: '🇸🇱', name: 'Sierra Leone', score: 65.2, change: +0.6, wars: 2, trade: 40, rank: 150, region: 'Afrique', gdelt_penalty: 7.3 },
  { code: 'SK', flag: '🇸🇰', name: 'Slovaquie', score: 65.1, change: -1.1, wars: 2, trade: 39, rank: 151, region: 'Europe', gdelt_penalty: 5.7 },
  { code: 'SI', flag: '🇸🇮', name: 'Slovénie', score: 65.1, change: +0.3, wars: 3, trade: 89, rank: 152, region: 'Europe', gdelt_penalty: 1.4 },
  { code: 'SO', flag: '🇸🇴', name: 'Somalie', score: 65.1, change: -0.7, wars: 2, trade: 39, rank: 153, region: 'Afrique', gdelt_penalty: 6.7 },
  { code: 'SS', flag: '🇸🇸', name: 'Soudan du Sud', score: 64.9, change: -1.2, wars: 2, trade: 36, rank: 154, region: 'Afrique', gdelt_penalty: 20.0 },
  { code: 'LK', flag: '🇱🇰', name: 'Sri Lanka', score: 64.6, change: -0.8, wars: 2, trade: 32, rank: 155, region: 'Asie', gdelt_penalty: 25.0 },
  { code: 'ZA', flag: '🇿🇦', name: 'Afrique du Sud', score: 64.3, change: +0.2, wars: 2, trade: 48, rank: 156, region: 'Afrique', gdelt_penalty: 0.0 },
  { code: 'SR', flag: '🇸🇷', name: 'Suriname', score: 63.9, change: +0.5, wars: 4, trade: 124, rank: 157, region: 'Amériques', gdelt_penalty: 20.4 },
  { code: 'TJ', flag: '🇹🇯', name: 'Tadjikistan', score: 63.8, change: -1.4, wars: 2, trade: 23, rank: 158, region: 'Asie', gdelt_penalty: 8.3 },
  { code: 'BR', flag: '🇧🇷', name: 'Brésil', score: 63.5, change: -0.3, wars: 2, trade: 42, rank: 159, region: 'Amériques', gdelt_penalty: 0.0 },
  { code: 'TZ', flag: '🇹🇿', name: 'Tanzanie', score: 63.4, change: -1.6, wars: 3, trade: 67, rank: 160, region: 'Afrique', gdelt_penalty: 12.2 },
  { code: 'TW', flag: '🇹🇼', name: 'Taïwan', score: 63.4, change: +1.2, wars: 2, trade: 18, rank: 161, region: 'Asie', gdelt_penalty: 19.7 },
  { code: 'TD', flag: '🇹🇩', name: 'Tchad', score: 63.3, change: +0.7, wars: 4, trade: 116, rank: 162, region: 'Afrique', gdelt_penalty: 2.0 },
  { code: 'CZ', flag: '🇨🇿', name: 'Tchéquie', score: 63.0, change: +1.9, wars: 2, trade: 13, rank: 163, region: 'Europe', gdelt_penalty: 8.6 },
  { code: 'IN', flag: '🇮🇳', name: 'Inde', score: 61.8, change: -2.0, wars: 3, trade: 54, rank: 164, region: 'Asie', gdelt_penalty: 0.0 },
  { code: 'TH', flag: '🇹🇭', name: 'Thaïlande', score: 61.6, change: -1.5, wars: 4, trade: 95, rank: 165, region: 'Asie', gdelt_penalty: 8.9 },
  { code: 'DZ', flag: '🇩🇿', name: 'Algérie', score: 61.5, change: +1.5, wars: 2, trade: 15, rank: 166, region: 'Afrique', gdelt_penalty: 0.7 },
  { code: 'TL', flag: '🇹🇱', name: 'Timor oriental', score: 61.3, change: -1.7, wars: 5, trade: 141, rank: 167, region: 'Asie', gdelt_penalty: 5.8 },
  { code: 'TG', flag: '🇹🇬', name: 'Togo', score: 61.2, change: -2.0, wars: 3, trade: 40, rank: 168, region: 'Afrique', gdelt_penalty: 9.9 },
  { code: 'FR', flag: '🇫🇷', name: 'France', score: 60.1, change: -1.2, wars: 6, trade: 115, rank: 169, region: 'Europe', gdelt_penalty: 0.0 },
  { code: 'TO', flag: '🇹🇴', name: 'Tonga', score: 59.6, change: -2.0, wars: 3, trade: 20, rank: 170, region: 'Océanie', gdelt_penalty: 18.4 },
  { code: 'TT', flag: '🇹🇹', name: 'Trinité-et-Tobago', score: 59.6, change: -1.2, wars: 5, trade: 120, rank: 171, region: 'Amériques', gdelt_penalty: 3.1 },
  { code: 'TN', flag: '🇹🇳', name: 'Tunisie', score: 59.0, change: -1.5, wars: 3, trade: 12, rank: 172, region: 'Afrique', gdelt_penalty: 7.9 },
  { code: 'TM', flag: '🇹🇲', name: 'Turkménistan', score: 58.9, change: -1.2, wars: 3, trade: 11, rank: 173, region: 'Asie', gdelt_penalty: 15.7 },
  { code: 'TR', flag: '🇹🇷', name: 'Turquie', score: 58.7, change: +2.4, wars: 4, trade: 59, rank: 174, region: 'Asie', gdelt_penalty: 5.3 },
  { code: 'TV', flag: '🇹🇻', name: 'Tuvalu', score: 58.6, change: +1.7, wars: 5, trade: 108, rank: 175, region: 'Océanie', gdelt_penalty: 18.3 },
  { code: 'UA', flag: '🇺🇦', name: 'Ukraine', score: 57.7, change: -0.7, wars: 4, trade: 46, rank: 176, region: 'Europe', gdelt_penalty: 2.5 },
  { code: 'UY', flag: '🇺🇾', name: 'Uruguay', score: 57.6, change: +0.3, wars: 5, trade: 95, rank: 177, region: 'Amériques', gdelt_penalty: 11.9 },
  { code: 'VU', flag: '🇻🇺', name: 'Vanuatu', score: 57.2, change: +2.0, wars: 4, trade: 40, rank: 178, region: 'Océanie', gdelt_penalty: 6.1 },
  { code: 'VA', flag: '🇻🇦', name: 'Vatican', score: 57.1, change: -1.0, wars: 4, trade: 39, rank: 179, region: 'Europe', gdelt_penalty: 16.7 },
  { code: 'VE', flag: '🇻🇪', name: 'Venezuela', score: 56.2, change: +2.1, wars: 4, trade: 28, rank: 180, region: 'Amériques', gdelt_penalty: 2.3 },
  { code: 'VN', flag: '🇻🇳', name: 'Vietnam', score: 55.9, change: -1.2, wars: 5, trade: 74, rank: 181, region: 'Asie', gdelt_penalty: 4.8 },
  { code: 'ZM', flag: '🇿🇲', name: 'Zambie', score: 55.9, change: +0.5, wars: 4, trade: 24, rank: 182, region: 'Afrique', gdelt_penalty: 20.7 },
  { code: 'NG', flag: '🇳🇬', name: 'Nigeria', score: 55.5, change: -0.5, wars: 4, trade: 30, rank: 183, region: 'Afrique', gdelt_penalty: 0.0 },
  { code: 'SY', flag: '🇸🇾', name: 'Syrie', score: 55.5, change: -1.5, wars: 3, trade: 5, rank: 184, region: 'Moyen-Orient', gdelt_penalty: 0.0 },
  { code: 'ZW', flag: '🇿🇼', name: 'Zimbabwe', score: 55.4, change: -1.5, wars: 5, trade: 67, rank: 185, region: 'Afrique', gdelt_penalty: 13.3 },
  { code: 'YE', flag: '🇾🇪', name: 'Yémen', score: 55.3, change: -2.0, wars: 3, trade: 4, rank: 186, region: 'Moyen-Orient', gdelt_penalty: 0.0 },
  { code: 'P103', flag: '🇺🇳', name: 'Pays 104', score: 54.9, change: +1.7, wars: 5, trade: 61, rank: 187, region: 'Afrique', gdelt_penalty: 17.8 },
  { code: 'SA', flag: '🇸🇦', name: 'Arabie Saoudite', score: 52.9, change: -0.8, wars: 5, trade: 35, rank: 188, region: 'Moyen-Orient', gdelt_penalty: 0.0 },
  { code: 'ET', flag: '🇪🇹', name: 'Éthiopie', score: 51.2, change: -1.0, wars: 5, trade: 22, rank: 189, region: 'Afrique', gdelt_penalty: 0.0 },
  { code: 'IL', flag: '🇮🇱', name: 'Israël', score: 49.1, change: -3.0, wars: 7, trade: 55, rank: 190, region: 'Moyen-Orient', gdelt_penalty: 0.0 },
  { code: 'SD', flag: '🇸🇩', name: 'Soudan', score: 46.2, change: -0.8, wars: 6, trade: 8, rank: 191, region: 'Afrique', gdelt_penalty: 0.0 },
  { code: 'IR', flag: '🇮🇷', name: 'Iran', score: 40.6, change: -4.5, wars: 8, trade: 15, rank: 192, region: 'Moyen-Orient', gdelt_penalty: 0.0 },
  { code: 'RU', flag: '🇷🇺', name: 'Russie', score: 29.4, change: -5.0, wars: 12, trade: 28, rank: 193, region: 'Europe', gdelt_penalty: 0.0 },
  { code: 'US', flag: '🇺🇸', name: 'États-Unis', score: 27.8, change: -3.0, wars: 42, trade: 214, rank: 194, region: 'Amériques', gdelt_penalty: 0.0 },
  { code: 'GB', flag: '🇬🇧', name: 'Royaume-Uni', score: 27.4, change: -4.0, wars: 14, trade: 62, rank: 195, region: 'Europe', gdelt_penalty: 0.0 },
];
const TRADE_AGREEMENTS = [
  { id: 1, countries: ['🇪🇺','🇨🇦'], name: 'CETA',        type: 'bilateral', status: 'actif',       signed: '2016-10-30' },
  { id: 2, countries: ['🇺🇸','🇲🇽','🇨🇦'], name: 'USMCA',  type: 'regional',  status: 'actif',       signed: '2020-07-01' },
  { id: 3, countries: ['🇨🇳','🌏'],   name: 'RCEP',        type: 'regional',  status: 'actif',       signed: '2022-01-01' },
  { id: 4, countries: ['🇬🇧','🇯🇵'], name: 'UK-Japon FTA', type: 'bilateral', status: 'actif',       signed: '2021-01-01' },
  { id: 5, countries: ['🇷🇺','🇨🇳'], name: 'Sanctions UE→RU', type: 'sanction', status: 'actif',    signed: '2022-03-01' },
];

const ALERTS = [
  { id: 1, level: 'critical', country: '🇮🇷', text: 'Frappes sur Téhéran — score RU −5 pts',      time: 'il y a 2h' },
  { id: 2, level: 'high',     country: '🇱🇧', text: '102 victimes au Liban — alerte humanitaire', time: 'il y a 4h' },
  { id: 3, level: 'high',     country: '🇺🇸', text: 'Nouvelles sanctions sur l\'Iran annoncées',   time: 'il y a 6h' },
  { id: 4, level: 'medium',   country: '🇩🇰', text: 'Accord commercial UE-Mercosur finalisé',      time: 'il y a 9h' },
  { id: 5, level: 'medium',   country: '🇮🇸', text: 'Score Islande : record historique 97.8',      time: 'il y a 12h' },
];

/* ── Cache en mémoire pour éviter les doubles fetch ── */
const _cache = {};

/* ── API wrapper : tente le JSON du pipeline, fallback sur mock ── */
async function fetchData(endpoint) {
  if (_cache[endpoint]) return _cache[endpoint];

  // Mapping endpoint → fichier JSON généré par le pipeline
  const fileMap = {
    '/countries': 'countries.json',
    '/conflicts': 'conflicts.json',
    '/trade':     'trade.json',
    '/alerts':    'alerts.json',
    '/stats':     'stats.json',
  };

  // Détail d'un pays : chercher dans countries.json
  if (endpoint.startsWith('/countries/')) {
    const code = endpoint.split('/')[2];
    const all  = await fetchData('/countries');
    return Array.isArray(all) ? (all.find(c => c.code === code) || null) : null;
  }

  const file = fileMap[endpoint];
  if (file) {
    try {
      const res = await fetch(`${DATA_BASE}/${file}`);
      if (res.ok) {
        const data = await res.json();
        _cache[endpoint] = data;
        return data;
      }
    } catch (_) { /* fichier absent → fallback mock */ }
  }

  // Fallback mock si le pipeline n'a pas encore tourné
  return getMock(endpoint);
}

function getMock(endpoint) {
  if (endpoint.startsWith('/countries/')) {
    const code = endpoint.split('/')[2];
    return COUNTRIES.find(c => c.code === code) || null;
  }
  const map = {
    '/countries':  COUNTRIES,
    '/conflicts':  CONFLICTS,
    '/trade':      TRADE_AGREEMENTS,
    '/alerts':     ALERTS,
    '/stats': {
      totalCountries: 195, peacefulCount: 42,
      activeConflicts: 28, tradeAgreements: 3840
    }
  };
  return map[endpoint] ?? [];
}

/* ── URL param helper ── */
function getParam(key) {
  return new URLSearchParams(window.location.search).get(key);
}
