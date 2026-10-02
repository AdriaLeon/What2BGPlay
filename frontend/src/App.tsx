import { useState } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { MainPage } from "./pages/MainPage/MainPage";
import { ProfilePage } from "./pages/ProfilePage/ProfilePage";
import { AuthPage } from "./pages/AuthPage/AuthPage";

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(localStorage.getItem("access_token") !== null);

  function handleLogout() {
    localStorage.removeItem("access_token");
    setIsAuthenticated(false);
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

        <Route
          path="/profile"
          element={
            <ProfilePage
              isAuthenticated={isAuthenticated}
              onLogout={handleLogout}
            />
          }
        />

        <Route
        path="/login"
        element={
          <AuthPage
            onLogin={() => setIsAuthenticated(true)}
          />
          }
        />

        <Route
          path="/register"
          element={
            <AuthPage
              onLogin={() => setIsAuthenticated(true)}
            />
          }
        />

      </Routes>
    </BrowserRouter>
  );
}

export default App;