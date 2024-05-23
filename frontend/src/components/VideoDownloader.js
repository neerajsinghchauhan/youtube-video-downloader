import React, { useState } from 'react';
import axios from 'axios';
import { saveAs } from 'file-saver';
import { Container, Form, Button, ProgressBar, Alert } from 'react-bootstrap';
import { ToastContainer, toast } from 'react-toastify';

const VideoDownloader = () => {
  const [url, setUrl] = useState('');
  const [format, setFormat] = useState('360p');
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState('');
  const [videoTitle, setVideoTitle] = useState('');

  const handleDownload = async () => {
    setLoading(true);
    setError('');
    setProgress(0);
    setVideoTitle('');

    try {
      const response = await axios.post('http://127.0.0.1:5000/download', { url, format }, {
        responseType: 'blob',
        onDownloadProgress: (progressEvent) => {
          const total = progressEvent.total;
          const current = progressEvent.loaded;
          setProgress((current / total) * 100);
        }
      });

      const title = response.headers['x-title'];
      if (title) {
        setVideoTitle(title);
      } else {
        setVideoTitle('video');
      }

      const blob = new Blob([response.data], { type: 'video/mp4' });
      saveAs(blob, `${videoTitle}.mp4`);
      const link = document.createElement('a');
      link.href = window.URL.createObjectURL(blob);
      link.download = `${videoTitle}.mp4`;
      link.click();

      toast.success('Download complete!');
    } catch (err) {
      setError('Failed to download video');
    }
    setLoading(false);
  };

  const isValidUrl = (url) => {
    try {
      new URL(url);
      return url.includes('youtube.com');
    } catch (error) {
      return false;
    }
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
      {videoTitle && <Alert variant="success" className="w-50 mt-3">Downloading: {videoTitle}</Alert>}
      <ToastContainer />
    </Container>
  );
};

export default VideoDownloader;