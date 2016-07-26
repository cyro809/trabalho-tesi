# -*- coding: utf-8 -*-

if __name__ == "__main__":

    # Nome do arquivo json que queremos fazer as operações
    json_filename = '../database_new.json'

    # Nome do arquivo com as urls novas que queremos adicionar no json
    input_filename = 'teste2.txt'

    # Leitura do arquivo json. Caso não exista, retorna uma lista vazia
    database_array = read_json(json_filename)

    # Leitura do arquivo de urls
    # urls_array = read_urls_file(input_filename) # Aqui colocamos a entrada desejada

    # # Chama a função para crawl das letras retornando uma lista de dicionários
    # lyrics_array = crawl_lyrics(urls_array)
    
    # # Adicionamos a nova lista ao final da lista de músicas que estavam
    # # no banco de dados
    # database_array.extend(classify_lyrics(lyrics_array))

    # Escrevemos no arquivo json
    shuffle(database_array)
    write_json("../database_new_shuffled2.json", database_array)

    # Exibimos o total de musicas por sentimento no json
    # sentiment_count(json_filename)

