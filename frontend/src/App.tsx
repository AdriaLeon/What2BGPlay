import { BrowserRouter, Routes, Route } from "react-router-dom";
import { MainPage } from "./pages/MainPage/MainPage";

function App() {
  const isAuthenticated =
    localStorage.getItem("access_token") !== null;

  function handleLogout() {
    localStorage.removeItem("access_token");
    window.location.href = "/";
  }

  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/"
          element={
            <MainPage
              isAuthenticated={isAuthenticated}
              onLogout={handleLogout}
            />
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;