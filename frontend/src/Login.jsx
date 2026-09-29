import { useState } from "react";

function Login({ onLogin, onRegister }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch(
        "http://127.0.0.1:5000/api/auth/login",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email: email,
            password: password,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        alert(data.error || "Login failed");
        return;
      }

      // Save logged-in user
      localStorage.setItem(
        "user",
        JSON.stringify({
          name: data.name,
          email: data.email,
        })
      );

      onLogin(data);

    } catch (error) {
      console.error("Login error:", error);

      alert("Unable to connect to server");
    }
  };

  return (
    <div className="login-page">

      <div className="login-box">

        <h1>NIT Placement AI</h1>

        <p>Login to your account</p>

        <form onSubmit={handleLogin}>

          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          <button type="submit">
            Login
          </button>

        </form>

        <p className="register-text">
          Don't have an account?

          <button
            type="button"
            className="link-button"
            onClick={onRegister}
          >
            Register
          </button>
        </p>

      </div>

    </div>
  );
}

export default Login;