import React from "react";
import ImageUpload from "./components/ImageUpload";
import ImageDashboard from "./components/ImageDashboard";

function App() {
  const [refresh, setRefresh] = React.useState(false);

  // Refresh dashboard after upload
  const handleUpload = () => setRefresh((v) => !v);

  return (
    <div style={{ maxWidth: 900, margin: "0 auto", padding: 30 }}>
      <h1>AutoAudit360 – MVP</h1>
      <ImageUpload onUpload={handleUpload} />
      <hr />
      <ImageDashboard key={refresh} />
    </div>
  );
}

export default App;
