export default function FileUploader({ files, onChange }) {
  function addFiles(event) {
    const selectedFiles = Array.from(event.target.files || []);
    onChange((currentFiles) => [...currentFiles, ...selectedFiles]);
    event.target.value = "";
  }

  function removeFile(fileToRemove) {
    onChange((currentFiles) => currentFiles.filter((file) => file !== fileToRemove));
  }

  return (
    <section className="files-section">
      <div className="files-heading">
        <div>
          <p className="eyebrow">REFERENCE MATERIAL</p>
          <h2>Files <span>{files.length}</span></h2>
        </div>
        <label className="upload-button">
          <input type="file" multiple onChange={addFiles} />
          <span aria-hidden="true">+</span> Add files
        </label>
      </div>
      {files.length ? (
        <ul className="file-list">
          {files.map((file, index) => (
            <li key={`${file.name}-${index}`}>
              <span className="file-icon" aria-hidden="true">FILE</span>
              <span className="file-name">{file.name}</span>
              <span className="file-size">{formatFileSize(file.size)}</span>
              <button
                type="button"
                className="remove-file"
                aria-label={`Remove ${file.name}`}
                onClick={() => removeFile(file)}
              >
                x
              </button>
            </li>
          ))}
        </ul>
      ) : (
        <p className="files-empty">Add reference files to keep them close to your task.</p>
      )}
    </section>
  );
}

function formatFileSize(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}
