import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function AddExercisePage() {
    const [name, setName] = useState('');
    const [reps, setReps] = useState(0);
    const [weight, setWeight] = useState(0);
    const [unit, setUnit] = useState('');
    const [date, setDate] = useState('');

    const navigate = useNavigate();

    const addExercise = async () => {
        const newExercise = {name, reps, weight, unit, date}
        const response = await fetch(
            '/exercises', {
                method: 'POST',
                headers: {'Content-type': 'application/json'},
                body: JSON.stringify(newExercise)
            }
        );
        if (response.status === 201){
            alert("Successfully added the exercise");
        } else {
            alert("Failed to add the exercise")
            console.log("addExercise failure - status code = " + response.status)
        }
        navigate('/')
    };

    return (
        <div>
            <h2>Add Exercise</h2>

            <label>Name:</label>
            <input 
                type="text" 
                placeholder="Enter name here"
                value={name}
                onChange={e => setName(e.target.value)} 
            />

            <br></br>

            <label>Reps:</label>
            <input 
                type="number" 
                value={reps}
                // For some reason, the users input gets stringified, this parses it back to an int
                onChange={e => setReps(parseInt(e.target.value))} 
            />

            <br></br>

            <label> Weight:</label>
            <input 
                type="number" 
                value={weight}
                // For some reason, the users input gets stringified, this parses it back to an int
                onChange={e => setWeight(parseInt(e.target.value))} 
            />

            <br></br>

            <label>Unit:</label>
            <select onChange={e => setUnit(e.target.value)}>
                <option value="none" selected disabled hidden>Select a unit</option>
                <option value="kgs">kgs</option>
                <option value="lbs">lbs</option>
            </select>

            <br></br>
        
            <label> Date:</label>
            <input 
                type="text" 
                placeholder="Enter date here"
                value={date}
                onChange={e => setDate(e.target.value)} 
            />

            <br></br>

            <button onClick={addExercise}>Add</button>

        </div>
    )
}

export default AddExercisePage;