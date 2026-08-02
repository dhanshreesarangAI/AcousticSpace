import "./Navbar.css";

function Navbar({ onHistoryClick }) {
  return (
    <nav className="navbar">

      <h1>🎙️ AcousticSpace</h1>

      <button
        className="history-btn"
        onClick={onHistoryClick}
      >
        History
      </button>

    </nav>
  );
}

export default Navbar;