# Generated by Django 3.0.5 on 2020-05-02 21:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suit', models.IntegerField(choices=[(0, 'Hearts'), (1, 'Diamonds'), (2, 'Clubs'), (3, 'Spades')])),
                ('rank', models.IntegerField(choices=[(0, 'Two'), (1, 'Three'), (2, 'Four'), (3, 'Five'), (4, 'Six'), (5, 'Seven'), (6, 'Eight'), (7, 'Nine'), (8, 'Ten'), (9, 'Jack'), (10, 'Queen'), (11, 'King'), (12, 'Ace')])),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_one_score', models.IntegerField()),
                ('team_two_score', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_name', models.CharField(max_length=30)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MatchPlayerGame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField(choices=[(0, 'First'), (1, 'Second'), (2, 'Third'), (3, 'Fourth')])),
                ('cards', models.ManyToManyField(related_name='_matchplayergame_cards_+', to='setback.Card')),
                ('currently_played', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='setback.Card')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setback.Game')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='setback.Player')),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='next_to_play',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='setback.MatchPlayerGame'),
        ),
        migrations.AddField(
            model_name='game',
            name='players',
            field=models.ManyToManyField(through='setback.MatchPlayerGame', to='setback.Player'),
        ),
    ]