// src/components/VideoDownloader.js
import React, { useState } from 'react';
import axios from 'axios';
import { Container, Form, Button, ProgressBar, Alert } from 'react-bootstrap';
import { ToastContainer, toast } from 'react-toastify';

const VideoDownloader = () => {
  const [url, setUrl] = useState('');
  const [format, setFormat] = useState('360p');
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState('');

  const handleDownload = async () => {
    setLoading(true);
    setError('');
    setProgress(0);
    const apiUrl = process.env.NODE_ENV === 'development' 
    ? 'http://localhost:5000/download' 
    : 'process.env.REACT_APP_BACKEND_URL/download';

    try {
      const response = await axios.post(apiUrl, { url, format }, {
        responseType: 'blob',
        onDownloadProgress: (progressEvent) => {
          const total = progressEvent.total;
          const current = progressEvent.loaded;
          setProgress((current / total) * 100);
        }
      });
      const blob = new Blob([response.data], { type: 'video/mp4' });
      const link = document.createElement('a');
      link.href = window.URL.createObjectURL(blob);
      link.download = 'video.mp4';
      link.click();
      toast.success('Download complete!');
    } catch (err) {
      setError('Failed to download video');
    }
    setLoading(false);
  };

  return (
    <Container className="d-flex flex-column justify-content-center align-items-center vh-100">
      <h1 className="mb-4">YouTube Video Downloader</h1>
      <Form className="w-50">
        <Form.Group controlId="formUrl">
          <Form.Label>YouTube URL</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter YouTube URL"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />
        </Form.Group>
        <Form.Group controlId="formFormat" className="mt-3">
          <Form.Label>Format</Form.Label>
          <Form.Control as="select" value={format} onChange={(e) => setFormat(e.target.value)}>
            <option value="360p">360p</option>
            <option value="480p">480p</option>
            <option value="720p">720p</option>
          </Form.Control>
        </Form.Group>
        <Button
          variant="primary"
          className="mt-3"
          onClick={handleDownload}
          disabled={loading}
        >
          Download
        </Button>
      </Form>
      {loading && <ProgressBar className="w-50 mt-3" now={progress} label={`${Math.round(progress)}%`} />}
      {error && <Alert variant="danger" className="w-50 mt-3">{error}</Alert>}
      <ToastContainer />
    </Container>
  );
};

export default VideoDownloader;