# Dokumentácia pre integráciu kódu do šablón


#### TBR Place - Quick Prompt Generator
- path: tbr_place/views.py
- Zobrazenie náhodne vygenerovaného promptu a prípadných správ používateľovi na stránke.
- variables : prompt_name, prompt_type, messages

##### 1. Zobrazenie generovaného promptu:

    {% if prompt_name != 'No prompts available' %}
        {{ prompt_name }} ({{ prompt_type }})
    {% else %}
        {{ prompt_name }}
    {% endif %}

Zobrazí názov promptu a jeho typ, ak je dostupný. Ak nie je, ošetrené správou.

##### 2. Zobrazenie správ:

    {% if messages %}
        <ul>
            {% for message in messages %}
                <li{% if message.tags %} class="{{ message.tags }}"{% endif %}>{{ message }}</li>
            {% endfor %}
        </ul>
    {% endif %}

Zobrazuje všetky správy, ktoré boli nastavené v rámci kódu pre generovanie promptu. 
Správy môžu mať rôzne typy (success, warning, error), ktoré ovplyvňujú ich štýl.
