{% if get.callback %}{{ get.callback }}({% endif %}
{% if attractions %}[
    {% for attraction in attractions %}
{
    id: "{{ attraction.id|escape }}",
    title: "{{ attraction.name|escape }}",
    location: {
        lat: {{ attraction.location.lat|escape }},
        lon: {{ attraction.location.lon|escape }}
    },
    datetime: {{ attraction.datetime|date:"U" }}
}{% if not forloop.last	%},{% endif %}
    {% endfor %}
]{% endif %}
{% if get.callback %});{% endif %}
