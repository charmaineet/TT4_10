import React from "react";

export default function Home() {
  const [balance, SetBalance] = React.useState("");

  const [toggle1, setToggle1] = React.useState(true);

  const [toggle2, setToggle2] = React.useState(true);

  function handleClick1() {
    setToggle1((prevtoggle1) => !prevtoggle1);
  }

  function handleClick2() {
    setToggle2((prevtoggle2) => !prevtoggle2);
  }
  React.useEffect(() => {
    fetch("https://")
      .then((res) => res.json())
      .then((data) => SetBalance(data.balance));
  }, []);

  return (
    <div>
      <nav className="navbar">
        <h1>DBS</h1>
      </nav>
      <span>Current Account Balance: </span>{" "}
      {toggle1 ? <span>$123</span> : <span>***</span>}{" "}
      <button onClick={handleClick1}>Hide</button>
      <hr />
      <span>Current Loan: </span>{" "}
      {toggle2 ? <span>$123</span> : <span>***</span>}{" "}
      <button onClick={handleClick2}>Hide</button>
      <hr />
      <h2>Loan History </h2>
      <button>Apply New Loan</button>
    </div>
  );
}