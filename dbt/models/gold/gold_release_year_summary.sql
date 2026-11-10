{# Gold: filmes populares por ano de lançamento. #}

select
    release_year,
    count(*)                         as movies,
    round(avg(vote_average), 2)      as avg_vote,
    round(avg(popularity), 2)        as avg_popularity,
    max(popularity)                  as top_popularity
from {{ ref('silver_movies') }}
where release_year is not null
group by release_year
order by release_year desc
