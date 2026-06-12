import { useState, useEffect, useRef } from 'preact/compat';
import './index.css';

const DELTA_VALUES = [-10, -5, -1, 1, 5, 10];

// WebSocket connection hook with automatic reconnection
const useWebSocket = (url) => {
  const ws = useRef(null);
  const [status, setStatus] = useState('disconnected');
  const [errorMessage, setErrorMessage] = useState(null);
  const reconnectTimeout = useRef(null);

  const connect = () => {
    console.log(`Attempting WebSocket connection to: ${url}`);
    setStatus('connecting');
    setErrorMessage(null);
    
    ws.current = new WebSocket(url);
    
    ws.current.onopen = () => {
      setStatus('connected');
      console.log('WebSocket connected to', url);
    };
    
    ws.current.onclose = (event) => {
      setStatus('disconnected');
      console.log('WebSocket disconnected:', event.code, event.reason);
      // Attempt to reconnect after 3 seconds
      reconnectTimeout.current = setTimeout(connect, 3000);
    };
    
    ws.current.onerror = (error) => {
      setStatus('error');
      setErrorMessage(error.message || 'Connection error');
      console.error('WebSocket error:', error);
    };
  };

  useEffect(() => {
    connect();
    
    return () => {
      if (reconnectTimeout.current) {
        clearTimeout(reconnectTimeout.current);
      }
      if (ws.current) {
        ws.current.close();
      }
    };
  }, [url]);

  const sendCommand = (theta, phi) => {
    if (ws.current && ws.current.readyState === WebSocket.OPEN) {
      const command = { theta, phi };
      ws.current.send(JSON.stringify(command));
      return true;
    }
    console.warn('WebSocket not connected');
    return false;
  };

  const reconnect = () => {
    if (reconnectTimeout.current) {
      clearTimeout(reconnectTimeout.current);
    }
    connect();
  };

  return { sendCommand, status, errorMessage, reconnect };
};

const ButtonGrid = ({ axis, values, onSelect, disabled }) => {
  return (
    <div className="button-grid">
      <h3>{axis}</h3>
      <div className="button-grid-container">
        {values.map((value) => (
          <button
            key={value}
            onClick={() => onSelect(axis.toLowerCase(), value)}
            disabled={disabled}
            className={`control-btn ${value > 0 ? 'positive' : value < 0 ? 'negative' : 'zero'}`}
          >
            {value > 0 ? `+${value}` : value}
          </button>
        ))}
      </div>
    </div>
  );
};

const ControlPanel = () => {
  // Use window.location to determine the WebSocket URL
  // This handles both localhost and 127.0.0.1, and works in production
  const wsUrl = `ws://${window.location.hostname}:8080/ws`;
  const { sendCommand, status, errorMessage, reconnect } = useWebSocket(wsUrl);

  const handleDeltaSelect = (axis, delta) => {
    // Send relative movement: only the axis being moved
    if (axis === 'theta') {
      sendCommand(delta, 0);
    } else {
      sendCommand(0, delta);
    }
  };

  return (
    <div className="control-panel">
      <h1>Motor Control Panel</h1>
      
      <div className={`status-bar ${status}`}>
        <div className="status-text">
          <span>Status: <strong>{status.toUpperCase()}</strong></span>
          {errorMessage && <div className="error-message">Error: {errorMessage}</div>}
          {status === 'connecting' && <div className="connecting-message">Attempting to connect...</div>}
        </div>
        {status !== 'connected' && (
          <button className="reconnect-btn" onClick={reconnect}>
            Reconnect
          </button>
        )}
      </div>

      <div className="button-grids">
        <ButtonGrid 
          axis="Theta" 
          values={DELTA_VALUES} 
          onSelect={handleDeltaSelect}
          disabled={status !== 'connected'}
        />
        <ButtonGrid 
          axis="Phi" 
          values={DELTA_VALUES} 
          onSelect={handleDeltaSelect}
          disabled={status !== 'connected'}
        />
      </div>
    </div>
  );
};

export function App() {
  return (
    <div className="app-container">
      <ControlPanel />
    </div>
  );
}
