import React from "react";

const PlantList = ({plants, onWaterPlant}) => {

  const tableStyle = {
    borderCollapse: "collapse",
    width: "100%",
    fontFamily: "Arial, sans-serif",
    marginTop: "20px"
  };

  const thStyle = {
    border: "1px solid #ddd",
    padding: "10px",
    backgroundColor: "#4CAF50",
    color: "white",
    textAlign: "left"
  };

  const tdStyle = {
    border: "1px solid #ddd",
    color: "black",
    padding: "10px"
  };

  const trStyle = (index) => ({
    backgroundColor: index % 2 === 0 ? "#ffffff" : "#f9f9f9"
  });

  return (
    <div>
      <h2>My Plants</h2>
      <table style={tableStyle}>
        <thead>
          <tr>
            <th style={thStyle}>ID</th>
            <th style={thStyle}>Name</th>
            <th style={thStyle}>Location</th>
            <th style={thStyle}>Water Amount</th>
            <th style={thStyle}>Unit</th>
            <th style={thStyle}>Frequency (days)</th>
            <th style={thStyle}>Last Watered</th>
            <th style={thStyle}>Needs Watering?</th>
            <th style={thStyle}>Action</th>
          </tr>
        </thead>
        <tbody>
          {plants.map((plant, index) => (
            <tr key={plant.id} style={trStyle(index)}>
              <td style={tdStyle}>{plant.id}</td>
              <td style={tdStyle}>{plant.name}</td>
              <td style={tdStyle}>{plant.location}</td>
              <td style={tdStyle}>{plant.water_amount}</td>
              <td style={tdStyle}>{plant.unit}</td>
              <td style={tdStyle}>{plant.frequency_days}</td>
              <td style={tdStyle}>{plant.last_watered ? new Date(plant.last_watered).toLocaleDateString() : 'N/A'}</td>
              <td style={tdStyle}>{plant.needs_watering ? 'Yes' : 'No'}</td>
              <td style={tdStyle}>
                <button onClick={() => onWaterPlant(plant.id)} style={{
                                                                padding: "5px 10px",
                                                                backgroundColor: "#4CAF50",
                                                                color: "white",
                                                                border: "none",
                                                                borderRadius: "4px",
                                                                cursor: "pointer"
                                                            }}>
                    💧 השקיתי
                </button> 
                </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default PlantList;