import Register from "./components/Register";
import Login from "./components/Login"
import {Routes, Route} from "react-router-dom";
import Layout from "./components/Layout";
import LinkPage from "./components/LinkPage";
import Unauthorized from "./components/Unauthorized";
import RequireAuth from "./components/RequireAuth";
import Home from "./components/Home"
import Admin from "./components/Admin";

const ROLES = {
    'User': 2001,
    'Editor': 1984,
    'Admin': 5150
}

function App() {

    return (
        <Routes>
            <Route path={"/"} element={<Layout/>}>
                <Route path={"register"} element={<Register/>}/>
                <Route path={"login"} element={<Login/>}/>
                <Route path={"linkpage"} element={<LinkPage/>}/>
                <Route path={"unauthozied"} element={<Unauthorized/>}/>

                <Route element={<RequireAuth allowedRoles={[ROLES.User]}/>}>
                    <Route path="/" element={<Home/>}/>
                </Route>

                <Route element={<RequireAuth allowedRoles={[ROLES.Admin]}/>}>
                    <Route path="admin" element={<Admin />}/>
                </Route>
            </Route>
        </Routes>
    );
}

export default App;