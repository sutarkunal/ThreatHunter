/**
 * Upload Page - PCAP file upload
 */
import { useState } from 'react';
import { Upload as UploadIcon, File, CheckCircle, AlertCircle } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import Card from '../components/common/Card';
import { sessionService } from '../services/sessionService';
import { formatBytes } from '../utils/formatters';

export default function Upload() {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const navigate = useNavigate();

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files[0]);
    }
  };

  const handleFileInput = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFileSelect(e.target.files[0]);
    }
  };

  const handleFileSelect = (selectedFile) => {
    // Validate file type
    const validExtensions = ['.pcap', '.pcapng', '.cap'];
    const fileExtension = selectedFile.name.substring(selectedFile.name.lastIndexOf('.')).toLowerCase();

    if (!validExtensions.includes(fileExtension)) {
      setError('Invalid file type. Please upload a .pcap, .pcapng, or .cap file.');
      return;
    }

    // Validate file size (100MB)
    const maxSize = 100 * 1024 * 1024;
    if (selectedFile.size > maxSize) {
      setError('File too large. Maximum size is 100MB.');
      return;
    }

    setFile(selectedFile);
    setError(null);
  };

  const handleUpload = async () => {
    if (!file) return;

    try {
      setUploading(true);
      setError(null);

      await sessionService.uploadPCAP(file);

      setSuccess(true);
      setTimeout(() => {
        navigate('/');
      }, 2000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to upload file');
    } finally {
      setUploading(false);
    }
  };

  const handleReset = () => {
    setFile(null);
    setSuccess(false);
    setError(null);
  };

  return (
    <div className="max-w-3xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Upload PCAP File</h1>
        <p className="text-gray-600 mt-2">
          Upload a network capture file for analysis and threat detection
        </p>
      </div>

      <Card>
        {success ? (
          <div className="text-center py-12">
            <CheckCircle className="w-16 h-16 text-success-500 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Upload Successful!</h3>
            <p className="text-gray-600 mb-4">Processing PCAP file and detecting threats...</p>
            <p className="text-sm text-gray-500">Redirecting to dashboard...</p>
          </div>
        ) : (
          <>
            {/* Drop Zone */}
            <div
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
              className={`border-2 border-dashed rounded-lg p-12 text-center transition-colors ${
                dragActive
                  ? 'border-primary-500 bg-primary-50'
                  : 'border-gray-300 hover:border-gray-400'
              }`}
            >
              <UploadIcon className="w-16 h-16 text-gray-400 mx-auto mb-4" />

              {file ? (
                <div className="space-y-4">
                  <div className="flex items-center justify-center space-x-3 p-4 bg-gray-50 rounded-lg max-w-md mx-auto">
                    <File className="w-8 h-8 text-primary-600" />
                    <div className="text-left flex-1">
                      <p className="font-medium text-gray-900">{file.name}</p>
                      <p className="text-sm text-gray-600">{formatBytes(file.size)}</p>
                    </div>
                  </div>

                  <div className="flex justify-center space-x-4">
                    <button
                      onClick={handleUpload}
                      disabled={uploading}
                      className="btn btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {uploading ? 'Uploading...' : 'Upload File'}
                    </button>
                    <button
                      onClick={handleReset}
                      disabled={uploading}
                      className="btn btn-secondary"
                    >
                      Choose Different File
                    </button>
                  </div>
                </div>
              ) : (
                <>
                  <p className="text-lg text-gray-700 mb-2">
                    Drag and drop your PCAP file here, or click to browse
                  </p>
                  <p className="text-sm text-gray-500 mb-4">
                    Supports .pcap, .pcapng, and .cap files (max 100MB)
                  </p>

                  <label className="btn btn-primary cursor-pointer">
                    Browse Files
                    <input
                      type="file"
                      accept=".pcap,.pcapng,.cap"
                      onChange={handleFileInput}
                      className="hidden"
                    />
                  </label>
                </>
              )}
            </div>

            {/* Error Message */}
            {error && (
              <div className="mt-4 p-4 bg-danger-50 border border-danger-200 rounded-lg flex items-start space-x-3">
                <AlertCircle className="w-5 h-5 text-danger-600 flex-shrink-0 mt-0.5" />
                <div>
                  <p className="font-medium text-danger-900">Upload Failed</p>
                  <p className="text-sm text-danger-700 mt-1">{error}</p>
                </div>
              </div>
            )}

            {/* Info */}
            <div className="mt-8 p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <h4 className="font-semibold text-blue-900 mb-2">What happens after upload?</h4>
              <ul className="text-sm text-blue-800 space-y-1 list-disc list-inside">
                <li>Packets are extracted and analyzed</li>
                <li>Threat detection algorithms run automatically</li>
                <li>Alerts are generated for suspicious activity</li>
                <li>Analytics and visualizations are prepared</li>
              </ul>
            </div>
          </>
        )}
      </Card>
    </div>
  );
}
