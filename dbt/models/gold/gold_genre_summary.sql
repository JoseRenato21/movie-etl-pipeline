{# Gold: resumo por gênero. Só entram gêneros com ao menos um filme. #}

select
    g.genre_name,
    count(*)                         as movies,
    round(avg(m.vote_average), 2)    as avg_vote,
    round(avg(m.popularity), 2)      as avg_popularity,
    sum(m.vote_count)                as total_votes
from {{ ref('silver_movie_genres') }} g
join {{ ref('silver_movies') }} m using (movie_id)
group by g.genre_name
order by movies desc, avg_vote desc
