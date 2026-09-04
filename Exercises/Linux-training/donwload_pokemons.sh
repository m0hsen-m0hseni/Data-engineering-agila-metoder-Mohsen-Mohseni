#!/bin/bash 

while IFS= read -r pokemon 
do 
    echo "Downloading $pokemon..."

    curl -sS \
        "https://pokeapi.co/api/v2/pokemon-species/$pokemon" \
        -o "data/pokemons/$pokemon.json"

    sleep 2 
done < data/pokemons/pokemon_list.txt

echo "Finished!"