// Student Name: Lucca Truitt
import mongoose from 'mongoose';
import 'dotenv/config';

const EXERCISE_DB_NAME = 'exercise_db';

let connection = undefined;

/**
 * This function connects to the MongoDB server and to the database
 *  'exercise_db' in that server.
 */
async function connect(){
    try{
        connection = await mongoose.connect(process.env.MONGODB_CONNECT_STRING, 
                {dbName: EXERCISE_DB_NAME});
        console.log("Successfully connected to MongoDB using Mongoose!");
    } catch(err){
        console.log(err);
        throw Error(`Could not connect to MongoDB ${err.message}`)
    }
}

const exerciseSchema = mongoose.Schema({
    name: { type: String, required: true},
    reps: { type: Number, required: true},
    weight: { type: Number, required: true},
    unit: { type: String, required: true},
    date: { type: String, required: true},
});

const Exercise = mongoose.model(EXERCISE_DB_NAME, exerciseSchema)

const createExercise = async (name, reps, weight, unit, date) => {
    const exercise = new Exercise({name: name, reps: reps, 
        weight: weight, unit: unit, date: date})
    return exercise.save();
}

const findExercise = async (filter) => {
    const query = Exercise.find(filter);
    return query.exec();
}

const findExerciseByID = async (_id) => {
    const query = Exercise.findById({_id: _id});
    return query.exec();
}

const updateExerciseByID = async (_id, filter) => {
    const query = Exercise.findByIdAndUpdate({_id: _id}, filter);
    return query.exec();
}

const deleteByID = async (_id) => {
    const query = Exercise.findByIdAndDelete({_id: _id});
    return query.exec();
}

export {connect, createExercise, findExercise, 
    findExerciseByID, updateExerciseByID, deleteByID};