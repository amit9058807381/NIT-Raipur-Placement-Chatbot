import { useState } from "react";

function Register({ onRegister }) {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleRegister = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch(
        "http://127.0.0.1:5000/api/auth/register",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            name: name.trim(),
            email: email.trim(),
            password: password,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        console.error("Register failed:", data);
        return;
      }

      // Registration successful
      const registeredUser = {
        name: name.trim(),
        email: email.trim(),
      };

      // Save user
      localStorage.setItem(
        "user",
        JSON.stringify(registeredUser)
      );

      // Directly go to chat page
      onRegister(registeredUser);

    } catch (error) {
      console.error("Register error:", error);
    }
  };

  return (
    <div className="login-page">

      <div className="login-box">

        <h1>NIT Placement AI</h1>

        <p>Create your account</p>

        <form onSubmit={handleRegister}>

          <input
            type="text"
            placeholder="Name"
            value={name}
            onChange={(e) =>
              setName(e.target.value)
            }
            required
          />

          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) =>
              setEmail(e.target.value)
            }
            required
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) =>
              setPassword(e.target.value)
            }
            required
          />

          <button type="submit">
            Register
          </button>

        </form>

        <p className="register-text">
          Already have an account?

          <button
            type="button"
            className="link-button"
            onClick={() => onRegister(null)}
          >
            Login
          </button>
        </p>

      </div>

    </div>
  );
}

export default Register;