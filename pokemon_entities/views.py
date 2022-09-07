import folium
from django.utils.timezone import localtime
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from.models import *


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemon_entities = PokemonEntity.objects.filter(appeared_at__lt=localtime(), disappeared_at__gt=localtime())
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.photo.url)
        )

    pokemons_on_page = []
    pokemons = Pokemon.objects.all()
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.photo.url),
            'title_ru': pokemon.title_ru,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })

def create_evolution_dict(request, base):
    if base:
        evolution = {
            'title_ru': base.title_ru,
            'title_en': base.title_en,
            'title_jp': base.title_jp,
            "pokemon_id": base.id,
            "img_url": request.build_absolute_uri(base.photo.url)
        }
    else:
        evolution = {}

    return evolution


def show_pokemon(request, pokemon_id):
    pokemon_entities = PokemonEntity.objects.filter(pokemon_id=pokemon_id, appeared_at__lt=localtime(), disappeared_at__gt=localtime())
    pokemon = Pokemon.objects.get(pk=pokemon_id)

    if pokemon and pokemon_entities:
        folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
        for pokemon_entity in pokemon_entities:
            add_pokemon(
                folium_map, pokemon_entity.lat,
                pokemon_entity.lon,
                request.build_absolute_uri(pokemon_entity.pokemon.photo.url))


        previous_evolution_params = pokemon.previous_evolution
        previous_evolution = create_evolution_dict(request, previous_evolution_params)

        next_evolution_params = pokemon.next_evolution.all().first()
        next_evolution = create_evolution_dict(request, next_evolution_params)

        pokemon_on_page = {
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.photo.url),
            'title_ru': pokemon.title_ru,
            'title_en': pokemon.title_en,
            'title_jp': pokemon.title_jp,
            "description": pokemon.description,
            "previous_evolution": previous_evolution,
            "next_evolution": next_evolution
        }

        return render(request, 'pokemon.html', context={
            'map': folium_map._repr_html_(), 'pokemon': pokemon_on_page
        })
    else:
        print("Такой покемон не найден")
