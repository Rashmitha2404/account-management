import React, { useState } from "react";

function FileUpload({ onUpload }) {
  const [file, setFile] = useState(null);

  const handleChange = (e) => setFile(e.target.files[0]);
  const handleUpload = () => {
    // Placeholder: call onUpload with file
    if (file) onUpload(file);
  };

  return (
    <div className="file-upload">
      <input type="file" accept=".xlsx,.csv" onChange={handleChange} />
      <button onClick={handleUpload} disabled={!file}>Upload</button>
    </div>
  );
}

export default FileUpload; 