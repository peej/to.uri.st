{% if get.callback %}{{ get.callback }}({% endif %}
{% if attractions %}[
    {% for attraction in attractions %}
{
    "id": "{{ attraction.id }}",
    "title": "{{ attraction.name }}",
    "location": {
        "lat": {{ attraction.location.lat }},
        "lon": {{ attraction.location.lon }}
    },
    "datetime": {{ attraction.datetime|date:"U" }}
}{% if not forloop.last	%},{% endif %}
    {% endfor %}
]{% endif %}
{% if get.callback %});{% endif %}
