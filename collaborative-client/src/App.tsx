// import { useState } from 'react'
import './App.css'

// const fetchData = async () => {
//   try {
//     const response = await fetch('http://localhost:5000/');
//     const data = await response.json();
//     alert(JSON.stringify(data)) // Update state with the response data
//   } catch (error) {
//     console.error('Error fetching data:', error);
//   }
// }

const url = "http://localhost:5000/data";

const sendTypedData = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
  console.log(e)
  const key = e.key;

  if (!e.altKey && !e.ctrlKey) {
    fetch(url, {method: 'POST', body: JSON.stringify({keycode: key})}).catch(e => console.log(e))

  }
}

// const textarea = document.querySelector('#editor');

function App() {
  // const [count, setCount] = useState(0)

  return (
    <>
      <div className="h-screen flex justify-center items-center bg-gray-200">
        <div className='main w-1/2 p-2'>
          <textarea className="w-full rounded-xl p-2" name="" id="editor" cols={30} rows={10} onKeyDown ={sendTypedData}>

          </textarea>
        </div>
        {/* <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <button onClick={() => {
          fetchData()
        }}>
          Get Data!
        </button>
        <p>
          Edit <code>src/App.jsx</code> and save to test HMR
        </p> */}
      </div>
    </>
  )
}

export default App
