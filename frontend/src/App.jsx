import Register from './components/Register';
import { Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";

function App() {

  return (
      <Routes>
          <Route path={"/"} element={<Layout />}>
              <Route path={"register"} element={<Register />}/>
          </Route>
      </Routes>
    // <main className="App">
    //   <Register />
    // </main>
  );
}

export default App;