import React from "react";


export default function Home() {

  const [balance, SetBalance] = React.useState("");

  const [loan, SetLoan] = React.useState("");

  const [loanHistory, SetLoanHistory] = React.useState([]);

  const [toggle1, setToggle1] = React.useState(true);

  const [toggle2, setToggle2] = React.useState(true);
  

  function handleClick1() {
    setToggle1((prevtoggle1) => !prevtoggle1);
  }

  function handleClick2() {
    setToggle2((prevtoggle2) => !prevtoggle2);
  }
  React.useEffect(() => {
    fetch("http://ec2-52-221-194-162.ap-southeast-1.compute.amazonaws.com:5000/customer?CustomerId=8")
      .then((res) => res.json())
      .then((data) => SetLoan(data));
  }, []
  );

  React.useEffect(() => {
    fetch("")
      .then((res) => res.json())
      .then((data) => SetBalance(data));
  }, []
  );

  React.useEffect(() => {
    fetch("")
      .then((res) => res.json())
      .then((data) => SetLoanHistory(data));
  }, []
  );

  const History = loanHistory.map((d) => <li key={d.name}>{d.name}</li>);
  
  return (
    <div>
      <nav className="navbar">
        <h1>DBS</h1>
      </nav>
      <span>Current Account Balance: </span>
      {toggle1 ? <span>{balance[1]}</span> : <span>***</span>}
      <button onClick={handleClick1}>Hide</button>
      <hr />
      <span>Current Loan: </span>
      {toggle2 ? <span>{loan[1]}</span> : <span>***</span>}
      <button onClick={handleClick2}>Hide</button>
      <hr />
      <h2>Loan History </h2>
      <button>Apply New Loan</button>
      {History}
    </div>
  );
}
