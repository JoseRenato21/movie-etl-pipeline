{# Silver: um filme por linha, tipado e sem duplicatas.
   Cada linha do Bronze é uma página com uma lista "results". Aqui a lista é
   aberta e, quando o mesmo filme aparece em várias extrações, vale a mais recente. #}

with pages as (

    select data, extracted_at
    from {{ source('bronze', 'bronze_movies') }}

),

flattened as (

    select
        movie,
        extracted_at
    from pages,
         jsonb_array_elements(data -> 'results') as movie

),

typed as (

    select
        (movie ->> 'id')::int                                    as movie_id,
        movie ->> 'title'                                        as title,
        movie ->> 'original_title'                               as original_title,
        movie ->> 'original_language'                            as original_language,
        nullif(movie ->> 'release_date', '')::date               as release_date,
        (movie ->> 'popularity')::numeric(10, 3)                 as popularity,
        (movie ->> 'vote_average')::numeric(4, 2)                as vote_average,
        (movie ->> 'vote_count')::int                            as vote_count,
        (movie ->> 'adult')::boolean                             as is_adult,
        nullif(movie ->> 'overview', '')                         as overview,
        movie ->> 'poster_path'                                  as poster_path,
        movie -> 'genre_ids'                                     as genre_ids,
        extracted_at
    from flattened

),

latest as (

    select
        *,
        row_number() over (partition by movie_id order by extracted_at desc) as rn
    from typed

)

select
    movie_id,
    title,
    original_title,
    original_language,
    release_date,
    extract(year from release_date)::int as release_year,
    popularity,
    vote_average,
    vote_count,
    is_adult,
    overview,
    poster_path,
    genre_ids,
    extracted_at
from latest
where rn = 1
