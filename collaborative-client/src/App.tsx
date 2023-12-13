import { useState } from 'react'
import './App.css'

const fetchData = async () => {
  try {
    const response = await fetch('http://localhost:5000/');
    const data = await response.json();
    alert(JSON.stringify(data)) // Update state with the response data
  } catch (error) {
    console.error('Error fetching data:', error);
  }
}

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <button onClick={() => {
          fetchData()
        }}>
          Get Data!
        </button>
        <p>
          Edit <code>src/App.jsx</code> and save to test HMR
        </p>
      </div>
    </>
  )
}

export default App
