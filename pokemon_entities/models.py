from django.db import models

class Pokemon(models.Model):
    title_ru = models.CharField("Имя покепона на русском", max_length=200)
    title_en = models.CharField("Имя покепона на английском", max_length=200, blank=True)
    title_jp = models.CharField("Имя покепона на японском", max_length=200, blank=True)

    photo = models.ImageField("Фото")
    description = models.TextField("Описание")

    previous_evolution = models.ForeignKey('self',
                                  verbose_name='Из кого эволюционирует',
                                  null=True,
                                  blank=True,
                                  related_name="next_evolution",
                                  on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.title_ru, self.title_en, self.title_jp}'

class PokemonEntity(models.Model):
    lat = models.FloatField("Широта")
    lon = models.FloatField("Долгота")
    pokemon = models.ForeignKey(Pokemon, verbose_name="Покемон", on_delete=models.CASCADE)
    appeared_at = models.DateTimeField("Появляется", null=True)
    disappeared_at = models.DateTimeField("Исчезает", null=True)

    level = models.IntegerField("Уровень")
    health = models.IntegerField("Здоровье")
    strength = models.IntegerField("Атака")
    defence = models.IntegerField("Защита")
    stamina = models.IntegerField("Выносливость")


