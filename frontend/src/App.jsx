import Register from "./components/Register";
import Login from "./components/Login"
import { Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import LinkPage from "./components/LinkPage";
import Unatuthorized from "./components/Unatuthorized";

function App() {

  return (
      <Routes>
          <Route path={"/"} element={<Layout />}>
              <Route path={"register"} element={<Register />}/>
              <Route path={"login"} element={<Login />}/>
              <Route path={"linkpage"} element={<LinkPage />}/>
              <Route path={"unauthozied"} element={<Unatuthorized />}/>
          </Route>
      </Routes>
  );
}

export default App;