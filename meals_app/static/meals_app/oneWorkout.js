let addWorkout = document.getElementById("One_Workout")
addWorkout.addEventListener('click', function(e){
console.log('button pressed')
fetch('/one_workout', {
    method: 'GET'
}).then(function(response){
    return response.json();
    })
    .then(function(myjson){
    console.log(myjson)
    myjson = myjson['workout'].split(',');
    console.log(myjson);
    myjson.forEach(function(line){
        if (line !== ' '){
            let workout_data = document.createElement('li');
            workout_data.innerText = line;
            document.getElementById('one_workout_list').appendChild(workout_data);
}
})
})
})
//    let meal_data = document.createElement('li');
//    meal_data.innerText = 'Name: ' + myjson['name'] + '  Prep Time: ' + myjson['prep_time'] + '  Cook Time: ' + myjson['cook time'] + '  Servings: ' + myjson['servings']
//    let meal_shopping_list = document.createElement('li');
//    meal_shopping_list.innerText = 'Shopping List: ' + myjson['shopping_list'];
//    let meal_recipe = document.createElement('li');
//    meal_recipe.innerText = 'Recipe: ' + myjson['recipe'];
//    let meal_directions = document.createElement('li');
//    meal_directions.innerText = 'Directions: ' + myjson['instructions'];
//    document.getElementById('one_meal_lists').appendChild(meal_data);
//    document.getElementById('one_meal_lists').appendChild(meal_shopping_list);
//    document.getElementById('one_meal_lists').appendChild(meal_recipe);
//    document.getElementById('one_meal_lists').appendChild(meal_directions);
//    document.getElementById('One_Meal').innerText = 'Add Another Meal';
//})
//})

