# SentiMusic

Projeto desenvolvido para a disciplina de Tópicos Especiais em Sistemas Inteligentes do curso de Ciência da Computação da UFRJ no período de 2016/1

Esse projeto possui 3 programas:
- Web Crawler
- Programa Principal (KMeans)
- Reordenador do Banco de Dados (Shuffle)


## Web Crawler
### Faz o crawl, classifica as músicas a partir de links do site Vagalume.com.br e adiciona na base de dados (JSON)

O Web Crawler possui duas maneiras de entrada:: arquivo texto e input do usuário

Para ler de um arquivo texto, execute a função read_urls_file() (linha 101 do arquivo web_crawler\main.py) passando o nome do seu arquivo
Para ler via input do terminal, execute a função a função read_urls_input(). Para multiplos links, separe-os por virgula.

## Programa principal
### Executa o KMeans e o K-Fold a partir de uma base de dados JSON e retorna a acurácia dos testes

Existem duas formas para executar:
- Executar testes apenas com o melhor dos treinamentos do K-Fold
- Executar testes com todos os treinamentos do K-Fold

É possível selecionar o corte K da matriz SVD, o tamanho do conjunto de treinamento e o tamanho da janela do K-Fold


