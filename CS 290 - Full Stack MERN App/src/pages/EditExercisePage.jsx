import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function EditExercisePage({exerciseToEdit}) {
    const [name, setName] = useState(exerciseToEdit.name);
    const [reps, setReps] = useState(exerciseToEdit.reps);
    const [weight, setWeight] = useState(exerciseToEdit.weight);
    const [unit, setUnit] = useState(exerciseToEdit.unit);
    const [date, setDate] = useState(exerciseToEdit.date);

    const navigate = useNavigate();

    const editExercise = async () => {
        const editedExercise = {name, reps, weight, unit, date}
        const response = await fetch(
            `/exercises/${exerciseToEdit._id}`, {
                method: 'PUT',
                headers: {'Content-type': 'application/json'},
                body: JSON.stringify(editedExercise)
            }
        );
        if (response.status === 200) {
            alert("Successfully edited the exercise")
        } else {
            alert("Failed to edit the exercise")
            console.log("editExercise failure - status code = " + response.status)
        }
        navigate('/')
    }

    return (
        <div>
            <h2>Edit Exercise</h2>

            <label>Name:</label>
            <input 
                type="text" 
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
                <option value={unit} selected disabled hidden>{unit}</option>
                <option value="kgs">kgs</option>
                <option value="lbs">lbs</option>
            </select>

            <br></br>

            <label> Date:</label>
            <input 
                type="text" 
                value={date}
                onChange={e => setDate(e.target.value)} 
            />

            <br></br>

            <button onClick={editExercise}>Update</button>

        </div>
    )
}

export default EditExercisePage;