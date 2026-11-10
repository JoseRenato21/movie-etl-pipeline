{# Teste genérico: falha se algum valor estiver fora do intervalo [min, max]. #}
{% test value_between(model, column_name, min, max) %}

select {{ column_name }}
from {{ model }}
where {{ column_name }} < {{ min }}
   or {{ column_name }} > {{ max }}

{% endtest %}
