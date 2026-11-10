{# Gold: ranking dos filmes por popularidade, com a nota e a posição por nota. #}

select
    rank() over (order by popularity desc)   as popularity_rank,
    movie_id,
    title,
    release_year,
    original_language,
    popularity,
    vote_average,
    vote_count,
    rank() over (order by vote_average desc, vote_count desc) as rating_rank
from {{ ref('silver_movies') }}
order by popularity_rank
