import React, { useState } from 'react';

interface UploadFormProps {
  onGenerate: (files: File[], prompt: string) => void;
  loading: boolean;
}

const UploadForm: React.FC<UploadFormProps> = ({ onGenerate, loading }) => {
  const [files, setFiles] = useState<File[]>([]);
  const [prompt, setPrompt] = useState<string>('');

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) setFiles(Array.from(e.target.files));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (files.length < 2) {
      alert('Please upload at least 2 documents.');
      return;
    }
    onGenerate(files, prompt);
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-white shadow rounded-lg p-6 space-y-6"
    >
      <h2 className="text-xl font-semibold text-gray-800">
        Upload Documents
      </h2>

      <div className="space-y-1">
        <label
          htmlFor="file-input"
          className="block text-sm font-medium text-gray-700"
        >
          Documents (PDF or TXT):
        </label>
        <input
          id="file-input"
          type="file"
          multiple
          accept=".pdf,.txt"
          onChange={handleFileChange}
          className="
          box-border             /* makes w-full include the padding & border */
          block w-full
          text-gray-900 bg-gray-50
          border border-gray-300
          rounded-lg cursor-pointer
          p-2
          "
        />
      </div>

      <div className="space-y-1">
        <label
          htmlFor="prompt-input"
          className="block text-sm font-medium text-gray-700"
        >
          Prompt:
        </label>
        <input
          id="prompt-input"
          type="text"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="E.g. Create a training manual on key points"
          className=" 
          box-border
          block w-full
          border border-gray-300 rounded-lg
          px-3 py-2
          focus:outline-none focus:ring-2 focus:ring-blue-500
          "
        />
      </div>

      <button
        type="submit"
        disabled={loading}
        className={`
          w-full flex items-center justify-center
          ${loading ? 'bg-blue-400' : 'bg-blue-600 hover:bg-blue-700'}
          text-white font-medium py-2 rounded-lg
          disabled:opacity-50 disabled:cursor-not-allowed
        `}
      >
        {loading ? 'Generating…' : 'Generate'}
      </button>
    </form>
  )
}

export default UploadForm