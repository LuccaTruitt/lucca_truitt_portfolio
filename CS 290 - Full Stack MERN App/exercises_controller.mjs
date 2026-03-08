// Student Name: Lucca Truitt
import 'dotenv/config';
import express from 'express';
import asyncHandler from 'express-async-handler';
import * as exercises from './exercises_model.mjs';

const ERROR_INVALID_REQ = {"Error": 'Invalid request'};
const ERROR_NOT_FOUND = {"Error": "Not found"};

const PORT = process.env.PORT;
const app = express();

app.use(express.json());

app.listen(PORT, async () => {
    await exercises.connect()
    console.log(`Server listening on port ${PORT}...`);
});

function isDateValid(date) {
    // Code from assignment page
    // Checks if date is correct format
    const format = /^\d\d-\d\d-\d\d$/;
    return format.test(date);
}

function isValid(req) {
    const name = req.body.name
    const reps = req.body.reps
    const weight = req.body.weight
    const unit = req.body.unit
    const date = req.body.date

    // Check there are five inputs
    if (Object.keys(req.body).length !== 5) {
        console.log("there isn't exactly 5 inputs")
        return false;
    }

    // Check if the five inputs we expect are present
    else if (
        typeof(name) === 'undefined'   ||
        typeof(reps) === 'undefined'   ||
        typeof(weight) === 'undefined' ||
        typeof(unit) === 'undefined'   ||
        typeof(date) === 'undefined') {
        console.log("something is undefined")
        return false;
    }

    // Check if 'name' is valid
    // Must be a string with a length of at least 1
    else if (typeof(name) !== 'string' || name.length < 1 ) {
        console.log("name isn't valid")
        return false;
    }

    // Check if 'reps' is valid
    // Must be an integer greater than 0
    else if (typeof(reps) !== 'number' || reps < 1) {
        console.log("reps isn't valid")
        return false;
    }

    // Check if 'weight' is valid'
    // Must be an integer greater than 0
    else if (typeof(weight) !== 'number' || weight < 1) {
        console.log("weight isn't valid")
        return false;
    }

    // Check if 'unit' is valid
    // Must be a string that is either 'kgs' or 'lbs'
    else if (typeof(unit) !== 'string' || (unit !== "kgs" && unit !== "lbs")) {
        console.log("unit isn't valid")
        return false;
    }

    // Check if 'date' is valid
    // Must be in date format aa-bb-cc, doesn't check if date is valid beyond this
    else if(typeof(date) !== 'string' || isDateValid(date) !== true) {
        console.log("date isn't correct")
        return false;
    }

    // Return true if all tests passed
    return true;
}

app.post('/exercises', asyncHandler(async (req, res) => {
    if(!isValid(req)) {
        res.status(400).json(ERROR_INVALID_REQ)
    } 
  else {
    const exercise = await exercises.createExercise(
        req.body.name, 
        req.body.reps,  
        req.body.weight,  
        req.body.unit,  
        req.body.date
    )
    res.status(201).json(exercise)
  }
}));

app.get('/exercises', asyncHandler(async (req, res) =>{
    const exercise = await exercises.findExercise(req.query);
    res.status(200).json(exercise)
}));

app.get('/exercises/:exercise_id', asyncHandler(async (req, res) => {
    const exercise = await exercises.findExerciseByID(req.params.exercise_id);
    if(exercise === null) {
        res.status(404).json(ERROR_NOT_FOUND);
    }
    else {
        res.status(200).json(exercise);
    }
}));

app.put('/exercises/:exercise_id', asyncHandler(async (req, res) => {
    // Verify validity of body
    if(!isValid(req)) {
        res.status(400).json(ERROR_INVALID_REQ)
    }
    else {
        // Update User
        const update_exercise = await exercises.updateExerciseByID(req.params.exercise_id, req.body);

        // If no user matches the inputted id, return error
        if(update_exercise === null) {
            res.status(404).json(ERROR_NOT_FOUND);
        }

        // If we found something to update, find updated user and return it
        // If you just return 'update_exercise', it returns the old version, even though it's updated on the database
        else {
            const return_exercise = await exercises.findExerciseByID(req.params.exercise_id);
            res.status(200).json(return_exercise);
        }
    }
}));

app.delete('/exercises/:exercise_id', asyncHandler(async (req, res) =>{
    const exercise = await exercises.deleteByID(req.params.exercise_id)
    if(exercise === null) {
        res.status(404).json(ERROR_NOT_FOUND)
    }
    else {
        res.status(204).json(exercise);
    }
}));