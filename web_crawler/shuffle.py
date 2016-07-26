# -*- coding: utf-8 -*-

# Leitura do arquivo json. Caso não exista, retorna uma lista vazia
database_array = read_json('../database_new.json')

shuffle(database_array)
write_json("../database_new_shuffled.json", database_array)
