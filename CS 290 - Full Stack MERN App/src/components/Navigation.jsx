import {Link} from 'react-router-dom'

function Navigation(){
    return (
        <nav className="app-nav">
            <Link id = "navLink" to="/">Home Page</Link>
            <Link id = "navLink" to="/add-exercise">Add Exercise</Link>
        </nav>
    )
}

export default Navigation;