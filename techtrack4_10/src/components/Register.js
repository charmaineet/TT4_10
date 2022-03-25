import React from "react";

export default function Register() {
  const [userName, setUsername] = React.useState("");
  const [passWord, setPassword] = React.useState("");
  const [confPassWord, setConfPassWord] = React.useState("");

  function handleChangeUsername() {
    setPassword();
  }
  function handleChangePassword() {
    setPassword();
  }

  function handleConfPassWord() {
    setConfPassWord();
  }

  const handleSubmit = (e) => {
    e.preventDefault();
    const data = new FormData(e.target);
  };

  React.useEffect(() => {
    fetch("https://")
      .then((res) => res.json())
      .then((data) => setUsername());
  }, []);
  return (
    <div>
      <form>
        <label>Username </label>
        <input placeholder="Username" onChange={handleChangeUsername}></input>
        <label>Password </label>
        <input placeholder="Password" onChange={handleChangePassword}></input>
        <label>Confirm Password </label>
        <input placeholder="Password" onChange={setConfPassWord}></input>
      </form>
      <button onSubmit={handleSubmit}>Register</button>
    </div>
  );
}
