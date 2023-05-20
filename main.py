from googleapiclient.discovery import build

# Defina a chave de API e o ID do projeto
api_key = 'AIzaSyCWbkbCj3eNg8pv8pe9V4fN7wUGpzytIWs'
project_id = '110577150454415986421'

# Crie uma instância do serviço da API do YouTube
youtube = build('youtube', 'v3', developerKey=api_key)

# Filtros para listar vídeos até o fim de 2015
video_filters = {
    'publishedBefore': '2016-01-01T00:00:00Z',
    'publishedAfter': '2005-01-01T00:00:00Z'
}

# Configurações da paginação
videos_per_page = 30  # Número de vídeos por página
current_page = 1  # Página atual

# Calcular o índice do primeiro vídeo na página atual
start_index = (current_page - 1) * videos_per_page + 1

# Fazer a solicitação para listar os vídeos com os filtros e a página atual
videos_request = youtube.videos().list(
    part='snippet',
    chart='mostPopular',
    maxResults=videos_per_page,
    startIndex=start_index,
    **video_filters
)

# Executar a solicitação e obter os resultados
videos_response = videos_request.execute()

# Processar e exibir os dados dos vídeos da página atual
for video in videos_response['items']:
    video_id = video['id']
    title = video['snippet']['title']
    description = video['snippet']['description']
    print(f'Video ID: {video_id}')
    print(f'Title: {title}')
    print(f'Description: {description}')
    print('---')

# Calcular o número total de páginas com base no total de vídeos e vídeos por página
total_videos = videos_response['pageInfo']['totalResults']
total_pages = (total_videos - 1) // videos_per_page + 1

# Exibir links para outras páginas
for page in range(1, total_pages + 1):
    if page == current_page:
        # Destacar a página atual
        print(f'[{page}]', end=' ')
    else:
        print(f'<a href="/videos?page={page}">{page}</a>', end=' ')

print()
