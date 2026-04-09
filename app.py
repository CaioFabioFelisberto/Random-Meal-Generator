import requests
from flask import Flask, render_template, request


url = "https://www.themealdb.com/api/json/v1/1/random.php"

app = Flask(__name__)

def get_ingredients():
    url = 'https://www.themealdb.com/api/json/v1/1/random.php'

    answer = requests.get(url)
    answer_list = answer.json()
    answer_dict = answer_list['meals'][0]

    ing_and_measure_list = []

    for i in range(20):
        ingredient_name = answer_dict.get(f'strIngredient{i+1}')
        measure_name = answer_dict.get(f'strMeasure{i+1}')
        if ingredient_name and measure_name:
            complete_item = f"{measure_name.strip()} : {ingredient_name.strip()}"
            ing_and_measure_list.append(complete_item)

    return ', '.join(ing_and_measure_list)


def get_tags():
    url = 'https://www.themealdb.com/api/json/v1/1/random.php'

    answer = requests.get(url)
    answer_list = answer.json()
    answer_dict = answer_list['meals'][0]

    tags = answer_dict.get('strTags')
    if tags:
        return ', '.join(tags.split(','))
    else:
        return 'No tags available'


@app.route('/', methods=['GET','POST'])
def index():
    try:
        answer = requests.get(url)
        answer_list = answer.json()
        answer_dict = answer_list['meals'][0]
        str_meal = answer_dict['strMeal']
        str_category = answer_dict['strCategory']
        str_area = answer_dict['strArea']
        ingredients = get_ingredients()
        str_instructions = answer_dict['strInstructions']
        tags = get_tags()
        image_url = answer_dict['strMealThumb']

    except requests.exceptions.HTTPError as err_h:
        print(f'HTTP Error: {err_h}')
    except requests.exceptions.ConnectionError:
        print(f'Connection error: Check your Internet!')
    except Exception as err:
        print(f"Unexpected error occurred: {err}")
    
    try:
        if request.method == 'POST':
            return render_template('index.html',meal=str_meal, category=str_category, area=str_area, tags=tags,ingredients=ingredients,instructions=str_instructions,image_url=image_url)
    
    except Exception as e:
        print(f'Error: {e}')

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)