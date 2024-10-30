// Variable Declarations Demo
function variableDemo() {
    var name = "Var Name";
    let age = 25;
    const country = "USA";
  
    document.getElementById("variable-demo").innerHTML = `
      <strong>var:</strong> ${name} <br>
      <strong>let:</strong> ${age} <br>
      <strong>const:</strong> ${country}
    `;
  }
  
  // Function Demo
  function functionDemo() {
    function greet(name) {
      return `Hello, ${name}!`;
    }
  
    const message = greet("JavaScript Learner");
    document.getElementById("function-demo").textContent = message;
  }
  
  // DOM Manipulation Demo
  function domManipulationDemo() {
    const domDemo = document.getElementById("dom-demo");
    domDemo.style.color = domDemo.style.color === "red" ? "#333" : "red";
  }
  
  // Promise Demo
  function promiseDemo() {
    const promise = new Promise((resolve, reject) => {
      setTimeout(() => {
        const success = true; // Change to false to see the rejection
        if (success) {
          resolve("Promise resolved successfully!");
        } else {
          reject("Promise was rejected.");
        }
      }, 1000);
    });
  
    promise
      .then((message) => {
        document.getElementById("promise-demo").textContent = message;
      })
      .catch((error) => {
        document.getElementById("promise-demo").textContent = error;
      });
  }
  
  // Async/Await and Fetch Demo
  async function fetchDemo() {
    const apiUrl = "https://jsonplaceholder.typicode.com/todos/1";
    const fetchDemoBox = document.getElementById("fetch-demo");
    fetchDemoBox.textContent = "Fetching data...";
  
    try {
      const response = await fetch(apiUrl);
      if (!response.ok) throw new Error("Network response was not ok.");
      
      const data = await response.json();
      fetchDemoBox.innerHTML = `
        <strong>Title:</strong> ${data.title} <br>
        <strong>Completed:</strong> ${data.completed}
      `;
    } catch (error) {
      fetchDemoBox.textContent = `Error: ${error.message}`;
    }
  }
  