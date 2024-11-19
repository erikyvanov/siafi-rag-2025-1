import requests
from bs4 import BeautifulSoup
import os

def save_pokemon_to_txt(base_path, pokemon_number, pokemon_name, pokemon_info, index):
    pokemon_folder_name = f'{base_path}/{pokemon_number}_{pokemon_name}'
    if not os.path.exists(pokemon_folder_name):
        os.makedirs(pokemon_folder_name)

    pokemon_info = pokemon_info.replace('\n', '')

    pokemon_file_path = f'{pokemon_folder_name}/info_{index}.txt'
    with open(pokemon_file_path, 'w') as file:
        file.write(pokemon_info)

wikidex_url = 'https://www.wikidex.net'
wikidex_pokemon_list_url = f'{wikidex_url}/wiki/Lista_de_Pok%C3%A9mon'

response = requests.get(wikidex_pokemon_list_url)
print(response.status_code)

if response.status_code != 200:
    raise 'La pagina no se pudo obtener'

pokemon_page_soup = BeautifulSoup(response.content, 'html.parser')
# print(pokemon_page_soup)

pokemon_generation_list = pokemon_page_soup.find_all('table', class_='tabpokemon')
print(len(pokemon_generation_list))

for generation in pokemon_generation_list:
    pokemon_list_rows = generation.find('tbody')
    pokemon_list = pokemon_list_rows.find_all('tr')

    print(len(pokemon_list))

    for pokemon in pokemon_list:
        pokemon_info = pokemon.find_all('td')
        is_normal_pokemon = len(pokemon_info) == 4

        if is_normal_pokemon:
            pokemon_number = pokemon_info[0].text.replace('\n', '')
            pokemon_number = pokemon_number.zfill(3)

            pokemon_name = pokemon_info[1].text.replace('\n', '')

            pokemon_link = pokemon_info[1].find('a')['href']
            pokemon_link = f'{wikidex_url}{pokemon_link}'

            print(f'{pokemon_number}\t{pokemon_name}\t{pokemon_link}')

            pokemon_response = requests.get(pokemon_link)

            pokemon_info_soup = BeautifulSoup(pokemon_response.content, 'html.parser')

            pokemon_p_info = pokemon_info_soup.find_all('p')

            for i, info in enumerate(pokemon_p_info):
                text = info.text

                if len(text) > 45 and not('siguientes' in text)and not(':' in text) and not('Ilustración' in text) and not ('Fondo de' in text):
                    print(i, text)
                    save_pokemon_to_txt('./pokemon_info', pokemon_number, pokemon_name, text, i)


    
    break
