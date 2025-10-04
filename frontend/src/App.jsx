import React, { useState, useEffect } from "react";
import PlantList from "./PlantList";
import axios from "axios";

function App() {
  const [plants, setPlants] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/plants/")
      .then((res) => {
        setPlants(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setError("לא ניתן לטעון את רשימת העציצים");
        setLoading(false);
      });
  }, []);

  return (
    <div className="App" style={{ padding: "20px", direction: "rtl" }}>
      <h1>Keep Them Alive 🌱</h1>

      {loading && <p>טוען את רשימת העציצים...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {!loading && !error && plants.length === 0 && <p>אין עציצים להצגה</p>}

      {!loading && !error && plants.length > 0 && <PlantList /> }
    </div>
  );
}

export default App;