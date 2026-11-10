{# Gold: filmes populares por idioma original. #}

select
    original_language,
    count(*)                         as movies,
    round(avg(vote_average), 2)      as avg_vote,
    round(avg(popularity), 2)        as avg_popularity
from {{ ref('silver_movies') }}
group by original_language
order by movies desc, avg_vote desc
