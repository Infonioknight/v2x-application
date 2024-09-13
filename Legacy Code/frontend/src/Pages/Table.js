import React from 'react'

function Table(props) {
    return (
        <div className="content">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Latitude</th>
                <th>Longitude</th>
                <th>Altitude</th>
                <th>Brake Status</th>
                <th>Speed</th>
                <th>Timestamp</th>
              </tr>
            </thead>
            <tbody>
              {props.data.map((entry) => (
                <tr key={entry.id}>
                  <td>{entry.id}</td>
                  <td>{entry.latitude}</td>
                  <td>{entry.longitude}</td>
                  <td>{entry.altitude}</td>
                  <td>{entry.brake_status}</td>
                  <td>{entry.speed}</td>
                  <td>{entry.timestamp}</td>
                </tr>
              ))}
            </tbody>
          </table>
         
        </div>
    )
}

export default Table;

