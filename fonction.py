# -*- coding: utf-8 -*-
"""Fichier contenant toutes les fonctions assurant la générations des morceaux ainsi que leur lecture"""
from time import sleep
import numpy as np
import random
import simpleaudio as sa
from tkinter import filedialog
from tkinter import *


def calc_frequencies(notes, f0):
    """
    Calcul les fréquences des notes donné en fonction de la fréquence du do
    :param notes: liste de notes sous forme de chaine de caractères
    :param f0: fréquence d'un do
    :type notes: list
    :type f0: int
    :return: liste de fréquence sous forme d'entiers
    :rtype: list
    """

    frequencies = []
    for note in notes:
        if note == "DO":
            frequencies.append(f0)
        elif note == "RE":
            frequencies.append(f0 + 33)
        elif note == "MI":
            frequencies.append(f0 + 66)
        elif note == "FA":
            frequencies.append(f0 + 88)
        elif note == "SOL":
            frequencies.append(f0 + 132)
        elif note == "LA":
            frequencies.append(f0 + 176)
        elif note == "SI":
            frequencies.append(f0 + 231)
        elif note == "Z":
            frequencies.append(-1)
        elif note == "":
            frequencies.append(frequencies[-1])
    return frequencies


def calc_duration(figures, d0):
    """
    Calcule la durée des notes donné en fonction de la durée d'une croche

    :param figures: liste de durée de notes sous forme de caractère
    :param d0: durée en milliseconde d'une croche
    :type figures: list
    :type d0: float
    :return: liste de durée sous forme de réel
    :rtype: list
    """

    durations = []
    for figure in figures:
        if figure == "r":
            durations.append(8 * d0)
        elif figure == "b":
            durations.append(4 * d0)
        elif figure == "n":
            durations.append(2 * d0)
        elif figure == "c":
            durations.append(d0)
        elif figure == "p":
            durations.append((durations[-1]) / 2)

    return durations


def read_line_file(f, num):
    """
    Lit une ligne spécifique du fichier et la retourne sous forme de chaine de caractère

    :param f: nom du fichier contenant la base de donnée de morceaux
    :param num: numéro de la ligne à lire
    :type f: str
    :type num: int
    :return: ligne correspondant au numéro de ligne fournie
    :rtype: str
    """

    # Ouverture du fichier en lecture et lecture des lignes contenue dans le fichier
    file = open(f, "r")
    lines = file.readlines()

    return lines[num]


def read_sheet(line):
    """
    Lit une chaine de caractère correspondant a un morceau et la convertie en une liste de durée et une liste de
    notes qu'elle retourne

    :param line: partition d'un morceau
    :type line: str
    :return: liste de notes, liste de durée
    :rtype: list
    """

    notes = []
    durations = []

    # séparation de la chaine de caractère en liste de chaine de cractère en fonction des espaces.
    sheet = line.split(" ")

    # Parcours de la liste des notes afin de séparer leur durée de leur valeur.
    for note in sheet:
        durations.append(note.rstrip()[-1])
        notes.append(note.rstrip()[:-1])

    return notes, durations


def play_song(f, num, f0, d0, image_note, notes_images, canva_note):
    """
    Joue un morceau à partir d'une partition, du numéro du morceau, de la fréquence d'un Do et de la durée d'une
    croche.

    :param f: nom du fichier contenant la base de donnée de morceaux
    :type f: str
    :param num: numéro de la ligne du morceau à lire
    :type num: int
    :param f0: fréquence du do à la quelle doit être joué le morceau
    :type f0: int
    :param d0: durée en milliseconde d'une croche
    :type d0: float
    :param image_note: element graphique tkinter
    :param notes_images: liste de d''image
    :type notes_images:list
    :param canva_note: canva tkinter
    """

    # Lecture de la partion du morceau afin de la séparer en une liste de notes et de durée.
    notes, durations = read_sheet(read_line_file(f, num))
    # Lecture du morceau à partir de la liste de durée et de notes
    play_sheet(calc_frequencies(notes, f0), calc_duration(durations, d0), notes, image_note, notes_images, canva_note)


def play_sheet(frequencies, durations, notes, image_note, notes_images, canva_note):
    """
    Joue un morceau à partir d'une liste de frequences et une liste de durée et affiche l'image correpondante à la
    note.
    :param frequencies: Partitions d'un morceau sous la forme d'une liste de fréquences
    :type frequencies: list
    :param durations: Liste des durée des notes d'un morceau
    :type durations: list
    :param notes: partitions d'un morceau sous la forme de liste de chaine de caractère
    :type notes: list
    :param image_note: element graphique tkinter
    :param notes_images: liste d'image
    :type notes_images: list
    :param canva_note: canva tkinter
    """
    notes_dict = {"DO": 0, "RE": 1, "MI": 2, "FA": 3, "SOL": 4, "LA": 5, "SI": 6, "": 7, "Z": 7}

    # Lecture des fréquences contenue dans la liste et affichage de l'image correspondante à celle-ci
    for i in range(len(frequencies)):
        canva_note.itemconfigure(image_note, image=notes_images[7])
        canva_note.update()
        canva_note.itemconfigure(image_note, image=notes_images[notes_dict[notes[i]]])
        canva_note.update()
        if frequencies[i] == -1:
            sleep(durations[i])
        else:
            sound(frequencies[i], durations[i])

    canva_note.itemconfigure(image_note, image=notes_images[7])
    canva_note.update()


def get_songs(f):
    """
    Retourne les noms des morceaux contenu dans la partition ainsi que le numéro de leur ligne sous la forme d'un
    dictionnaire.

    :param f: nom du fichier contnant la base de donnée de morceaux
    :type f: str
    :return: liste des morceaux contenue dans la base de donnée
    :rtype: dict
    """

    # ouverture du fichier contenant la base de donnée en lecture
    file = open(f, "r", encoding="utf-8")
    # lecture des lignes du fichier
    lines = file.readlines()
    songs = {}
    # parcours des lignes afin de récupérer le nom des morceaux et le numéro de la ligne coresspondant au morceau
    for line in lines:
        if line[0][0] == "#":
            songs[(line.rstrip()[1:])] = (lines.index(line) + 1)

    return songs


def load_songs(songs, list_songs):
    """
    Charge une liste de morceau donné dans la listbox tkinter
    :param songs: liste des morceaux à charger
    :type songs: dict
    :param list_songs: listbox tkinter
    """
    # vidage de la listebox tkinter
    list_songs.delete(0, 500)

    # parcours de la liste des morceau en les ajoutant à la listebox tkinter
    for song in songs.keys():
        list_songs.insert(END, song)

    # selection par défaut du premier morceau
    list_songs.select_anchor(0)
    list_songs.select_set(0)


def get_song_number(list_select, list_songs, songs):
    """
    retourne le numéro des morceaux contenu dans la liste des morceaux selectionné fournie

    :param list_select: liste des morceaux sélectionné
    :param list_songs: element graphique tkinter listebox
    :param songs: dictionnaire associant le nom des morceaux à leur numéro
    :type songs: dict
    :return: numéros des morceaux sélectionné
    :rtype: list
    """

    songs_numbers = []
    for nbr in list_select:
        songs_numbers.append(songs[list_songs.get(nbr)])

    return songs_numbers


def inversion(line):
    """
    Génère l'inversion d'un morceau à patir d'une partion original
    :param line: numéro de la ligne correspondant a la partition du morceaux sélectionné
    """

    # Lecture de la partions du morceau sélectionné et conversion en liste de chaine de caratère
    sheet = read_line_file("partitions.txt", line).rstrip().split(" ")

    # création de nom du nouveau morceau à partir du nom du morceaux sélectionné
    name = "#" + str(len(get_songs("partitions.txt")) + 1) + " Inversion " + (
        read_line_file("partitions.txt", line - 1).rstrip()[3:]) + "\n"

    # Inversion du morceau sélectionné
    sheet2 = sheet.copy()
    for i in range(len(sheet)):
        sheet2[(len(sheet) - 1) - i] = sheet[i]

    # Enregistrement du morceaux générée dans la base donnée
    file_2 = open("partitions.txt", "a", encoding="utf-8")
    file_2.write(name)
    file_2.write(" ".join(sheet2) + "\n")


def markov(list_of_songs):
    """
    génère un morceau grâce à la formule de markov à partie des numéro des morceaux fournie

    :param list_of_songs: numéros de ligne des morceaux sélectionnée
    :type list_of_songs: list
    """
    songs = ""
    new_song = []
    keys = []
    notes_possible = {}

    # création du nom du nouveau morceau à partir des nom des morceaux sélectionnée
    name = "#" + str(len(get_songs("partitions.txt")) + 1) + " Markov"

    # récupération des partions ainsi que le nom des morceaux sélectionné à partir des numéro de ligne
    for element in list_of_songs:
        songs = read_line_file("partitions.txt", element).rstrip() + " " + songs
        name = name + " | " + (read_line_file("partitions.txt", element - 1).rstrip()[3:])

    # séparation de la chaine de caractère correspondant aux partitions des morceaux sélectionné en liste de chaine
    # de caractère
    sheet = songs.strip().split(" ")

    # parcour de la liste des notes afin de récupérer toutes les notes possible dans le morceaux ansi que les notes
    # apparaissant après celle-ci
    for i in range(len(sheet) - 1):
        if sheet[i] not in notes_possible:
            notes_possible[sheet[i]] = []
            if sheet[i + 1] != sheet[-1]:
                notes_possible[sheet[i]].append(sheet[i + 1])
        else:
            if sheet[i + 1] not in notes_possible[sheet[i]]:
                if sheet[i + 1] != sheet[-1]:
                    notes_possible[sheet[i]].append(sheet[i + 1])

    # créations d'une liste contenat toute les notes possible dans le morceau
    for key in notes_possible.keys():
        keys.append(key)

    # choix de manière aléatoire dans la liste des notes possible de la première notes du morceaux et ajoue de
    # celle-ci dans la liste des notes du nouveau morceau.
    new_song.append(random.choice(keys))

    # génaration de la suite du morceau en choisissant et en ajoutant une notes parmie la liste des notes possible de
    # la notes précédemment ajouté au morceau.
    for i in range(len(sheet) - 1):
        new_song.append(random.choice(notes_possible[new_song[-1]]))

    # Inscription du nouveau morceau généré dans la base de donnée des morceaux
    file_2 = open("partitions.txt", "a", encoding="utf-8")
    file_2.write(name + "\n")
    file_2.write(" ".join(new_song) + "\n")


def markov2(list_of_songs):
    """
    génère un morceau grâce à la version 2 de la formule de markov à partie des numéro des morceaux fournie

    :param list_of_songs: numéros de ligne des morceaux sélectionnée
    :type list_of_songs: list
    """

    songs = ""
    new_song = []
    max_occurrence = 0
    val = ""
    notes_possible = {}
    occurrences = {}

    # récupération des partions ainsi que le nom des morceaux sélectionné à partir des numéro de ligne
    name = "#" + str(len(get_songs("partitions.txt")) + 1) + " Markov 2"

    # récupération des partions ainsi que le nom des morceaux sélectionné à partir des numéro de ligne
    for song in list_of_songs:
        songs = read_line_file("partitions.txt", song).rstrip() + " " + songs
        name = name + " | " + (read_line_file("partitions.txt", song - 1).rstrip()[3:])

    # séparation de la chaine de caractère correspondant aux partitions des morceaux sélectionné en liste de chaine
    # de caractère.
    sheet = songs.strip().split(" ")

    # parcour de la liste des notes afin de récupérer toutes les notes possible dans le morceaux ansi que les notes
    # apparaissant après celle-ci et le nombre d'occurences de chaque notes
    for i in range(len(sheet) - 1):
        if sheet[i] not in notes_possible:
            notes_possible[sheet[i]] = []
            if sheet[i + 1] != sheet[-1]:
                notes_possible[sheet[i]].append(sheet[i + 1])
            occurrences[sheet[i]] = 1
        else:
            if sheet[i + 1] != sheet[-1]:
                notes_possible[sheet[i]].append(sheet[i + 1])
            occurrences[sheet[i]] += 1

    # Répération de la notes apparaissant le plus de fois dans le morceau
    for element in occurrences.keys():
        if occurrences[element] > max_occurrence:
            val = element

    # choix de manière aléatoire dans la liste des notes possible de la première notes du morceaux et ajoue de
    # celle-ci dans la liste des notes du nouveau morceau.
    new_song.append(val)

    # génaration de la suite du morceau en choisissant et en ajoutant une notes parmie la liste des notes possible de
    # la notes précédemment ajouté au morceau.
    for i in range(len(sheet) - 1):
        new_song.append(random.choice(notes_possible[new_song[-1]]))

    # Inscription du nouveau morceau généré dans la base de donnée des morceaux
    file_2 = open("partitions.txt", "a", encoding="utf-8")
    file_2.write(name + "\n")
    file_2.write(" ".join(new_song) + "\n")


def sound(freq, duration):
    """
    Joue un son en fonction d'une fréquence et de la durée

    :param freq: liste de fréquences correspondant aux notes du morceau
    :type freq: int
    :param duration: liste de durée correspondant aux notes du morceau
    :type freq: int
    """

    sample_rate = 48000
    t = np.linspace(0, duration, int(duration * sample_rate), False)
    tone = np.sin(freq * t * 2 * np.pi)
    tone *= 8388607 / np.max(np.abs(tone))
    tone = tone.astype(np.int32)
    i = 0
    byte_array = []
    for b in tone.tobytes():
        if i % 4 != 3:
            byte_array.append(b)
        i += 1
    audio = bytearray(byte_array)
    play_obj = sa.play_buffer(audio, 1, 3, sample_rate)
    play_obj.wait_done()


def add_song(window):
    """

    Ajoute de nouveau morceau contenu dans un fichier fournie par l'utilistaeur à la base de donnée

    :param window: fenêtre tkinter
    """

    # ouvre une fenêtre de dialogue permetant le choix d'un fichier
    window.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                 filetypes=(("texte files", "*.txt"), ("all files", "*.*")))

    # ouvre le fichier content la base de donnée en lecture et le fichier choisit par l'utilisateur en lecture
    file_1 = open(window.filename, "r", encoding="utf-8")
    file_2 = open("partitions.txt", "a", encoding="utf-8")

    # lit les lignes du fichier choisit par l'utilisateur et les ajoute au fichier contenant la base de donnée.
    lines_1 = file_1.readlines()
    for line in lines_1:
        file_2.write(line)
