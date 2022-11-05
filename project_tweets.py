import csv, json, os
from email.policy import default
from re import sub
from time import sleep

def clear_screen():
    """
        Função responsável por limpar terminal
    """
    os.system('cls') or None


def get_title(title):
    print(f'{title:=^80}\n')


def read_csv_generator(adress: str, delimiter: str, lineterminator: str):
    '''
    Função para gerar um arquivo temporário com os dados
    '''
    import csv
    arquivo = open(adress, "r", encoding='utf-8')
    planilha = csv.reader(
        arquivo,
        delimiter=delimiter,
        lineterminator=lineterminator
    )
    return planilha


def welcome():
    '''
    Função para dar boas vindas e solicitar uma opção
    '''
    clear_screen()
    get_title(' Boas Vindas ')

    options = """
        1 - Buscar tweets por data
        2 - Buscar tweets por termo
        3 - Buscar tweets por assunto
        4 - Salvar resultado da busca
        5 - Sair
    """
    print(options)


def new_date_creator(row: str):
    '''
    Função para transformar a data de AAAA-MM-DD HH:MM:SS zone para DD/MM/AAAA
    '''
    new_date = [new_date.split("-") for new_date in ["".join(row[0][:10])]]
    new_date = [dmy for dmy in new_date[0]]
    new_date.reverse()
    new_date = "/".join(new_date)
    return new_date


def date_search(generator):
    '''
    Função para filtrar os dados por data
    '''
    clear_screen()
    get_title(' Busca por data ')

    date_list_format, date_list, content_list, subject_list = [], [], [], []
    input_date = input("Digite uma data (DD/MM/AAAA): ")
    next(generator)
    for row in generator:
        new_date = new_date_creator(row)
        if input_date == new_date:
            date_list_format.append(new_date)
            date_list.append(row[0])
            content_list.append(row[3])
            subject_list.append(row[4])

    return date_list_format, date_list, content_list, subject_list


def term_search(generator):
    '''
    Função para filtrar os dados por termo
    '''
    clear_screen()
    get_title(' Busca por termo ')
    
    input_term = input("Digite uma uma palavra: ").lower()
    date_list_format, date_list, content_list, subject_list = [], [], [], []
    next(generator)
    for row in generator:
        new_date = new_date_creator(row)
        if input_term in row[3].lower():
            date_list_format.append(new_date)
            date_list.append(row[0])
            content_list.append(row[3])
            subject_list.append(row[4])

    return date_list_format, date_list, content_list, subject_list


def subject_search(generator):
    '''
    Função para filtrar os dados por assunto
    '''
    clear_screen()
    get_title(' Busca por assunto ')
    
    input_subject = choose_subject()
    date_list_format, date_list, content_list, subject_list = [], [], [], []
    next(generator)
    for row in generator:
        new_date = new_date_creator(row)
        if input_subject == row[4].lower():
            date_list_format.append(new_date)
            date_list.append(row[0])
            content_list.append(row[3])
            subject_list.append(row[4])

    return date_list_format, date_list, content_list, subject_list


def choose_subject():
    '''
    Função para solicitar o assunto desejado da busca
    '''
    clear_screen()
    get_title(' Busca por assunto ')

    assuntos = """
        1. Copa do Mundo
        2. Eleições 
        3. Ciência de Dados 
        4. COVID-19: "
    """
    print(assuntos)
  
    #while True:
    try:
        subject = input('Escolha um assunto: ').strip().lower()
        if subject in ["Copa do Mundo".lower(),"Eleições".lower(),\
                    "Ciência de Dados".lower(),"COVID-19".lower()]:
            return subject
    except ValueError:
        print("Esse assunto não existe")


def show_search_result(date_list_format: list, content_list: list, subject_list: list):
    '''
    Função para imprimir o resultado da busca
    '''
    clear_screen()
    get_title(' Resultado da busca ')

    if not bool(date_list_format):
        print('Não há dados aqui para essa busca...')
    else:
        print("Data", "  |  ", "Conteúdo", "  |  ", "Assunto")
        for i in range(0, len(date_list_format)):
            print(date_list_format[i], "  |  ",
                content_list[i], "  |  ", subject_list[i])

    input('\nPressione ENTER para sair...')


def salve_json(date_list, content_list, subject_list):
    '''
    Função para salvar o resultado da última busca em um arquivo .json
    O nome do arquivo é fornecido pelo usuário e o arquivo é salvo no diretório atual
    '''
    twitter = {"data": date_list,
               "conteudo": content_list,
               "assunto": subject_list}
    string_json = json.dumps(twitter)
    file_name = input("Digite o nome do arquivo a ser salvo: ")
    with open(f"{file_name}.json", "w") as arquivo:
        json.dump(twitter, arquivo)
    
    clear_screen()
    print("\nResultado salvo com sucesso!")
    sleep(1.5)


def good_by():
    clear_screen()
    print('\nObrigado por usar o programa. Até mais!')
    sleep(2)
    clear_screen()
    exit()


def main():
    while True:
        welcome()
        choice = None
        generator = read_csv_generator('projeto_LP_tweets_2022.csv', ',', '\n')
        while True:
            try:
                choice = int(input('Escolha uma das opções: '))
                if isinstance(choice, int):
                    break
            except ValueError:
                print('\nEscolha uma das opções acima 1,2,3,4 ou 5.')
                
        match choice:
            case 1:
                date_list_format, date_list, content_list, subject_list = date_search(
                    generator)
                show_search_result(
                    date_list_format, content_list, subject_list)

            case 2:
                date_list_format, date_list, content_list, subject_list = term_search(generator)
                show_search_result(date_list_format, content_list, subject_list)                   
                
            case 3:
                date_list_format, date_list, content_list, subject_list = subject_search(
                    generator)
                show_search_result(date_list_format, content_list, subject_list)

            case 4:
                salve_json(date_list, content_list, subject_list)

            case 5:
                good_by()

            case _:
                print('\nApenas 1,2,3,4 ou 5')
                sleep(1.5)


if __name__ == '__main__':
    main()

# def main(file):
#     '''
#     Função para executar o programa e manter o loop quando preciso
#     Recebe o endereço do arquivo .csv como argumento
#     '''
#     request = 0
#     while request != 5:
#         welcome()
# 		try:
#             request = int(input('Insira uma das opções acima: '))
# 		except ValueError:
#         	print('Digite apenas números')
# 		generator = read_csv_generator(file, ",", "\n")
#         if request == 1:
#             # Filtro por data
#             # input_date = input("Digite uma data (DD/MM/AAAA): ")
#             date_list_format, date_list, content_list, subject_list = date_search(
#                 generator)
#             show_search_result(date_list_format, content_list, subject_list)
#         elif request == 2:
#             # Filtro por termo
#             input_term = input("Digite uma uma palavra: ").lower()
#             date_list_format, date_list, content_list, subject_list = term_search(
#                 input_term, generator)
#             show_search_result(date_list_format, content_list, subject_list)
#         elif request == 3:
#             # Filtro por assunto
#             input_subject = choose_subject()
#             date_list_format, date_list, content_list, subject_list = subject_search(
#                 input_subject, generator)
#             show_search_result(date_list_format, content_list, subject_list)
#         elif request == 4:
#             # salvar arquivo como json (está sobrescrevendo o arquivo já existente)
#             salve_json(date_list, content_list, subject_list)
#         elif request == 5:
#             print("Programa finalizado!")
#             break
#         else:
#             print("Solicitação inválida.")
#             break


# main(file="projeto_LP_tweets_2022.csv")
