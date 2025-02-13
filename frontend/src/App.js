import React, { useEffect, useState } from 'react';

const App = () => {
    const [backendMessage, setBackendMessage] = useState("");

    useEffect(() => {
        fetch("http://localhost:8000/api/hello")
            .then(response => response.json())
            .then(data => setBackendMessage(data.message))
            .catch(error => console.error("Error fetching data: ", error));
    }, []);

    return (
        <div style={{ textAlign: 'center', marginTop: '50px' }}>
            <h1>Welcome to RJ Dental Care PH</h1>
            <p>This is the frontend of our supervised AI agent architecture.</p>
            <p>Backend says: {backendMessage}</p>
        </div>
    );
};

export default App;