{% if get.callback %}{{ get.callback }}({% endif %}
{% if attractions %}[
    {% for attraction in recommended %}
{
    "id": "{{ attraction.id }}",
    "url": "/attractions/{{ attraction.id }}",
    "title": "{{ attraction.name }}",
    "description": "{{ attraction.description|truncatewords:20 }}",
    "location": {
        "lat": {{ attraction.location.lat }},
        "lon": {{ attraction.location.lon }}
    },
    "thumbnail": "{{ attraction.thumbnail }}",
    "tags": [{% for tag in attraction.tags %}"{{ tag|escape }}"{% if not forloop.last %},{% endif %}{% endfor %}],
    "datetime": {{ attraction.datetime|date:"U" }}
}{% if not forloop.last %},{% endif %}
    {% endfor %}
]{% endif %}
{% if get.callback %});{% endif %}
