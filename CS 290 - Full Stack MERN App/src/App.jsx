import './App.css';
import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navigation from './components/Navigation'
import HomePage from './pages/HomePage';
import AddExercisePage from './pages/AddExercisePage';
import EditExercisePage from './pages/EditExercisePage';

function App() {

  const [exerciseToEdit, setExerciseToEdit] = useState();

  return (
    <>
      <header>
        <h1>Exercise App</h1>
        <p>This app lets you add, edit, and remove exercises.</p>
      </header>
      <div className="app">
        <Router>
          <Navigation/>
          <Routes>
            <Route path="/" element={ <HomePage setExerciseToEdit={setExerciseToEdit} /> }></Route>
            <Route path="/add-exercise" element={ <AddExercisePage />}></Route>
            <Route path="/edit-exercise" element={ <EditExercisePage exerciseToEdit={exerciseToEdit} />}></Route>
          </Routes>
        </Router>
      </div>
      <footer>
        <p>&copy; Lucca Truitt</p>
      </footer>
    </>
    
  );
}

export default App;