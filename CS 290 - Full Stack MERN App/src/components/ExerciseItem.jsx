import '../App.css';
import { MdEdit , MdClear} from "react-icons/md";

function ExerciseItem({exercise, onDelete, onEdit}) {

    return (
        <tr>
            <td>{exercise.name}</td>
            <td>{exercise.reps}</td>
            <td>{exercise.weight}</td>
            <td>{exercise.unit}</td>
            <td>{exercise.date}</td>
            <td><MdEdit  onClick={e => {e.preventDefault(); onEdit(exercise)}} /></td>
            <td><MdClear onClick={e => {e.preventDefault(); onDelete(exercise._id)}} /></td>
        </tr>
    );
}

export default ExerciseItem;