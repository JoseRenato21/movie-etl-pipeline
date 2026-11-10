{# Silver: relação filme x gênero (uma linha por par), com o nome do gênero vindo do seed. #}

select
    m.movie_id,
    g.genre_id,
    g.genre_name
from {{ ref('silver_movies') }} m
cross join lateral jsonb_array_elements_text(m.genre_ids) as gid(value)
join {{ ref('genres') }} g
  on g.genre_id = gid.value::int
