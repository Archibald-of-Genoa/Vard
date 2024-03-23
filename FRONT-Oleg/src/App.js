import logo from './logo.svg';
import './App.css';
import SearchBar from './SearchBar';

function App() {
  return (
    <div>
      <SearchBar variation="default" />
      <SearchBar variation="connection" />
      <SearchBar variation="files" />
      <SearchBar variation="charts" />
      <SearchBar variation="wiki" />
    </div>
  );
}

export default App;
