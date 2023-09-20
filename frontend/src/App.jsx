import Register from "./components/Register";
import Login from "./components/Login"
import { Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";

function App() {

  return (
      <Routes>
          <Route path={"/"} element={<Layout />}>
              <Route path={"register"} element={<Register />}/>
              <Route path={"login"} element={<Login />}/>
          </Route>
      </Routes>
  );
}

export default App;