import { useState, useEffect} from 'react';
import ExerciseCollection from '../components/ExerciseCollection'
import { Link } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';

function HomePage({setExerciseToEdit}) {
    const [exercises, setExercises] = useState([])
    const navigate = useNavigate()

    const loadExercises = async () => {
        const response = await fetch('/exercises');
        const data = await response.json();
        setExercises(data);
    }

    useEffect( () =>{
        loadExercises();
    }, []);

    const onDelete = async (_id) => {
        console.log("onDelete id ", _id)
        const response = await fetch(
            `/exercises/${_id}`,
            {method: 'DELETE'}
        );
        if(response.status === 204){
            setExercises(exercises.filter(m => m._id !== _id))
        } else {
            alert(`Failed to delete the exercise with _id = ${_id}, status code = ${response.status}`)
        }
    }

    const onEdit = (exercise) => {
        setExerciseToEdit(exercise)
        navigate('/edit-exercise')
    }

    return (
        <>
            <h2>List of Exercises</h2>
            <ExerciseCollection exercises={exercises} onDelete={onDelete} onEdit={onEdit} ></ExerciseCollection>
            <Link id = "addLink" to="/add-exercise">Add an exercise</Link>
        </>
    )
}

export default HomePage;